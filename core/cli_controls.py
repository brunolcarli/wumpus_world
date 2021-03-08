"""
Define controls for the agent.
"""


def action_controller(player, action):
    """
    Duck typed function that expects an agent as object and and action as str.
    The agent will execute the action and return is current status.

    param : agent : <Hunter>
    param : action : <str>
    return : <Hunter>
    """
    if action == 'walk':
        print('You walked to the next area!')
        player.walk()

    elif action == 'turn left':
        print('You turned left.')
        player.turn_around('left')

    elif action == 'turn right':
        print('You turned right.')
        player.turn_around('right')

    elif action == 'inspect':
        print('You are inspecting the area around you ....')
        perceptions = player.evaluate_area()
        print('You sent:')
        if not any(perceptions):
            print('Nothig')
        else:
            for perception in perceptions:
                if perception:
                    print(str(perception).capitalize())

    elif action == 'collect':
        player.collect()

    elif action == 'exit cave':
        exit_coords = [0, 0]

        if player.current_position != exit_coords:
            print('Theres no stairs to outside here.')
            print('Move to the entrance to exit the cave.')

        else:
            print('There is a stair leading up to the surface.')
            player.exited_cave = True

    elif action == 'shoot':
        print('You get your bow and then ...')
        player.shoot()

    return player
