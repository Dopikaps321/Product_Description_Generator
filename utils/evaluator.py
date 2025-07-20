def evaluate_description(input_data, generated_output):
    """Evaluate generated description according to challenge criteria"""
    score = 0
    
    
    
    
    features_mentioned = all(
        feature.lower() in generated_output.get('detailed_description', '').lower()
        for feature in input_data.get('key_features', [])
    )
    if features_mentioned:
        score += 10
    
    
    detailed_desc = generated_output.get('detailed_description', '')
    word_count = len(detailed_desc.split())
    if 50 <= word_count <= 200:
        score += 10
    
    
    price = input_data.get('price', 0)
    price_terms = ['premium', 'luxury', 'budget', 'affordable', 'value', 'investment']
    if any(term in detailed_desc.lower() for term in price_terms):
        score += 5
    
    
    target_audience = input_data.get('target_audience', '').lower()
    if target_audience in detailed_desc.lower():
        score += 10
    
    
    cta = generated_output.get('call_to_action', '')
    if cta and len(cta) > 10:
        score += 5
    
    return score

def get_evaluation_report(input_data, generated_output):
    """Generate detailed evaluation report"""
    report = {
        'total_score': 0,
        'breakdown': {},
        'issues': []
    }
    
    
    features_mentioned = all(
        feature.lower() in generated_output.get('detailed_description', '').lower()
        for feature in input_data.get('key_features', [])
    )
    report['breakdown']['features_mentioned'] = 10 if features_mentioned else 0
    if not features_mentioned:
        report['issues'].append("Not all features mentioned in description")
    
    
    word_count = len(generated_output.get('detailed_description', '').split())
    report['breakdown']['appropriate_length'] = 10 if 50 <= word_count <= 200 else 0
    if not (50 <= word_count <= 200):
        report['issues'].append(f"Description length {word_count} words (should be 50-200)")
    
    
    report['total_score'] = sum(report['breakdown'].values())
    
    return report