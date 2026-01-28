---
name: download-pdfs
description: 수집된 논문의 PDF 파일을 다운로드. PDF 다운로드, 논문 파일 저장 시 사용.
argument-hint: <학회명> [연도] [--limit N]
allowed-tools: Bash, Read
---

# 논문 PDF 다운로드

## 인자
- `$0`: 학회명 (예: vldb)
- `$1`: 연도 (선택, 기본값: 2025)
- `--limit N`: 다운로드할 최대 논문 수 (선택)

## 실행 절차

### 1. 학회 정보 조회

```bash
uv run python -c "
import sys
sys.path.insert(0, '.')

from src.storage.database import Database

db = Database()
conf = db.get_conference('$0'.upper(), ${1:-2025})

if not conf:
    print('해당 학회를 찾을 수 없습니다. 먼저 /collect-papers를 실행하세요.')
    exit(1)
else:
    print(f'학회: {conf.name} {conf.year}')
    print(f'학회 ID: {conf.id}')
    stats = db.get_stats(conf.id)
    print(f'대기 중인 논문: {stats[\"pending\"]}개')
"
```

### 2. PDF 다운로드 실행

전체 다운로드:
```bash
uv run python -c "
import sys
sys.path.insert(0, '.')

from src.storage.database import Database
from src.utils.pdf_handler import PDFHandler

db = Database()
conf = db.get_conference('$0'.upper(), ${1:-2025})
handler = PDFHandler()

result = handler.download_all(
    conference_id=conf.id,
    delay=1.0
)

print(f'\n=== 다운로드 완료 ===')
print(f'처리된 논문: {result[\"total\"]}')
print(f'성공: {result[\"success\"]}')
print(f'실패: {result[\"failed\"]}')
"
```

제한된 다운로드 (--limit 옵션):
```bash
uv run python -c "
import sys
import time
sys.path.insert(0, '.')

from src.storage.database import Database
from src.utils.pdf_handler import PDFHandler

db = Database()
conf = db.get_conference('$0'.upper(), ${1:-2025})
handler = PDFHandler()

papers = db.get_papers_by_conference(conf.id, status='pending')
limit = $LIMIT  # 인자에서 추출
papers = papers[:limit]

success = failed = 0
for i, paper in enumerate(papers):
    print(f'[{i+1}/{len(papers)}] {paper.title[:50]}...')
    if handler.download_paper(paper):
        success += 1
    else:
        failed += 1
    if i < len(papers) - 1:
        time.sleep(1.0)

print(f'\n성공: {success}, 실패: {failed}')
"
```

## 다운로드 위치
- PDF 파일: `data/pdfs/`
- 파일명 형식: `{paper_id}_{title}.pdf`

## 오류 처리
- PDF URL이 없는 경우: 해당 논문 스킵
- 다운로드 실패: 오류 메시지 출력 후 다음 논문으로 진행
- 이미 존재하는 파일: 스킵
