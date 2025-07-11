import streamlit as st
import asyncio
import io
from PIL import Image
from dotenv import load_dotenv

from src.vision import extract_menu_items_from_image, extract_menu_items_from_text
from src.imaging import generate_images_for_menu

# Load environment variables from .env file
load_dotenv()

def initialize_ui():
    """Initializes the Streamlit page configuration and UI elements."""
    st.set_page_config(
        page_title="Menu-Vision AI", 
        page_icon="📸", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("📸 Menu-Vision AI")
    st.markdown("""
    **Transform any menu into a visual feast!** 🍽️
    
    Upload a menu image or paste menu text, and watch as AI creates beautiful, realistic photos for each dish.
    
    • **Powered by**: Gemini 2.5 Flash Lite (OCR) + Google Imagen-4 (Image Generation)
    • **Process**: Menu → Extract Items → Generate Food Photos → Visual Menu
    """)
    
    st.divider()

def display_menu_item(item, col):
    """Display a single menu item in a card format with proper error handling."""
    with col:
        with st.container():
            # Create a styled card
            st.markdown(
                """
                <style>
                .menu-card {
                    border: 1px solid #e0e0e0;
                    border-radius: 10px;
                    padding: 15px;
                    margin: 10px 0;
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .menu-item-name {
                    font-size: 1.2em;
                    font-weight: bold;
                    color: #2e2e2e;
                    margin: 10px 0 5px 0;
                }
                .menu-item-description {
                    font-size: 0.9em;
                    color: #666;
                    margin: 5px 0;
                    font-style: italic;
                }
                .menu-item-price {
                    font-size: 1.1em;
                    font-weight: bold;
                    color: #ff6b35;
                    margin: 5px 0;
                }
                .no-image-placeholder {
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 8px;
                    padding: 40px 20px;
                    text-align: center;
                    color: #666;
                    font-style: italic;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Display image with error handling
            if item.get('image_bytes'):
                try:
                    image = Image.open(io.BytesIO(item['image_bytes']))
                    st.image(image, use_column_width=True, caption="")
                except Exception as e:
                    st.markdown(
                        '<div class="no-image-placeholder">🖼️ Image Error<br><small>Could not load generated image</small></div>',
                        unsafe_allow_html=True
                    )
            else:
                # Placeholder for failed image generation
                st.markdown(
                    '<div class="no-image-placeholder">🎨 Image Generation Failed<br><small>Try regenerating or check API keys</small></div>',
                    unsafe_allow_html=True
                )
            
            # Display item name (required field)
            name = item.get('name', 'Unknown Dish')
            st.markdown(f'<div class="menu-item-name">{name}</div>', unsafe_allow_html=True)
            
            # Display description if available and not empty
            description = item.get('description', '').strip()
            if description:
                st.markdown(f'<div class="menu-item-description">{description}</div>', unsafe_allow_html=True)
            
            # Display price if available and not empty
            price = item.get('price', '').strip()
            if price:
                st.markdown(f'<div class="menu-item-price">{price}</div>', unsafe_allow_html=True)

def display_menu_grid(menu_items_with_images):
    """Display menu items in a responsive grid layout."""
    if not menu_items_with_images:
        st.warning("No menu items to display.")
        return
    
    st.subheader(f"🍽️ Visual Menu ({len(menu_items_with_images)} items)")
    
    # Create responsive columns (2-4 columns based on screen size)
    num_cols = min(3, len(menu_items_with_images))  # Max 3 columns for better readability
    cols = st.columns(num_cols)
    
    for i, item in enumerate(menu_items_with_images):
        col_index = i % num_cols
        display_menu_item(item, cols[col_index])

async def process_menu_async(menu_items):
    """Process menu items and generate images asynchronously with progress tracking."""
    if not menu_items:
        return []
    
    # Generate images for all menu items
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text(f"🎨 Generating images for {len(menu_items)} menu items...")
    progress_bar.progress(25)
    
    try:
        # Use the new generate_images_for_menu function
        menu_items_with_images = await generate_images_for_menu(menu_items)
        
        progress_bar.progress(100)
        
        # Calculate success rate
        success_rate = len(menu_items_with_images) / len(menu_items) * 100 if menu_items else 0
        
        if menu_items_with_images:
            if success_rate == 100:
                status_text.text(f"✅ Generated {len(menu_items_with_images)} images successfully!")
            else:
                status_text.text(f"⚠️ Generated {len(menu_items_with_images)}/{len(menu_items)} images ({success_rate:.0f}% success rate)")
        else:
            status_text.text("❌ Failed to generate any images")
        
        return menu_items_with_images
        
    except Exception as e:
        progress_bar.progress(0)
        status_text.text(f"❌ Error during image generation: {str(e)}")
        st.error("Image generation failed. Please check your API keys and try again.")
        return []

def validate_menu_items(menu_items):
    """Validate extracted menu items and provide user feedback."""
    if not menu_items:
        return False, "No menu items were extracted. Please try a clearer image or check your text format."
    
    # Check for valid items
    valid_items = []
    issues = []
    
    for i, item in enumerate(menu_items, 1):
        if not item.get('name', '').strip():
            issues.append(f"Item {i}: Missing name")
        elif not item.get('prompt', '').strip():
            issues.append(f"Item {i} ({item['name']}): Missing image prompt")
        else:
            valid_items.append(item)
    
    if not valid_items:
        return False, f"No valid menu items found. Issues: {'; '.join(issues)}"
    
    if issues:
        st.warning(f"Some items have issues but will proceed with {len(valid_items)} valid items: {'; '.join(issues)}")
    
    return True, f"Successfully extracted {len(valid_items)} valid menu items!"

def main():
    """Main application function."""
    initialize_ui()
    
    # Check API keys on startup
    import os
    api_status = []
    if not os.getenv('GOOGLE_API_KEY'):
        api_status.append("❌ GOOGLE_API_KEY missing")
    else:
        api_status.append("✅ Gemini API key found")
    
    if not os.getenv('REPLICATE_API_TOKEN'):
        api_status.append("❌ REPLICATE_API_TOKEN missing")
    else:
        api_status.append("✅ Replicate API key found")
    
    if len(api_status) > 0:
        with st.expander("🔑 API Key Status", expanded=False):
            for status in api_status:
                st.text(status)
    
    # Sidebar for input options
    with st.sidebar:
        st.header("📋 Menu Input")
        input_method = st.radio(
            "Choose input method:",
            ["Upload Image", "Paste Text"],
            index=0
        )
        
        menu_items = []
        
        if input_method == "Upload Image":
            st.subheader("📸 Upload Menu Image")
            uploaded_file = st.file_uploader(
                "Choose a menu image...",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a clear image of a restaurant menu"
            )
            
            if uploaded_file is not None:
                try:
                    # Display the uploaded image
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Menu", use_column_width=True)
                    
                    if st.button("🔍 Extract Menu Items", type="primary"):
                        with st.spinner("Extracting menu items from image..."):
                            menu_items = extract_menu_items_from_image(image)
                            
                            # Validate extracted items
                            is_valid, message = validate_menu_items(menu_items)
                            
                            if is_valid:
                                st.success(message)
                                # Store in session state for processing
                                st.session_state['menu_items'] = menu_items
                            else:
                                st.error(message)
                                
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
        
        elif input_method == "Paste Text":
            st.subheader("📝 Menu Text")
            menu_text = st.text_area(
                "Paste your menu text here:",
                height=200,
                placeholder="Example:\nCaesar Salad - Fresh romaine lettuce with parmesan cheese - $12.99\nGrilled Salmon - Atlantic salmon with lemon butter sauce - $18.99"
            )
            
            if st.button("🔍 Extract Menu Items", type="primary"):
                if menu_text.strip():
                    with st.spinner("Extracting menu items from text..."):
                        menu_items = extract_menu_items_from_text(menu_text)
                        
                        # Validate extracted items
                        is_valid, message = validate_menu_items(menu_items)
                        
                        if is_valid:
                            st.success(message)
                            # Store in session state for processing
                            st.session_state['menu_items'] = menu_items
                        else:
                            st.error(message)
                else:
                    st.warning("Please enter some menu text first.")
    
    # Main content area
    if 'menu_items' in st.session_state and st.session_state['menu_items']:
        menu_items = st.session_state['menu_items']
        
        # Show extracted menu items
        with st.expander("📋 Extracted Menu Items", expanded=False):
            for i, item in enumerate(menu_items, 1):
                st.write(f"**{i}. {item.get('name', 'Unknown')}**")
                if item.get('description'):
                    st.write(f"   *{item['description']}*")
                if item.get('price'):
                    st.write(f"   💰 {item['price']}")
                if item.get('prompt'):
                    with st.expander(f"🎨 Image Prompt for {item.get('name', 'Unknown')}", expanded=False):
                        st.write(item['prompt'])
                st.divider()
        
        # Generate images button
        if st.button("🎨 Generate Visual Menu", type="primary", use_container_width=True):
            with st.spinner("Creating beautiful food images..."):
                try:
                    # Run async processing
                    menu_items_with_images = asyncio.run(process_menu_async(menu_items))
                    
                    if menu_items_with_images:
                        # Store results in session state
                        st.session_state['menu_items_with_images'] = menu_items_with_images
                        st.success("🎉 Visual menu created successfully!")
                    else:
                        st.error("Failed to generate any images. Please check your API keys and try again.")
                        
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
    
    # Display visual menu if available
    if 'menu_items_with_images' in st.session_state:
        display_menu_grid(st.session_state['menu_items_with_images'])
        
        # Optional: Download button for results
        if st.session_state['menu_items_with_images']:
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 Clear Results", use_container_width=True):
                    # Clear session state
                    for key in ['menu_items', 'menu_items_with_images']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()

if __name__ == "__main__":
    main() 