import streamlit as st
import json
import os
from dotenv import load_dotenv
from legal_agent import LegalAgent

# Load environment variables (API Key)
load_dotenv()

st.set_page_config(
    page_title="Legal AI Agent", 
    page_icon="⚖️",
    layout="wide"
)


@st.dialog("System Architecture", width="large")
def show_architecture_modal():
    image_path = "architecture.png"
    
    if os.path.exists(image_path):
        st.image(image_path, caption="Single-Pass AI Agent Workflow", use_container_width=True)
    else:
        st.error(f"❌ File '{image_path}' not found.")
        st.info("Please make sure you have an image named 'architecture.png' in your project folder.")

st.title("⚖️ Universal Credit Act 2025 AI Agent")
st.markdown("""
This agent is designed to:
1. **Extract** text from legal PDF documents.
2. **Summarize** key points (Purpose, Eligibility, etc.).
3. **Extract** specific legislative sections into JSON.
4. **Validate** compliance against 6 predefined rules.
""")

with st.sidebar:
    st.header("⚙️ Settings")
    
    env_key = os.getenv("GEMINI_API_KEY")
    api_key = st.text_input("Enter Gemini API Key", value=env_key if env_key else "", type="password")
    
    if not api_key:
        st.warning("⚠️ API Key required to proceed.")
        st.stop()
    
    st.success("API Key Loaded")
    st.markdown("---")
    
    st.header("🛠️ System Architecture")
    
    if st.button("Show Architecture Diagram"):
        show_architecture_modal()

    st.markdown("---")
    st.info("Built for NIYAMR Internship Assignment")

st.markdown("### 📂 Document Upload")
st.write("Please upload the **Universal Credit Act 2025 (PDF)** to begin analysis.")

uploaded_file = st.file_uploader("Upload Act PDF", type=['pdf'], help="Limit 200MB per file")

if st.button("🚀 Analyze Document", type="primary"):
    if not uploaded_file:
        st.error("❌ Please upload a PDF document first.")
        st.stop()

    agent = LegalAgent(api_key)
    
    with st.status("Processing Document...", expanded=True) as status:
        
        st.write("📄 Extracting text from PDF...")
        try:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            text = agent.extract_text_from_pdf("temp.pdf")
            
            if len(text) < 100:
                st.warning("⚠️ Warning: Extracted text is very short.")
            else:
                st.write(f"✅ Text extracted successfully ({len(text)} characters).")

            st.write("🧠 Sending to AI for analysis (Tasks 2, 3 & 4)...")
            results = agent.analyze_document(text)

            if "error" in results:
                status.update(label="Analysis Failed", state="error")
                st.error(results["error"])
                st.stop()
            else:
                status.update(label="Analysis Complete!", state="complete")

        except Exception as e:
            status.update(label="System Error", state="error")
            st.error(f"An error occurred: {e}")
            st.stop()
        finally:
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Executive Summary", "🔍 Key Sections", "✅ Rule Validation", "💾 Raw JSON"])
    
    with tab1:
        st.header("Executive Summary (Task 2)")
        if "summary" in results and isinstance(results["summary"], list):
            for point in results["summary"]:
                st.markdown(f"• {point}")
        else:
            st.info("No summary available.")
    
    with tab2:
        st.header("Legislative Sections (Task 3)")
        sections = results.get("sections", {})
        for key, value in sections.items():
            with st.expander(f"📌 {key.title().replace('_', ' ')}"):
                st.markdown(value)

    with tab3:
        st.subheader("📋 Compliance Rule Validation (Task 4)")
        
        rules = results.get("rules_analysis", [])
        total_rules = len(rules)
        pass_count = sum(1 for r in rules if r.get('status', '').lower() == 'pass')
        
        score_col1, score_col2 = st.columns([1, 4])
        with score_col1:
            st.metric("Compliance Score", f"{pass_count}/{total_rules}", help="Number of rules passed")
        with score_col2:
            st.caption("Overall Compliance Progress")
            if total_rules > 0:
                prog_value = pass_count / total_rules
                color = "green" if prog_value == 1.0 else "orange"
                st.progress(prog_value)
            else:
                st.progress(0)
        
        st.markdown("---")
        
        for rule in rules:
            status = rule.get('status', 'fail').lower()
            is_pass = status == 'pass'
            
            icon = "✅" if is_pass else "⚠️"
            rule_text = rule.get('rule', 'Unknown Rule')
            
            with st.expander(f"{icon} {rule_text}", expanded=not is_pass):
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown("**Status Result:**")
                    if is_pass:
                        st.success("PASS")
                    else:
                        st.error("FAIL - Attention Needed")     
                    st.markdown(f"**AI Confidence:** `{rule.get('confidence', 0)}%`")
                with c2:
                    st.markdown("**🕵️ Evidence Extracted:**")
                    evidence = rule.get('evidence', 'No specific evidence found in text.')
                    st.info(evidence)

    with tab4:
        st.header("JSON Output")
        st.json(results)
        
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Final JSON Report",
            data=json_str,
            file_name="universal_credit_analysis.json",
            mime="application/json"
        )