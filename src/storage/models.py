"""데이터 모델 정의"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Conference:
    """학회 정보"""
    name: str
    year: int
    volume: Optional[str] = None
    proceedings_url: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class Paper:
    """논문 메타정보"""
    title: str
    authors: str
    conference_id: int
    issue: Optional[int] = None
    start_page: Optional[int] = None
    end_page: Optional[int] = None
    pdf_url: Optional[str] = None
    pdf_path: Optional[str] = None
    abstract: Optional[str] = None
    status: str = "pending"  # pending, downloaded, summarized
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class PaperTag:
    """논문 분류/태그"""
    paper_id: int
    tag: str
    confidence: float = 1.0
