import importlib.util

import pytest

from tests.conftest import ROOT

spec = importlib.util.spec_from_file_location("check_docs_sync", ROOT / "scripts" / "check_docs_sync.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

BLOCK = f"{sync.START}\nnew numbers\n{sync.END}"


def test_only_the_marked_block_is_replaced():
    current = f"# Title\n\nintro\n\n{sync.START}\nold numbers\n{sync.END}\n\noutro\n"
    out = sync.render_readme(current, BLOCK)
    assert out == f"# Title\n\nintro\n\n{BLOCK}\n\noutro\n"


def test_missing_markers_fail_loudly():
    with pytest.raises(SystemExit):
        sync.render_readme("# no block here", BLOCK)


def test_readme_has_the_markers_and_states_no_numbers_outside_them():
    import re
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert sync.START in text and sync.END in text
    outside = re.sub(re.escape(sync.START) + r".*?" + re.escape(sync.END), "", text, flags=re.DOTALL)
    assert not re.search(r"\b\d{2,3}(\.\d)?\s?%", outside)
