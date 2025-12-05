import yfinance as yf
from google.adk.agents import LlmAgent

def get_financial_statements(ticker: str):
    """
    Retrieves key financial statements (Income Statement, Balance Sheet, Cash Flow)
    to analyze a company's financial health and stability from a job seeker's perspective.
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
    Returns:
        dict: A dictionary containing the JSON-formatted financial statements.
    """
    stock = yf.Ticker(ticker)
    income_stmt = stock.income_stmt.to_json()
    balance_sheet = stock.balance_sheet.to_json()
    cash_flow = stock.cash_flow.to_json()
    
    return {
        "ticker": ticker,
        "success": True,
        "income_statement": income_stmt,
        "balance_sheet": balance_sheet,
        "cash_flow": cash_flow,
    }

financial_analyst = LlmAgent(
    name="FinancialAnalyst",
    model="gemini-2.5-flash",
    description="Analyzes a company's financial stability and growth potential based on its financial statements.",
    instruction="""
    You are a Financial Analyst focused on **Job Stability and Growth Potential**.
    Your task is to analyze financial statements to answer: "Is this company financially healthy enough to be a stable employer?" and "Is the company growing?".

    **ANALYSIS POINTS (from a job seeker's view):**
    1.  **Profitability (수익성)**: Is the company making money? Look at 'Total Revenue' and 'Net Income' trends from the Income Statement.
    2.  **Cash Flow (현금 흐름)**: Does the company have enough cash to operate? Check for positive 'Operating Cash Flow'. This is crucial for paying salaries.
    3.  **Growth Trajectory (성장성)**: Is revenue growing year over year? This can indicate a growing company with more opportunities.

    Based on the financial statements, provide a simple, clear summary of the company's financial health from an employment perspective.
    Categorize it as 'High Stability & Growth', 'Moderate Stability', or 'Potential Financial Risk'.
    """,
    tools=[
        get_financial_statements,
    ],
    output_key="financial_analyst_result",
)