"""
Custom UI Theme & CSS Styling Tokens.
Provides responsive layout, typography, glassmorphism cards, and syntax diff boxes.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

code, pre {
    font-family: 'Fira Code', monospace !important;
}

.main-header {
    background: linear-gradient(135deg, #1e1e2f 0%, #151522 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}

.main-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-bottom: 0;
}

.step-card {
    background: #181926;
    border: 1px solid #2e3045;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 16px;
}

.step-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #f1f5f9;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}

.badge-success {
    background-color: #064e3b;
    color: #34d399;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}

.badge-danger {
    background-color: #7f1d1d;
    color: #f87171;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    display: inline-block;
}

.badge-tag {
    background-color: #1e293b;
    color: #38bdf8;
    border: 1px solid #334155;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.82rem;
    margin-right: 6px;
    display: inline-block;
    font-family: monospace;
}
</style>
"""


def apply_custom_styles(streamlit_instance):
    """Injects custom CSS styling into the Streamlit app."""
    streamlit_instance.markdown(CUSTOM_CSS, unsafe_allow_html=True)
