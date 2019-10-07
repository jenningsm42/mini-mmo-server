from collections import defaultdict
from datetime import datetime

from .util.vector import Vector


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

    def __init__(self, server_map):
        self.cell_size = 100
        self.characters = {}
        self.grid = defaultdict(set)
        self.map = server_map

    def __iter__(self):
        return iter(self.characters.items())

    def get_coords(self, position):
        return position // self.cell_size

    def add(self, client, character):
        self.characters[client] = character
        coords = self.get_coords(character.last_position)
        self.grid[coords].add(PlayerCollection.GridElement(
            client, character.last_position))

    def remove(self, client):
        character = self.characters.pop(client)
        if not character:
            return

        coords = self.get_coords(character.last_position)
        self.grid[coords].remove(PlayerCollection.GridElement(
            client, character.last_position))

    def update_character(self, client, character):
        old_character = self.characters[client]

        if old_character.last_position != character.last_position:
            self.update_position(client, character.last_position)

        self.characters[client] = character

    def update_all_positions(self):
        now = datetime.now()
        for client in self.characters.keys():
            self.update_position(client, now=now)

    def update_position(self, client, position=None, now=None):
        character = self.characters[client]
        old_position = character.last_position

        if not position:
            # Update position with collision resolution if not given
            character.update_position(self.map, now)
            position = character.last_position

        if position == old_position:
            return

        # Update character grid if necessary
        old_coords = self.get_coords(old_position)
        new_coords = self.get_coords(position)

        self.characters[client].set_position(position)

        self.grid[old_coords].remove(PlayerCollection.GridElement(
            client, old_position))

        new_grid_element = PlayerCollection.GridElement(client, position)

        if old_coords != new_coords:
            self.grid[new_coords].add(new_grid_element)
        else:
            self.grid[old_coords].add(new_grid_element)

    def get_clients_in_range(self, center, radius):
        top_left_coords = self.get_coords(
            center - Vector(radius, radius))
        bottom_right_coords = self.get_coords(
            center + Vector(radius, radius))

        range_squared = radius * radius
        clients = []

        for x in range(top_left_coords.x, bottom_right_coords.x + 1):
            for y in range(top_left_coords.y, bottom_right_coords.y + 1):
                for entity in self.grid[Vector(x, y)]:
                    p = entity.position
                    dx = p.x - center.x
                    dy = p.y - center.y
                    distance_squared = dx * dx + dy * dy
                    if distance_squared <= range_squared:
                        clients.append(entity.client)

        return clients
