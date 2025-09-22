import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def generate_notes(texts: list[str]) -> dict:
    """
    Generates structured deal notes from a list of text contents from multiple documents.
    """
    print("Running Deal Notes Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    # Combine all text content into a single string with separators
    combined_text = "\n\n---" + "-" + "-" + " NEW DOCUMENT " + "---" + "\n\n".join(texts)

    prompt = f"""
    You are a venture capital analyst. You have been given a collection of documents related to a potential investment deal. These documents may include pitch decks, call transcripts, founder updates, and email threads.

    Your task is to synthesize all the information from these documents into a single, structured set of "deal notes".

    Review the combined text from all documents provided below and generate a JSON object with the following structure:

    - "company_summary": A brief overview of the startup.
    - "recent_updates": Key progress points and updates mentioned in the documents.
    - "key_discussion_points": Salient points from transcripts and emails.
    - "action_items": Any follow-ups or next steps identified.
    - "red_flags": Potential issues or concerns raised across the documents.

    If any section is not applicable or no information is found, use "Not found".

    Combined Document Text:
    ---
    {combined_text}
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
            "company_summary": "Error",
            "recent_updates": "Error",
            "key_discussion_points": "Error",
            "action_items": "Error",
            "red_flags": "Error"
        }
