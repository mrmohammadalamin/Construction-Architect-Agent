# **Construction AI Multi-Agent System \- Backend**

This repository contains the backend for a sophisticated AI-powered multi-agent system designed to assist in construction project planning and analysis. It leverages Google's Agent Development Kit (ADK) and Google Cloud's Vertex AI (Gemini and Imagen models) to provide comprehensive insights based on user input.

## **Features**

* **Multi-Agent Architecture:** Utilizes 18 specialized AI agents, each focusing on a specific aspect of construction (e.g., Budget, Scheduling, Architectural Design, Risk Management, Sustainability).  
* **Intelligent Orchestration:** A central FastAPI application orchestrates the flow, receiving user input, dispatching tasks to relevant agents, and consolidating their outputs.  
* **Google AI Integration:** Seamlessly integrates with Google's Gemini (for text generation and analysis) and Imagen (for hyper-realistic image generation) models via Vertex AI.  
* **Structured Output:** Agents are designed to provide structured (JSON) outputs, making it easy to consume and display their insights.  
* **Scalable & Modular:** Built with modularity in mind, allowing easy addition of new agents or services.

## **Technologies Used**

* **Framework:** FastAPI  
* **AI Agent Framework:** Google Agent Development Kit (ADK)  
* **LLMs:** Google Gemini (via Vertex AI)  
* **Image Generation:** Google Imagen (via Vertex AI)  
* **Language:** Python 3.9+  
* **Dependency Management:** pip with requirements.txt  
* **Environment Variables:** python-dotenv and pydantic-settings

## **Setup Instructions**

Follow these steps to get the backend up and running on your local machine.

### **1\. Clone the Repository**

git clone url  
cd your-construction-ai/backend

### **2\. Create and Activate a Python Virtual Environment**

It's highly recommended to use a virtual environment to manage dependencies.

\# Create virtual environment  
python \-m venv venv

\# Activate virtual environment  
\# On Windows (Command Prompt):  
.\\venv\\Scripts\\activate.bat  
\# On Windows (PowerShell):  
.\\venv\\Scripts\\Activate.ps1  
\# On Linux/macOS:  
source venv/bin/activate

### **3\. Install Dependencies**

With your virtual environment activated, install the required Python packages:

pip install \-r requirements.txt

### **4\. Google Cloud Project Setup & Authentication**

This project requires access to Google Cloud's Vertex AI services (Gemini and Imagen).

* **Create a Google Cloud Project:** If you don't have one, create a new project in the [Google Cloud Console](https://console.cloud.google.com/).  
* **Enable APIs:** Ensure the "Vertex AI API" is enabled for your project.  
* **Create a Service Account:**  
  * Go to IAM & Admin \> Service Accounts.  
  * Create a new service account.  
  * Grant it the Vertex AI User role (or more granular roles if you prefer, e.g., Vertex AI Administrator for broader access).  
  * **Create a JSON Key:** After creating the service account, click on it, go to the "Keys" tab, and "Add Key" \-\> "Create new key" \-\> "JSON". Download this JSON file. **Keep this file secure and do not share it or commit it to your repository.**

### **5\. Configure Environment Variables**

Create a .env file in the backend/ directory (at the same level as main.py).

\# backend/.env  
\# Replace with the actual, full path to your downloaded GCP service account JSON key.  
GOOGLE\_APPLICATION\_CREDENTIALS="/path/to/your/service-account-key.json"

\# Replace with your actual Google Cloud Project ID.  
PROJECT\_ID="your-gcp-project-id"

\# Optional: Specify the Google Cloud region and Gemini model name.  
\# Defaults are "us-central1" and "gemini-1.5-flash".  
\# LOCATION="us-central1"  
\# GEMINI\_MODEL\_NAME="gemini-1.5-flash"

**Important:** The GOOGLE\_APPLICATION\_CREDENTIALS and PROJECT\_ID environment variables **must be set in your terminal session** every time you run the backend server.

* **On Windows (Command Prompt):**  
  set GOOGLE\_APPLICATION\_CREDENTIALS="C:\\path\\to\\your\\service-account-key.json"  
  set PROJECT\_ID="your-gcp-project-id"

* **On Windows (PowerShell):**  
  $env:GOOGLE\_APPLICATION\_CREDENTIALS="C:\\path\\to\\your\\service-account-key.json"  
  $env:PROJECT\_ID="your-gcp-project-id"

* **On Linux/macOS:**  
  export GOOGLE\_APPLICATION\_CREDENTIALS="/path/to/your/service-account-key.json"  
  export PROJECT\_ID="your-gcp-project-id"

### **6\. Run the FastAPI Backend**

With your virtual environment activated and environment variables set, run the FastAPI application:

uvicorn main:app \--reload \--port 8000

The backend server will start, typically on http://127.0.0.1:8000. You should see logs indicating that the ADK system and all agents have been successfully initialized.

## **API Endpoints**

### **GET /**

* **Description:** Basic health check endpoint.  
* **Response:** {"message": "Construction AI Multi-Agent System is running\! Access /docs for API documentation."}

### **POST /process\_project**

* **Description:** The main endpoint to submit a new construction project inquiry. It triggers the multi-agent workflow, processes the input through all specialized agents, and returns a consolidated analysis.  
* **Request Body (JSON):**  
  {  
    "project\_type": "residential",  
    "client\_name": "EcoHome Developers",  
    "budget\_range": "$750,000 \- $1,200,000",  
    "location": "London, UK",  
    "desired\_features": \["Smart Home Tech", "Green Roof", "Open Concept Living", "Large Garden", "Energy-efficient HVAC"\],  
    "initial\_ideas\_url": "https://example.com/eco-home-ideas",  
    "project\_description": "Design and build a two-story modern eco-friendly family house with smart home technology, a green roof, and an emphasis on energy efficiency and natural light.",  
    "project\_size": "medium"  
  }

* Response Body (JSON):  
  A comprehensive JSON object containing:  
  * overall\_status: "success", "partial\_success", or "failure".  
  * user\_input\_received: The original input data.  
  * consolidated\_project\_data: An aggregated dictionary of all successful agent outputs, enriched with details like architectural\_concept, digital\_twin\_output (including base64 images), cost\_supply\_chain\_analysis, etc.  
  * agent\_outputs\_raw: The raw output from each individual agent, useful for debugging.  
  * summary\_message: A high-level summary of the analysis.

## **Project Structure (Backend)**

backend/  
├── main.py                     \# FastAPI entry point, orchestrates agents  
├── requirements.txt            \# Python dependencies  
├── .env                        \# Environment variables (DO NOT commit to Git\!)  
├── adk\_core/  
│   ├── \_\_init\_\_.py             \# Initializes ADK system, registers agents  
│   ├── agents/                 \# Directory for individual agent implementations  
│   │   ├── \_\_init\_\_.py         \# Makes 'agents' a Python package  
│   │   ├── base\_agent.py       \# Abstract base class for all specialized agents  
│   │   ├── strategic\_client\_engagement\_agent.py  
│   │   ├── site\_intelligence\_regulatory\_compliance\_agent.py  
│   │   ├── generative\_architectural\_design\_agent.py  
│   │   ├── integrated\_systems\_engineering\_agent.py  
│   │   ├── interior\_experiential\_design\_agent.py  
│   │   ├── hyper\_realistic\_3d\_digital\_twin\_agent.py  
│   │   ├── predictive\_cost\_supply\_chain\_agent.py  
│   │   ├── adaptive\_project\_management\_robotics\_orchestration\_agent.py  
│   │   ├── proactive\_risk\_safety\_management\_agent.py  
│   │   ├── ai\_driven\_quality\_assurance\_control\_agent.py  
│   │   ├── semantic\_data\_integration\_ontology\_agent.py  
│   │   ├── learning\_adaptation\_agent.py  
│   │   ├── human\_ai\_collaboration\_explainability\_agent.py  
│   │   ├── sustainability\_green\_building\_agent.py  
│   │   ├── financial\_investment\_analysis\_agent.py  
│   │   ├── legal\_contract\_management\_agent.py  
│   │   ├── workforce\_management\_hr\_agent.py  
│   │   ├── post\_construction\_facility\_management\_agent.py  
│   │   └── public\_relations\_stakeholder\_communication\_agent.py  
│   ├── services/               \# Directory for external service wrappers (e.g., LLMs)  
│   │   ├── \_\_init\_\_.py  
│   │   └── gemini\_service.py   \# Wrapper for Gemini/Imagen API calls  
│   └── utils/                  \# Directory for common utility functions  
│       ├── \_\_init\_\_.py  
│       └── common.py           \# Utility functions (e.g., input parsing, output formatting)  
└── config/                     \# Directory for application configuration  
    └── settings.py             \# Configuration loader (reads from .env)

