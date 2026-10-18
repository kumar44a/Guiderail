"""FastAPI service. Run: uvicorn guiderail.api:app --app-dir src --port 9070"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from . import __version__, config
from .generators import Generator
from .index import load_index
from .service import QAService


class QARequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)

    @field_validator("question")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must not be blank")
        return value


class Citation(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    agency: str
    year: int
    version: int
    section: str
    score: float


class QAResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float = Field(ge=0.0, le=1.0)
    status: Literal["validated", "needs_review"]
    debug: dict | None = None      # present only when ?debug=true


class HealthResponse(BaseModel):
    status: Literal["ok"]
    version: str
    index_sha256: str
    documents: int
    chunks: int
    generator: str
    threshold: float


def _build_generator() -> Generator | None:
    if config.generator_name() == "llm":
        from .generators.llm import LlmGenerator

        return LlmGenerator()
    return None  # QAService default (extractive)


def create_app(index_dir=None, generator: Generator | None = None, threshold: float | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        loaded = load_index(index_dir or config.index_dir())
        app.state.service = QAService(
            loaded,
            generator=generator or _build_generator(),
            threshold=config.threshold() if threshold is None else threshold,
        )
        yield

    app = FastAPI(
        title="GuideRail: Healthcare Guidelines RAG Assistant",
        version=__version__,
        description="Citation-first answers from guideline documents, validated against the retrieved evidence.",
        lifespan=lifespan,
    )

    def service_of(request: Request) -> QAService:
        service = getattr(request.app.state, "service", None)
        if service is None:
            raise HTTPException(status_code=503, detail="index not loaded")
        return service

    @app.post("/qa", response_model=QAResponse, response_model_exclude_none=True)
    def qa(body: QARequest, request: Request, debug: bool = False) -> QAResponse:
        result = service_of(request).ask(body.question, body.top_k)
        return QAResponse(
            answer=result.answer,
            citations=result.citations,
            confidence=result.confidence,
            status=result.status,
            debug=result.debug if debug else None,
        )

    @app.get("/health", response_model=HealthResponse)
    def health(request: Request) -> HealthResponse:
        service = service_of(request)
        manifest = service.loaded.manifest
        return HealthResponse(
            status="ok",
            version=__version__,
            index_sha256=manifest["hashes"]["index_sha256"],
            documents=manifest["counts"]["documents"],
            chunks=manifest["counts"]["chunks"],
            generator=service.generator.name,
            threshold=service.threshold,
        )

    return app


app = create_app()
