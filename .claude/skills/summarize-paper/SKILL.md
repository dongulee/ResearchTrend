---
name: summarize-paper
description: 다운로드된 논문 PDF를 읽고 요약 정보 생성. 논문 요약, 주제 분류, 핵심 내용 추출 시 사용.
argument-hint: <paper_id> | --conference <학회명> [연도] [--limit N]
allowed-tools: Bash, Read, Write
---

# 논문 요약 생성

## 인자
- `$0`: paper_id (단일 논문) 또는 `--conference`
- `$1`: 학회명 (--conference 사용 시)
- `$2`: 연도 (선택)
- `--limit N`: 요약할 최대 논문 수

## 실행 절차

### 1. 논문 텍스트 추출

```bash
uv run python -c "
import sys
sys.path.insert(0, '.')

from src.storage.database import Database
from src.utils.pdf_handler import PDFHandler

db = Database()
handler = PDFHandler()

paper = db.get_paper($0)
if not paper:
    print('논문을 찾을 수 없습니다.')
    exit(1)

text = handler.get_paper_text($0)
if not text:
    print('PDF 텍스트를 추출할 수 없습니다. 먼저 /download-pdfs를 실행하세요.')
    exit(1)

print(f'제목: {paper.title}')
print(f'저자: {paper.authors}')
print(f'텍스트 길이: {len(text)} 문자')
print('---')
print(text[:3000])
"
```

### 2. 요약 생성

PDF 텍스트를 분석하여 다음 구조로 요약을 생성:

```json
{
  "paper_id": <paper_id>,
  "title": "<논문 제목>",
  "authors": "<저자 목록>",
  "summary": {
    "objective": "<연구 목적>",
    "methodology": "<방법론>",
    "contributions": ["<핵심 기여 1>", "<핵심 기여 2>"],
    "experiments": "<실험 결과 요약>",
    "limitations": "<한계점>"
  },
  "tags": [
    {"tag": "<주제 태그>", "confidence": 0.9}
  ],
  "key_findings": ["<핵심 발견 1>", "<핵심 발견 2>"]
}
```

### 3. 주제 분류 태그

**데이터베이스/시스템**
- Query Processing, Query Optimization, Indexing
- Transaction Processing, Concurrency Control
- Storage Systems, Distributed Systems
- Stream Processing, Real-time Analytics

**데이터 관리**
- Data Integration, Data Quality, Data Cleaning
- Schema Design, Data Modeling

**분석/ML**
- Machine Learning, Deep Learning
- Graph Analytics, Network Analysis
- Natural Language Processing

**응용**
- Cloud Computing, Serverless
- Privacy, Security
- Benchmarking, Performance

### 4. 요약 저장

```bash
uv run python -c "
import json
from pathlib import Path
import sys
sys.path.insert(0, '.')

from src.utils.config import Config
from src.storage.database import Database
from src.storage.models import PaperTag

db = Database()
paper_id = $0

# summary_data는 위에서 생성한 요약 데이터
summary_data = $SUMMARY_JSON

summary_path = Config.SUMMARIES_DIR / f'{paper_id}.json'
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(summary_data, f, ensure_ascii=False, indent=2)

for tag_info in summary_data['tags']:
    tag = PaperTag(
        paper_id=paper_id,
        tag=tag_info['tag'],
        confidence=tag_info['confidence']
    )
    db.add_paper_tag(tag)

db.update_paper_status(paper_id, 'summarized')
print(f'요약 저장됨: {summary_path}')
"
```

## 출력 예시

```
=== 논문 요약 ===
제목: The Key to Effective UDF Optimization...
저자: Samuel Arch, Yuchen Liu, ...

[연구 목적]
사용자 정의 함수(UDF)의 최적화 효율성 향상

[방법론]
- 새로운 UDF 분석 프레임워크 제안
- 비용 기반 최적화 기법 적용

[핵심 기여]
1. UDF 실행 비용 모델링
2. 최적화 알고리즘 설계

[태그] Query Optimization, UDF, Performance
```
