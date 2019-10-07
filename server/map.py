from os import listdir
from os.path import isfile, join
import logging
import re

import yaml

from .util.aabb import AABB
from .util.vector import Vector

logger = logging.getLogger(__name__)

CHUNK_FILE_REGEX = re.compile('chunk_(-?\d+)_(-?\d+).ya?ml')
CHUNK_WIDTH = 8192


class MapObject:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class MapChunk:
    class MapChunkObject:
        def __init__(self, object_id, x, y):
            self.object_id = object_id
            self.x = x
            self.y = y

    def __init__(self):
        self.objects = []

    def __iter__(self):
        return iter(self.objects)

    def add_object(self, object_id, x, y):
        self.objects.append(MapChunk.MapChunkObject(object_id, x, y))


class Map:
    def __init__(self, chunks_directory, objects_path):
        self.chunks_directory = chunks_directory
        self.objects_path = objects_path

        # Objects maps object id to MapObject
        self.objects = {}

        # Chunks maps chunk coordinates to MapChunk
        self.chunks = {}

        self.load_objects()
        self.load_chunks()

    def load_objects(self):
        with open(self.objects_path) as objects_file:
            objects_data = yaml.safe_load(objects_file)

        for object_id, object_info in objects_data.items():
            self.objects[object_id] = MapObject(
                object_info['aabb_width'],
                object_info['aabb_height'])

    def load_chunks(self):
        chunk_paths = [path for path in listdir(self.chunks_directory)
                       if isfile(join(self.chunks_directory, path))]

        for path in chunk_paths:
            match = CHUNK_FILE_REGEX.match(path)
            if not match:
                logger.warn('Found extra file in map folder: %r', path)
                continue

            groups = match.groups()
            chunk_id = (int(groups[0]), int(groups[1]))

            with open(join(self.chunks_directory, path)) as chunk_file:
                chunk_data = yaml.safe_load(chunk_file)

            chunk = MapChunk()
            for object_info in chunk_data:
                chunk.add_object(
                    int(object_info['id']),
                    int(object_info['x']),
                    int(object_info['y']))

            self.chunks[chunk_id] = chunk

    def get_chunk_coordinates(self, position):
        ''' Returns chunk coordinates from world coordinates '''
        return position // CHUNK_WIDTH

    def handle_collision(self, old_position, velocity, aabb):
        ''' Returns the correct position of the entity after accounting
            for collision detection '''
        # Get surrounding chunks of entity
        center_chunk_id = self.get_chunk_coordinates(old_position)

        chunk_coordinates = [
            (center_chunk_id.x - 1, center_chunk_id.y - 1),
            (center_chunk_id.x - 1, center_chunk_id.y),
            (center_chunk_id.x - 1, center_chunk_id.y + 1),

            (center_chunk_id.x, center_chunk_id.y - 1),
            (center_chunk_id.x, center_chunk_id.y),
            (center_chunk_id.x, center_chunk_id.y + 1),

            (center_chunk_id.x + 1, center_chunk_id.y - 1),
            (center_chunk_id.x + 1, center_chunk_id.y),
            (center_chunk_id.x + 1, center_chunk_id.y + 1),
        ]

        # Cache AABBs of potential colliders
        worldAABBs = []
        for coordinates in chunk_coordinates:
            chunk = self.chunks.get(coordinates)
            if not chunk:
                continue

            # TODO: Replace with quadtree per chunk
            for map_object in chunk:
                worldAABBs.append(AABB(
                    map_object.x,
                    map_object.y - self.objects[map_object.object_id].height,
                    self.objects[map_object.object_id].width,
                    self.objects[map_object.object_id].height))

        # Save difference between bounding box and position
        bounding_box_difference = Vector(
            old_position.x - aabb.left,
            old_position.y - aabb.top)

        # Test horizontal collision
        aabb.left += velocity.x

        for worldBoundingBox in worldAABBs:
            if aabb.intersects(worldBoundingBox):
                if velocity.x > 0:
                    aabb.left = worldBoundingBox.left - aabb.width
                else:
                    aabb.left = worldBoundingBox.left + worldBoundingBox.width

        # Test vertical collision
        aabb.top += velocity.y

        for worldBoundingBox in worldAABBs:
            if aabb.intersects(worldBoundingBox):
                if velocity.y > 0:
                    aabb.top = worldBoundingBox.top - aabb.height
                else:
                    aabb.top = worldBoundingBox.top + worldBoundingBox.height

        return Vector(aabb.left + bounding_box_difference.x,
                      aabb.top + bounding_box_difference.y)
