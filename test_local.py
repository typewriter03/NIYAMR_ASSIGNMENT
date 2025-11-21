import os
import json
from dotenv import load_dotenv
from legal_agent import LegalAgent

# --- SETUP ---
# 1. Load Environment Variables from .env file
load_dotenv()

# 2. Get API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found.")
    print("   Please create a '.env' file with the line: GEMINI_API_KEY=your_key")
    exit(1)

# 3. File Path
pdf_path = "Universal Credit Act 2025.pdf" 
# Note: Ensure the PDF file is in this directory or update the path

if not os.path.exists(pdf_path):
    print(f"❌ Error: File '{pdf_path}' not found.")
    print("   Please download the Act PDF and place it in this folder.")
    exit(1)

# --- EXECUTION ---
def main():
    print("🚀 Starting AI Agent Test...")
    print("🔑 API Key loaded from environment.")
    
    agent = LegalAgent(api_key)

    # Step 1: Extract
    print(f"📂 Reading {pdf_path}...")
    try:
        text = agent.extract_text_from_pdf(pdf_path)
        print(f"✅ Text Extracted ({len(text)} chars)")
    except Exception as e:
        print(f"❌ Extraction Error: {e}")
        exit(1)

    # Step 2 & 3: Analyze
    print("🧠 Sending to Gemini for Analysis (Tasks 2, 3, & 4)...")
    results = agent.analyze_document(text)

    if "error" in results:
        print(f"❌ Analysis Failed: {results['error']}")
    else:
        print("\n✅ Analysis Complete!")
        print("-" * 40)
        
        # Show Task 2: Summary
        print("\n📄 TASK 2: SUMMARY")
        for idx, point in enumerate(results.get("summary", []), 1):
            print(f"{idx}. {point}")

        # Show Task 3: Sections
        print("\n🔍 TASK 3: KEY SECTIONS EXTRACTED")
        sections = results.get("sections", {})
        for key, value in sections.items():
            val_str = str(value)
            preview = val_str[:100] + "..." if len(val_str) > 100 else val_str
            print(f"   [{key.upper()}]: {preview}")

        # Save to JSON (Deliverable requirement)
        output_filename = "final_report.json"
        with open(output_filename, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 JSON Report saved to: {output_filename}")

if __name__ == "__main__":
    main()