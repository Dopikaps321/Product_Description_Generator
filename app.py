from flask import Flask, request, jsonify
import google.generativeai as genai
import json
import time
import re
from config import Config
from utils.validators import validate_input, validate_output
from utils.evaluator import evaluate_description, get_evaluation_report
from prompts.prompt_templates import get_product_description_prompt
from collections import OrderedDict

app = Flask(__name__)
app.config.from_object(Config)

# Configure Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def validate_and_mark_invalid_fields(data):
    """Validate input data and mark invalid fields with 'Invalid input'"""
    validated_data = data.copy()
    has_valid_data = True

    # Validate product_name
    if 'product_name' not in data or not isinstance(data.get('product_name'), str) or not data.get('product_name').strip():
        validated_data['product_name'] = "Invalid input"
        has_valid_data = False

    # Validate category (must be a string and a known category)
    valid_categories = [
        "Electronics", "Wearables", "Smartphone", "Clothing", "Home", "Beauty", "Sports"
    ]
    if 'category' not in data or not isinstance(data.get('category'), str) or not data.get('category').strip() or data.get('category').capitalize() not in valid_categories:
        validated_data['category'] = "Invalid input"
        has_valid_data = False

    # Validate key_features
    if 'key_features' not in data:
        validated_data['key_features'] = "Invalid input"
        has_valid_data = False
    elif not isinstance(data.get('key_features'), list):
        validated_data['key_features'] = "Invalid input"
        has_valid_data = False
    elif not all(isinstance(feature, str) and feature.strip() for feature in data.get('key_features', [])):
        validated_data['key_features'] = "Invalid input"
        has_valid_data = False

    # Validate price
    if 'price' not in data:
        validated_data['price'] = "Invalid input"
        has_valid_data = False
    elif not isinstance(data.get('price'), (int, float)):
        validated_data['price'] = "Invalid input"
        has_valid_data = False
    elif data.get('price') < 0:
        validated_data['price'] = "Invalid input"
        has_valid_data = False

    # Validate optional fields
    if 'target_audience' in data and (not isinstance(data.get('target_audience'), str) or not data.get('target_audience').strip()):
        validated_data['target_audience'] = "Invalid input"

    if 'tone' in data and (not isinstance(data.get('tone'), str) or not data.get('tone').strip()):
        validated_data['tone'] = "Invalid input"

    # Set defaults for optional fields if not provided
    if 'target_audience' not in validated_data:
        validated_data['target_audience'] = 'general'
    if 'tone' not in validated_data:
        validated_data['tone'] = 'professional'

    return validated_data, has_valid_data

def clean_json_response(raw_response):
    """Clean and parse JSON response from Gemini API"""
    try:
        if raw_response.startswith('```json'):
            raw_response = raw_response[7:-3]
        elif raw_response.startswith('```'):
            raw_response = raw_response[3:-3]

        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            raw_response = json_match.group()

        return json.loads(raw_response)
    except:
        try:
            raw_response = raw_response.strip()
            raw_response = re.sub(r',\s*}', '}', raw_response)
            raw_response = re.sub(r',\s*]', ']', raw_response)
            return json.loads(raw_response)
        except:
            raise ValueError("Could not parse JSON response")

@app.route('/generate-description', methods=['POST'])
def generate_description():
    """Main API endpoint for generating product descriptions"""
    start_time = time.time()

    try:
        # Parse JSON safely
        try:
            data = request.get_json(force=True)
        except Exception as json_err:
            return jsonify({"error": f"Invalid JSON format: {str(json_err)}"}), 400

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate and mark invalid fields
        validated_data, has_valid_required_data = validate_and_mark_invalid_fields(data)
        
        # Debug prints (optional - remove in production)
        print(f"DEBUG: Input data = {data}")
        print(f"DEBUG: Validated data = {validated_data}")
        print(f"DEBUG: Has valid required data = {has_valid_required_data}")
        
        # If any required field is invalid, return the input with 'Invalid input' markers (only for those fields)
        if not has_valid_required_data:
            # Only return the validated input, preserving all fields and marking only invalid ones
            return jsonify(validated_data), 400

        # If all required fields are valid, proceed with generation
        clean_data = {k: v for k, v in validated_data.items() if v != "Invalid input"}
        prompt = get_product_description_prompt(clean_data)

        # Call Gemini API with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                raw_response = response.text
                generated_output = clean_json_response(raw_response)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    return jsonify({"error": f"AI generation failed after {max_retries} attempts: {str(e)}"}), 500
                time.sleep(1)

        # Validate LLM output
        is_valid, validation_message = validate_output(generated_output)
        if not is_valid:
            return jsonify({"error": f"Invalid output format: {validation_message}"}), 500

        final_output = OrderedDict([
            ("short_description", generated_output.get("short_description", "")),
            ("detailed_description", generated_output.get("detailed_description", "")),
            ("bullet_points", generated_output.get("bullet_points", [])),
            ("seo_keywords", generated_output.get("seo_keywords", [])),
            ("call_to_action", generated_output.get("call_to_action", ""))
        ])

        return app.response_class(
            response=json.dumps(final_output),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/validate-input', methods=['POST'])
def validate_input_only():
    """Endpoint to only validate input without generating content"""
    try:
        # Parse JSON safely
        try:
            data = request.get_json(force=True)
        except Exception as json_err:
            return jsonify({"error": f"Invalid JSON format: {str(json_err)}"}), 400

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate and mark invalid fields
        validated_data, has_valid_required_data = validate_and_mark_invalid_fields(data)
        
        response_data = {
            "input_validation": validated_data,
            "is_valid": has_valid_required_data,
            "message": "All required fields are valid" if has_valid_required_data else "Some required fields contain invalid input"
        }
        
        status_code = 200 if has_valid_required_data else 400
        return jsonify(response_data), status_code

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/evaluate', methods=['POST'])
def evaluate_generated_description():
    """Endpoint for evaluating generated descriptions"""
    try:
        data = request.get_json()
        if not data or 'input_data' not in data or 'generated_output' not in data:
            return jsonify({"error": "Missing input_data or generated_output"}), 400

        input_data = data['input_data']
        generated_output = data['generated_output']
        report = get_evaluation_report(input_data, generated_output)

        return jsonify(report), 200

    except Exception as e:
        return jsonify({"error": f"Evaluation failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "gemini_configured": bool(Config.GEMINI_API_KEY)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)