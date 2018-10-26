import libtcodpy as libtcod
import math
from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, position_x, position_y, char, color, name, 
                 blocks=False, render_order=RenderOrder.CORPSE, fighter=None, 
                 ai=None):
        """
        Initialise the entity
        """
        self.position_x = position_x
        self.position_y = position_y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

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

    def move_towards(self, target_x, target_y, game_map, entities):
        """

        moves the entity towards a specific target location

        Parameters
        ----------
        self: 
        target_x: 
        target_y: 
        game_map: 
        entities: 

        Returns
        -------

        """   
        dx = target_x - self.position_x
        dy = target_y - self.position_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.position_x + dx, self.position_y + dy) or
                get_blocking_entities_at_location(entities, self.position_x + dx, self.position_y + dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(
                    fov, entity.position_x, entity.position_y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0
        # if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.position_x, self.position_y, target.position_x, target.position_y)

        # Check if the path exists, and in this case, also the path is shorter 
        # than 25 tiles.
        # The path size matters if you want the monster to use alternative 
        # longer paths (for example through other rooms) if for example the 
        # player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters 
        # from running around the map if there's an alternative path really 
        # far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.position_x = x
                self.position_y = y
        else:
            # Keep the old move function as a backup so that if there are 
            # no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.position_x,
                              target.position_y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        """
        calculates the distance to an another entity

        Parameters
        ----------
        self: 
        other: the other entity we want to know the distace to

        Returns
        -------
        Distance to the other entity

        """   
        dx = other.position_x - self.position_x
        dy = other.position_y - self.position_y
        return math.sqrt(dx ** 2 + dy ** 2)

# helper functions outside of class
# TODO: I feel like this could be better places elsewhere?
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
