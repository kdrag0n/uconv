import collections

from .data import Conversion


def find_shortest_path(graph, start, goal):
    # Create dummy Conversion object for start unit
    start_conv = Conversion(1, start, 1, start)
    # All visited nodes (to avoid cycles)
    visited = set()
    # Paths to be explored
    path_queue = collections.deque([[start_conv]])

    # If we're already at the goal, nothing needs to be done
    if start == goal:
        return []

    # Loop until all possible paths have been traversed
    while path_queue:
        # Get the first path on the queue
        path = path_queue.popleft()
        # Get the last node from the path to visit
        node = path[-1]

        # Visit node if not already visited
        if node not in visited:
            # Go through all neighbors
            neighbors = graph[node.to_unit]
            for neighbor in neighbors:
                # Extend current path with new step (this neighbor)
                new_path = [*path, neighbor]

                # Return current path if it gets us to our goal
                if neighbor.to_unit == goal:
                    # Strip starting unit from path
                    return new_path[1:]

                # Otherwise, save it for further traversal
                path_queue.append(new_path)

            # Mark node as visited
            visited.add(node)

    # If we didn't find any paths
    return None
