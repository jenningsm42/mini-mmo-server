class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'<Vector({self.x}, {self.y})>'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        return Vector(int(self.x // scalar), int(self.y // scalar))

    def distance_squared(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def is_zero(self, dead_zone=0.001):
        ''' Returns true if either x or y is less than the dead zone '''
        return abs(self.x) < dead_zone and abs(self.y) < dead_zone

    def clear_zero_values(self, dead_zone=0.001):
        ''' Sets values less than the dead zone to zero '''
        if abs(self.x) < dead_zone:
            self.x = 0

        if abs(self.y) < dead_zone:
            self.y = 0

    def copy(self):
        return Vector(self.x, self.y)
