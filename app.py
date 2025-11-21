import streamlit as st
import json
import os
from dotenv import load_dotenv
from legal_agent import LegalAgent

# Load environment variables (API Key)
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Legal AI Agent", 
    page_icon="⚖️",
    layout="wide"
)

# --- HELPER: ARCHITECTURE POPUP ---
# @st.dialog creates a modal popup window
# width="large" makes the popup wider so the image is big and clear
@st.dialog("System Architecture", width="large")
def show_architecture_modal():
    image_path = "architecture.png"
    
    if os.path.exists(image_path):
        # Displays the image using the full width of the large modal
        st.image(image_path, caption="Single-Pass AI Agent Workflow", use_container_width=True)
    else:
        st.error(f"❌ File '{image_path}' not found.")
        st.info("Please make sure you have an image named 'architecture.png' in your project folder.")

# --- UI HEADER ---
st.title("⚖️ Universal Credit Act 2025 AI Agent")
st.markdown("""
This agent is designed to:
1. **Extract** text from legal PDF documents.
2. **Summarize** key points (Purpose, Eligibility, etc.).
3. **Extract** specific legislative sections into JSON.
4. **Validate** compliance against 6 predefined rules.
""")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Auto-load key from .env if available, otherwise ask user
    env_key = os.getenv("GEMINI_API_KEY")
    api_key = st.text_input("Enter Gemini API Key", value=env_key if env_key else "", type="password")
    
    if not api_key:
        st.warning("⚠️ API Key required to proceed.")
        st.stop()
    
    st.success("API Key Loaded")
    st.markdown("---")
    
    # --- ARCHITECTURE BUTTON ---
    st.header("🛠️ System Architecture")
    
    # Clicking this triggers the modal defined above
    if st.button("Show Architecture Diagram"):
        show_architecture_modal()

    st.markdown("---")
    st.info("Built for NIYAMR Internship Assignment")

# --- FILE UPLOADER SECTION ---
st.markdown("### 📂 Document Upload")
st.write("Please upload the **Universal Credit Act 2025 (PDF)** to begin analysis.")

# This creates the drag-and-drop area
uploaded_file = st.file_uploader("Upload Act PDF", type=['pdf'], help="Limit 200MB per file")

# --- ANALYSIS LOGIC ---
if st.button("🚀 Analyze Document", type="primary"):
    if not uploaded_file:
        st.error("❌ Please upload a PDF document first.")
        st.stop()

    agent = LegalAgent(api_key)
    
    # Create a progress container
    with st.status("Processing Document...", expanded=True) as status:
        
        # 1. Extraction Phase
        st.write("📄 Extracting text from PDF...")
        try:
            # Save temp file to disk so pypdf can read it
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            text = agent.extract_text_from_pdf("temp.pdf")
            
            if len(text) < 100:
                st.warning("⚠️ Warning: Extracted text is very short.")
            else:
                st.write(f"✅ Text extracted successfully ({len(text)} characters).")

            # 2. Analysis Phase (Gemini)
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
            # Cleanup temp file
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

    # --- RESULTS DISPLAY ---
    st.divider()
    
    # Create tabs for cleaner display
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
        
        # Scoreboard
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
        
        # Rule List
        for rule in rules:
            status = rule.get('status', 'fail').lower()
            is_pass = status == 'pass'
            
            icon = "✅" if is_pass else "⚠️"
            rule_text = rule.get('rule', 'Unknown Rule')
            
            # Auto-expand if Failed
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
        
        # JSON Download Button
        json_str = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Final JSON Report",
            data=json_str,
            file_name="universal_credit_analysis.json",
            mime="application/json"
        )