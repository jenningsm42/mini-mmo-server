from collections import defaultdict


class PlayerCollection:
    class GridElement:
        def __init__(self, client, position):
            self.client = client
            self.position = position

        def __hash__(self):
            return hash(self.client)

        def __eq__(self, other):
            # Clients are unique in the grid, no need to check the position
            return (other is not None and
                    self.client == other.client)

    def __init__(self):
        self.cell_size = 100
        self.players = {}
        self.grid = defaultdict(set)

    def get_coords(self, position):
        x = int(position[0] / self.cell_size)
        y = int(position[1] / self.cell_size)
        return x, y

    def add(self, client, position):
        self.players[client] = position
        coords = self.get_coords(position)
        self.grid[coords].add(PlayerCollection.GridElement(client, position))

    def remove(self, client):
        position = self.players.get(client)
        if not position:
            return

        coords = self.get_coords(position)
        self.grid[coords].remove(PlayerCollection.GridElement(client, position))

    def update_position(self, client, position):
        old_position = self.players[client]
        old_coords = self.get_coords(old_position)
        new_coords = self.get_coords(position)

        self.players[client] = position

        self.grid[old_coords].remove(PlayerCollection.GridElement(client, old_position))

        new_grid_element = PlayerCollection.GridElement(client, position)

        if old_coords != new_coords:
            self.grid[new_coords].add(new_grid_element)
        else:
            self.grid[old_coords].add(new_grid_element)

    def get_players_in_range(self, center, radius):
        top_left_coords = self.get_coords((center[0] - radius, center[1] - radius))
        bottom_right_coords = self.get_coords((center[0] + radius, center[1] + radius))

        range_squared = radius * radius
        clients = []

        for x in range(top_left_coords[0], bottom_right_coords[0] + 1):
            for y in range(top_left_coords[1], bottom_right_coords[1] + 1):
                for entity in self.grid[x, y]:
                    p = entity.position
                    dx = p[0] - center[0]
                    dy = p[1] - center[1]
                    distance_squared = dx * dx + dy * dy
                    if distance_squared <= range_squared:
                        clients.append(entity.client)

        return clients
