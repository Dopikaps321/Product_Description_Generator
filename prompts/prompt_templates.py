def get_product_description_prompt(product_data):
    """
    Generate a sophisticated prompt for product description generation
    """
    # Price positioning logic
    price = product_data.get('price', 0)
    if price < 1000:
        price_category = "budget-friendly"
    elif price < 10000:
        price_category = "mid-range"
    elif price < 50000:
        price_category = "premium"
    else:
        price_category = "luxury"
    
    # Category-specific context
    category_context = {
        'smartphone': 'cutting-edge technology and connectivity',
        'electronics': 'innovative features and performance',
        'clothing': 'style, comfort, and quality',
        'home': 'functionality and aesthetic appeal',
        'beauty': 'enhancement and self-care',
        'sports': 'performance and durability'
    }
    
    category_lower = product_data.get('category', '').lower()
    context = category_context.get(category_lower, 'quality and value')
    
    # Format features for the prompt
    features_list = product_data.get('key_features', [])
    features_str = ', '.join(features_list)
    
    prompt = f"""You are an expert e-commerce copywriter specializing in {product_data.get('category', 'products')}.
Your task is to create compelling, conversion-focused product descriptions that drive sales.

PRODUCT DETAILS:
- Product Name: {product_data.get('product_name')}
- Category: {product_data.get('category')}
- Key Features: {features_str}
- Price: ₹{product_data.get('price')} ({price_category})
- Target Audience: {product_data.get('target_audience', 'general')}
- Tone: {product_data.get('tone', 'professional')}

WRITING GUIDELINES:
- Focus on {context}
- Highlight value proposition for {price_category} segment
- Use {product_data.get('tone', 'professional')} tone throughout
- Appeal to {product_data.get('target_audience', 'general')} specifically
- Include emotional triggers and benefits, not just features

EXAMPLE OUTPUT FORMAT:
{{
  "short_description": "Samsung Galaxy S24 - Premium smartphone with 256GB storage and 50MP camera",
  "detailed_description": "Experience cutting-edge technology with the Samsung Galaxy S24. This premium smartphone delivers exceptional performance with its advanced processor and stunning camera system. Perfect for tech enthusiasts who demand the best.",
  "bullet_points": [
    "256GB storage - Never run out of space for your digital life",
    "50MP camera - Capture professional-quality photos and videos",
    "6.2 inch display - Immersive viewing experience for all your content"
  ],
  "seo_keywords": [
    "Samsung Galaxy S24",
    "smartphone",
    "256GB",
    "50MP camera",
    "premium phone"
  ],
  "call_to_action": "Upgrade to premium technology - Order your Galaxy S24 today!"
}}

CRITICAL REQUIREMENTS:
- Mention ALL key features: {features_str}
- Short description: EXACTLY 20-50 words
- Detailed description: EXACTLY 50-200 words
- Bullet points: EXACTLY 3-5 items, each explaining the benefit of the feature
- SEO keywords: Include product name and key features
- Call to action: Create urgency and encourage purchase
- Consider the {price_category} price point in positioning
- Adapt language for {product_data.get('target_audience', 'general')} audience
- Use {product_data.get('tone', 'professional')} tone consistently

Return ONLY valid JSON format with the exact structure shown above. No additional text before or after the JSON."""

    return prompt