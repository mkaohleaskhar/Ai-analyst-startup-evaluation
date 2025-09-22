import os
from .gcp_clients import get_vision_client
from google.cloud import vision

def parse_file(file_path):
    """Parses the input file and returns its content."""
    _, extension = os.path.splitext(file_path)

    if extension.lower() == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif extension.lower() == '.pdf':
        print("PDF file detected. Processing with Cloud Vision API...")
        return parse_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

def parse_pdf(file_path):
    """Extracts text from a PDF using Cloud Vision API."""
    client = get_vision_client()

    with open(file_path, 'rb') as f:
        content = f.read()

    input_config = vision.InputConfig(content=content, mime_type='application/pdf')
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateFileRequest(
        input_config=input_config,
        features=[feature]
    )

    response = client.batch_annotate_files(requests=[request])

    full_text = ""
    for image_response in response.responses[0].responses:
        full_text += image_response.full_text_annotation.text + '\n'

    print("PDF processing complete.")
    return full_text
