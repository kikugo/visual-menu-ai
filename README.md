# Menu-Vision AI

Transform any restaurant menu into a visual feast using the power of AI! Upload a menu image or paste text, and watch as AI creates beautiful, realistic photos for each dish.

![Python](https://img.shields.io/badge/Python-3.8+-green) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)

## Features

- **Smart Menu Reading**: Advanced OCR using Google Gemini 2.5 Flash Lite
- **AI Image Generation**: Beautiful food photos via a model from Black Forest Labs
- **Dual Input Support**: Upload images or paste text menus
- **Structured Extraction**: Name, description, price, and custom prompts
- **Clever Search**: AI-powered search to filter dishes by name, description, and AI-generated tags (e.g., "spicy", "vegetarian").
- **Responsive UI**: Clean, modern interface with error handling

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web interface
- **OCR & Menu Parsing**: [Google Gemini 2.5 Flash Lite](https://deepmind.google/technologies/gemini/)
- **Image Generation**: [Black Forest Labs](https://replicate.com/black-forest-labs) model via [Replicate](https://replicate.com/)
- **Language**: Python 3.8+

## Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd menu_vision_ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY="your_gemini_api_key_here"
REPLICATE_API_TOKEN="your_replicate_api_token_here"
```

**Get your API keys:**
- 🔗 [Google Gemini API Key](https://makersuite.google.com/app/apikey)
- 🔗 [Replicate API Token](https://replicate.com/account/api-tokens)

### 4. Run the Application
```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser and start transforming menus!

## How It Works

1. **Upload/Input**: Choose to upload a menu image or paste menu text
2. **Extract**: Gemini AI reads, structures, and generates tags for the menu items.
3. **Generate**: The image generation model creates professional food photos for each dish.
4. **Display**: View your visual menu in a beautiful responsive grid.
5. **Search**: Use the search bar to filter dishes instantly by name, description, or tags.

### Menu Item Structure
Each extracted item includes:
```json
{
  "name": "Dish name",
  "description": "Brief description", 
  "price": "Price string",
  "tags": ["tag1", "tag2"],
  "prompt": "Custom image generation prompt"
}
```

## Testing

The `tests` folder contains scripts to test the core API integrations independently from the main application.

### Prerequisites

1.  Make sure you have set up your `.env` file in the project root with your API keys.
2.  Ensure all dependencies are installed: `pip install -r requirements.txt`

### Running the Tests

To run the scripts, navigate to the `tests` directory and execute them:

```bash
cd tests

# Test Google Gemini API (OCR and menu extraction)
python test_gemini.py

# Test Replicate API (Image generation)
python test_replicate.py
```

### Expected Results

-   **Gemini Test**: Should show "✅ All Gemini tests passed!"
    -   *Tests*: Basic text generation, menu extraction from text, and menu extraction from an image (if `example.jpeg` or similar is present in examples folder).
-   **Replicate Test**: Should show "✅ All Replicate tests passed!"
    -   *Tests*: API connectivity and generation of several test images. Generated images are saved in the `tests` folder for you to review.

If any tests fail, double-check your API keys in the `.env` file and your internet connection.

## Project Structure

```
menu_vision_ai/
├── app.py                  # Main Streamlit application
├── src/
│   ├── __init__.py        # Makes src a Python package
│   ├── vision.py          # Gemini OCR & menu extraction  
│   └── imaging.py         # Replicate image generation
├── tests/
│   ├── test_gemini.py     # Gemini API tests
│   └── test_replicate.py  # Replicate API tests
├── examples/
│   ├── sample_menu.txt    # Sample menu text for input
│   ├── example.jpeg       # Sample menu images
│   ├── example2.jpeg
│   └── example3.jpeg
├── requirements.txt        # Python dependencies
├── .env                    # API keys (create this yourself)
├── .gitignore              # Git ignore rules
├── LICENSE                 # Project license
└── README.md               # This file
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ Yes |
| `REPLICATE_API_TOKEN` | Replicate API token | ✅ Yes |

### Customization

- **Image Aspect Ratio**: Modify in `src/imaging.py` (default: 1:1 for food photos)
- **Menu Prompt Template**: Update `SYSTEM_PROMPT` in `src/vision.py`
- **UI Layout**: Customize grid columns in `app.py` `display_menu_grid()`

## Troubleshooting

### Common Issues

**"API Key not found"**
- Verify `.env` file exists in project root
- Check API key format and validity

**"Image generation failed"**  
- Confirm Replicate API token is correct
- Check internet connection
- Verify API service status

**"Menu extraction failed"**
- Try a clearer image or better formatted text
- Check Gemini API quota and limits

**PowerShell errors on Windows**
- Use `python -m streamlit run app.py` instead

### Debug Mode
Run tests to isolate issues:
```bash
cd tests
python test_gemini.py    # Test menu extraction
python test_replicate.py # Test image generation
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`) 
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Andrej Karpathy](https://karpathy.bearblog.dev/vibe-coding-menugen/) for the original MenuGen inspiration
- [Nutlope/picMenu](https://github.com/Nutlope/picMenu) for the open-source reference
- Google for the Gemini API
- Black Forest Labs & Replicate for the image generation API

## Future Improvements

We have exciting plans to make Menu-Vision AI even smarter. Future versions may include:

- **Advanced Semantic Search**: Instead of keyword matching, we plan to implement a true semantic search engine. This will allow the application to understand the *meaning* and *context* behind user queries.
  - **How it will work**: By converting both the menu items and the user's query into vector embeddings, the app will be able to find the closest conceptual matches.
  - **User benefit**: You could search for "something hearty for a cold day" and get recommendations for soups or rich pasta dishes, or search for "light and healthy" and get salads and grilled fish.

- **Cuisine Style Detection**: Automatically identify the cuisine type (e.g., Italian, Mexican, Thai) and allow users to filter by it.

- **Interactive Menu Analysis**: Provide aggregated insights from the menu, such as the ratio of vegetarian to non-vegetarian dishes or the most common ingredients.

Stay tuned for more updates! 