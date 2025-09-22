import os
import argparse
import vertexai
from dotenv import load_dotenv

from utils import file_parser
from agents import (
    financial_agent,
    market_agent,
    team_agent,
    public_data_agent,
    risk_agent,
    benchmark_agent,
    recommendation_agent
)


def run_analysis(file_path):
    """Runs the full analysis pipeline on a given file."""
    # Initialize Vertex AI with the correct project from .env
    print(f"--- DEBUG: Initializing Vertex AI with project: {os.getenv('GOOGLE_CLOUD_PROJECT')} ---")
    vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION"))
    try:
        # 1. Document Ingestion
        content = file_parser.parse_file(file_path)
        company_name = content.splitlines()[0] if content else "Unknown Company"

        # 2. Parallel Processing Agents
        financial_data = financial_agent.analyze_financials(content)
        market_data = market_agent.analyze_market(content)
        team_data = team_agent.analyze_team(content)
        public_data = public_data_agent.analyze_public_data(company_name)

        # Combine parallel results
        combined_data = {
            "company_name": company_name,
            **financial_data,
            **market_data,
            **team_data,
            **public_data
        }

        # 3. Sequential Analysis Agents
        risk_data = risk_agent.analyze_risk(combined_data)
        benchmark_data = benchmark_agent.benchmark_metrics(combined_data)

        # Combine all data for final recommendation
        final_data = {**combined_data, **risk_data, **benchmark_data}

        recommendation_data = recommendation_agent.generate_recommendation(final_data)

        # 4. Final Output Assembly
        report = {
            "company_name": company_name,
            "recommendation": recommendation_data,
            "metrics": {
                "revenue": financial_data.get('revenue'),
                "cac": financial_data.get('cac'),
                "ltv": financial_data.get('ltv'),
                "tam": market_data.get('tam'),
                "sam": market_data.get('sam'),
                "som": market_data.get('som'),
                "country": market_data.get('country'),
            },
            "team": team_data,
            "public_data": public_data,
            "risk": risk_data,
            "benchmark": benchmark_data,
        }
        return report

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return {"error": str(e)}

def main():
    # Explicitly load .env from the script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(dotenv_path=os.path.join(base_dir, '.env'), override=True)

    parser = argparse.ArgumentParser(description="AI Startup Investment Analyst")
    parser.add_argument("input_file", help="Path to the startup material file.")
    args = parser.parse_args()

    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    print(f"Analyzing {args.input_file}...")
    report = run_analysis(args.input_file)

    if "error" in report:
        print(f"Analysis failed: {report['error']}")
        return

    # Print formatted report to console
    print("\n--- Investment Analysis Report ---")
    print(f"COMPANY: {report['company_name']}")
    print(f"RECOMMENDATION: {report['recommendation'].get('recommendation')} (Confidence: {report['recommendation'].get('confidence')} %)")
    print(f"Rationale: {report['recommendation'].get('investment_rationale')}\n")
    print("METRIC SCORECARD:")
    metrics = report['metrics']
    print(f"  Revenue: {metrics.get('revenue')}, CAC: {metrics.get('cac')}, LTV: {metrics.get('ltv')}")
    print(f"  TAM: {metrics.get('tam')}, SAM: {metrics.get('sam')}, SOM: {metrics.get('som')} (Market: {metrics.get('country')})")
    print("\nTEAM ASSESSMENT:")
    team = report['team']
    print(f"  Founders Background: {team.get('founders_background')}")
    print(f"  Team Size: {team.get('team_size')}")
    print(f"  IP/Patents: {team.get('ip_patents')}")
    print("\nPUBLIC DATA:")
    public = report['public_data']
    print(f"  Sentiment: {public.get('news_sentiment')}")
    print(f"  Summary: {public.get('public_data_summary')}")
    print("\nRISK MATRIX:")
    risk = report['risk']
    print(f"  Financial: {risk.get('financial_risk')}")
    print(f"  Market: {risk.get('market_risk')}")
    print(f"  Execution: {risk.get('execution_risk')}")
    print(f"  Overall Risk: {risk.get('overall_risk')}")
    print("\nBENCHMARK ANALYSIS:")
    benchmark = report['benchmark']
    print(f"  {benchmark.get('benchmark_summary')}")
    print("---------------------------------")


if __name__ == "__main__":
    main()
