from timeline.basics import *
from core.geometry import *

def calculate_min_distance(box1, box2, direction):
    """Calculate the minimum distance between two boxes"""
    if direction == "vertical":
        if box1.bottom < box2.top:
            distance = box2.top - box1.bottom
        elif box2.bottom < box1.top:
            distance = box1.top - box2.bottom
        else:
            distance = 0    
    if direction == "horizontal":
        if box1.right < box2.left:
            distance = box2.left - box1.right
        elif box2.right < box1.left:
            distance = box1.left - box2.right
        else:
            distance = 0
    return distance

def resolve_cross_level1_overlaps(placed_nodes, step_x, step_y, direction):
    """Resolve overlaps between different level=1 parent nodes"""
    while True:
        overlap_found = False
        for id1, data1 in placed_nodes.items():
            node1 = data1["node"]
            if node1.level < 2:
                continue  # Only handle nodes of level=2 and above

            for id2, data2 in placed_nodes.items():
                node2 = data2["node"]
                level1_parent_1 = node1.find_parent(1)
                level1_parent_2 = node2.find_parent(1)
                if node2.level < 2 or id1 == id2:
                    continue  # Skip the same node
                if node1.is_direction != node2.is_direction:
                    continue  # Skip nodes with different direction
                if level1_parent_1 == level1_parent_2:
                    continue  # Skip nodes with same level=1 parent

                if node1.shape.is_overlapping(node2.shape) or \
                    calculate_min_distance(node1.shape, node2.shape, direction) < 2 * DETAIL_SPACING:
                    # Different level=1 parents; move the one ranked lower
                    overlap_found = True
                    # Determine the starting node to shift to the right
                    if level1_parent_1.id > level1_parent_2.id:
                        start_level1 = level1_parent_1
                    else:
                        start_level1 = level1_parent_2
                    # Move all subsequent level=1 nodes starting from start_level1
                    for id, data in placed_nodes.items():
                        node = data["node"]
                        if node.level == 1 and node.id >= start_level1.id:
                            shift_subtree(node, step_x, step_y)
                    break
            if overlap_found:
                break
        if not overlap_found:
            break  # Exit loop if no overlaps found

def resolve_within_level1_overlaps(placed_nodes, step_x, step_y, direction):
    """Resolve overlaps within the same level=1 parent nodes"""
    while True:
        overlap_found = False
        for id1, data1 in placed_nodes.items():
            node1 = data1["node"]
            if node1.level < 2:
                continue  # Only handle nodes of level=2 and above

            for id2, data2 in placed_nodes.items():
                node2 = data2["node"]
                if node2.level < 2 or id1 == id2:
                    continue  # Skip the same node
                
                if node1.shape.is_overlapping(node2.shape):
                    level1_parent_1 = node1.find_parent(1)
                    level1_parent_2 = node2.find_parent(1)

                    if level1_parent_1 == level1_parent_2:
                        # Same level=1 parent; move the one ranked lower
                        overlap_found = True
                        # Determine the starting node to shift upward
                        if node1.id > node2.id:
                            start_level2 = node1.find_parent(2)
                        else:
                            start_level2 = node2.find_parent(2)
                        # Move all subsequent level=2 nodes starting from start_level2
                        for id, data in placed_nodes.items():
                            node = data["node"]
                            factor_x = 1
                            factor_y = 1
                            level1_parent_3 = node.find_parent(1)
                            if level1_parent_3 != level1_parent_1:  
                                continue
                            if node.level == 2 and node.id >= start_level2.id:
                                if direction == "vertical":
                                    if node.is_direction:
                                       factor_x = -1
                                elif direction == "horizontal":
                                    if node.is_direction:
                                        factor_y = -1
                                shift_subtree(node, factor_x * step_x, factor_y * step_y)
                        break
            if overlap_found:
                break
        if not overlap_found:
            break  # Exit loop if no overlaps found