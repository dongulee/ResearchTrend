"""VLDB Proceedings 크롤러"""
import json
import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

from ..storage.database import Database
from ..storage.models import Conference, Paper
from ..utils.config import Config


class VLDBCollector:
    """VLDB proceedings 논문 수집기"""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def collect(self, url: str, year: int = 2025) -> dict:
        """
        VLDB proceedings 페이지에서 논문 메타정보 수집

        Args:
            url: proceedings 페이지 URL (e.g., https://www.vldb.org/pvldb/volumes/18/)
            year: 학회 연도

        Returns:
            수집 결과 통계 dict
        """
        # 볼륨 번호 추출
        volume_match = re.search(r'/volumes/(\d+)', url)
        volume = volume_match.group(1) if volume_match else None

        # 학회 등록
        conf = Conference(
            name="VLDB",
            year=year,
            volume=volume,
            proceedings_url=url
        )
        conference_id = self.db.add_conference(conf)

        # 페이지 가져오기
        response = requests.get(
            url,
            headers=Config.REQUEST_HEADERS,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()

        # JSON 데이터 파싱
        papers_data = self._extract_papers_json(response.text)

        # 논문 저장
        added_count = 0
        skipped_count = 0

        for paper_info in papers_data:
            # Front Matter 스킵
            if paper_info.get('title', '').lower().startswith('front matter'):
                continue

            paper = Paper(
                conference_id=conference_id,
                title=paper_info.get('title', ''),
                authors=paper_info.get('authors', ''),
                issue=paper_info.get('issue'),
                start_page=paper_info.get('start_page'),
                end_page=paper_info.get('end_page'),
                pdf_url=paper_info.get('pdf'),
                status='pending'
            )

            paper_id = self.db.add_paper(paper)
            if paper_id:
                added_count += 1
            else:
                skipped_count += 1

        return {
            'conference': f"VLDB {year}",
            'conference_id': conference_id,
            'total_found': len(papers_data),
            'added': added_count,
            'skipped': skipped_count
        }

    def _extract_papers_json(self, html: str) -> list[dict]:
        """HTML에서 논문 JSON 데이터 추출"""
        soup = BeautifulSoup(html, 'html.parser')

        # script 태그에서 JSON 데이터 찾기
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'groupedIssues' in script.string:
                # JSON 객체 추출
                match = re.search(r'groupedIssues\s*[=:]\s*({[^;]+})', script.string)
                if match:
                    try:
                        grouped = json.loads(match.group(1))
                        papers = []
                        for issue_num, issue_papers in grouped.items():
                            for paper in issue_papers:
                                paper['issue'] = int(issue_num) if issue_num.isdigit() else None
                                papers.append(paper)
                        return papers
                    except json.JSONDecodeError:
                        pass

        # 대안: 직접 JSON 패턴 매칭
        json_pattern = r'\{["\']issue["\']:\s*\d+[^}]+\}'
        matches = re.findall(json_pattern, html)
        papers = []
        for match in matches:
            try:
                paper = json.loads(match.replace("'", '"'))
                papers.append(paper)
            except json.JSONDecodeError:
                continue

        return papers


def collect_vldb(url: str, year: int = 2025) -> dict:
    """VLDB 논문 수집 편의 함수"""
    collector = VLDBCollector()
    return collector.collect(url, year)
