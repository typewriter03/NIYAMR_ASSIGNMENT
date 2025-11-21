AI Legal Agent - Universal Credit Act 2025 Analyzer

Overview

This project is an AI-powered agent designed to read, summarize, and analyze the Universal Credit Act 2025. It uses Google Gemini 1.5 Flash for natural language understanding and pypdf for text extraction.

Features

Task 1: Automated PDF Text Extraction.

Task 2: Intelligent Summarization (Purpose, Obligations, etc.).

Task 3: Structured Extraction of Key Sections (JSON).

Task 4: Automated Rule Compliance Checking with Confidence Scores.

Bonus: Interactive Streamlit Web Interface.

Architecture

Input: PDF Document / Raw Text.

Extraction Layer: Python pypdf.

Cognitive Layer: Gemini 1.5 Flash (via google.generativeai).

Presentation Layer: Streamlit UI & JSON Report.

Installation

Clone the repository.

Install dependencies:

pip install -r requirements.txt


Setup API Key:

Create a file named .env in the root folder.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here


Usage

Option 1: Run the Test Script (Console)

Run this to generate the JSON report directly in your terminal.

python test_local.py


Option 2: Run the Web App (UI)

Run this for the interactive demo.

streamlit run app.py
