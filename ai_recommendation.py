import google.generativeai as genai
import os

def get_ai_recommendation(room_width, room_height, room_type, style, furniture_list):
    """
    Calls the Google Gemini API to generate personalized room layout and styling recommendations.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Gemini API Key not found. Please set the GEMINI_API_KEY environment variable or enter it in the sidebar to get AI recommendations."

    try:
        genai.configure(api_key=api_key)
        # Dynamically find a supported model to avoid 404 errors
        supported_model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                supported_model = m.name
                if 'flash' in m.name:  # Prefer faster flash models if available
                    break
                    
        if not supported_model:
            return "Error: No text generation models are available for this API key."
            
        model = genai.GenerativeModel(supported_model)
        furniture_str = ", ".join(furniture_list) if furniture_list else "None"
        
        prompt = f"""
        You are an expert interior designer. I am designing a room with the following parameters:
        - Room Size: {room_width} ft x {room_height} ft
        - Room Type: {room_type}
        - Preferred Style: {style}
        - Selected Furniture: {furniture_str}
        
        Provide a short (3-4 sentences), highly actionable design and layout recommendation. 
        Focus on space optimization, color themes that fit the '{style}' style, and practical placement tips for the selected furniture.
        Do not use markdown formatting, just return plain text.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"Error generating AI recommendation: {str(e)}"
