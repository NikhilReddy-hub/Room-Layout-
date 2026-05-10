import plotly.graph_objects as go
import numpy as np

def draw_3d_layout(room_width, room_height, placed_items):
    """
    Generates an interactive 3D floor plan visualization using Plotly.
    Returns the Plotly Figure object.
    """
    fig = go.Figure()

    # Room floor boundaries
    room_x = [0, room_width, room_width, 0]
    room_y = [0, 0, room_height, room_height]
    room_z = [0, 0, 0, 0]

    # Add the floor
    fig.add_trace(go.Mesh3d(
        x=room_x,
        y=room_y,
        z=room_z,
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color='lightgrey',
        opacity=0.5,
        name='Floor',
        hoverinfo='skip'
    ))

    # Colors for different furniture types
    color_map = {
        "Bed": "lightblue",
        "Study Table": "navajowhite",
        "Sofa": "lightcoral",
        "Wardrobe": "sandybrown",
        "TV Unit": "silver",
        "Bookshelf": "plum"
    }

    # Draw each piece of furniture as a 3D box
    for item in placed_items:
        name = item['name']
        x, y = item['x'], item['y']
        w, d = item['w'], item['h']
        z_h = item['z']
        
        color = color_map.get(name, "lightgreen")
        
        # 8 vertices of a box
        # 0-3: bottom face, 4-7: top face
        box_x = [x, x+w, x+w, x,   x, x+w, x+w, x]
        box_y = [y, y, y+d, y+d,   y, y, y+d, y+d]
        box_z = [0, 0, 0, 0,       z_h, z_h, z_h, z_h]
        
        # 12 triangles forming the 6 faces
        # i, j, k define the vertices of each triangle
        i = [0, 0, 4, 4, 0, 0, 3, 3, 0, 0, 1, 1]
        j = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 2, 6]
        k = [2, 3, 6, 7, 5, 4, 6, 7, 7, 4, 6, 5]
        
        fig.add_trace(go.Mesh3d(
            x=box_x, y=box_y, z=box_z,
            i=i, j=j, k=k,
            color=color,
            opacity=0.9,
            name=name,
            text=name,
            hoverinfo='text'
        ))

    # Configure the layout and 3D scene
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='Width (ft)', range=[0, room_width]),
            yaxis=dict(title='Depth (ft)', range=[0, room_height]),
            zaxis=dict(title='Height (ft)', range=[0, 10]),
            aspectmode='data' # Ensures equal scaling for x, y, z
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig
