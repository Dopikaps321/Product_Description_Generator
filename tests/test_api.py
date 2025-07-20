import requests
import json
import time
from test_cases import TEST_CASES

BASE_URL = "http://localhost:5000"

def test_single_case(test_case):
    """Test a single case against the API"""
    start_time = time.time()
    
    try:
        response = requests.post(f"{BASE_URL}/generate-description", json=test_case)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            
            # Validate response format
            required_fields = ['short_description', 'detailed_description', 'bullet_points', 'seo_keywords', 'call_to_action']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                return {
                    "success": False,
                    "error": f"Missing required fields: {missing_fields}",
                    "test_case": test_case
                }
            
            # Check word counts
            short_words = len(result['short_description'].split())
            detailed_words = len(result['detailed_description'].split())
            
            validation_issues = []
            if not (20 <= short_words <= 50):
                validation_issues.append(f"Short description: {short_words} words (should be 20-50)")
            if not (50 <= detailed_words <= 200):
                validation_issues.append(f"Detailed description: {detailed_words} words (should be 50-200)")
            
            return {
                "success": True,
                "response_time": end_time - start_time,
                "result": result,
                "validation_issues": validation_issues,
                "test_case": test_case
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "test_case": test_case
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "test_case": test_case
        }

def test_example_case():
    """Test the specific example from the PDF"""
    example_input = {
        "product_name": "Samsung Galaxy S24",
        "category": "Smartphone",
        "key_features": ["256GB storage", "50MP camera", "6.2 inch display"],
        "price": 75000,
        "target_audience": "tech enthusiasts",
        "tone": "professional"
    }
    
    print("Testing PDF Example Case...")
    print("=" * 50)
    print(f"Input: {json.dumps(example_input, indent=2)}")
    
    result = test_single_case(example_input)
    
    if result["success"]:
        print("\n SUCCESS!")
        print(f"Response Time: {result['response_time']:.2f}s")
        print(f"Output: {json.dumps(result['result'], indent=2)}")
        
        if result.get('validation_issues'):
            print(f"\n  Validation Issues: {result['validation_issues']}")
    else:
        print(f"\n FAILED: {result['error']}")
    
    return result

def run_all_tests():
    """Run all test cases"""
    results = []
    
    
    pdf_result = test_example_case()
    results.append(pdf_result)
    
    print("\n" + "=" * 50)
    print("Running All Test Cases...")
    print("=" * 50)
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test {i}/{len(TEST_CASES)}: {test_case['product_name']}")
        
        result = test_single_case(test_case)
        results.append(result)
        
        if result["success"]:
            print(f" Success - {result['response_time']:.2f}s")
            if result.get('validation_issues'):
                print(f"     Issues: {result['validation_issues']}")
        else:
            print(f" Failed - {result['error']}")
        print()
    
    
    successful = sum(1 for r in results if r["success"])
    total_tests = len(results)
    avg_time = sum(r.get('response_time', 0) for r in results if r["success"]) / max(successful, 1)
    
    print("=" * 50)
    print(f"SUMMARY: {successful}/{total_tests} tests passed")
    print(f"Average Response Time: {avg_time:.2f}s")
    print(f"Success Rate: {(successful/total_tests)*100:.1f}%")
    
    return results

if __name__ == "__main__":
    results = run_all_tests()