import os
import json
import re
from typing import Dict, List, Optional
import google.generativeai as genai
from pypdf import PdfReader

# --- CONFIGURATION ---
# In a real env, use: os.environ.get("GEMINI_API_KEY")
API_KEY = os.environ.get("GEMINI_API_KEY", "") 

class LegalAgent:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Task 1: Extract text from PDF.
        Includes cleaning steps to ensure "clean and structured" output.
        """
        try:
            reader = PdfReader(pdf_path)
            full_text = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    # Basic cleaning per page
                    clean_page = self._clean_text(text)
                    full_text.append(clean_page)
            
            return "\n\n".join(full_text)
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")

    def _clean_text(self, text: str) -> str:
        """
        Task 1 Requirement: 'The extracted text must be clean and structured.'
        Generalizes cleaning for UK Legislation style PDFs (removing recurring headers/footers).
        """
        # 1. Generalize header removal using Regex
        # Detects patterns like "Universal Credit Act 2025 (c. 22)" or "Data Protection Act 2018 (c. 12)"
        # Logic: Matches text ending with "Act Year (c. Number)"
        text = re.sub(r'.*Act \d{4}\s+\(c\.\s*\d+\)', '', text)
        
        # 2. Remove page numbers and standard copyright lines
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines
            if not stripped:
                continue
            # Skip isolated page numbers (lines that are just digits)
            if stripped.isdigit(): 
                continue
            # Skip common footer text found in UK legislation
            if "Crown copyright" in stripped or "Stationery Office" in stripped:
                continue
                
            cleaned_lines.append(line)
        
        text = "\n".join(cleaned_lines)
        
        # 3. Remove multiple newlines which break reading flow
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text

    def analyze_document(self, text: str) -> Dict:
        """Runs Tasks 2, 3, and 4 in a single efficient pipeline."""
        
        prompt = f"""
        You are a legal AI agent analyzing a UK Act of Parliament.
        
        DOCUMENT TEXT:
        {text[:30000]} 
        
        ---
        PERFORM THE FOLLOWING TASKS AND RETURN ONLY RAW JSON.
        
        TASK 2: SUMMARIZE
        Summarize the entire Act in 5-10 bullet points focusing on: Purpose, Key definitions, Eligibility, Obligations, Enforcement elements.
        
        TASK 3: EXTRACT SECTIONS
        Extract exact text or summary for: definitions, obligations, responsibilities, eligibility, payments, penalties, record_keeping.
        
        TASK 4: RULE CHECKS
        Check these 6 rules. Return status (pass/fail), evidence, and confidence (0-100).
        1. Act must define key terms
        2. Act must specify eligibility criteria
        3. Act must specify responsibilities of the administering authority
        4. Act must include enforcement or penalties
        5. Act must include payment calculation or entitlement structure
        6. Act must include record-keeping or reporting requirements
        
        ---
        REQUIRED JSON OUTPUT FORMAT:
        {{
            "summary": ["point 1", "point 2"...],
            "sections": {{
                "definitions": "...",
                "obligations": "...",
                "responsibilities": "...",
                "eligibility": "...",
                "payments": "...",
                "penalties": "...",
                "record_keeping": "..."
            }},
            "rules_analysis": [
                {{
                    "rule": "Act must define key terms",
                    "status": "pass",
                    "evidence": "Section X mentions...",
                    "confidence": 100
                }},
                ... (repeat for all 6 rules)
            ]
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            json_str = self._clean_json_string(response.text)
            return json.loads(json_str)
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def _clean_json_string(self, json_str: str) -> str:
        """Helper to extract valid JSON from Markdown code blocks."""
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]
        return json_str.strip()