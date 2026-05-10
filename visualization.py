import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_2d_layout(room_width, room_height, placed_items):
    """
    Generates a 2D floor plan visualization using Matplotlib.
    Returns the Matplotlib figure.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw room boundary
    room_rect = patches.Rectangle((0, 0), room_width, room_height, linewidth=3, edgecolor='black', facecolor='none')
    ax.add_patch(room_rect)
    
    # Colors for different furniture types
    color_map = {
        "Bed": "lightblue",
        "Study Table": "navajowhite",
        "Sofa": "lightcoral",
        "Wardrobe": "sandybrown",
        "TV Unit": "silver",
        "Bookshelf": "plum"
    }

    # Draw placed items
    for item in placed_items:
        name = item['name']
        x, y = item['x'], item['y']
        w, h = item['w'], item['h']
        
        color = color_map.get(name, "lightgreen")
        
        # Add rectangle for furniture
        rect = patches.Rectangle((x, y), w, h, linewidth=1.5, edgecolor='black', facecolor=color, alpha=0.8)
        ax.add_patch(rect)
        
        # Add label
        center_x = x + w / 2
        center_y = y + h / 2
        ax.text(center_x, center_y, name, ha='center', va='center', fontsize=9, weight='bold', color='black')

    # Set axis limits with some padding
    ax.set_xlim(-1, room_width + 1)
    ax.set_ylim(-1, room_height + 1)
    
    # Set grid and labels
    ax.set_xticks(range(0, int(room_width) + 1, 2))
    ax.set_yticks(range(0, int(room_height) + 1, 2))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlabel("Width (ft)")
    ax.set_ylabel("Height (ft)")
    ax.set_title("2D Room Layout", fontsize=14, weight='bold')
    ax.set_aspect('equal')
    
    return fig
