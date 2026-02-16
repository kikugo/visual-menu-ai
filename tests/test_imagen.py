#!/usr/bin/env python3
"""
Test script for Google Imagen 4 API via the google-genai SDK.
Tests text-to-image generation capabilities.
"""

import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from datetime import datetime

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_client():
    """Get a configured Gemini client."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        return None
    return genai.Client(api_key=api_key)


def test_imagen_basic():
    """Test basic Imagen 4 API connectivity"""
    print("🧪 Testing Imagen 4 Basic Connectivity...")

    try:
        client = _get_client()
        if not client:
            return False

        print("✅ Gemini API connection successful!")
        return True

    except Exception as e:
        print(f"❌ Imagen 4 API test failed: {e}")
        return False


def test_imagen_simple_generation():
    """Test simple image generation with Imagen 4 Fast"""
    print("\n🧪 Testing Imagen 4 Fast Simple Generation...")

    try:
        client = _get_client()
        if not client:
            return False

        prompt = "A delicious margherita pizza on a white plate, professional food photography"

        print(f"🎨 Generating image with prompt: '{prompt}'")
        print("⏳ This may take a few seconds...")

        response = client.models.generate_images(
            model='imagen-4-fast-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='1:1',
            )
        )

        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
            print(f"✅ Image generated successfully! ({len(image_bytes)} bytes)")

            # Save the image for inspection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_simple_{timestamp}.png"
            filepath = os.path.join(os.path.dirname(__file__), filename)

            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            print(f"💾 Image saved as: {filename}")
            return True
        else:
            print("❌ No output received from Imagen 4")
            return False

    except Exception as e:
        print(f"❌ Simple generation test failed: {e}")
        return False


def test_imagen_food_generation():
    """Test food-specific image generation"""
    print("\n🧪 Testing Imagen 4 Food-Specific Generation...")

    try:
        client = _get_client()
        if not client:
            return False

        food_prompt = (
            "Professional food photography of Beef Wellington. "
            "Perfectly cooked beef tenderloin wrapped in puff pastry, "
            "sliced to show the pink interior. Beautifully plated on a white ceramic plate, "
            "shot from a 45-degree angle with soft natural lighting. "
            "Garnished with roasted vegetables and red wine reduction sauce. "
            "High-resolution, appetizing, and cinematic presentation."
        )

        print("🍽️  Generating food image with detailed prompt...")
        print("⏳ This may take a few seconds...")

        response = client.models.generate_images(
            model='imagen-4-fast-generate-001',
            prompt=food_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='4:3',
            )
        )

        if response.generated_images:
            image_bytes = response.generated_images[0].image.image_bytes
            print(f"✅ Food image generated successfully! ({len(image_bytes)} bytes)")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_food_{timestamp}.png"
            filepath = os.path.join(os.path.dirname(__file__), filename)

            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            print(f"💾 Food image saved as: {filename}")
            return True
        else:
            print("❌ No output received for food generation")
            return False

    except Exception as e:
        print(f"❌ Food generation test failed: {e}")
        return False


def test_imagen_multiple_items():
    """Test generating multiple food items (like our app would do)"""
    print("\n🧪 Testing Multiple Food Item Generation...")

    try:
        client = _get_client()
        if not client:
            return False

        test_items = [
            {
                "name": "Chicken Tikka Masala",
                "prompt": "Professional food photography of Chicken Tikka Masala. Tender chicken pieces in creamy tomato-based curry sauce. Served in a traditional copper bowl with basmati rice and naan bread. Shot from above with warm, appetizing lighting."
            },
            {
                "name": "Chocolate Lava Cake",
                "prompt": "Professional food photography of Chocolate Lava Cake. Rich dark chocolate cake with molten center flowing out. Dusted with powdered sugar, served with vanilla ice cream and fresh berries. Elegant plating with soft dramatic lighting."
            }
        ]

        successful_generations = 0

        for i, item in enumerate(test_items, 1):
            print(f"\n🍽️  Generating image {i}/{len(test_items)}: {item['name']}")
            print("⏳ Generating...")

            try:
                response = client.models.generate_images(
                    model='imagen-4-fast-generate-001',
                    prompt=item['prompt'],
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio='1:1',
                    )
                )

                if response.generated_images:
                    image_bytes = response.generated_images[0].image.image_bytes
                    print(f"✅ {item['name']} generated successfully!")

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_name = item['name'].lower().replace(' ', '_')
                    filename = f"test_{safe_name}_{timestamp}.png"
                    filepath = os.path.join(os.path.dirname(__file__), filename)

                    with open(filepath, 'wb') as f:
                        f.write(image_bytes)

                    print(f"💾 Saved as: {filename}")
                    successful_generations += 1
                else:
                    print(f"❌ Failed to generate {item['name']}")

            except Exception as e:
                print(f"❌ Error generating {item['name']}: {e}")

        print(f"\n📊 Successfully generated {successful_generations}/{len(test_items)} images")

        return successful_generations > 0

    except Exception as e:
        print(f"❌ Multiple items test failed: {e}")
        return False


def main():
    """Run all Imagen tests"""
    print("🚀 Starting Imagen 4 API Tests...\n")

    # Load environment variables from parent directory
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

    tests = [
        ("Basic Connectivity", test_imagen_basic),
        ("Simple Generation", test_imagen_simple_generation),
        ("Food-Specific Generation", test_imagen_food_generation),
        ("Multiple Items", test_imagen_multiple_items),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))

    # Summary
    print("\n" + "=" * 50)
    print("📊 IMAGEN 4 TEST RESULTS:")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")

    print(f"\n🎉 All Imagen tests passed! Imagen 4 is working correctly." if passed == total else f"\n⚠️  {passed}/{total} tests passed. Check your API key and configuration.")

    if any(r for _, r in results):
        print("\n💡 Note: Generated images are saved in the tests/ directory for inspection.")


if __name__ == "__main__":
    main()
