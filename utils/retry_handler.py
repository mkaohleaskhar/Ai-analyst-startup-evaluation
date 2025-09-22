import time
import random
from google.api_core.exceptions import ResourceExhausted

def gemini_request_with_retry(model, prompt, max_retries=5, backoff_factor=2):
    """Makes a request to the Gemini model with exponential backoff retry logic."""
    for i in range(max_retries):
        try:
            print(f"Attempt {i + 1} of {max_retries} to call the AI model...")
            response = model.generate_content(prompt)
            print("AI model call successful.")
            return response
        except ResourceExhausted as e:
            if i == max_retries - 1:
                print("Maximum retries reached. Failing.")
                raise e

            # Exponential backoff with jitter
            wait_time = backoff_factor ** i + random.uniform(0, 1)
            print(f"Rate limit hit. Waiting for {wait_time:.2f} seconds before retrying...")
            time.sleep(wait_time)
    raise Exception("Exhausted all retry attempts.")
