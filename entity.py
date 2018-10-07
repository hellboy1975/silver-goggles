class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, position_x, position_y, char, color):
        """
        Initialise the entity
        """
        self.position_x = position_x
        self.position_y = position_y
        self.char = char
        self.color = color

    def move(self, direction_x, direction_y):
        """
        Move the entity by a given amount
        """
        self.position_x += direction_x
        self.position_y += direction_y
