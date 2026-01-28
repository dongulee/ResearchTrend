"""PDF 다운로드 및 텍스트 추출"""
import time
from pathlib import Path
from typing import Optional

import requests

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

from ..storage.database import Database
from ..storage.models import Paper
from ..utils.config import Config


class PDFHandler:
    """PDF 다운로드 및 텍스트 추출 핸들러"""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
        Config.ensure_dirs()

    def download_paper(self, paper: Paper) -> Optional[Path]:
        """
        논문 PDF 다운로드

        Args:
            paper: 논문 객체

        Returns:
            저장된 파일 경로 또는 None
        """
        if not paper.pdf_url:
            return None

        # 파일명 생성 (ID_제목일부.pdf)
        safe_title = "".join(c for c in paper.title[:50] if c.isalnum() or c in ' -_').strip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"{paper.id}_{safe_title}.pdf"
        filepath = Config.PDF_DIR / filename

        # 이미 존재하면 스킵
        if filepath.exists():
            return filepath

        try:
            response = requests.get(
                paper.pdf_url,
                headers=Config.REQUEST_HEADERS,
                timeout=Config.REQUEST_TIMEOUT,
                stream=True
            )
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # DB 상태 업데이트
            self.db.update_paper_status(paper.id, 'downloaded', str(filepath))

            return filepath

        except requests.RequestException as e:
            print(f"다운로드 실패 [{paper.id}]: {e}")
            return None

    def download_all(self, conference_id: int, delay: float = None) -> dict:
        """
        학회의 모든 논문 PDF 다운로드

        Args:
            conference_id: 학회 ID
            delay: 다운로드 간 대기 시간 (초)

        Returns:
            다운로드 결과 통계
        """
        delay = delay or Config.PDF_DOWNLOAD_DELAY
        papers = self.db.get_papers_by_conference(conference_id, status='pending')

        success = 0
        failed = 0

        for i, paper in enumerate(papers):
            print(f"[{i+1}/{len(papers)}] 다운로드 중: {paper.title[:50]}...")

            result = self.download_paper(paper)
            if result:
                success += 1
            else:
                failed += 1

            if i < len(papers) - 1:
                time.sleep(delay)

        return {
            'total': len(papers),
            'success': success,
            'failed': failed
        }

    def extract_text(self, pdf_path: Path) -> Optional[str]:
        """
        PDF에서 텍스트 추출

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            추출된 텍스트 또는 None
        """
        if not pdf_path.exists():
            return None

        # PyMuPDF 우선 사용
        if HAS_PYMUPDF:
            return self._extract_with_pymupdf(pdf_path)

        # pdfplumber 대안
        if HAS_PDFPLUMBER:
            return self._extract_with_pdfplumber(pdf_path)

        raise RuntimeError("PDF 텍스트 추출 라이브러리가 설치되지 않음 (PyMuPDF 또는 pdfplumber 필요)")

    def _extract_with_pymupdf(self, pdf_path: Path) -> str:
        """PyMuPDF로 텍스트 추출"""
        doc = fitz.open(pdf_path)
        text_parts = []

        for page in doc:
            text_parts.append(page.get_text())

        doc.close()
        return "\n".join(text_parts)

    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """pdfplumber로 텍스트 추출"""
        text_parts = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        return "\n".join(text_parts)

    def get_paper_text(self, paper_id: int) -> Optional[str]:
        """논문 ID로 텍스트 추출"""
        paper = self.db.get_paper(paper_id)
        if not paper or not paper.pdf_path:
            return None

        return self.extract_text(Path(paper.pdf_path))
