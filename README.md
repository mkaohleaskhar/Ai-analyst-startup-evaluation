# AI Investment Analyst

This project is an AI-powered tool designed to assist investment analysts in evaluating startups. It uses a multi-agent system to analyze various aspects of a startup from provided documents, such as business plans, financial statements, and pitch decks. The system provides a comprehensive report and a recommendation on whether to invest.

## Features

- **Multi-Agent Analysis:** The tool uses a team of specialized AI agents to analyze different facets of a startup, including:
    - **Financials:** Extracts and analyzes key financial metrics.
    - **Market:** Assesses the market size (TAM, SAM, SOM) and competitive landscape.
    - **Team:** Evaluates the strength and experience of the founding team.
    - **Public Data:** Gathers and analyzes public data and news sentiment about the company.
    - **Risk:** Identifies potential financial, market, and execution risks.
    - **Benchmarking:** Compares the startup's metrics against industry benchmarks.
    - **Recommendation:** Provides a final investment recommendation with a confidence score.
- **Web Interface:** A user-friendly web interface to upload documents and view the analysis results.
- **Command-Line Interface (CLI):** A CLI for power users and for integrating the tool into automated workflows.
- **Deal Notes Generation:** A feature to generate summary notes from multiple documents.

## How It Works

The AI Investment Analyst employs a multi-agent system built on top of Google's Vertex AI. When a document is provided, it's first parsed, and then a team of AI agents is orchestrated to perform the analysis. Some agents work in parallel to process the document from different perspectives, while others work sequentially to build upon the previous analysis. The final output is a consolidated report that provides a holistic view of the startup.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mkaohleaskhar/Ai-analyst-startup-evaluation.git
    cd Ai-analyst-startup-evaluation
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Google Cloud credentials:**
    - This project uses Google Vertex AI, so you need to have a Google Cloud project with the AI Platform API enabled.
    - Create a service account with the "Vertex AI User" role and download the JSON key file.
    - Create a `.env` file in the root of the project and add the following, replacing the values with your own:
      ```
      GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
      GOOGLE_CLOUD_LOCATION="your-gcp-location"  # e.g., us-central1
      GOOGLE_API_KEY="your-google-api-key"
      ```
    - The application will also look for the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to be set to the path of your JSON key file.

## How to Run

### Command-Line Interface (CLI)

To run the analysis on a startup document from the command line, use the following command:

```bash
python main.py /path/to/your/startup_document.txt
```

The tool will output a detailed analysis report to the console.

### Web Interface

To start the web server, run the following command:

```bash
uvicorn web_server:app --host 0.0.0.0 --port 8001
```

Then, open your web browser and navigate to `http://localhost:8001`. You can upload a startup document through the web interface and view the analysis report.

## Example Output (from CLI)

```
--- Investment Analysis Report ---
COMPANY: InnovateTech
RECOMMENDATION: Positive (Confidence: 85 %)
Rationale: InnovateTech presents a strong investment case due to its experienced team, large addressable market, and solid initial traction.

METRIC SCORECARD:
  Revenue: $500K ARR, CAC: $5K, LTV: $25K
  TAM: $1B, SAM: $100M, SOM: $10M (Market: Global)

TEAM ASSESSMENT:
  Founders Background: Ex-Google and Ex-Microsoft engineers with PhDs in AI.
  Team Size: 15
  IP/Patents: 2 pending patents.

PUBLIC DATA:
  Sentiment: Positive
  Summary: Recent press coverage has been favorable, highlighting the company's innovative technology.

RISK MATRIX:
  Financial: Low
  Market: Medium
  Execution: Medium
  Overall Risk: Medium

BENCHMARK ANALYSIS:
  InnovateTech's LTV/CAC ratio of 5 is above the industry average of 3.
---------------------------------
```

## Running the Sample

This repository includes a sample startup description file named `sample_startup.txt`. You can use this file to test the tool.

### CLI

```bash
python main.py sample_startup.txt
```

### Web Interface

1.  Start the web server: `uvicorn web_server:app --host 0.0.0.0 --port 8001`
2.  Open your browser to `http://localhost:8001`.
3.  Click the "Choose File" button and select `sample_startup.txt`.
4.  Click the "Analyze" button to see the report.
