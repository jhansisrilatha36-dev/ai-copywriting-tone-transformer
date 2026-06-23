# model.py
"""
Generative AI Model Integration.
Supports OpenAI API, Google Gemini API, and a high-quality Local Demo Fallback mode.
"""

import os
import warnings
from dotenv import load_dotenv

# Suppress deprecation warnings from google-generativeai
warnings.filterwarnings("ignore", category=FutureWarning)

# Load environment variables from multiple potential locations
dir_path = os.path.dirname(os.path.abspath(__file__))
# 1. Project folder (.env)
load_dotenv(os.path.join(dir_path, ".env"))
# 2. Workspace root (.env)
load_dotenv(os.path.join(os.path.dirname(dir_path), ".env"))
# 3. Current working directory (.env)
load_dotenv()


from openai import OpenAI
import google.generativeai as genai



def generate_copy(prompt, temperature, top_p, provider="OpenAI", api_key=None, model_name=None):
    """
    Generate marketing copy using the selected AI provider.
    
    Parameters:
        prompt (str): Compiled prompt containing product details and formatting guidelines.
        temperature (float): Controls creativity (0.0 = deterministic, 1.0 = creative).
        top_p (float): Nucleus sampling control.
        provider (str): 'OpenAI', 'Gemini', or 'Demo (Offline)'.
        api_key (str): Optional API key. If not provided, will look in environment variables.
        model_name (str): Optional custom model name.
        
    Returns:
        str: Generated copywriting text.
    """
    if provider == "OpenAI":
        # Resolve key and strip whitespace/quotes
        key = api_key
        if not key or not key.strip():
            key = os.getenv("OPENAI_API_KEY")
        
        if key:
            key = key.strip().strip('"').strip("'")
            
        if not key or key == "your_key_here" or key == "":
            raise ValueError("OpenAI API Key is missing. Please configure it in the sidebar or .env file.")
        
        selected_model = model_name or "gpt-4o-mini"
        
        # Initialize client
        client = OpenAI(api_key=key)
        
        # Call chat completion
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a professional copywriting assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            top_p=top_p
        )
        return response.choices[0].message.content.strip()

    elif provider == "Gemini":
        # Resolve key and strip whitespace/quotes
        key = api_key
        if not key or not key.strip():
            key = os.getenv("GEMINI_API_KEY")
            
        if key:
            key = key.strip().strip('"').strip("'")
            
        if not key or key == "your_gemini_api_key_here" or key == "":
            raise ValueError("Gemini API Key is missing. Please configure it in the sidebar or .env file.")
        
        selected_model = model_name or "gemini-1.5-flash"
        
        # Configure Gemini
        genai.configure(api_key=key)
        model = genai.GenerativeModel(selected_model)
        
        # Call generation
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            top_p=top_p
        )
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text.strip()

    elif provider == "Demo (Offline)":
        return generate_demo_copy(prompt, temperature, top_p)
        
    else:
        raise ValueError(f"Unknown provider: {provider}")

def generate_demo_copy(prompt, temperature, top_p):
    """
    Offline fallback copy generator. Parses the prompt to extract key parameters
    and generates rich, formatted copywriting using structured templates.
    """
    # Parse parameters from prompt text (fallback values if parsing fails)
    platform = "LinkedIn"
    if "Instagram" in prompt:
        platform = "Instagram"
    elif "Email" in prompt:
        platform = "Email"
        
    tone = "Professional"
    for t in ["Professional", "Friendly", "Luxury", "Funny", "Creative"]:
        if f" {t.lower()} " in prompt.lower() or f"\n{t.lower()}" in prompt.lower():
            tone = t
            break
            
    product_name = "Innovative Product"
    if "Product Name:" in prompt:
        try:
            product_name = prompt.split("Product Name:")[1].split("\n")[0].strip()
        except Exception:
            pass
            
    description = "A wonderful product that solves everyday challenges."
    if "Description:" in prompt:
        try:
            description = prompt.split("Description:")[1].split("\n\n")[0].strip()
        except Exception:
            try:
                description = prompt.split("Description:")[1].split("Formatting")[0].strip()
            except Exception:
                pass

    # Craft realistic marketing content offline
    intro = {
        "Professional": f"Introducing {product_name}—a game-changer in its class. Built for high-performers who value efficiency.",
        "Friendly": f"Hey everyone! Meet {product_name}! We're so excited to share this with you all. It's designed to make your life just a little bit easier.",
        "Luxury": f"Experience the pinnacle of sophistication. Presenting {product_name}: where craftsmanship meets unparalleled performance.",
        "Funny": f"Let's be honest: life is hard. That's why we created {product_name}. Because doing things the hard way is so last year.",
        "Creative": f"Imagine a world where complexity melts away. That's the magic of {product_name}—reimagining the future, starting today."
    }[tone]
    
    body = f"It solves a key problem: {description}. If you have been looking for a solution that combines durability with modern design, this is it."
    
    cta = {
        "LinkedIn": f"👉 Let's connect! Have you experienced this challenge in your business? Share your thoughts below, or visit our website to learn how {product_name} can transform your operations today.",
        "Instagram": f"✨ Ready to elevate your routine? Tap the link in our bio to shop {product_name} now! 🛍️ Support local, live better.",
        "Email": f"If you're ready to make a change, click the button below to secure your {product_name} today:\n\n👉 [Get Started with {product_name} Now]"
    }[platform]

    hashtags = {
        "LinkedIn": "#innovation #productivity #businessgrowth #leadership",
        "Instagram": "#lifestyle #musthave #goals #aesthetic #supportlocal #trend",
        "Email": ""
    }[platform]

    if platform == "Email":
        subject_line = {
            "Professional": f"Subject: Elevate your team's workflow with {product_name}",
            "Friendly": f"Subject: Say hello to your new favorite helper: {product_name}!",
            "Luxury": f"Subject: Exclusive access to {product_name}",
            "Funny": f"Subject: You can stop looking now. {product_name} is here.",
            "Creative": f"Subject: A fresh perspective on productivity: {product_name}"
        }[tone]
        
        preview = f"Preview: Learn how {product_name} can change the way you work today."
        
        output = (
            f"📧 [DEMO OFFLINE GENERATION]\n\n"
            f"{subject_line}\n"
            f"{preview}\n\n"
            f"Dear Reader,\n\n"
            f"{intro}\n\n"
            f"{body}\n\n"
            f"Why choose {product_name}?\n"
            f"• Tailored results\n"
            f"• Saves valuable time\n"
            f"• High quality standards\n\n"
            f"{cta}\n\n"
            f"Best regards,\n"
            f"The {product_name} Team\n\n"
            f"*(Generated in Demo Mode at Temperature={temperature}, Top_P={top_p})*"
        )
    elif platform == "Instagram":
        output = (
            f"📸 [DEMO OFFLINE GENERATION]\n\n"
            f"{intro}\n\n"
            f"{body} 🔥\n\n"
            f"{cta}\n\n"
            f".\n.\n.\n"
            f"{hashtags}\n\n"
            f"*(Generated in Demo Mode at Temperature={temperature}, Top_P={top_p})*"
        )
    else:  # LinkedIn
        output = (
            f"💼 [DEMO OFFLINE GENERATION]\n\n"
            f"{intro}\n\n"
            f"{body} 🚀\n\n"
            f"Key takeaways:\n"
            f"1️⃣ Innovation-first design\n"
            f"2️⃣ Seamless integration\n"
            f"3️⃣ Proven results\n\n"
            f"{cta}\n\n"
            f"{hashtags}\n\n"
            f"*(Generated in Demo Mode at Temperature={temperature}, Top_P={top_p})*"
        )

    return output
