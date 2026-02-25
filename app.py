import streamlit as st
import google.generativeai as genai
import os

# Configure Streamlit Page
st.set_page_config(page_title="Risk Scanner", layout="centered")

# Setup Gemini API (Assumes GEMINI_API_KEY is in .streamlit/secrets.toml)
try:
    print("API Key loaded:", st.secrets["GEMINI_API_KEY"][:10] + "...")  # 只印前10字元
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')   
except Exception as e:
    st.error("API Key missing or invalid. Please check your secrets.")
    st.stop()

# UI Components
st.title("Black Swan Startup Risk Scanner – Free Test")

user_input = st.text_area(
    "Paste your business plan summary here (English preferred)",
    height=250,
    placeholder="Describe your tech stack, market entry, and current capital commitments..."
)

analyze_button = st.button("Analyze Risk")

# System Prompt Construction
SYSTEM_PROMPT = """You are a high-stakes startup risk advisor using L0-L3 Irreversible Commitment Framework + Black Swan/Gray Rhino detection + Responsibility Navigation.

L0: Abstract Goal (low cost)
L1: Technology Path Locked
L2: Process Defined (high change cost)
L3: Irreversible Constraint

Rules:
- Output MUST strictly follow this exact format. No extra text, no explanations outside the format.
- Total output: 150–250 words max.
- English only.
- Anti-analysis-paralysis: Emphasize "action first, good enough mindset". Never encourage over-optimization. Include delay risk warning if needed.
- Black Swan: Use historical pattern analogy (e.g. "Similar to FTX debt lock-in"). Low probability but high impact. Add silver lining if possible.
- Gray Rhino: Detect high-probability but ignored risks (e.g. tax changes, supply chain deterioration). 
- Always separate Black Swan and Gray Rhino into two distinct lines.
- Responsibility: Every action step must suggest a responsible person (e.g. Founder, CTO).
- Limit bullets to critical/fatal items only.
- End with a short motivational note.

Output format:
Current Commitment Level: L[0–3]  
Reason: ...

Unverified Assumptions: ...

Irreversible Commitments / Cost Dependencies: ...

Black Swan: ...
Gray Rhino: ...

Decision: Upgrade Commitment? [Yes/No/Pause]  
Reason: ...

Recommended Actions: ...
- Step 1: ... (Responsible: ...)
- Step 2: ... (Responsible: ...)

[Motivational Note]
"""

if analyze_button:
    if not user_input.strip():
        st.warning("Please enter a summary to analyze.")
    else:
        with st.spinner("Scanning for fatal risks..."):
            try:
                # API Call
                full_prompt = f"{SYSTEM_PROMPT}\n\nUser input: {user_input}"
                response = model.generate_content(full_prompt)
                
                # Display Results
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# Footer
st.caption("High-stakes framework: L0-L3 Irreversible Commitment Detection.")
st.divider()
st.subheader("快速反饋（幫助我們改進）")
helpful = st.slider("這份分析有幫助嗎？", 1, 5, 3, format="%d 分")
pay_willing = st.radio("你願意付費嗎？", ["願意 $9/次", "願意 $29/月", "免費就好", "還不值得付"])
comment = st.text_area("有什麼建議？（e.g. 太長、太泛、想加功能）")
if st.button("送出反饋"):
    st.success("感謝！我們會盡快改進。")
    # 之後可連 Google Sheet 記錄