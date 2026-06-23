# app.py
"""
AI Copywriting & Tone Transformer - Streamlit Frontend
Integrates design system, input widgets, generation variations, SQLite history, and metrics.
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Import custom modules
from prompt_template import compile_prompt, get_versions, get_version_info
from model import generate_copy
from database import init_db, save_history, get_history, update_quality_score, clear_history

# Load environment variables from multiple potential locations
dir_path = os.path.dirname(os.path.abspath(__file__))
# 1. Project folder (.env)
load_dotenv(os.path.join(dir_path, ".env"))
# 2. Workspace root (.env)
load_dotenv(os.path.join(os.path.dirname(dir_path), ".env"))
# 3. Current working directory (.env)
load_dotenv()



# Initialize SQLite database
init_db()

# --- Page Config ---
st.set_page_config(
    page_title="AI Copywriting & Tone Transformer",
    page_icon="🤖",
    layout="wide"
)

# --- Custom Premium Dark Mode Styling ---
st.markdown(
    """
    <style>
    /* Entire page background */
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Titles & Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Custom main title styling with a gradient */
    .main-title {
        font-size: 3rem;
        background: linear-gradient(90deg, #6f42c1, #007bff, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 0px 0px 15px rgba(111, 66, 193, 0.2);
    }
    
    .subtitle {
        color: #8f94fb;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }

    /* Input labels */
    label, .stSlider > label {
        color: #a8b2c1 !important;
        font-weight: 600 !important;
        font-size: 0.95rem;
    }

    /* Input boxes */
    input, textarea, [data-baseweb="input"] {
        background-color: #1e1e24 !important;
        color: #ffffff !important;
        border: 1px solid #33333d !important;
        border-radius: 8px !important;
    }
    
    input:focus, textarea:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25) !important;
    }

    /* Disabled inputs/textareas (e.g. Live Prompt Preview) */
    input:disabled, textarea:disabled, [data-baseweb="input"] input:disabled, [data-baseweb="textarea"] textarea:disabled {
        color: #e0e0e0 !important;
        -webkit-text-fill-color: #e0e0e0 !important;
        background-color: #12131a !important;
        opacity: 1 !important; /* Prevent browser from dimming the text */
    }


    /* Select boxes */
    div[data-baseweb="select"] {
        background-color: #1e1e24 !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    .stSelectbox div {
        background-color: #1e1e24 !important;
        color: #ffffff !important;
    }

    /* Buttons styling */
    .stButton > button {
        background-color: #33333d !important;
        color: #ffffff !important;
        border: 1px solid #4f5261 !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
    }
    
    /* Primary action button style */
    .generate-btn button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        font-size: 1.1rem;
        width: 100%;
        margin-top: 1rem;
        padding: 0.8rem !important;
    }
    
    .generate-btn button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.5);
    }

    /* Cards and Containers */
    .copy-card {
        background-color: #15161e;
        border: 1px solid #222533;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    
    .metric-badge {
        background-color: #1e2030;
        border: 1px solid #2b304c;
        border-radius: 6px;
        padding: 0.25rem 0.6rem;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
        color: #a8b2c1;
    }
    
    /* Custom tabs styling */
    .stTabs [data-baseweb="tab"] {
        color: #a8b2c1;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background-color: #1e1e24 !important;
        border-bottom: 2px solid #007bff !important;
    }

    /* Expanders */
    .stExpander {
        background-color: #15161e !important;
        border: 1px solid #222533 !important;
        border-radius: 10px !important;
    }
    
    /* Code block container tweaks */
    .stCode {
        border-radius: 8px;
        border: 1px solid #222533;
        background-color: #0b0c10 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Initialize Session States ---
# Initializing UI control variables for reloading inputs from history
if "prod_name" not in st.session_state:
    st.session_state.prod_name = ""
if "prod_desc" not in st.session_state:
    st.session_state.prod_desc = ""
if "platform_val" not in st.session_state:
    st.session_state.platform_val = "LinkedIn"
if "tone_val" not in st.session_state:
    st.session_state.tone_val = "Professional"
if "version_val" not in st.session_state:
    st.session_state.version_val = "v1.0 (Standard)"
if "temp_val" not in st.session_state:
    st.session_state.temp_val = 0.7
if "top_p_val" not in st.session_state:
    st.session_state.top_p_val = 0.9
if "generated_results" not in st.session_state:
    # List of dicts representing generated copy variations and their database record ID
    st.session_state.generated_results = None
if "restore_toast" not in st.session_state:
    st.session_state.restore_toast = False

# Display toast if restored
if st.session_state.restore_toast:
    st.toast("Settings restored to input fields!", icon="🔄")
    st.session_state.restore_toast = False

# --- Helper Functions ---
def handle_clear():
    """Reset input states."""
    st.session_state.prod_name = ""
    st.session_state.prod_desc = ""
    st.session_state.platform_val = "LinkedIn"
    st.session_state.tone_val = "Professional"
    st.session_state.version_val = "v1.0 (Standard)"
    st.session_state.temp_val = 0.7
    st.session_state.top_p_val = 0.9
    st.session_state.generated_results = None
    st.toast("Inputs cleared!", icon="🧹")

def handle_restore(record):
    """Restore selected history parameters using Streamlit callbacks."""
    st.session_state.prod_name = record["product_name"]
    st.session_state.prod_desc = record["description"]
    st.session_state.platform_val = record["platform"]
    st.session_state.tone_val = record["tone"]
    st.session_state.version_val = record["prompt_version"]
    st.session_state.temp_val = float(record["temperature"])
    st.session_state.top_p_val = float(record["top_p"])
    st.session_state.restore_toast = True


# --- UI Header ---
st.markdown('<div class="main-title">🤖 AI Copywriting & Tone Transformer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate professional, platform-tailored marketing copy using state-of-the-art Generative AI.</div>', unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    # API Provider Selection
    # Detect available keys to set the default option intelligently
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    has_openai = bool(openai_key and openai_key.strip() and openai_key.strip() != "your_key_here")
    has_gemini = bool(gemini_key and gemini_key.strip() and gemini_key.strip() != "your_gemini_api_key_here")

    if has_openai:
        default_provider_index = 0
    elif has_gemini:
        default_provider_index = 1
    else:
        default_provider_index = 2

    provider = st.selectbox(
        "AI Provider",
        options=["OpenAI", "Gemini", "Demo (Offline)"],
        index=default_provider_index,
        help="Select the AI service. Demo Mode runs offline without credentials."
    )
    
    # API Key Handling
    user_api_key = ""
    if provider == "OpenAI":
        env_key = os.getenv("OPENAI_API_KEY")
        key_placeholder = "••••••••••••••••" if env_key else "Enter OpenAI API Key"
        user_api_key = st.text_input("Enter OpenAI API Key", type="password", placeholder=key_placeholder, help="Leave blank if configured in .env file.")
        
        # Model selector
        model_name = st.selectbox("OpenAI Model", options=["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
        
    elif provider == "Gemini":
        env_key = os.getenv("GEMINI_API_KEY")
        key_placeholder = "••••••••••••••••" if env_key else "Enter Gemini API Key"
        user_api_key = st.text_input("Enter Gemini API Key", type="password", placeholder=key_placeholder, help="Leave blank if configured in .env file.")

        
        # Model selector
        model_name = st.selectbox("Gemini Model", options=["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    else:
        model_name = "Offline Rule Engine"
        st.info("💡 **Demo Mode**: The application will run offline using pre-formatted copywriting frameworks based on your product parameters. No API key needed.")

    st.markdown("---")
    st.markdown("### 🎛️ Creativity Settings")
    
    # Temperature and Top P sliders bound to session state
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        key="temp_val",
        help="Higher values make outputs more creative, lower values make them more deterministic."
    )
    
    top_p = st.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        key="top_p_val",
        help="Nucleus sampling threshold. Filters pool of top tokens during generation."
    )

    st.markdown("---")
    st.markdown("### 📋 Generation Settings")
    
    num_variations = st.slider(
        "Number of Variations",
        min_value=1,
        max_value=5,
        value=2,
        help="Generate multiple versions of the copywriting in one request."
    )
    
    # Quick clear history
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History Database", use_container_width=True):
        clear_history()
        st.toast("SQLite Database cleared successfully!", icon="🔥")
        st.rerun()

# --- Main Layout ---
col_inputs, col_preview = st.columns([3, 2])

# Platform specific configuration constraints
PLATFORM_CONSTRAINTS = {
    "LinkedIn": {
        "max_chars": 3000,
        "recommendation": "Ideal LinkedIn length is 1,000–2,000 chars.",
        "icon": "💼"
    },
    "Instagram": {
        "max_chars": 2200,
        "recommendation": "Instagram captions must be under 2,200 characters.",
        "icon": "📸"
    },
    "Email": {
        "max_chars": 10000,
        "recommendation": "Best email size is under 5,000 characters for high readability.",
        "icon": "📧"
    }
}

with col_inputs:
    st.markdown("### 📝 Input Details")
    
    # Product Name
    product_name = st.text_input(
        "Product / Brand Name",
        placeholder="e.g., ZenithFlow",
        key="prod_name",
        help="Enter the brand name of the product or service."
    )
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        # Platform Selection
        target_platform = st.selectbox(
            "Target Platform",
            options=["LinkedIn", "Instagram", "Email"],
            key="platform_val",
            help="Choose where this copy will be published."
        )
    with row1_col2:
        # Tone Selection
        marketing_tone = st.selectbox(
            "Marketing Tone",
            options=["Professional", "Friendly", "Luxury", "Funny", "Creative"],
            key="tone_val",
            help="Tone used to write the copywriting."
        )
        
    # Prompt Template Selection & Preview Info
    prompt_version = st.selectbox(
        "Prompt Template Version",
        options=get_versions(),
        key="version_val",
        help="Different prompt versions focus on distinct copywriting strategies."
    )
    
    # Show dynamic version card
    version_info = get_version_info(prompt_version)
    st.markdown(
        f"""
        <div style="background-color: #1e1e24; border-left: 4px solid #764ba2; border-radius: 4px; padding: 0.6rem; margin-bottom: 1rem;">
            <span style="font-size: 1.1rem;">{version_info['icon']}</span> <strong>{prompt_version} Strategy:</strong><br>
            <span style="font-size: 0.9rem; color: #a8b2c1;">{version_info['description']}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Description
    product_description = st.text_area(
        "Product / Offer Description",
        placeholder="Explain what the product is, key features, target audience, and any special offers...",
        height=150,
        key="prod_desc",
        help="Provide details about the product. Be specific for better results."
    )
    
    # Character count and validation info for input text
    char_count = len(product_description)
    st.markdown(
        f'<div style="text-align: right; font-size: 0.85rem; color: #888;">Input Description Length: {char_count} characters</div>',
        unsafe_allow_html=True
    )
    
    # Validation constraint check
    constraints = PLATFORM_CONSTRAINTS[target_platform]
    st.markdown(
        f"""
        <div style="font-size: 0.9rem; color: #a8b2c1; margin-top: 0.2rem; margin-bottom: 1rem;">
            {constraints['icon']} <strong>Platform Rules</strong>: {constraints['recommendation']}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Actions Buttons
    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        generate_clicked = st.button("🚀 Generate Marketing Copy", key="gen_btn", use_container_width=True)
    with btn_col2:
        st.button("🧹 Clear", on_click=handle_clear, use_container_width=True)

with col_preview:
    st.markdown("### 🔍 Live Prompt Preview")
    if product_name or product_description:
        preview_prompt = compile_prompt(
            product_name=product_name if product_name else "[Product Name]",
            description=product_description if product_description else "[Description]",
            platform=target_platform,
            tone=marketing_tone,
            version=prompt_version
        )
        st.text_area("Dynamically Compiled Prompt Template", value=preview_prompt, height=440, disabled=True)
    else:
        st.info("Fill out the 'Product Name' and 'Product Description' to preview the dynamically compiled prompt.")

# --- Generating Copy Logic ---
if generate_clicked:
    # Error Validation
    if not product_name.strip():
        st.error("⚠️ Product Name cannot be empty!")
    elif not product_description.strip():
        st.error("⚠️ Product Description cannot be empty!")
    else:
        # Prompt Compile
        compiled_prompt = compile_prompt(
            product_name=product_name,
            description=product_description,
            platform=target_platform,
            tone=marketing_tone,
            version=prompt_version
        )
        
        generated_list = []
        
        # Generation loop with visual loading
        with st.spinner(f"✨ Orchestrating {provider} AI model... generating {num_variations} variations"):
            try:
                for idx in range(num_variations):
                    # We slightly alter the prompt seed or add instructions for subsequent variations to get diverse text
                    final_prompt = compiled_prompt
                    if num_variations > 1:
                        final_prompt += f"\n\nMake this version unique and distinct from previous attempts. (Variation Seed: {idx + 1})"
                    
                    # Generate copy using model.py
                    raw_copy = generate_copy(
                        prompt=final_prompt,
                        temperature=temperature,
                        top_p=top_p,
                        provider=provider,
                        api_key=user_api_key,
                        model_name=model_name
                    )
                    
                    # Save to SQLite database history
                    inserted_id = save_history(
                        product_name=product_name,
                        description=product_description,
                        platform=target_platform,
                        tone=marketing_tone,
                        prompt_version=prompt_version,
                        prompt_compiled=final_prompt,
                        generated_copy=raw_copy,
                        temperature=temperature,
                        top_p=top_p,
                        quality_score=0.0  # default rating
                    )
                    
                    generated_list.append({
                        "id": inserted_id,
                        "variation_num": idx + 1,
                        "copy": raw_copy
                    })
                
                st.session_state.generated_results = generated_list
                st.toast("Copy variations successfully created!", icon="🎉")
                
            except Exception as e:
                st.error(f"❌ AI Generation Failed: {str(e)}")

# --- Display Generated Copies ---
if st.session_state.generated_results:
    st.markdown("---")
    st.markdown("### 🏆 Generated Marketing Copy")
    
    # Create tabs for each variation
    tab_names = [f"✨ Variation {v['variation_num']}" for v in st.session_state.generated_results]
    tabs = st.tabs(tab_names)
    
    for idx, tab in enumerate(tabs):
        var_data = st.session_state.generated_results[idx]
        copy_text = var_data["copy"]
        record_id = var_data["id"]
        
        with tab:
            st.markdown(f'<div class="copy-card">', unsafe_allow_html=True)
            
            # Word and Char metrics
            words = len(copy_text.split())
            chars = len(copy_text)
            
            col_met1, col_met2, col_met3 = st.columns([1, 1, 2])
            with col_met1:
                st.markdown(f'<span class="metric-badge">📝 {words} Words</span>', unsafe_allow_html=True)
            with col_met2:
                st.markdown(f'<span class="metric-badge">🔢 {chars} Characters</span>', unsafe_allow_html=True)
            with col_met3:
                # Validate length against limits
                max_allowed = PLATFORM_CONSTRAINTS[target_platform]["max_chars"]
                if chars <= max_allowed:
                    st.markdown(f'<span class="metric-badge" style="color: #2ec4b6; border-color: #2ec4b6;">✅ Platform Compliant</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="metric-badge" style="color: #e71d36; border-color: #e71d36;">⚠️ Exceeds Limit ({max_allowed} max)</span>', unsafe_allow_html=True)
            
            # Text Render Container
            st.markdown("<br>", unsafe_allow_html=True)
            st.code(copy_text, language="markdown")
            
            # Action: Quality scoring & feedback
            st.markdown("---")
            score_col, save_col = st.columns([3, 1])
            with score_col:
                rating = st.slider(
                    "Rate this variation (0 = Poor, 10 = Outstanding)",
                    min_value=0.0,
                    max_value=10.0,
                    value=5.0,
                    step=0.5,
                    key=f"rating_{record_id}"
                )
            with save_col:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Save Rating", key=f"save_rate_{record_id}", use_container_width=True):
                    update_quality_score(record_id, rating)
                    st.toast(f"Saved score of {rating} for Variation {idx+1}!", icon="🎯")
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- SQLite History Explorer ---
st.markdown("---")
with st.expander("📚 SQLite Copywriting History Logs", expanded=False):
    st.markdown("View previously generated copywriting versions, scores, parameters, and reload them instantly.")
    
    # Load from db
    history_records = get_history(limit=50)
    
    if not history_records:
        st.info("No records found in history. Start generating to build your logs!")
    else:
        # Platform/Tone filters
        hist_filter_col1, hist_filter_col2 = st.columns(2)
        with hist_filter_col1:
            platform_filter = st.selectbox("Filter by Platform", options=["All", "LinkedIn", "Instagram", "Email"])
        with hist_filter_col2:
            tone_filter = st.selectbox("Filter by Tone", options=["All", "Professional", "Friendly", "Luxury", "Funny", "Creative"])
            
        # Filter logic
        filtered_records = []
        for r in history_records:
            if platform_filter != "All" and r["platform"] != platform_filter:
                continue
            if tone_filter != "All" and r["tone"] != tone_filter:
                continue
            filtered_records.append(r)
            
        if not filtered_records:
            st.warning("No records match the active filter criteria.")
        else:
            for record in filtered_records:
                # Single history card
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background-color: #1e1e24; border: 1px solid #33333d; border-radius: 8px; padding: 1rem; margin-bottom: 0.8rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <strong>{record['product_name']}</strong> 
                                <span style="font-size: 0.85rem; color: #888;">{record['timestamp']}</span>
                            </div>
                            <div style="margin-bottom: 0.5rem;">
                                <span class="metric-badge">{record['platform']}</span>
                                <span class="metric-badge">{record['tone']}</span>
                                <span class="metric-badge">{record['prompt_version']}</span>
                                <span class="metric-badge" style="color: #8f94fb;">⭐ Rating: {record['quality_score']}/10</span>
                            </div>
                            <div style="font-size: 0.9rem; color: #a8b2c1; max-height: 100px; overflow-y: auto; background-color: #0b0c10; padding: 0.5rem; border-radius: 4px; margin-bottom: 0.5rem; white-space: pre-wrap;">{record['generated_copy']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Action row for record
                    act_col1, act_col2, _ = st.columns([1, 1, 4])
                    with act_col1:
                        # Restore button
                        st.button(
                            "🔄 Restore Settings", 
                            key=f"restore_{record['id']}", 
                            on_click=handle_restore, 
                            args=(record,), 
                            use_container_width=True
                        )
                    with act_col2:
                        # View prompt button
                        with st.popover("💬 View Prompt"):
                            st.text_area("Compiled Prompt", value=record["prompt_compiled"], height=300, disabled=True)
