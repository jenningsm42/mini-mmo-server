class AABB:
    def __init__(self, x, y, w, h):
        self.left = x
        self.top = y
        self.width = w
        self.height = h

    def __repr__(self):
        return (f'<AABB left={self.left} top={self.top} ' +
                f'w={self.width} h={self.height}>')

    def intersects(self, aabb):
        return not (
            self.left + self.width <= aabb.left or
            self.top + self.height <= aabb.top or
            self.left >= aabb.left + aabb.width or
            self.top >= aabb.top + aabb.height)
