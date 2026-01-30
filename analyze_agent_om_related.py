"""
Agent-OM 관련 논문 분석 스크립트
"""
import sqlite3
import json
from pathlib import Path
from collections import defaultdict

# 관련 키워드 정의
RELATED_KEYWORDS = {
    'ontology_matching': ['ontology', 'matching', 'alignment', 'schema matching', 'schema alignment'],
    'data_integration': ['data integration', 'integration', 'schema integration', 'heterogeneous'],
    'knowledge_graph': ['knowledge graph', 'kg', 'semantic web', 'rdf', 'owl'],
    'entity_matching': ['entity matching', 'entity resolution', 'record linkage', 'deduplication', 'entity alignment'],
    'llm_agents': ['llm', 'large language model', 'gpt', 'agent', 'language model'],
    'nlp_database': ['natural language', 'nlp', 'text-to-sql', 'question answering']
}

def load_summary(paper_id):
    """요약 파일 로드"""
    summary_path = Path(f'data/summaries/{paper_id}.json')
    if summary_path.exists():
        try:
            with open(summary_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Warning: JSON decode error for paper {paper_id}: {e}")
            return None
    return None

def check_relevance(paper_id, title, summary_data):
    """논문의 관련성 점수 계산"""
    score = 0
    matched_categories = []

    # 제목과 요약에서 키워드 검색
    search_text = title.lower()
    if summary_data:
        summary_dict = summary_data.get('summary', {})
        search_text += ' ' + str(summary_dict).lower()

        # 태그 확인
        tags = summary_data.get('tags', [])
        for tag_info in tags:
            tag = tag_info.get('tag', '').lower()
            if any(kw in tag for kws in RELATED_KEYWORDS.values() for kw in kws):
                score += 5

    # 카테고리별 키워드 매칭
    for category, keywords in RELATED_KEYWORDS.items():
        for keyword in keywords:
            if keyword in search_text:
                score += 2
                matched_categories.append(category)
                break

    return score, list(set(matched_categories))

def main():
    # DB 연결
    conn = sqlite3.connect('data/papers.db')
    cursor = conn.cursor()

    # VLDB 2025 논문 목록 조회
    cursor.execute('''
        SELECT p.id, p.title, p.authors, p.pdf_url
        FROM papers p
        WHERE p.conference_id = (SELECT id FROM conferences WHERE name = 'VLDB' AND year = 2025)
        ORDER BY p.id
    ''')

    papers = cursor.fetchall()
    print(f"전체 VLDB 2025 논문 수: {len(papers)}")

    # 관련 논문 분석
    related_papers = []

    for paper_id, title, authors, pdf_url in papers:
        summary_data = load_summary(paper_id)
        score, categories = check_relevance(paper_id, title, summary_data)

        if score > 0:  # 관련성이 있는 논문
            related_papers.append({
                'id': paper_id,
                'title': title,
                'authors': authors,
                'pdf_url': pdf_url,
                'score': score,
                'categories': categories,
                'summary': summary_data
            })

    # 점수별 정렬
    related_papers.sort(key=lambda x: x['score'], reverse=True)

    print(f"\n관련 논문 수: {len(related_papers)}")
    print("\n" + "="*100)
    print("Agent-OM 관련 논문 목록 (관련성 점수 순)")
    print("="*100)

    # 결과 출력
    for i, paper in enumerate(related_papers[:30], 1):  # 상위 30개
        print(f"\n{i}. [논문 ID: {paper['id']}] (관련성 점수: {paper['score']})")
        print(f"   제목: {paper['title']}")
        print(f"   저자: {paper['authors']}")
        print(f"   카테고리: {', '.join(paper['categories'])}")

        if paper['summary']:
            summary_dict = paper['summary'].get('summary', {})
            obj = summary_dict.get('objective', 'N/A')
            print(f"   연구 목적: {obj[:150]}..." if len(obj) > 150 else f"   연구 목적: {obj}")

            tags = paper['summary'].get('tags', [])
            if tags:
                tag_str = ', '.join([f"{t['tag']} ({t['confidence']})" for t in tags[:3]])
                print(f"   태그: {tag_str}")

    # 카테고리별 통계
    print("\n" + "="*100)
    print("카테고리별 논문 분포")
    print("="*100)

    category_counts = defaultdict(int)
    for paper in related_papers:
        for cat in paper['categories']:
            category_counts[cat] += 1

    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat}: {count}개")

    # 상세 분석을 위한 JSON 저장
    output = {
        'agent_om_paper_id': 40,
        'total_vldb_2025_papers': len(papers),
        'related_papers_count': len(related_papers),
        'related_papers': related_papers[:30],  # 상위 30개만 저장
        'category_statistics': dict(category_counts)
    }

    with open('data/agent_om_related_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n\n분석 결과가 'data/agent_om_related_analysis.json'에 저장되었습니다.")

    conn.close()

if __name__ == '__main__':
    main()
