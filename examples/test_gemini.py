#!/usr/bin/env python3
"""
Test script for Google Gemini API
Tests both text-to-text and image-to-text capabilities with new JSON structure
"""

import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import json

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gemini_text_to_text():
    """Test Gemini's text-to-text capabilities"""
    print("🧪 Testing Gemini Text-to-Text...")
    
    try:
        # Configure the API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
        
        genai.configure(api_key=api_key)
        
        # Initialize the model - using Gemini 2.5 Flash Lite
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
        
        # Test prompt
        test_prompt = "Tell me a fun fact about artificial intelligence in exactly 2 sentences."
        
        # Generate response
        response = model.generate_content(test_prompt)
        
        print("✅ Gemini Text-to-Text Response:")
        print(f"   {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini Text-to-Text test failed: {e}")
        return False

def test_gemini_menu_extraction():
    """Test Gemini's menu extraction with new JSON structure"""
    print("\n🧪 Testing Gemini Menu Extraction (Text)...")
    
    try:
        # Configure the API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
        
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
        
        # Test menu text
        test_menu = """
        APPETIZERS
        Caesar Salad - Fresh romaine lettuce, parmesan cheese, croutons with house caesar dressing - $12.99
        Buffalo Wings - 10 pieces of crispy chicken wings with buffalo sauce - $14.99
        
        MAIN COURSES
        Grilled Salmon - Fresh Atlantic salmon with lemon butter sauce, served with vegetables - $24.99
        Beef Burger - Angus beef patty with lettuce, tomato, pickles on brioche bun - $16.99
        """
        
        # System prompt for menu extraction
        system_prompt = """
        Extract menu items from the following text and return a JSON array with this structure:
        [
          {
            "name": "Dish name",
            "description": "Brief description or empty string",
            "price": "Price or empty string", 
            "prompt": "Detailed image generation prompt for professional food photography"
          }
        ]
        
        For the image prompt, create appetizing descriptions like:
        "Professional food photography of [dish name]. [Description]. Beautifully plated, soft natural lighting, appetizing presentation."
        
        Return ONLY the JSON array, no markdown formatting or additional text.
        """
        
        # Generate response
        full_prompt = f"{system_prompt}\n\nMenu text:\n{test_menu}"
        response = model.generate_content(full_prompt)
        
        # Clean and parse JSON (using same function as in vision.py)
        def clean_json_response(response_text):
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            elif cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            return cleaned.strip()
        
        # Try to parse JSON
        try:
            cleaned_response = clean_json_response(response.text)
            menu_items = json.loads(cleaned_response)
            print("✅ Gemini Menu Extraction successful!")
            print(f"   Extracted {len(menu_items)} menu items:")
            
            for i, item in enumerate(menu_items, 1):
                print(f"   {i}. {item.get('name', 'Unknown')}")
                if item.get('price'):
                    print(f"      Price: {item['price']}")
                if item.get('description'):
                    print(f"      Description: {item['description']}")
                print(f"      Prompt: {item.get('prompt', 'No prompt')[:100]}...")
                print()
            
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response: {response.text}")
            print(f"Cleaned response: {clean_json_response(response.text)}")
            return False
        
    except Exception as e:
        print(f"❌ Gemini Menu Extraction test failed: {e}")
        return False

def test_gemini_image_to_text():
    """Test Gemini's image-to-text capabilities with example image"""
    print("\n🧪 Testing Gemini Image-to-Text...")
    
    # Look for example images in the examples folder
    image_paths = [
        os.path.join(os.path.dirname(__file__), "example_menu.jpg"),
        os.path.join(os.path.dirname(__file__), "example_menu.jpeg"),
        os.path.join(os.path.dirname(__file__), "example_menu.png"),
        os.path.join(os.path.dirname(__file__), "example.jpg"),
        os.path.join(os.path.dirname(__file__), "example.jpeg"),
        os.path.join(os.path.dirname(__file__), "example.png"),
    ]
    
    image_path = None
    for path in image_paths:
        if os.path.exists(path):
            image_path = path
            break
    
    try:
        # Check if image exists
        if not image_path:
            print(f"❌ No example image found in examples folder")
            print("   Please add an example menu image (example_menu.jpg/png or example.jpg/png)")
            return False
        
        # Configure the API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
        
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
        
        # Load and process the image
        image = Image.open(image_path)
        print(f"   📸 Loaded image: {os.path.basename(image_path)} ({image.size} pixels)")
        
        # Test prompt for image analysis
        prompt = "Describe what you see in this image. Focus on any text, menus, or food items visible."
        
        # Generate response
        response = model.generate_content([prompt, image])
        
        print("✅ Gemini Image-to-Text Response:")
        print(f"   {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini Image-to-Text test failed: {e}")
        return False

def main():
    """Run all Gemini tests"""
    print("🚀 Starting Gemini API Tests...\n")
    
    # Load environment variables from parent directory
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
    
    # Run tests
    tests = [
        ("Text-to-Text", test_gemini_text_to_text),
        ("Menu Extraction", test_gemini_menu_extraction),
        ("Image-to-Text", test_gemini_image_to_text),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        print("-" * 50)
    
    # Summary
    print("\n📊 Test Results Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Gemini tests passed!")
    else:
        print("⚠️  Some tests failed. Please check your API key and configuration.")

if __name__ == "__main__":
    main() 