# AI-Powered Parametric Room Layout Generator

An AI-powered parametric design system that generates intelligent room layout suggestions based on user-defined parameters such as room size, room type, furniture requirements, and preferred design style. It combines rule-based spatial logic with Generative AI (Google Gemini) to produce optimized room arrangement recommendations.

## Features
- **User Input System**: Enter dimensions, room type, style, and select furniture.
- **Parametric Layout Engine**: Rule-based system for non-overlapping spatial placement.
- **AI Recommendation Engine**: Context-aware suggestions using Google Gemini API.
- **2D Room Visualization**: Real-time rendering of the floor plan using Matplotlib.

## Installation

1. Clone or download this project.
2. Navigate to the `ai-room-layout-generator` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Get a Google Gemini API Key from Google AI Studio.
5. Set the API key as an environment variable or input it directly in the Streamlit app sidebar.
   ```bash
   # Windows (Powershell)
   $env:GEMINI_API_KEY="your_api_key_here"
   ```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to use the generator.
