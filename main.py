from core.cave import Cave, Area
from core.wumpus import Wumpus
from core.agent import Hunter
from core.cli_controls import action_controller


if __name__ == '__main__':
    cave = Cave()
    player = Hunter(cave)
    player.set_position(0, 0)
    plays = 0
    print(cave)

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
