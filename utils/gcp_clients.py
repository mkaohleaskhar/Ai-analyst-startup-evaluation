from google.cloud import aiplatform
from google.cloud import vision
from google.api_core.client_options import ClientOptions
import os

def get_vertex_ai_client():
    """Initializes and returns the Vertex AI client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    print(f"Initializing Vertex AI with project: {project_id}")
    aiplatform.init(project=project_id, location=os.getenv("GOOGLE_CLOUD_LOCATION"))
    return aiplatform

def get_vision_client():
    """Initializes and returns the Vision API client with the correct quota project."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    return vision.ImageAnnotatorClient(
        client_options=ClientOptions(quota_project_id=project_id)
    )
