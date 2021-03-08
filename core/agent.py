from core.util import get_perception


class KnowledgeBasedAgent:
    def __init__(self):
        self.kb = []
        self.performance = 0


class Hunter(KnowledgeBasedAgent):
    def __init__(self, cave):
        KnowledgeBasedAgent.__init__(self)
        self.cave = cave
        self.current_position = [0, 0]
        self.direction = 'east'  # deafult to East
        self.valid_directions = ['left', 'right']
        self.is_alive = True
        self.exited_cave = False
        self.arrows = 1

    def set_position(self, x, y):
        area = self.cave.set_agent_position(self, x, y)

        if area.pit:  # agent falls on the pit and dies
            self.performance -= 1000
            self.is_alive = False
            print('You fell deep into a dark pit and died.')

        if area.wumpus:  # agent is eaten by the wumpus
            if area.wumpus.is_alive:
                self.performance -= 1000
                self.is_alive = False
                print('You entered the Wumpus nest.')
                print('Without thinking twice, the ferocious Wumpus devoured you.')

    def turn_around(self, direction):
        """
        Turns the agent 90˚ left or right.
        """
        self.performance -= 1
        if direction not in self.valid_directions:
            print('Invalid action. Agent is standing by without movement.')
            return self.direction

        self.performance -= 1
        if self.direction == 'north':
            if direction == 'right':
                self.direction = 'east'
            else:
                self.direction = 'west'

        elif self.direction == 'south':
            if direction == 'right':
                self.direction = 'west'
            else:
                self.direction = 'east'

        elif self.direction == 'east':
            if direction == 'right':
                self.direction = 'south'
            else:
                self.direction = 'north'

        elif self.direction == 'west':
            if direction == 'right':
                self.direction = 'north'
            else:
                self.direction = 'south'

        print(f'Agent is now faced to {self.direction}')

        return self.direction

    def walk(self):
        self.performance -= 1

        # y moves east and west as long x moves north and south
        controls = {
            'north': lambda x, y: [x-1, y],
            'south': lambda x, y: [x+1, y],
            'east': lambda x, y: [x, y+1],
            'west': lambda x, y: [x, y-1],
        }
        current_x, current_y = self.current_position
        x, y = controls[self.direction](current_x, current_y)

        if x < 0 or y < 0:
            print('There is a wall ahead. You rushed into it and got an impact.')
            return get_perception(self, self.cave, 'impact')

        try:
            self.set_position(x, y)
        except IndexError:
            print('There is a wall ahead. You rushed into it and got an impact.')
            self.set_position(current_x, current_y)
            return get_perception(self, self.cave, 'impact')

        return get_perception(self, self.cave)

    def evaluate_area(self):
        self.performance -= 1
        return get_perception(self, self.cave)

    def get_compass(self):
        """
        Returns the unicode pointing compass arrow for the direction the agent
        is pointing.
        """
        arrows = {
            'north': u'\u21e7',
            'south': u'\u21e9',
            'east': u'\u21e8',
            'west': u'\u21e6'
        }

        return arrows[self.direction]

    def collect(self):
        """
        Collects gold in the area.
        """
        x, y = self.current_position
        if self.cave[x][y].shine:
            print('The shine in this place is a sack of pure gold.')
            print('You collected the gold.')
            self.performance += 1000

        else:
            print('There is nothing here to collect.')
            self.performance -= 1

    def shoot(self):
        """
        Shoots an arrow on player direction.
        Returns a boolean indicating if player succesfully fired the arrow.
        """
        if not self.arrows:
            print('You have no arrows to shoot.')
            self.performance -= 1
            return False

        print('Fired your arrow toward the darkness')
        self.arrows -= 1
        self.performance -= 10

        x, y = self.current_position

        if self.direction == 'north':
            for i in range(self.cave.max_height - 1):
                if self.cave[x-i][y].wumpus:
                    self.cave[x-i][y].wumpus.hit()
                    break

        elif self.direction == 'south':
            for i in range(self.cave.max_height - 1):
                if self.cave[x+i][y].wumpus:
                    self.cave[x+i][y].wumpus.hit()
                    break

        elif self.direction == 'east':
            for i in range(self.cave.max_width - 1):
                if self.cave[x][y+1].wumpus:
                    self.cave[x][y+1].wumpus.hit()
                    break

        elif self.direction == 'west':
            for i in range(self.cave.max_width - 1):
                if self.cave[x][y-1].wumpus:
                    self.cave[x][y-1].wumpus.hit()
                    break
