import tcod as libtcod
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all

def main():
    """
    The main game process
    """

    # these variables will define the dimensions of the console and map
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    # configure the number of rooms per map and their sizes
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    # set the colours for the map blocks
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # create entity objects for the player and an NPC, then poke them in
    # an array
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)
    entities = [npc, player]

    # set the default font and colour values for the console
    libtcod.console_set_custom_font(
        'arial10x10.png',
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    # move the console into a variable so that we can manipulate it a bit better
    con = libtcod.console_new(screen_width, screen_height)

    # create the object which contains the map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size,
                      map_width, map_height, player)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    # listen for the most recent Keyboard and Mouse events
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # main game loop, will continue looping until some action closes the window
    while not libtcod.console_is_window_closed():
        # check to see which events were received from the inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        # compute the field of view values for the player
        if fov_recompute:
            recompute_fov(fov_map, player.position_x, player.position_y, fov_radius,
                          fov_light_walls, fov_algorithm)

        # main rendering command - calculates and paints the various elements 
        # appearing in the console
        render_all(con, entities, game_map, fov_map, fov_recompute,
                   screen_width, screen_height, colors)

        fov_recompute = False

        # flush the contents of the console to the screen
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.position_x + dx, player.position_y + dy):
                player.move(dx, dy)

                fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__': 
    main()
