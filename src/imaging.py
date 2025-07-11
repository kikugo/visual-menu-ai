import os
import replicate
import asyncio
import functools
import aiohttp
from typing import Optional, Dict, Any

async def fetch_image_bytes(session, url: str) -> Optional[bytes]:
    """Asynchronously fetches an image from a URL and returns its bytes."""
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.read()
    except aiohttp.ClientError as e:
        print(f"Error fetching image from {url}: {e}")
        return None

async def generate_image_async(menu_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generates an image for a menu item using Replicate's Imagen-4 model.
    
    Args:
        menu_item: Dictionary containing menu item data with 'name', 'description', 'price', and 'prompt'
        
    Returns:
        Dictionary with menu item data plus 'image_bytes' field, or None if generation fails
    """
    try:
        # Configure Replicate API token
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            raise ValueError("Replicate API Token not found. Please set the REPLICATE_API_TOKEN environment variable.")
        
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Extract the prompt from the menu item
        prompt = menu_item.get('prompt', '')
        if not prompt:
            print(f"No prompt found for menu item: {menu_item.get('name', 'Unknown')}")
            return None
        
        # Configure input for Imagen-4
        input_data = {
            "prompt": prompt,
            "aspect_ratio": "1:1",  # Square format works well for food photos
            "safety_filter_level": "block_medium_and_above"
        }
        
        print(f"🎨 Generating image for: {menu_item.get('name', 'Unknown')}")
        
        # Run the model asynchronously
        loop = asyncio.get_event_loop()
        
        # Use run_in_executor to make the synchronous replicate call asynchronous
        def run_replicate():
            return replicate.run("google/imagen-4", input=input_data)
        
        output = await loop.run_in_executor(None, run_replicate)
        
        if output:
            # Fetch the image bytes asynchronously
            async with aiohttp.ClientSession() as session:
                image_bytes = await fetch_image_bytes(session, output)
                
                if image_bytes:
                    # Return the menu item with image data
                    result = menu_item.copy()
                    result['image_bytes'] = image_bytes
                    result['image_url'] = output  # Keep the URL as well for reference
                    print(f"✅ Successfully generated image for: {menu_item.get('name', 'Unknown')}")
                    return result
                else:
                    print(f"❌ Failed to fetch image bytes for: {menu_item.get('name', 'Unknown')}")
                    return None
        else:
            print(f"❌ No output from Imagen-4 for: {menu_item.get('name', 'Unknown')}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating image for {menu_item.get('name', 'Unknown')}: {e}")
        return None

async def generate_images_for_menu(menu_items: list) -> list:
    """
    Generates images for all menu items concurrently.
    
    Args:
        menu_items: List of menu item dictionaries
        
    Returns:
        List of menu items with image data (successful generations only)
    """
    if not menu_items:
        return []
    
    print(f"🚀 Starting image generation for {len(menu_items)} menu items...")
    
    # Create tasks for concurrent image generation
    tasks = [generate_image_async(item) for item in menu_items]
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out None results and exceptions
    successful_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Exception for item {i}: {result}")
        elif result is not None:
            successful_results.append(result)
        else:
            print(f"❌ Failed to generate image for item {i}: {menu_items[i].get('name', 'Unknown')}")
    
    print(f"✅ Successfully generated {len(successful_results)} out of {len(menu_items)} images")
    return successful_results

def test_replicate_connection():
    """
    Test function to verify Replicate API connectivity.
    """
    try:
        api_token = os.getenv('REPLICATE_API_TOKEN')
        if not api_token:
            print("❌ REPLICATE_API_TOKEN not found in environment variables")
            return False
        
        os.environ['REPLICATE_API_TOKEN'] = api_token
        
        # Test with a simple prompt
        test_input = {
            "prompt": "A delicious cheeseburger on a white plate, professional food photography",
            "aspect_ratio": "1:1",
            "safety_filter_level": "block_medium_and_above"
        }
        
        print("🧪 Testing Replicate connection...")
        output = replicate.run("google/imagen-4", input=test_input)
        
        if output:
            print("✅ Replicate API connection successful!")
            return True
        else:
            print("❌ Replicate API returned no output")
            return False
            
    except Exception as e:
        print(f"❌ Replicate API test failed: {e}")
        return False 