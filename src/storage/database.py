"""SQLite 데이터베이스 관리"""
import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from .models import Conference, Paper, PaperTag
from ..utils.config import Config


class Database:
    """SQLite 데이터베이스 관리 클래스"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.DB_PATH
        Config.ensure_dirs()
        self._init_schema()

    @contextmanager
    def _get_connection(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self):
        """데이터베이스 스키마 초기화"""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS conferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    volume TEXT,
                    proceedings_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(name, year)
                );

                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conference_id INTEGER NOT NULL REFERENCES conferences(id),
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    issue INTEGER,
                    start_page INTEGER,
                    end_page INTEGER,
                    pdf_url TEXT,
                    pdf_path TEXT,
                    abstract TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(conference_id, title)
                );

                CREATE TABLE IF NOT EXISTS paper_tags (
                    paper_id INTEGER NOT NULL REFERENCES papers(id),
                    tag TEXT NOT NULL,
                    confidence REAL DEFAULT 1.0,
                    PRIMARY KEY (paper_id, tag)
                );

                CREATE INDEX IF NOT EXISTS idx_papers_conference ON papers(conference_id);
                CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(status);
                CREATE INDEX IF NOT EXISTS idx_paper_tags_tag ON paper_tags(tag);
            """)

    # Conference CRUD
    def add_conference(self, conf: Conference) -> int:
        """학회 추가 (이미 존재하면 ID 반환)"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id FROM conferences WHERE name = ? AND year = ?",
                (conf.name, conf.year)
            )
            row = cursor.fetchone()
            if row:
                return row['id']

            cursor = conn.execute(
                """INSERT INTO conferences (name, year, volume, proceedings_url)
                   VALUES (?, ?, ?, ?)""",
                (conf.name, conf.year, conf.volume, conf.proceedings_url)
            )
            return cursor.lastrowid

    def get_conference(self, name: str, year: int) -> Optional[Conference]:
        """학회 조회"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM conferences WHERE name = ? AND year = ?",
                (name, year)
            )
            row = cursor.fetchone()
            if row:
                return Conference(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    volume=row['volume'],
                    proceedings_url=row['proceedings_url'],
                    created_at=row['created_at']
                )
            return None

    # Paper CRUD
    def add_paper(self, paper: Paper) -> int:
        """논문 추가 (이미 존재하면 ID 반환)"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT id FROM papers WHERE conference_id = ? AND title = ?",
                (paper.conference_id, paper.title)
            )
            row = cursor.fetchone()
            if row:
                return row['id']

            cursor = conn.execute(
                """INSERT INTO papers
                   (conference_id, title, authors, issue, start_page, end_page,
                    pdf_url, pdf_path, abstract, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (paper.conference_id, paper.title, paper.authors, paper.issue,
                 paper.start_page, paper.end_page, paper.pdf_url, paper.pdf_path,
                 paper.abstract, paper.status)
            )
            return cursor.lastrowid

    def get_paper(self, paper_id: int) -> Optional[Paper]:
        """논문 조회"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_paper(row)
            return None

    def get_papers_by_conference(self, conference_id: int, status: Optional[str] = None) -> list[Paper]:
        """학회별 논문 목록 조회"""
        with self._get_connection() as conn:
            if status:
                cursor = conn.execute(
                    "SELECT * FROM papers WHERE conference_id = ? AND status = ? ORDER BY issue, start_page",
                    (conference_id, status)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM papers WHERE conference_id = ? ORDER BY issue, start_page",
                    (conference_id,)
                )
            return [self._row_to_paper(row) for row in cursor.fetchall()]

    def update_paper_status(self, paper_id: int, status: str, pdf_path: Optional[str] = None):
        """논문 상태 업데이트"""
        with self._get_connection() as conn:
            if pdf_path:
                conn.execute(
                    "UPDATE papers SET status = ?, pdf_path = ? WHERE id = ?",
                    (status, pdf_path, paper_id)
                )
            else:
                conn.execute(
                    "UPDATE papers SET status = ? WHERE id = ?",
                    (status, paper_id)
                )

    # Paper Tags
    def add_paper_tag(self, tag: PaperTag):
        """논문 태그 추가"""
        with self._get_connection() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO paper_tags (paper_id, tag, confidence)
                   VALUES (?, ?, ?)""",
                (tag.paper_id, tag.tag, tag.confidence)
            )

    def get_paper_tags(self, paper_id: int) -> list[PaperTag]:
        """논문 태그 조회"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM paper_tags WHERE paper_id = ? ORDER BY confidence DESC",
                (paper_id,)
            )
            return [
                PaperTag(paper_id=row['paper_id'], tag=row['tag'], confidence=row['confidence'])
                for row in cursor.fetchall()
            ]

    # Statistics
    def get_stats(self, conference_id: Optional[int] = None) -> dict:
        """통계 조회"""
        with self._get_connection() as conn:
            if conference_id:
                where = "WHERE conference_id = ?"
                params = (conference_id,)
            else:
                where = ""
                params = ()

            cursor = conn.execute(f"""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'downloaded' THEN 1 ELSE 0 END) as downloaded,
                    SUM(CASE WHEN status = 'summarized' THEN 1 ELSE 0 END) as summarized
                FROM papers {where}
            """, params)
            row = cursor.fetchone()
            return {
                'total': row['total'] or 0,
                'pending': row['pending'] or 0,
                'downloaded': row['downloaded'] or 0,
                'summarized': row['summarized'] or 0
            }

    def _row_to_paper(self, row) -> Paper:
        """Row를 Paper 객체로 변환"""
        return Paper(
            id=row['id'],
            conference_id=row['conference_id'],
            title=row['title'],
            authors=row['authors'],
            issue=row['issue'],
            start_page=row['start_page'],
            end_page=row['end_page'],
            pdf_url=row['pdf_url'],
            pdf_path=row['pdf_path'],
            abstract=row['abstract'],
            status=row['status'],
            created_at=row['created_at']
        )
