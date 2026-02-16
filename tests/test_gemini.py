#!/usr/bin/env python3
"""
Test script for Google Gemini API using the new google-genai SDK.
Tests both text-to-text and image-to-text capabilities with JSON structured output.
"""

import os
import sys
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_client():
    """Get a configured Gemini client."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return None
    return genai.Client(api_key=api_key)


def test_gemini_text_to_text():
    """Test Gemini's text-to-text capabilities"""
    print("🧪 Testing Gemini Text-to-Text...")

    try:
        client = _get_client()
        if not client:
            return False

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents='Tell me a fun fact about artificial intelligence in exactly 2 sentences.'
        )

        print("✅ Gemini Text-to-Text Response:")
        print(f"   {response.text}")
        return True

    except Exception as e:
        print(f"❌ Gemini Text-to-Text test failed: {e}")
        return False


def test_gemini_menu_extraction():
    """Test Gemini's menu extraction with structured JSON output"""
    print("\n🧪 Testing Gemini Menu Extraction (Text)...")

    try:
        client = _get_client()
        if not client:
            return False

        test_menu = """
        APPETIZERS
        Caesar Salad - Fresh romaine lettuce, parmesan cheese, croutons with house caesar dressing - $12.99
        Buffalo Wings - 10 pieces of crispy chicken wings with buffalo sauce - $14.99
        
        MAIN COURSES
        Grilled Salmon - Fresh Atlantic salmon with lemon butter sauce, served with vegetables - $24.99
        Beef Burger - Angus beef patty with lettuce, tomato, pickles on brioche bun - $16.99
        """

        system_prompt = """
        Extract menu items from the following text and return a JSON array with this structure:
        [
          {
            "name": "Dish name",
            "description": "Brief description or empty string",
            "price": "Price or empty string", 
            "ingredients": ["ingredient1", "ingredient2"],
            "tags": ["tag1", "tag2"],
            "prompt": "Detailed image generation prompt for professional food photography"
          }
        ]
        Return ONLY the JSON array.
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=f"{system_prompt}\n\nMenu text:\n{test_menu}",
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
            )
        )

        menu_items = json.loads(response.text)
        print("✅ Gemini Menu Extraction successful!")
        print(f"   Extracted {len(menu_items)} menu items:")

        for i, item in enumerate(menu_items, 1):
            print(f"   {i}. {item.get('name', 'Unknown')}")
            if item.get('price'):
                print(f"      Price: {item['price']}")
            if item.get('tags'):
                print(f"      Tags: {', '.join(item['tags'])}")
            print()

        return True

    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print(f"Raw response: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Gemini Menu Extraction test failed: {e}")
        return False


def test_gemini_image_to_text():
    """Test Gemini's image-to-text capabilities with example image"""
    print("\n🧪 Testing Gemini Image-to-Text...")

    # Look for example images
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'examples')
    image_extensions = ['jpeg', 'jpg', 'png']
    image_path = None

    for ext in image_extensions:
        for prefix in ['example', 'example_menu']:
            path = os.path.join(examples_dir, f"{prefix}.{ext}")
            if os.path.exists(path):
                image_path = path
                break
        if image_path:
            break

    try:
        if not image_path:
            print("⚠️ No example image found in examples/ folder, skipping")
            return True  # Not a failure, just no image to test

        client = _get_client()
        if not client:
            return False

        image = Image.open(image_path)
        print(f"   📸 Loaded image: {os.path.basename(image_path)} ({image.size} pixels)")

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[
                "Describe what you see in this image. Focus on any text, menus, or food items visible.",
                image
            ]
        )

        print("✅ Gemini Image-to-Text Response:")
        print(f"   {response.text[:300]}...")
        return True

    except Exception as e:
        print(f"❌ Gemini Image-to-Text test failed: {e}")
        return False


def main():
    """Run all Gemini tests"""
    print("🚀 Starting Gemini API Tests...\n")

    # Load environment variables from parent directory
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

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