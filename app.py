import streamlit as st
import google.generativeai as genai
import os

# Configure Streamlit Page
st.set_page_config(page_title="Irreversible Navigator – High-Stakes Decision Scanner")

# Setup Gemini API (Assumes GEMINI_API_KEY is in .streamlit/secrets.toml)
try:
    print("API Key loaded:", st.secrets["GEMINI_API_KEY"][:10] + "...")  # 只印前10字元
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')   
except Exception as e:
    st.error("API Key missing or invalid. Please check your secrets.")
    st.stop()

# UI Components
st.title("Irreversible Navigator – High-Stakes Decision Scanner")

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
st.subheader("Quick Feedback – Help Us Improve")

with st.form("feedback_form"):
    helpful = st.slider("Was this analysis helpful?", 1, 5, 3, format="%d / 5")
    pay_willing = st.radio("Would you pay for this tool?", [
        "Yes, $9 per analysis",
        "Yes, $29/month unlimited",
        "Free is fine",
        "Not worth paying yet"
    ])
    comment = st.text_area("Any suggestions? (e.g. too short, too vague, add features)")
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    from datetime import datetime
    import requests

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSf5mtaEITUb2xU9kTAdLLfH43nVpJVTRbr7Wgp2A4l0-NCeDg/formResponse"

    data = {
        "entry.1411806970": str(helpful),          # Was this analysis helpful? (1-5)
        "entry.1122506764": pay_willing,           # Would you pay? (must match exact option text)
        "entry.1881486862": comment                # Any suggestions?
        # 如果有時間欄位，再加 "entry.你的時間ID": timestamp
    }

    try:
        response = requests.post(form_url, data=data)
        print("送出狀態:", response.status_code)
        print("回應文字:", response.text[:500])  # 看錯誤
        if response.status_code in [200, 302]:
            st.success("Thank you! Feedback recorded in Google Sheets.")
        else:
            st.error(f"Submit failed (HTTP {response.status_code}) - Check text match or entry ID")
    except Exception as e:
        st.error(f"Error: {str(e)}")