---
name: generate-report
description: 요약된 논문 정보를 기반으로 학회 연구 동향 보고서 생성. 보고서 작성, 트렌드 분석, 연구 동향 파악 시 사용.
argument-hint: <학회명> [연도] [overview|trends|detailed]
allowed-tools: Bash, Read, Write
---

# 종합 보고서 생성

## 인자
- `$0`: 학회명 (예: vldb)
- `$1`: 연도 (선택, 기본값: 2025)
- `$2`: 보고서 유형 (overview/trends/detailed, 기본값: overview)

## 보고서 유형
- `overview`: 전체 개요 보고서
- `trends`: 연구 트렌드 분석
- `detailed`: 상세 논문 목록

## 실행 절차

### 1. 데이터 수집

```bash
uv run python -c "
import sys
import json
sys.path.insert(0, '.')

from src.storage.database import Database
from src.utils.config import Config

db = Database()
conf = db.get_conference('$0'.upper(), ${1:-2025})

if not conf:
    print('해당 학회를 찾을 수 없습니다.')
    exit(1)

papers = db.get_papers_by_conference(conf.id)
stats = db.get_stats(conf.id)

summaries = []
for paper in papers:
    summary_path = Config.SUMMARIES_DIR / f'{paper.id}.json'
    if summary_path.exists():
        with open(summary_path, 'r', encoding='utf-8') as f:
            summaries.append(json.load(f))

print(f'학회: {conf.name} {conf.year}')
print(f'전체 논문: {stats[\"total\"]}')
print(f'요약된 논문: {len(summaries)}')
"
```

### 2. Overview 보고서 형식

```markdown
# {학회명} {연도} 연구 동향 보고서

## 개요
- **학회**: {학회명} {연도}
- **총 논문 수**: {total}편
- **분석된 논문**: {summarized}편
- **생성일**: {날짜}

## 주제별 분포

| 연구 주제 | 논문 수 | 비율 |
|-----------|---------|------|
| Query Optimization | N | X% |
| Machine Learning | N | X% |

## 주요 연구 트렌드

### 1. [트렌드 1 제목]
{트렌드 설명 및 관련 논문}

## 핵심 논문 하이라이트

### {논문 제목}
- **저자**: {저자}
- **핵심 기여**: {기여 요약}

## 결론
{전반적인 연구 동향 요약}
```

### 3. Trends 보고서 형식

```markdown
# {학회명} {연도} 연구 트렌드 분석

## 주요 연구 영역 변화

### 상승 트렌드
- {트렌드 1}: {설명}

### 신규 연구 주제
- {새로운 주제들}

## 키워드 빈도 분석
{논문 제목/요약에서 추출한 키워드 분석}

## 연구 방향 예측
{향후 연구 방향에 대한 분석}
```

### 4. Detailed 보고서 형식

```markdown
# {학회명} {연도} 논문 상세 목록

## Issue 1

### 1. {논문 제목}
- **저자**: {저자}
- **페이지**: {start}-{end}
- **태그**: {태그 목록}
- **요약**: {요약}
```

### 5. 보고서 저장

```bash
uv run python -c "
from datetime import datetime
from pathlib import Path
import sys
sys.path.insert(0, '.')

from src.utils.config import Config

report_type = '${2:-overview}'
filename = f'$0_{${1:-2025}}_{report_type}.md'
report_path = Config.REPORTS_DIR / filename

# report_content는 위에서 생성한 보고서 내용
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f'보고서 생성됨: {report_path}')
"
```

## 보고서 품질 체크리스트
- [ ] 통계 수치가 정확한가?
- [ ] 주제별 분류가 논리적인가?
- [ ] 트렌드 분석이 데이터 기반인가?
- [ ] 마크다운 형식이 올바른가?
