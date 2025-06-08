import os
import openai
import base64
from dotenv import load_dotenv
from pathlib import Path
import sys

# Load API keys from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("Missing required OpenAI API key. Please check your .env file.")

# Configuration
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

def validate_image_path(image_path):
    """Validate the image path and file format."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image format. Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
    return path

def encode_image(image_file):
    """Convert image to base64 encoding."""
    if hasattr(image_file, 'getvalue'):  # Streamlit UploadedFile
        return base64.b64encode(image_file.getvalue()).decode('utf-8')
    else:  # Regular file path
        with open(image_file, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_outfit_with_gpt4o(base64_image):
    """
    Use GPT-4 Vision to analyze an outfit from an image
    
    Args:
        base64_image (str): Base64 encoded image string
        
    Returns:
        str: Style analysis and recommendations
        
    Raises:
        Exception: For API or other errors
    """
    try:
        prompt = """
You are a professional fashion stylist. Analyze this outfit and provide:

1. A detailed analysis of the outfit's style and aesthetic
2. Identify the style genre (e.g., streetwear, classic, minimalist)
3. Give 2–3 specific suggestions to elevate the look
4. Recommend 3 shoppable items that would complement this style

Be specific about colors, patterns, and style elements you observe in the image.
"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing outfit: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    try:
        image_path = "images/sample_outfit.jpg"  # Replace with your own image path
        print("👗 Analyzing outfit with GPT-4 Vision...")
        result = analyze_outfit_with_gpt4o(image_path)
        print("\n✨ Style Feedback:\n")
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
