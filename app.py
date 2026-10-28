import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="DorkCraft AI Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for a sleek, modern look
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    .reportview-container {
        background: #0e1117;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Configuration for Groq API Key & Settings
st.sidebar.title("⚙️ Lab Controls")
st.sidebar.markdown(
    "Configure your Groq API key to power real-time AI security processing."
)

# Check environment variable first, else allow manual input
default_api_key = os.environ.get("GROQ_API_KEY", "")
api_key_input = st.sidebar.text_input(
    "Groq API Key",
    value=default_api_key,
    type="password",
    help="Get your free key from console.groq.com",
)

model_choice = st.sidebar.selectbox(
    "Select Inference Model",
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
    help="Choose between maximum speed (8b) or maximum reasoning depth (70b).",
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**DorkCraft AI Lab v2.5**\n\nBuilt for automated threat intelligence, OSINT recon, and secure code evaluation."
)

# Main App Header
st.title("🛡️ DorkCraft AI Lab")
st.markdown(
    "### Intelligent OSINT, Attack Surface Mapping & Vulnerability Analysis Studio"
)
st.markdown("---")

# Tabs for different lab tools
tab1, tab2, tab3 = st.tabs(
    [
        "🔍 OSINT Dork Generator",
        "🗺️ Recon Strategy Planner",
        "💻 Code Security Auditor",
    ]
)

# Initialize Groq client helper function
def get_groq_response(system_prompt, user_prompt, api_key, model):
    if not api_key:
        st.error(
            "⚠️ Please enter your Groq API Key in the sidebar or set the GROQ_API_KEY environment variable."
        )
        return None
    try:
        client = Groq(api_key=api_key)
        with st.spinner("Analyzing target parameters through Groq LPU..."):
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5,
                max_tokens=1500,
            )
            return completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the Groq API: {e}")
        return None


# --- TAB 1: OSINT Dork Generator ---
with tab1:
    st.header("Automated OSINT Google Dork Studio")
    st.markdown(
        "Generate advanced query strings to unearth exposed documents, admin panels, config files, and sub-domains."
    )

    col1, col2 = st.columns(2)
    with col1:
        target_domain = st.text_input(
            "Target Domain / Organization",
            placeholder="e.g., target-company.com",
        )
    with col2:
        recon_objective = st.selectbox(
            "Recon Objective",
            [
                "Exposed Configuration & Log Files",
                "Admin & Login Portals",
                "Directory Traversal & Sensitive Endpoints",
                "API Keys & Secret Leaks",
                "Custom Open Source Intelligence",
            ],
        )

    additional_keywords = st.text_input(
        "Keywords / File extensions (Optional)",
        placeholder="e.g., .env, password, config, AWS_ACCESS_KEY",
    )

    if st.button("Generate Dorks", key="dork_btn"):
        if not target_domain:
            st.warning("Please provide a target domain to begin.")
        else:
            sys_prompt = (
                "You are an expert cybersecurity OSINT engineer. "
                "Provide advanced Google Dorks and search engine operators "
                "formatted cleanly with brief usage instructions and safety notes."
            )
            usr_prompt = (
                f"Target Domain: {target_domain}\n"
                f"Objective: {recon_objective}\n"
                f"Specific Keywords/Extensions: {additional_keywords}\n\n"
                "Provide 5-8 highly effective Google Dork queries with markdown code blocks "
                "and explain what each query targets."
            )

            result = get_groq_response(
                sys_prompt, usr_prompt, api_key_input, model_choice
            )
            if result:
                st.markdown("### 🎯 Generated Recon Queries")
                st.markdown(result)


# --- TAB 2: Recon Strategy Planner ---
with tab2:
    st.header("Attack Surface Recon & Workflow Planner")
    st.markdown(
        "Design comprehensive reconnaissance playbooks, subdomain enumeration frameworks, and threat assessment pipelines."
    )

    scope_description = st.text_area(
        "Define Target Scope & Environment Details",
        placeholder="e.g., Web application hosted on AWS with a mobile API backend and public client dashboard.",
    )

    focus_area = st.multiselect(
        "Select Focus Modules",
        [
            "Subdomain Enumeration",
            "Port Scanning & Service Fingerprinting",
            "Content Discovery / Directory Brute-forcing",
            "Cloud Bucket (S3/Azure) Misconfigurations",
            "Social Engineering Vector Assessment",
        ],
        default=["Subdomain Enumeration", "Content Discovery / Directory Brute-forcing"],
    )

    if st.button("Build Recon Strategy", key="recon_btn"):
        if not scope_description:
            st.warning("Please enter a target scope description.")
        else:
            sys_prompt = (
                "You are a senior penetration tester and red-team operations lead. "
                "Create structured, professional, step-by-step technical reconnaissance plans."
            )
            usr_prompt = (
                f"Scope Description: {scope_description}\n"
                f"Focus Modules: {', '.join(focus_area)}\n\n"
                "Build a structured markdown operational playbook including recommended toolsets "
                "(e.g., Nmap, Gobuster, Amass, Burp Suite), execution steps, and risk evaluation guidelines."
            )

            result = get_groq_response(
                sys_prompt, usr_prompt, api_key_input, model_choice
            )
            if result:
                st.markdown("### 📋 Recommended Recon Playbook")
                st.markdown(result)


# --- TAB 3: Code Security Auditor ---
with tab3:
    st.header("AI Code Vulnerability & Security Auditor")
    st.markdown(
        "Paste your script (Python, C++, JS) to check for security flaws, memory risks, or injection vulnerabilities."
    )

    source_code = st.text_area(
        "Paste Source Code Here",
        height=200,
        placeholder="def insecure_query(user_input):\n    query = f'SELECT * FROM users WHERE name = {user_input}'\n    return db.execute(query)",
    )

    language = st.selectbox("Language", ["Python", "C++", "JavaScript", "SQL", "Other"])

    if st.button("Audit Code Security", key="audit_btn"):
        if not source_code:
            st.warning("Please paste code to audit.")
        else:
            sys_prompt = (
                "You are an expert application security auditor and secure coding advisor. "
                "Identify vulnerabilities, rate risk levels, and provide cleanly refactored code blocks."
            )
            usr_prompt = (
                f"Language: {language}\n"
                f"Source Code:\n```{language.lower()}\n{source_code}\n```\n\n"
                "1. Identify security vulnerabilities or logic flaws.\n"
                "2. Provide a severity score (Low, Medium, High, Critical).\n"
                "3. Provide the securely refactored version of the code block."
            )

            result = get_groq_response(
                sys_prompt, usr_prompt, api_key_input, model_choice
            )
            if result:
                st.markdown("### 🔒 Security Audit & Mitigation Report")
                st.markdown(result)
