"""
Define command line interface functions.
"""
from core.cave import Cave, Area
from core.wumpus import Wumpus
from core.agent import Hunter
from core.util import ascii_banner


def cli_main_menu():
    """
    Shows command line interface game main menu
    """
    print(ascii_banner())
    while True:
        print('-------------------------')
        print('1 - Play\n2 - Autopilot\n3 - Ranking\n4 - About\n5 - Exit game')
        print('-------------------------')
        options = {
            '1': cli_game,
            '2': cli_autopilot,
            '3': cli_ranking,
            '4': cli_about,
            '5': lambda: None
        }
        option = None
        while option not in options.keys():
            option = input('Choose an valid option.\n> ')

        if option == '5':
            break

        else:
            options[option]()


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


def cli_game():
    """
    A command interface game mode.
    """
    cave = Cave()
    player = Hunter(cave)
    player.set_position(0, 0)
    plays = 0

    while True:
        print('\n-------------------------')
        print(f'Round {plays + 1}')
        print('-------------------------')
        print('Map:')
        print(cave)
        print(f'You are faced to {player.direction.capitalize()}')
        if not player.arrows:
            print(f'You have {player.arrows} arrows\n')
        else:
            print(f'You have {player.arrows} arrow\n')

        plays += 1
        valid_actions = [
            'inspect', 'walk', 'collect',
            'shoot', 'turn left', 'turn right',
            'exit cave', 'exit game',
        ]
        for action in valid_actions:
            print(f'-> {action}')
        
        while True:
            action = input('What you gonna do?\n').lower()
            if action in valid_actions:
                break
            else:
                print('\nInvalid action!\n')

        print('-------------------------\n')

        if action == 'exit game':
            break

        player = action_controller(player, action)
        if not player.is_alive:
            print('You died')
            break

        if player.exited_cave:
            print('You exited the cave...')
            break

    print('-------------------------')
    print(f'Performance: {player.performance}')
    print(f'Rounds played: {plays}')
    print('-------------------------')

    print('Game Over')
    print('-------------------------')


def cli_autopilot():
    print('Not implemented yet')


def cli_ranking():
    print('Not implemented yet')


def cli_about():
    print('Not implemented yet')
