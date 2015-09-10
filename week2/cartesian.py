class Point:
    """A coordinate on a Cartesian plane."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        """Calculate the distance between this point and another point."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def quadrant(self):
        """Calculates which quadrant of the Cartesian plane this point is in.

        Crude diagram:

          4  |  1
             |
        -----------
             |
          3  |  2

        For purposes of this calculation, zero counts as a positive number.
        """
        if x >= 0 and y >= 0:
            return 1
        elif x >= 0:
            return 2
        elif y < 0:
            return 3
        else:
            return 4

    def rotate(self, quarters=1):
        """Rotate the point around the center for some number of quarter turns."""
        if quarters is 1:
            return Point(self.y, -self.x)
        else:
            return Point(self.y, -self.x).rotate(quarters - 1)

    def __str__(self):
        """String representation of a point."""
        return "Point({}, {})".format(self.x, self.y)

    def __repr__(self):
        """Representation by Python output."""
        return self.__str__()
