import os
from google import genai
from google.genai import types
from typing import Optional, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed


def _get_client():
    """Get or create a Gemini API client."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
    return genai.Client(api_key=api_key)


def generate_image(menu_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generates an image for a menu item using Google Imagen 4 Fast.
    
    Args:
        menu_item: Dictionary containing menu item data with 'name' and 'prompt'
        
    Returns:
        Dictionary with menu item data plus 'image_bytes' field, or None if generation fails
    """
    try:
        client = _get_client()

        # Extract the prompt from the menu item
        prompt = str(menu_item.get('prompt', ''))
        if not prompt:
            print(f"No prompt found for menu item: {menu_item.get('name', 'Unknown')}")
            return None

        print(f"🎨 Generating image for: {menu_item.get('name', 'Unknown')}")

        # Generate image using Imagen 4 Fast
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

            # Return the menu item with image data
            result = menu_item.copy()
            result['image_bytes'] = image_bytes
            print(f"✅ Successfully generated image for: {menu_item.get('name', 'Unknown')}")
            return result

        print(f"❌ Failed to generate image for: {menu_item.get('name', 'Unknown')}")
        return None

    except Exception as e:
        print(f"❌ Error generating image for {menu_item.get('name', 'Unknown')}: {e}")
        return None


def generate_images_for_menu(menu_items: list, on_progress: Optional[Callable] = None) -> list:
    """
    Generates images for all menu items concurrently.
    
    Args:
        menu_items: List of menu item dictionaries
        on_progress: Optional callback called with (completed_count, total_count, item_name) 
                     after each image completes
    
    Returns:
        List of menu item dictionaries with image data
    """
    if not menu_items:
        return []

    total = len(menu_items)
    print(f"🚀 Starting image generation for {total} menu items...")

    successful_results = []
    completed = 0

    # Use ThreadPoolExecutor for concurrent generation
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        future_to_item = {
            executor.submit(generate_image, item): item
            for item in menu_items
        }

        # Collect results as they complete
        for future in as_completed(future_to_item):
            completed += 1
            item = future_to_item[future]
            
            try:
                result = future.result()
                if result:
                    successful_results.append(result)
            except Exception as e:
                print(f"❌ Error generating image for {item.get('name', 'Unknown')}: {e}")

            if on_progress:
                on_progress(completed, total, item.get('name', 'Unknown'))

    print(f"✅ Successfully generated {len(successful_results)} out of {total} images")
    return successful_results