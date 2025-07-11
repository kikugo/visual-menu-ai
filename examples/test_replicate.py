#!/usr/bin/env python3
"""
Test script for Replicate API using Google Imagen-4
Tests text-to-image generation capabilities
"""

import os
import sys
import replicate
from dotenv import load_dotenv
import requests
from datetime import datetime

# Add parent directory to path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_replicate_basic():
    """Test basic Replicate API connectivity"""
    print("🧪 Testing Replicate Basic Connectivity...")
    
    try:
        # Check if API token is available
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            print("❌ REPLICATE_API_TOKEN not found in environment variables")
            return False
        
        # Set the token
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        print("✅ Replicate API connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Replicate API test failed: {e}")
        return False

def test_replicate_simple_generation():
    """Test simple image generation with Imagen-4"""
    print("\n🧪 Testing Imagen-4 Simple Generation...")
    
    try:
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            print("❌ REPLICATE_API_TOKEN not found")
            return False
        
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Simple test prompt
        prompt = "A delicious margherita pizza on a white plate, professional food photography"
        
        print(f"🎨 Generating image with prompt: '{prompt}'")
        print("⏳ This may take 30-60 seconds...")
        
        # Run Imagen-4
        output = replicate.run(
            "google/imagen-4",
            input={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "safety_filter_level": "block_medium_and_above"
            }
        )
        
        if output:
            print("✅ Image generated successfully!")
            print(f"🔗 Image URL: {output}")
            
            # Save the image for inspection
            response = requests.get(output)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_simple_{timestamp}.png"
                filepath = os.path.join(os.path.dirname(__file__), filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"💾 Image saved as: {filename}")
            
            return True
        else:
            print("❌ No output received from Imagen-4")
            return False
            
    except Exception as e:
        print(f"❌ Simple generation test failed: {e}")
        return False

def test_replicate_food_generation():
    """Test food-specific image generation"""
    print("\n🧪 Testing Imagen-4 Food-Specific Generation...")
    
    try:
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            print("❌ REPLICATE_API_TOKEN not found")
            return False
        
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Detailed food prompt
        food_prompt = """
        Professional food photography of Beef Wellington. 
        Perfectly cooked beef tenderloin wrapped in puff pastry, 
        sliced to show the pink interior. Beautifully plated on a white ceramic plate, 
        shot from a 45-degree angle with soft natural lighting. 
        Garnished with roasted vegetables and red wine reduction sauce. 
        High-resolution, appetizing, and cinematic presentation.
        """
        
        print("🍽️  Generating food image with detailed prompt...")
        print("⏳ This may take 30-60 seconds...")
        
        # Run Imagen-4 with food-specific prompt
        output = replicate.run(
            "google/imagen-4",
            input={
                "prompt": food_prompt.strip(),
                "aspect_ratio": "4:3",
                "safety_filter_level": "block_medium_and_above"
            }
        )
        
        if output:
            print("✅ Food image generated successfully!")
            print(f"🔗 Image URL: {output}")
            
            # Save the image
            response = requests.get(output)
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"test_food_{timestamp}.png"
                filepath = os.path.join(os.path.dirname(__file__), filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"💾 Food image saved as: {filename}")
            
            return True
        else:
            print("❌ No output received for food generation")
            return False
            
    except Exception as e:
        print(f"❌ Food generation test failed: {e}")
        return False

def test_replicate_multiple_items():
    """Test generating multiple food items (like our app would do)"""
    print("\n🧪 Testing Multiple Food Item Generation...")
    
    try:
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            print("❌ REPLICATE_API_TOKEN not found")
            return False
        
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Sample menu items with prompts
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
                output = replicate.run(
                    "google/imagen-4",
                    input={
                        "prompt": item['prompt'],
                        "aspect_ratio": "1:1",
                        "safety_filter_level": "block_medium_and_above"
                    }
                )
                
                if output:
                    print(f"✅ {item['name']} generated successfully!")
                    
                    # Save the image
                    response = requests.get(output)
                    if response.status_code == 200:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        safe_name = item['name'].lower().replace(' ', '_')
                        filename = f"test_{safe_name}_{timestamp}.png"
                        filepath = os.path.join(os.path.dirname(__file__), filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
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
    """Run all Replicate tests"""
    print("🚀 Starting Replicate API Tests...\n")
    
    # Load environment variables from parent directory
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
    
    # Run tests
    tests = [
        ("Basic Connectivity", test_replicate_basic),
        ("Simple Generation", test_replicate_simple_generation),
        ("Food-Specific Generation", test_replicate_food_generation),
        ("Multiple Items", test_replicate_multiple_items),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 REPLICATE TEST RESULTS:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\n🎉 All Replicate tests passed! Imagen-4 is working correctly." if passed == total else f"\n⚠️  {passed}/{total} tests passed. Check your API key and configuration.")
    
    if any(results):
        print("\n💡 Note: Generated images are saved in the examples/ directory for inspection.")

if __name__ == "__main__":
    main() 