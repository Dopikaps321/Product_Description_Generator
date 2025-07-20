def validate_input(data):
    """Validate input data according to API specification"""
    errors = []

    required_fields = ['product_name', 'category', 'key_features', 'price']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if 'product_name' in data and not isinstance(data['product_name'], str):
        errors.append("product_name must be a string")

    if 'category' in data and not isinstance(data['category'], str):
        errors.append("category must be a string")

    if 'key_features' in data:
        if not isinstance(data['key_features'], list):
            errors.append("key_features must be an array")
        elif not all(isinstance(feature, str) for feature in data['key_features']):
            errors.append("all key_features must be strings")

    # Removed: price type check (now handled in app.py)

    if 'target_audience' in data and not isinstance(data['target_audience'], str):
        errors.append("target_audience must be a string")

    if 'tone' in data and not isinstance(data['tone'], str):
        errors.append("tone must be a string")

    return errors



def validate_output(output):
    """Validate generated output format"""
    required_fields = ['short_description', 'detailed_description', 'bullet_points', 'seo_keywords', 'call_to_action']
    
    for field in required_fields:
        if field not in output:
            return False, f"Missing required field: {field}"
    
    
    if not isinstance(output.get('bullet_points'), list):
        return False, "bullet_points must be an array"
    
    if not isinstance(output.get('seo_keywords'), list):
        return False, "seo_keywords must be an array"
    
    
    short_desc_words = len(output.get('short_description', '').split())
    if not (20 <= short_desc_words <= 50):
        return False, f"short_description must be 20-50 words, got {short_desc_words}"
    
    detailed_desc_words = len(output.get('detailed_description', '').split())
    if not (50 <= detailed_desc_words <= 200):
        return False, f"detailed_description must be 50-200 words, got {detailed_desc_words}"
    
    return True, "Valid"
