import os
import json
import google.generativeai as genai

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

def clean_json_response(response_text):
    """
    Clean the response text to extract valid JSON from markdown code blocks or other formatting.
    """
    # Remove common markdown code block formatting
    cleaned = response_text.strip()
    
    # Remove ```json and ``` markers
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]  # Remove ```json
    elif cleaned.startswith('```'):
        cleaned = cleaned[3:]  # Remove ```
    
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]  # Remove closing ```
    
    # Strip any remaining whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def extract_menu_items_from_image(image_data):
    """
    Extracts menu items from an uploaded image using Google Gemini 2.5 Flash Lite.
    
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
        
        genai.configure(api_key=api_key)
        
        # Initialize the model - using Gemini 2.5 Flash Lite
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
        
        # Generate response
        response = model.generate_content([
            SYSTEM_PROMPT,
            image_data
        ])
        
        # Parse the JSON response
        try:
            # Clean the response text to handle markdown formatting
            cleaned_response = clean_json_response(response.text)
            menu_items = json.loads(cleaned_response)
            
            # Validate the structure
            if not isinstance(menu_items, list):
                raise ValueError("Response is not a JSON array")
            
            for item in menu_items:
                required_fields = ['name', 'description', 'price', 'prompt']
                if not all(field in item for field in required_fields):
                    raise ValueError(f"Missing required fields in menu item: {item}")
            
            return menu_items
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text}")
            print(f"Cleaned response: {clean_json_response(response.text)}")
            return []
            
    except Exception as e:
        print(f"Error extracting menu items: {e}")
        return []

def extract_menu_items_from_text(menu_text):
    """
    Extracts menu items from plain text using Google Gemini 2.5 Flash Lite.
    
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
        
        genai.configure(api_key=api_key)
        
        # Initialize the model - using Gemini 2.5 Flash Lite
        model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-06-17')
        
        # Create prompt for text-based menu
        text_prompt = f"""
        {SYSTEM_PROMPT}
        
        Here is the menu text to analyze:
        {menu_text}
        """
        
        # Generate response
        response = model.generate_content(text_prompt)
        
        # Parse the JSON response
        try:
            # Clean the response text to handle markdown formatting
            cleaned_response = clean_json_response(response.text)
            menu_items = json.loads(cleaned_response)
            
            # Validate the structure
            if not isinstance(menu_items, list):
                raise ValueError("Response is not a JSON array")
            
            for item in menu_items:
                required_fields = ['name', 'description', 'price', 'prompt']
                if not all(field in item for field in required_fields):
                    raise ValueError(f"Missing required fields in menu item: {item}")
            
            return menu_items
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response.text}")
            print(f"Cleaned response: {clean_json_response(response.text)}")
            return []
            
    except Exception as e:
        print(f"Error extracting menu items from text: {e}")
        return [] 