# **AI Legal Agent – Universal Credit Act 2025 Analyzer**

An AI-powered legal analysis agent designed to **read, summarize, and interpret** the *Universal Credit Act 2025*. It leverages **Google Gemini 1.5 Flash** for advanced natural language analysis and **pypdf** for accurate PDF text extraction.

---

## 🚀 **Overview**

The system automates legal document understanding through:

* High-accuracy PDF text extraction
* AI-driven summarization and interpretation
* Rule extraction and compliance analytics
* A fully interactive web-based interface

---

## 🧩 **Features**

### **1. Automated PDF Text Extraction**

* Uses **pypdf** to extract text from legal PDFs.
* Automatically handles multi-page, structured government documents.

### **2. Intelligent Summarization**

* Powered by **Gemini 1.5 Flash**
* Generates:

  * Purpose & intent of the Act
  * Key obligations & rights
  * Eligibility criteria
  * Enforcement details
  * Exceptions, penalties & procedural guidance

### **3. Structured Section Extraction (JSON)**

* Extracts legal clauses into machine-readable **JSON** formats:

  ```json
  {
    "section": "3A",
    "title": "Eligibility Requirements",
    "summary": "…",
    "keywords": ["income", "residence", "employment"]
  }
  ```

### **4. Automated Compliance Checking**

* Analyzes user inputs or scenarios.
* Returns:

  * Pass/Fail compliance outcome
  * Matched legal clauses
  * **Confidence scores**

### **5. Bonus: Streamlit Web Interface**

* Upload PDFs
* View instant summaries
* Explore extracted sections
* Download JSON reports

---

## 🏗️ **Architecture**

```
                 ┌──────────────────────────┐
                 │      Input Layer         │
                 │  PDF Document / Text     │
                 └────────────┬─────────────┘
                              │
                    ┌─────────▼───────────┐
                    │  Extraction Layer    │
                    │     pypdf            │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │   Cognitive Layer    │
                    │ Gemini 1.5 Flash API │
                    └─────────┬───────────┘
                              │
             ┌────────────────▼─────────────────┐
             │      Presentation Layer           │
             │   Streamlit UI & JSON Output      │
             └───────────────────────────────────┘
```

---

## 📦 **Installation**

### **1. Clone the Repository**

```bash
git clone <repo-url>
cd <repo-folder>
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Setup API Key**

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🧪 **Usage**

### **Option 1: Run Test Script (Console Mode)**

Generate the JSON report directly:

```bash
python test_local.py
```

---

### **Option 2: Run the Web App (UI Mode)**

Launch the Streamlit interface:

```bash
streamlit run app.py
```

---

If you want, I can also prepare:
✅ A perfect README.md
✅ Project folder structure
✅ Badges (Python, Streamlit, Gemini)
✅ Logo/banner for the repo
