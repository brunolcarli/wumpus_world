"""
Define command line interface functions.
"""
from core.cave import Cave, Area
from core.wumpus import Wumpus
from core.agent import Hunter
from core.util import ascii_banner
from core.external_requests import Query, Mutation


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
            option = input('Choose a valid option.\n> ')

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

    # ask to save performance
    cli_register_score(player.performance, plays)

    print('Game Over')
    print('-------------------------')


def cli_autopilot():
    print('Not implemented yet')


def cli_ranking():
    top10 = Query.get_top_10().get('data')
    print('Showing top 10\n')
    print('-------------------------')
    print('NAME PERFORMANCE ROUNDS DATE')
    for score in top10.get('wumpusScores', []):
        name = score.get('playerName')
        performance = score.get('performance')
        rounds = score.get('rounds')
        date = score.get('gameDatetime')
        print(f'{name} {performance} {rounds} {date}')
    print('-------------------------\n')


def cli_register_score(performance, rounds):
    save = input('Do you want to save your performance?\n1 - yes\n2 - no\n> ')
    valid_options = ['yes', 'y', '1']
    if save not in valid_options:
        return

    name = None
    while not name:
        name = input('Insert a valid name!\n> ')

    print('-------------------------\n')
    print('Please wait, connecting withe the server...')
    score = Mutation.register_score(name, performance, rounds).get('data')
    score = score.get('createWumpusScore', {})
    score = score.get('score')
    if score:
        name = score.get('playerName')
        performance = score.get('performance')
        rounds = score.get('rounds')
        date = score.get('gameDatetime')

        print('Registered score:\n')
        print('-------------------------')
        print('NAME PERFORMANCE ROUNDS DATE')
        print(f'{name} {performance} {rounds} {date}')
    else:
        print('No response received from server.')


def cli_about():
    about = '''
    This simple game was developed by an very nice
    brazilian software engineer called Bruno Luvizotto Carli
    (Beelzebruno) while studying contents from his
    specialization in Applied Artificial Intelligence course.

    In this version of the game you are a Hunter who
    enters a dark cave to find a lost sack of gold.
    But the cave hids many dangers as bottomless pits
    and a ferocious (and stinky) Wumpus.

    Your main objective is to find the treasure and exit
    the cave.

    This version was adapted from the content described on the book
    Artificial Intelligence by Stuart Russel and Peter Norvig 3rd ed. (2013).
    The original Wumpus World is a common Aritifial Intelligence problem
    that was first developed by Gregory Yob in 1973 with the name
    Hunt the Wumpus.

    Bruno L. Carli, 2021.
    '''
    print(about)
