Product Description Generator
A Flask-based REST API that uses Gemini 1.5 Flash to generate structured, SEO-friendly product descriptions for e-commerce platforms.

Features
Generates short & detailed descriptions, bullet points, SEO keywords, and call-to-action

Accepts product data as JSON input

Includes evaluation and health check endpoints

Built with robust input/output validation and retry logic

Sample Input

{
  "product_name": "iPhone 15 Pro",
  "category": "smartphone",
  "price": 999,
  "key_features": ["A17 Pro chip", "48MP camera", "Titanium body"],
  "target_audience": "tech-savvy users",
  "tone": "professional"
}

Expected Output (JSON format)

{
  "short_description": "The iPhone 15 Pro combines cutting-edge performance with premium design, ideal for tech-savvy users.",
  "detailed_description": "Powered by the new A17 Pro chip, the iPhone 15 Pro offers blazing-fast performance, a stunning 48MP camera, and a sleek titanium body for durability and style.",
  "bullet_points": [
    "A17 Pro chip for unmatched speed",
    "48MP professional-grade camera",
    "Lightweight and durable titanium body"
  ],
  "seo_keywords": [
    "iPhone 15 Pro",
    "A17 chip smartphone",
    "48MP camera phone",
    "Titanium smartphone"
  ],
  "call_to_action": "Upgrade to the iPhone 15 Pro today and experience the future of mobile technology."
}


🧪 Endpoints
POST /generate-description → Generate product content

POST /evaluate → Evaluate generated descriptions

GET /health → Check API status

