class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, position_x, position_y, char, color, name, blocks=False):
        """
        Initialise the entity
        """
        self.position_x = position_x
        self.position_y = position_y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, direction_x, direction_y):
        """
        Move the entity by a given amount

        Parameters
        ----------
        self: 
        direction_x: the direction for the entity to move on the x axis
        direction_y: the direction for the entity to move on the y axis

        Returns
        -------
        Nothing!

        """
        self.position_x += direction_x
        self.position_y += direction_y

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    """
    check for a blocking entity

    Parameters
    ----------
        entities (library) a library of entities
        destination_x (int) the x coortdinate the entity is trying to move to
        destination_y (int) the y coortdinate the entity is trying to move to
    """
    for entity in entities:
        if entity.blocks and entity.position_x == destination_x and entity.position_y == destination_y:
            return entity

    return None
