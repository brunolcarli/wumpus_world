from random import randint
from core.wumpus import Wumpus

class Area:
    """
    Defines states of an specific area of the cave.
    """
    def __init__(self, coord):
        self.coord = coord
        self.stink = None
        self.breeze = None
        self.pit = None
        self.wumpus = None
        self.shine = None
        self.explored = None
        self.agent = None
        self.state = None

    def __str__(self):
        return self.agent.get_compass() if self.agent else '?'


class Cave:
    def __init__(self, max_height=4, max_width=4):
        self.max_height = max_height
        self.max_width = max_width
        self._map = self.build()

        # Initialize pits and wumpus
        self.init_pit_position()
        self.init_wumpus_position()

    def build(self):
        """
        Init the cave.
        """
        return [[Area([x, y]) for y in range(self.max_width)] for x in range(self.max_height)]

    def __str__(self):
        image = '\n'
        for row in self._map:
            image += ' '.join(str(i) for i in row)
            image+= '\n'
        return image

    def __getitem__(self, index):
        return self._map.__getitem__(index)

    def __delitem__(self, index):
        self._map.__delitem__(index )

    def insert(self, index, value):
        self._map.insert(index, value)

    def __setitem__(self, index, value):
        self._map.__setitem__(index, value)

    def __getitem__(self, index):
        return self._map.__getitem__(index)

    def set_agent_position(self, agent, x, y):
        current_x, current_y = agent.current_position
        self._map[current_x][current_y].agent = None
        self._map[x][y].agent = agent
        agent.current_position = [x, y]

        return self._map[x][y]

    def init_pit_position(self):
        pits_coords = []

        while len(pits_coords) < 3:
            x, y = randint(0, self.max_height-1), randint(0, self.max_width-1)
            if [x, y] != [0, 0]:
                pits_coords.append([x, y])

        for pit in pits_coords:
            x, y = pit
            self._map[x][y].__setattr__('pit', 'pit')

            # set breeze positions based on pit location
            if x == 0:
                self._map[x+1][y].breeze = 'breeze'

            elif x == self.max_height - 1:
                self._map[x-1][y].breeze = 'breeze'

            else:
                self._map[x+1][y].breeze = 'breeze'
                self._map[x-1][y].breeze = 'breeze'

            if y == 0:
                self._map[x][y+1].breeze = 'breeze'

            elif y == self.max_width - 1:
                self._map[x][y-1].breeze = 'breeze'

            else:
                self._map[x][y+1].breeze = 'breeze'
                self._map[x][y-1].breeze = 'breeze'

    def init_wumpus_position(self):
        wumpus = Wumpus()
        wumpus_coords = None

        while not wumpus_coords:
            x, y = randint(0, self.max_height-1), randint(0, self.max_width-1)
            area = self._map[x][y]

            if not area.pit:
                wumpus_coords = [x, y]
                break

        x, y = wumpus_coords
        self._map[x][y].__setattr__('wumpus', wumpus)

        # set wumpus stinky smell positions based on wumpus location
        if x == 0:
            self._map[x+1][y].stink = 'stink'

        elif x == self.max_height - 1:
            self._map[x-1][y].stink = 'stink'

        else:
            self._map[x+1][y].stink = 'stink'
            self._map[x-1][y].stink = 'stink'

        if y == 0:
            self._map[x][y+1].stink = 'stink'

        elif y == self.max_width - 1:
            self._map[x][y-1].stink = 'stink'

        else:
            self._map[x][y+1].stink = 'stink'
            self._map[x][y-1].stink = 'stink'

    def init_gold_position(self):
        goold_coords = None

        while not gold_coords:
            x, y = randint(0, self.max_height-1), randint(0, self.max_width-1)
            area = self._map[x][y]

            if not area.pit and not area.wumpus:
                gold_coords = [x, y]
                break

        x, y = gold_coords
        self._map[x][y].__setattr__('shine', 'shine')
