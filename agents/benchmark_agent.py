import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def benchmark_metrics(analysis_data: dict) -> dict:
    """
    Benchmarks metrics against industry standards using a generative AI model.
    """
    print("Running Benchmark Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    input_data_str = json.dumps(analysis_data, indent=2)

    prompt = f"""
    As a startup analyst, review the following structured data.
    Compare the financial and market metrics (e.g., LTV/CAC ratio, revenue, market size) against typical benchmarks for a startup at this stage and sector.

    Provide a "benchmark_summary" of how the startup compares to its peers (e.g., "LTV/CAC ratio is strong, but market penetration is low").

    Return the result as a single-key JSON object with the key "benchmark_summary".

    Input Data:
    ---
    {input_data_str}
    ---

    JSON Output:
    """

    response = gemini_request_with_retry(model, prompt)

    try:
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing AI response: {e}")
        return {
            "benchmark_summary": "Error processing benchmark analysis."
        }
