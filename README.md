# 📊 Superstore Insight Copilot

An AI-powered data analysis chatbot built with Python, LangGraph, and Streamlit. The application allows users to ask natural-language questions about the Superstore dataset and receive analytical answers, calculations, and visualizations.

## 🚀 Features

* Natural-language data analysis
* LangGraph-based agent orchestration
* Planner and routing logic
* Data Query Tool
* Calculation Tool
* Chart/Visualization Tool
* Visible reasoning/plan
* Analyst-style insights
* Multi-turn conversation
* Interactive Streamlit interface

## 🏗️ Architecture

The application uses LangGraph to orchestrate a reasoning and tool-using data analysis agent.

The agent receives a user question, creates a short plan, routes the query to the appropriate tool, processes the tool output, and generates a human-readable analytical response.

![Insight Copilot Architecture](image/README/1791133884121.png)

## **🛠️ Tools**

### 1. Data Query Tool

Used to retrieve, filter, group, and analyze data from the Superstore dataset.

### 2. Calculation Tool

Used for calculations such as totals, averages, comparisons, growth rates, and other statistical metrics.

### 3. Chart Tool

Used to generate visualizations such as category, region, and trend charts.

## 🧠 Agent Workflow

User enters a natural-language question.

Planner Node understands the question and creates a short plan.

Router Node determines which tool or tools are required.

The selected tool processes the dataset.

The results are passed to the insight / synthesis stage.

The agent generates a clear final response.

## 📊 Dataset

The project uses the Superstore sales dataset for data analysis and business insights.

## 💻 Tech Stack

Python

LangGraph

LangChain

Streamlit

Pandas

NumPy

Matplotlib

Ollama / Mistral

## ⚙️ Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd superstore_insight_copilot

Install the required dependencies:

pip install -r requirements.txt

Make sure the required local LLM / model environment is configured before running the application.

## ▶️ Run the Application

streamlit run app.py

The application will open in the browser through the Streamlit interface.

## 🧪 Testing

The application was tested using questions covering:

Basic data queries

Aggregations and calculations

Category and region comparisons

Chart generation

Follow-up questions

Multi-step analytical questions

Unsupported questions and edge cases

## ⚠️ Known Limitations

The chatbot is designed primarily for questions related to the provided dataset.

Answers depend on the quality and structure of the dataset.

Complex questions outside the implemented tools may not be supported.

Local model performance may depend on available system resources.

## 🔍 Assumptions

The uploaded dataset contains the required fields for sales analysis.

Users primarily ask questions related to the dataset.

The implemented tools are sufficient for the supported analytical use cases.

## 📌 Future Improvements

Add more advanced statistical analysis

Add additional visualization types

Support more datasets

Add cloud / API-based LLM support

Improve handling of complex multi-step queries

Deploy with scalable cloud infrastructure

## 👤 Project

Superstore Insight Copilot

Built as a GenAI / LLM / Agentic AI project demonstrating LangGraph-based reasoning, tool selection, data analysis, and insight generation.
