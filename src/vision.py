import os
import json
from google import genai
from google.genai import types

# Enhanced system prompt to guide the AI model in extracting menu items and generating image prompts
SYSTEM_PROMPT = """
You are MenuVisionAI, an expert at reading restaurant menus and creating detailed food imagery prompts.

Your task is to:
1. Analyze the menu image and extract each dish
2. Create a detailed image generation prompt for each dish
3. Return everything in a structured JSON format

For each menu item, extract:
- "name": The exact name of the dish from the menu
- "description": Brief description if available (empty string if none)
- "price": Price as string if available (empty string if none)
- "ingredients": A list of the main ingredients as strings. If none are listed, provide a reasonable guess based on the dish name.
- "tags": A list of relevant tags describing flavor profiles (e.g., spicy, sweet, savory), main ingredients (e.g., chicken, beef, vegetarian), and potential cuisine types (e.g., italian, mexican).
- "prompt": A detailed, appetizing image generation prompt

For the image prompt, create a professional food photography description that includes:
- The dish name and key ingredients/components
- Presentation style (plated, served in bowl, etc.)
- Lighting (soft, natural, studio lighting)
- Camera angle (overhead, 45-degree, close-up)
- Background and styling details
- Adjectives that make the food look appetizing

Example image prompt format:
"Professional food photography of [dish name]. [Description of ingredients and preparation]. Beautifully plated on a white ceramic plate, shot from a 45-degree angle with soft natural lighting. Garnished elegantly, with a clean restaurant background. High-resolution, appetizing, and cinematic presentation."

Return ONLY a valid JSON array in this exact format:
[
  {
    "name": "Dish name",
    "description": "Brief description or empty string",
    "price": "Price or empty string", 
    "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
    "tags": ["flavor_tag", "ingredient_tag", "cuisine_tag"],
    "prompt": "Detailed image generation prompt"
  }
]

Important rules:
- Do NOT include price information in the image prompt
- Focus on making the food look as appetizing as possible
- Use professional food photography terminology
- If no description exists, leave as empty string
- If no price exists, leave as empty string
- Always include proper garnishing and presentation details in prompts
- Return ONLY the JSON array, no markdown formatting or additional text
"""

def extract_menu_items_from_image(image_data):
    """
    Extracts menu items from an uploaded image using Google Gemini 2.5 Flash.
    
    Args:
        image_data: PIL Image object or image bytes
        
    Returns:
        list: List of dictionaries containing name, description, price, and prompt for each menu item
    """
    try:
        # Configure the API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        
        client = genai.Client(api_key=api_key)
        
        # Generate response using Gemini 2.5 Flash with structured JSON output
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[SYSTEM_PROMPT, image_data],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Parse the JSON response
        try:
            menu_items = json.loads(response.text)
            
            # Validate the structure
            if not isinstance(menu_items, list):
                raise ValueError("Response is not a JSON array")
            
            for item in menu_items:
                required_fields = ['name', 'description', 'price', 'ingredients', 'tags', 'prompt']
                if not all(field in item for field in required_fields):
                    raise ValueError(f"Missing required fields in menu item: {item}")
            
            return menu_items
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error extracting menu items: {e}")
        return []

def extract_menu_items_from_text(menu_text):
    """
    Extracts menu items from plain text using Google Gemini 2.5 Flash.
    
    Args:
        menu_text: String containing the menu text
        
    Returns:
        list: List of dictionaries containing name, description, price, and prompt for each menu item
    """
    try:
        # Configure the API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        
        client = genai.Client(api_key=api_key)
        
        # Create prompt for text-based menu
        text_prompt = f"""
        {SYSTEM_PROMPT}
        
        Here is the menu text to analyze:
        {menu_text}
        """
        
        # Generate response using Gemini 2.5 Flash with structured JSON output
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=text_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Parse the JSON response
        try:
            menu_items = json.loads(response.text)
            
            # Validate the structure
            if not isinstance(menu_items, list):
                raise ValueError("Response is not a JSON array")
            
            for item in menu_items:
                required_fields = ['name', 'description', 'price', 'ingredients', 'tags', 'prompt']
                if not all(field in item for field in required_fields):
                    raise ValueError(f"Missing required fields in menu item: {item}")
            
            return menu_items
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text}")
            return []
            
    except Exception as e:
        print(f"Error extracting menu items from text: {e}")
        return [] 