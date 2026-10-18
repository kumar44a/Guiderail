"""GuideRail Streamlit client. Display only: every answer comes from the REST API.

    streamlit run ui/app.py            # API at GUIDERAIL_API_URL (default http://localhost:9070)
"""

from __future__ import annotations

import os

import httpx
import streamlit as st

API_URL = os.environ.get("GUIDERAIL_API_URL", "http://localhost:9070").rstrip("/")
TIMEOUT_SECONDS = 90   # the optional LLM generator can take several seconds

st.set_page_config(page_title="GuideRail", page_icon="🩺", layout="wide")


def fetch_health() -> dict | None:
    try:
        response = httpx.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError):
        return None


def ask(question: str, top_k: int, debug: bool) -> tuple[dict | None, str | None]:
    try:
        response = httpx.post(f"{API_URL}/qa", params={"debug": str(debug).lower()},
                              json={"question": question, "top_k": top_k}, timeout=TIMEOUT_SECONDS)
        if response.status_code == 422:
            return None, "The API rejected the question (it must be 1 to 1000 characters)."
        response.raise_for_status()
        return response.json(), None
    except httpx.HTTPError as exc:
        return None, f"Could not reach the API at {API_URL}: {exc}"


st.title("GuideRail")
st.caption("Citation-first answers from healthcare guideline documents. Every answer is checked against its evidence "
           "and sent to review when the support is weak.")

with st.sidebar:
    st.header("Service")
    health = fetch_health()
    if health is None:
        st.error(f"API not reachable at {API_URL}")
    else:
        st.success("API online")
        st.write(f"Documents: {health['documents']}")
        st.write(f"Chunks: {health['chunks']}")
        st.write(f"Generator: {health['generator']}")
        st.write(f"Threshold: {health['threshold']}")
        st.caption(f"Index {health['index_sha256'][:12]}")
    st.header("Options")
    top_k = st.slider("Passages to retrieve (top_k)", min_value=1, max_value=20, value=5)
    show_debug = st.checkbox("Show validator details", value=False)

question = st.text_input("Question", placeholder="e.g. How long should alcohol-based hand rub be applied?")

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Type a question first.")
    else:
        with st.spinner("Searching the guidelines..."):
            result, error = ask(question.strip(), top_k, show_debug)
        if error:
            st.error(error)
        else:
            left, right = st.columns([4, 1])
            with right:
                st.metric("Confidence", f"{result['confidence']:.2f}")
                if result["status"] == "validated":
                    st.success("validated")
                else:
                    st.warning("needs_review")
            with left:
                st.subheader("Answer")
                st.write(result["answer"])
                if result["status"] == "needs_review":
                    st.info("This answer was not validated. Treat it as unconfirmed and check the cited sources.")
            st.subheader("Citations")
            if result["citations"]:
                st.dataframe(
                    [{"Source": c["title"], "Agency": c["agency"], "Year": c["year"], "Version": c["version"],
                      "Section": c["section"], "Score": round(c["score"], 3)} for c in result["citations"]],
                    use_container_width=True, hide_index=True)
            else:
                st.write("No supporting passages.")
            if show_debug and result.get("debug"):
                with st.expander("Validator details"):
                    st.json(result["debug"])
