from google.adk.agents import LlmAgent
from tools import web_search_tool
import json

def analyze_job_role_from_web(company_name: str, job_role: str) -> str:
    """
    Searches press outlets for in-depth information about a specific job role at a given company,
    focusing on aspects relevant to a senior (50-60) job seeker.
    """
    search_query = f"매일경제 {company_name} {job_role} 직무 인터뷰 채용 공고 요구 역량 커리어 경로"
    search_results = web_search_tool(search_query)

    return json.dumps({
        "company_name": company_name,
        "job_role": job_role,
        "search_results": search_results,
        "analysis_hint": "Based on the provided articles, analyze the key responsibilities, required skills, career path, and suitability of this job role for a senior candidate."
    })

job_market_analyst = LlmAgent(
    name="JobMarketAnalyst",
    model="gemini-2.5-flash",
    description="Performs an in-depth analysis of a specific job role within a company for a senior candidate.",
    instruction="""
    You are a Job Market Analyst specializing in assessing specific job roles for 5060 senior candidates.
    Your mission is to conduct a deep analysis of the provided job role based on information from reliable media outlets.

    **Data Source Constraint**:
    Your analysis MUST be grounded in information from press outlets.
    Prioritize major economic newspapers like 'Maeil Business Newspaper' (매일경제).

    **ANALYSIS POINTS (for the specific {Job Role}):**
    1.  **Main Responsibilities (주요 업무)**: What are the core tasks and duties of this job, based on interviews or job descriptions in the press?
    2.  **Required Skills & Experience (요구 역량)**: What specific skills, technologies, or years of experience are mentioned as necessary? Are there any certifications or qualifications preferred?
    3.  **Career Path & Vision (커리어 경로 및 비전)**: Do articles mention the growth prospects of this role? What is the typical career progression?
    4.  **Suitability for Seniors (5060 적합성)**: Based on the required skills and reported work environment, how suitable is this role for an experienced professional in their 50-60s? Does it value experience and wisdom over physical energy?

    Use the provided web search results to build a detailed and practical analysis of the job role.
    """,
    tools=[
        analyze_job_role_from_web,
    ],
    output_key="job_market_analyst_result",
)