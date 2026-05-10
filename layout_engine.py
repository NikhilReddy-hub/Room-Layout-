class LayoutEngine:
    def __init__(self, room_width, room_height):
        self.room_width = room_width
        self.room_height = room_height
        self.furniture_catalog = {
            "Bed": {"width": 6.0, "height": 6.5, "z_height": 2.0},
            "Study Table": {"width": 4.0, "height": 2.0, "z_height": 2.5},
            "Sofa": {"width": 6.0, "height": 3.0, "z_height": 3.0},
            "Wardrobe": {"width": 4.0, "height": 2.0, "z_height": 6.5},
            "TV Unit": {"width": 4.0, "height": 1.5, "z_height": 2.0},
            "Bookshelf": {"width": 3.0, "height": 1.5, "z_height": 6.0}
        }
        self.placed_items = []

    def check_overlap(self, rect1, rect2):
        # rect = (x, y, w, h)
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        
        # Check if one rectangle is on left side of other
        if x1 >= x2 + w2 or x2 >= x1 + w1:
            return False
        # Check if one rectangle is above other
        if y1 >= y2 + h2 or y2 >= y1 + h1:
            return False
            
        return True

    def is_valid_placement(self, x, y, w, h):
        # Check room boundaries
        if x < 0 or y < 0 or x + w > self.room_width or y + h > self.room_height:
            return False
            
        # Check overlaps
        new_rect = (x, y, w, h)
        for item in self.placed_items:
            existing_rect = (item['x'], item['y'], item['w'], item['h'])
            if self.check_overlap(new_rect, existing_rect):
                return False
                
        return True

    def place_furniture(self, item_name):
        if item_name not in self.furniture_catalog:
            return None
            
        w = self.furniture_catalog[item_name]["width"]
        h = self.furniture_catalog[item_name]["height"]
        z = self.furniture_catalog[item_name].get("z_height", 3.0)
        
        # Simple heuristic placement based on item type
        # Step size for scanning
        step = 0.5
        
        # Determine preferred starting positions
        if item_name == "Bed":
            # Preferred: Top-left or Top-right
            start_x, start_y = 0.5, self.room_height - h - 0.5
        elif item_name == "Wardrobe":
            # Preferred: Bottom-left
            start_x, start_y = 0.5, 0.5
        elif item_name == "Study Table":
            # Preferred: Top-right (near a hypothetical window)
            start_x, start_y = self.room_width - w - 0.5, self.room_height - h - 0.5
        elif item_name == "Sofa":
            # Preferred: Center-ish
            start_x, start_y = (self.room_width - w) / 2, 2.0
        elif item_name == "TV Unit":
            # Preferred: Facing sofa
            start_x, start_y = (self.room_width - w) / 2, self.room_height - h - 0.5
        else:
            start_x, start_y = 0.5, 0.5

        # Try to place at preferred, if failed, scan the room
        if self.is_valid_placement(start_x, start_y, w, h):
            self.placed_items.append({"name": item_name, "x": start_x, "y": start_y, "w": w, "h": h, "z": z})
            return True
            
        # Scan the room grid to find an empty spot
        x = 0.5
        while x <= self.room_width - w - 0.5:
            y = 0.5
            while y <= self.room_height - h - 0.5:
                if self.is_valid_placement(x, y, w, h):
                    self.placed_items.append({"name": item_name, "x": x, "y": y, "w": w, "h": h, "z": z})
                    return True
                y += step
            x += step
            
        # Try rotating the furniture if it didn't fit
        x = 0.5
        while x <= self.room_width - h - 0.5:
            y = 0.5
            while y <= self.room_height - w - 0.5:
                if self.is_valid_placement(x, y, h, w):
                    self.placed_items.append({"name": item_name, "x": x, "y": y, "w": h, "h": w, "z": z})
                    return True
                y += step
            x += step

        return False

    def generate_layout(self, selected_furniture):
        # Sort furniture by size (place largest first)
        sorted_furniture = sorted(
            selected_furniture, 
            key=lambda item: self.furniture_catalog.get(item, {"width": 0, "height": 0})["width"] * self.furniture_catalog.get(item, {"width": 0, "height": 0})["height"],
            reverse=True
        )
        
        for item in sorted_furniture:
            self.place_furniture(item)
            
        return self.placed_items

    def calculate_space_utilization(self):
        total_area = self.room_width * self.room_height
        used_area = sum([item['w'] * item['h'] for item in self.placed_items])
        return (used_area / total_area) * 100 if total_area > 0 else 0
