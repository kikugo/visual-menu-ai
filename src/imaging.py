import os
import replicate
import requests
from typing import Optional, Dict, Any

def fetch_image_bytes(url: str) -> Optional[bytes]:
    """Synchronously fetches an image from a URL and returns its bytes."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from {url}: {e}")
        return None

def generate_image(menu_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generates an image for a menu item using Replicate's flux-schnell model.
    
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
        
        # Create Replicate client
        client = replicate.Client(api_token=api_token)
        
        # Extract the prompt from the menu item and ensure it's a string
        prompt = str(menu_item.get('prompt', ''))
        if not prompt:
            print(f"No prompt found for menu item: {menu_item.get('name', 'Unknown')}")
            return None
        
        # Configure input for flux-schnell
        input_data = {
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "num_outputs": 1,
            "go_fast": True,
            "output_format": "webp",
            "output_quality": 80
        }
        
        print(f"🎨 Generating image for: {menu_item.get('name', 'Unknown')}")
        
        # Run the model synchronously
        output = client.run("black-forest-labs/flux-schnell", input=input_data)
        
        if output and len(output) > 0:
            url = output[0]
            image_bytes = fetch_image_bytes(url)
            
            if image_bytes:
                # Return the menu item with image data
                result = menu_item.copy()
                result['image_bytes'] = image_bytes
                result['image_url'] = url
                print(f"✅ Successfully generated image for: {menu_item.get('name', 'Unknown')}")
                return result
        
        print(f"❌ Failed to generate or fetch image for: {menu_item.get('name', 'Unknown')}")
        return None
            
    except replicate.exceptions.ReplicateError as e:
        if e.status == 402:
            print(f"❌ Billing required for {menu_item.get('name', 'Unknown')}: Please set up billing on Replicate.")
        else:
            print(f"❌ Replicate error for {menu_item.get('name', 'Unknown')}: {e}")
        return None
    except Exception as e:
        print(f"❌ Error generating image for {menu_item.get('name', 'Unknown')}: {e}")
        return None

def generate_images_for_menu(menu_items: list) -> list:
    """
    Generates images for all menu items sequentially.
    """
    if not menu_items:
        return []
    
    print(f"🚀 Starting image generation for {len(menu_items)} menu items...")
    
    successful_results = []
    for item in menu_items:
        result = generate_image(item)
        if result:
            successful_results.append(result)
    
    print(f"✅ Successfully generated {len(successful_results)} out of {len(menu_items)} images")
    return successful_results 