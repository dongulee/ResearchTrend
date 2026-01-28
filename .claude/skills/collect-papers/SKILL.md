---
name: collect-papers
description: 학회 proceedings 웹페이지에서 논문 메타정보(제목, 저자, PDF 링크)를 수집하여 데이터베이스에 저장. 논문 수집, 메타데이터 크롤링, proceedings 파싱 시 사용.
argument-hint: <학회명> <proceedings_url> [연도]
allowed-tools: Bash, Read, Write, WebFetch
---

# 학회 논문 목록 수집

## 인자
- `$0`: 학회명 (예: vldb, sigmod, icde)
- `$1`: proceedings URL
- `$2`: 연도 (선택, 기본값: 2025)

## 실행 절차

### 1. VLDB 논문 수집

```bash
uv run python -c "
import sys
sys.path.insert(0, '.')

from src.collectors.vldb_collector import VLDBCollector

collector = VLDBCollector()
result = collector.collect(
    url='$1',
    year=${2:-2025}
)

print(f'\n=== 수집 완료 ===')
print(f'학회: {result[\"conference\"]}')
print(f'학회 ID: {result[\"conference_id\"]}')
print(f'발견된 논문 수: {result[\"total_found\"]}')
print(f'새로 추가됨: {result[\"added\"]}')
print(f'이미 존재함: {result[\"skipped\"]}')
"
```

### 2. 수집 결과 확인

```bash
uv run python -c "
from src.storage.database import Database

db = Database()
stats = db.get_stats()

print(f'\n=== 데이터베이스 통계 ===')
print(f'전체 논문: {stats[\"total\"]}')
print(f'대기 중: {stats[\"pending\"]}')
print(f'다운로드됨: {stats[\"downloaded\"]}')
print(f'요약됨: {stats[\"summarized\"]}')
"
```

## 오류 처리
- URL이 잘못된 경우: "올바른 proceedings URL을 입력해주세요"
- 네트워크 오류: "페이지에 접근할 수 없습니다. URL을 확인해주세요"
- 파싱 실패: "논문 정보를 파싱하는데 실패했습니다"

## 지원 학회
- **VLDB**: https://www.vldb.org/pvldb/volumes/{volume}/
