import streamlit as st
import os
from layout_engine import LayoutEngine
from ai_recommendation import get_ai_recommendation
from visualization import draw_2d_layout
from visualization_3d import draw_3d_layout

# Page config
st.set_page_config(page_title="AI Room Layout Generator", page_icon="🏠", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1 {
        color: #2e3b4e;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 AI-Powered Parametric Room Layout Generator")
st.markdown("Generate intelligent room layout suggestions based on your room dimensions, style preferences, and furniture choices.")

# Sidebar for Inputs
st.sidebar.header("1. Room Dimensions")
room_width = st.sidebar.number_input("Width (feet)", min_value=8.0, max_value=40.0, value=12.0, step=0.5)
room_height = st.sidebar.number_input("Height (feet)", min_value=8.0, max_value=40.0, value=10.0, step=0.5)

st.sidebar.header("2. Room Details")
room_type = st.sidebar.selectbox("Room Type", ["Bedroom", "Study Room", "Living Room", "Office"])
style = st.sidebar.selectbox("Preferred Style", ["Minimal", "Modern", "Gaming", "Professional", "Cozy"])

st.sidebar.header("3. Furniture Requirements")
available_furniture = ["Bed", "Study Table", "Sofa", "Wardrobe", "TV Unit", "Bookshelf"]
selected_furniture = st.sidebar.multiselect("Select Furniture", available_furniture, default=["Bed", "Wardrobe"])

# Check if API key is already configured (e.g., via Streamlit Community Cloud Secrets)
api_key_configured = os.environ.get("GEMINI_API_KEY") or (hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets)

if not api_key_configured:
    st.sidebar.header("4. AI Settings")
    api_key_input = st.sidebar.text_input("Gemini API Key", type="password", help="Required to get AI recommendations.")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

generate_btn = st.sidebar.button("Generate Layout", type="primary")

# Main Content Area
if generate_btn:
    if not selected_furniture:
        st.warning("Please select at least one piece of furniture.")
    else:
        with st.spinner("Generating Layout & AI Recommendations..."):
            # 1. Parametric Layout Generation
            engine = LayoutEngine(room_width, room_height)
            placed_items = engine.generate_layout(selected_furniture)
            
            # Check for unplaced items
            placed_names = [item['name'] for item in placed_items]
            unplaced = [item for item in selected_furniture if item not in placed_names]
            
            # 2. Layout Summary metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Room Area", f"{room_width * room_height} sq ft")
            col2.metric("Space Utilization", f"{engine.calculate_space_utilization():.1f}%")
            col3.metric("Items Placed", f"{len(placed_items)}/{len(selected_furniture)}")
            
            if unplaced:
                st.error(f"⚠️ Could not fit the following items in the room: {', '.join(unplaced)}")

            # 3. Visualization and AI Recommendations side-by-side
            row1_col1, row1_col2 = st.columns([3, 2])
            
            with row1_col1:
                st.subheader("Room Layout")
                tab1, tab2 = st.tabs(["2D View", "3D View (Interactive)"])
                
                with tab1:
                    fig_2d = draw_2d_layout(room_width, room_height, placed_items)
                    st.pyplot(fig_2d)
                
                with tab2:
                    fig_3d = draw_3d_layout(room_width, room_height, placed_items)
                    st.plotly_chart(fig_3d, use_container_width=True)
                
            with row1_col2:
                st.subheader("✨ AI Recommendations")
                ai_response = get_ai_recommendation(room_width, room_height, room_type, style, selected_furniture)
                st.info(ai_response)
                
                st.subheader("📍 Placement Coordinates")
                for item in placed_items:
                    st.write(f"- **{item['name']}**: x={item['x']}, y={item['y']} (w={item['w']}, h={item['h']})")

else:
    st.info("👈 Enter your preferences in the sidebar and click 'Generate Layout' to start.")
