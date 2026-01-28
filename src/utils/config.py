"""설정 관리 모듈"""
from pathlib import Path


class Config:
    """프로젝트 설정"""

    # 프로젝트 루트 디렉토리
    ROOT_DIR = Path(__file__).parent.parent.parent

    # 데이터 디렉토리
    DATA_DIR = ROOT_DIR / "data"
    PDF_DIR = DATA_DIR / "pdfs"
    SUMMARIES_DIR = DATA_DIR / "summaries"
    REPORTS_DIR = DATA_DIR / "reports"

    # 데이터베이스
    DB_PATH = DATA_DIR / "papers.db"

    # HTTP 요청 설정
    REQUEST_TIMEOUT = 30
    REQUEST_HEADERS = {
        "User-Agent": "PaperResearch/1.0 (Academic Research Tool)"
    }

    # PDF 다운로드 설정
    PDF_DOWNLOAD_DELAY = 1.0  # 초 단위 대기 시간

    @classmethod
    def ensure_dirs(cls):
        """필요한 디렉토리 생성"""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.PDF_DIR.mkdir(exist_ok=True)
        cls.SUMMARIES_DIR.mkdir(exist_ok=True)
        cls.REPORTS_DIR.mkdir(exist_ok=True)
