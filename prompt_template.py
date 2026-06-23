# prompt_template.py
"""
Dynamic Prompt Engineering and Versioning module.
Provides platform-specific templates (LinkedIn, Instagram, Email)
and manages multiple prompt versions (v1.0 Standard, v2.0 Conversion Focused, v3.0 Storytelling).
"""

# Version descriptions for UI representation
VERSION_DETAILS = {
    "v1.0 (Standard)": {
        "description": "Engaging, standard copy suitable for general audiences. Focuses on clarity and friendliness.",
        "icon": "📝"
    },
    "v2.0 (Conversion Focused)": {
        "description": "Optimized using direct response marketing. Focuses on hooks, benefit lists, and strong Calls to Action (CTA).",
        "icon": "⚡"
    },
    "v3.0 (Storytelling)": {
        "description": "Uses narrative hooks and relatable scenarios. Focuses on emotional connection before presenting the solution.",
        "icon": "📖"
    }
}

# Platform-specific and version-specific prompt templates
TEMPLATES = {
    "v1.0 (Standard)": {
        "LinkedIn": (
            "You are an expert LinkedIn content strategist and copywriter.\n\n"
            "Create a {tone} marketing post for LinkedIn.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Formatting & Style Guidelines:\n"
            "- Start with an engaging hook related to the professional space.\n"
            "- Keep paragraphs short (1-3 sentences) for readability on mobile.\n"
            "- Tone should be distinctly {tone}.\n"
            "- Use 2-3 relevant professional emojis.\n"
            "- End with a clear call to action (CTA) encouraging professionals to comment or learn more.\n"
            "- Include 3-4 industry-specific hashtags."
        ),
        "Instagram": (
            "You are a social media manager and creative Instagram copywriter.\n\n"
            "Create a {tone} caption for an Instagram post.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Formatting & Style Guidelines:\n"
            "- Start with an attention-grabbing first line (the 'hook') that stops users from scrolling.\n"
            "- Use spacing and paragraphs to make the caption easily scannable.\n"
            "- The overall feel must be {tone}.\n"
            "- Use expressive emojis throughout to add personality.\n"
            "- Include a clear call to action (e.g., 'Click the link in bio', 'Double tap if you agree', 'Share with a friend').\n"
            "- Add a block of 5-8 relevant, trending hashtags at the end."
        ),
        "Email": (
            "You are a conversion-focused email marketing copywriter.\n\n"
            "Write a highly engaging {tone} marketing email.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Formatting & Style Guidelines:\n"
            "- Include a clear, click-worthy 'Subject Line:'.\n"
            "- Include a brief, complementary 'Preview Text:'.\n"
            "- Start with a warm, {tone} greeting.\n"
            "- The body should address a common reader problem, and introduce {product_name} as the solution.\n"
            "- Use a structured layout with bullet points for key features if helpful.\n"
            "- Keep the writing style personal and conversational, in a {tone} tone.\n"
            "- End with a single, highly visible call to action (CTA) and a friendly sign-off."
        )
    },
    
    "v2.0 (Conversion Focused)": {
        "LinkedIn": (
            "You are a world-class direct-response copywriter specializing in B2B and LinkedIn growth.\n\n"
            "Write a high-converting {tone} LinkedIn post targeting decision-makers.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Copywriting Strategy (Direct Response):\n"
            "- The Hook: Open with a bold, scroll-stopping question, stat, or contrarian statement (e.g. 'Most people get [Topic] wrong...').\n"
            "- The Pain Point: Agitate a critical professional pain point that {product_name} solves.\n"
            "- The Solution: Position {product_name} as the ultimate solution.\n"
            "- The Core Benefits: List 3 high-impact bulleted outcomes using emoji checkboxes (e.g., ✔️, 🚀).\n"
            "- Style: Energetic, authority-building, and {tone}.\n"
            "- The CTA: Direct action call (e.g., 'DM me for access', 'Click below to read more').\n"
            "- Hashtags: 3 targeted hashtags."
        ),
        "Instagram": (
            "You are a growth marketing specialist and Instagram conversion copywriter.\n\n"
            "Write a high-converting, viral-style {tone} Instagram caption.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Copywriting Strategy:\n"
            "- The Hook: Use capital letters or a shocking statement in the first line to trigger curiosity (e.g., 'STOP doing [Action]', 'This simple trick changed...').\n"
            "- Value Stack: Share 3 fast, actionable takeaways or benefits of {product_name}.\n"
            "- Tone: Fun, persuasive, and {tone}.\n"
            "- Social Proof / FOMO: Create urgency or highlight exclusive value.\n"
            "- CTA: High-conversion prompt (e.g., 'Save this post for later', 'Comment [Keyword] to get the link sent to your DMs').\n"
            "- Hashtags: 5-8 hyper-focused hashtags, separated by space."
        ),
        "Email": (
            "You are an elite email copywriter trained in high-conversion sales funnels.\n\n"
            "Write a persuasive, direct-response {tone} email using the PAS (Problem-Agitate-Solve) formula.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Copywriting Strategy:\n"
            "- Subject Line: High curiosity or urgency (e.g. 'The truth about [Problem]', '[Name], are you making this mistake?').\n"
            "- Preview Text: Short hook that continues the subject line.\n"
            "- Problem: Identify a pressing pain point the subscriber faces.\n"
            "- Agitate: Agitate that pain point. Show the cost of doing nothing.\n"
            "- Solve: Introduce {product_name} as the immediate, painless solution.\n"
            "- CTA: Clear, singular link CTA (e.g. '[Click here to get [Product] for 20% off]').\n"
            "- Tone: Convincing, direct, and {tone}.\n"
            "- Include a P.S. (Postscript) containing urgency or a secondary push."
        )
    },
    
    "v3.0 (Storytelling)": {
        "LinkedIn": (
            "You are a narrative copywriter specializing in LinkedIn story-selling.\n\n"
            "Write a storytelling-style {tone} LinkedIn post that weaves a narrative.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Storytelling Framework:\n"
            "- The Hook: Start in media res—in the middle of a moment or conflict (e.g., 'I was sitting in my office when...', 'Three years ago, I failed...').\n"
            "- The Struggle: Describe a relatable personal or customer challenge.\n"
            "- The Epiphany/Climax: The realization that led to the creation or use of {product_name}.\n"
            "- The Lesson: Share the broader industry or professional lesson learned.\n"
            "- Tone: Authentic, vulnerable, inspiring, and {tone}.\n"
            "- Connection: Gracefully transition from the story to {product_name}.\n"
            "- CTA: Soft invitation to connect, discuss, or visit the link."
        ),
        "Instagram": (
            "You are a storytelling copywriter and visual brand storyteller for Instagram.\n\n"
            "Write an authentic, narrative-style {tone} Instagram caption.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Storytelling Framework:\n"
            "- The Hook: Open with an emotional hook or a 'picture this' scenario.\n"
            "- The Story: Tell a brief, vivid story of a customer, a day in the life, or the 'behind-the-scenes' origin of {product_name}.\n"
            "- Tone: Relatable, engaging, aesthetic, and {tone}.\n"
            "- Value / Reflection: What this story teaches us or why it matters.\n"
            "- Call to Action: Invite story sharing in the comments (e.g., 'Have you ever felt like this? Let me know below!').\n"
            "- Hashtags: 5-7 aesthetic and community-oriented hashtags."
        ),
        "Email": (
            "You are a narrative email marketer specializing in relationship-building copy.\n\n"
            "Write an engaging storytelling {tone} newsletter/email.\n\n"
            "Product Name: {product_name}\n"
            "Product/Service Description:\n{description}\n\n"
            "Storytelling Framework:\n"
            "- Subject Line: Narrative/Metaphor (e.g., 'A quick story about a coffee cup...', 'What my dog taught me about [Topic]').\n"
            "- Preview Text: Short opening hook of the story.\n"
            "- The Narrative: Start with an interesting, funny, or emotional anecdote. Keep the reader hooked line-by-line.\n"
            "- The Bridge: Bridge the story naturally to the core problem solved by {product_name}.\n"
            "- The Solution: Pitch {product_name} warmly as a natural helper in this journey.\n"
            "- Tone: Humorous, authentic, conversational, and {tone}.\n"
            "- CTA: Warm invitation to try or purchase."
        )
    }
}

def compile_prompt(product_name, description, platform, tone, version):
    """
    Retrieves the correct prompt template for the given platform and version,
    and interpolates user-specific variables.
    
    Parameters:
        product_name (str): Name of the product
        description (str): Description of the product
        platform (str): 'LinkedIn', 'Instagram', or 'Email'
        tone (str): 'Professional', 'Friendly', 'Luxury', 'Funny', or 'Creative'
        version (str): The template version key (e.g. 'v1.0 (Standard)')
        
    Returns:
        str: Compiled prompt ready for LLM consumption.
    """
    # Fallback to v1.0 and Standard template if inputs are missing or invalid
    version_dict = TEMPLATES.get(version, TEMPLATES["v1.0 (Standard)"])
    template = version_dict.get(platform, version_dict["LinkedIn"])
    
    # Inject variables
    compiled = template.format(
        product_name=product_name,
        description=description,
        platform=platform,
        tone=tone
    )
    
    return compiled

def get_versions():
    """Returns list of available version names."""
    return list(TEMPLATES.keys())

def get_version_info(version):
    """Returns description and icon for a specific version."""
    return VERSION_DETAILS.get(version, {"description": "", "icon": "❓"})
