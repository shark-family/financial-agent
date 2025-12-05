# main.py
from client import GeminiClient
from prompt_builder import PromptBuilder
from parser import ResponseParser
from models import AnalysisInput, UserProfile


def run_analysis():
    # === 사용자 입력 ===
    company = input("회사명: ")
    job = input("직무명: ")

    user_skills = input("보유 기술 (쉼표로 구분): ").split(",")
    user_exps = input("주요 경력 (세미콜론으로 구분): ").split(";")
    print("진행 중 ...")

    user_profile = UserProfile(skills=user_skills, experiences=user_exps)

    analysis_input = AnalysisInput(
        company_name=company,
        job_role=job,
        user_profile=user_profile,
    )

    # === 프롬프트 생성 ===
    prompt = PromptBuilder.build_prompt(analysis_input)

    # === Gemini 요청 ===
    client = GeminiClient()
    response_text = client.request(prompt)

    # === 응답 파싱 ===
    parsed = ResponseParser.parse(response_text)

    # === 결과 출력 ===
    print("\n\n===== 분석 결과 =====\n")

    # 1) 회사/재무/동향
    for section in [
        parsed.company_info,
        parsed.financial_status,
        parsed.trends,
    ]:
        print(f"📌 {section.title}\n{section.content}\n")

    # 2) 직무 심층 분석 (개요 + 주요 업무 + 요구 역량 + 커리어 경로)
    ja = parsed.job_analysis
    print(f"📌 {ja.title}\n")
    print(f"[개요]\n{ja.overview}\n")

    if ja.main_tasks:
        print("[주요 업무]")
        for t in ja.main_tasks:
            print(f" - {t}")
        print()

    if ja.required_skills:
        print("[요구 역량]")
        for s in ja.required_skills:
            print(f" - {s}")
        print()

    if ja.career_path:
        print("[커리어 경로]")
        for c in ja.career_path:
            print(f" - {c}")
        print()

    # 3) 지원자 강점/핵심 과제
    sf = parsed.senior_fit
    print(f"📌 {sf.title}\n")
    print("[강점]")
    print(sf.strengths, "\n")
    print("[핵심 과제]")
    print(sf.key_challenges, "\n")

    # 4) Coach's Tip
    print(f"📌 {parsed.coach_tip.title}\n{parsed.coach_tip.content}\n")

    # 5) 관련 뉴스
    if parsed.related_news:
        print("===== 관련 매일경제 기사 =====\n")
        for news in parsed.related_news:
            print(f"📰 {news.title}")
            print(f"   출처: {news.source}")
            print(f"   링크: {news.url}")
            print(f"   이유: {news.reason}\n")


if __name__ == "__main__":
    run_analysis()
