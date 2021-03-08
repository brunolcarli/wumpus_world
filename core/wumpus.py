


class Wumpus:
    def __init__(self, name=None):
        self.name = name or self.random_name()
        self.is_alive = True

    def __str__(self):
        state = 'Alive' if self.is_alive else 'Dead'
        if state == 'Dead':
            return f'Wumpus {self.name} is {state} by your arrow. Still stinking as hell...'

        return self.name

    def random_name(self):
        return ''.join(str(chr(id(self)//i)) for i in range(100000, 100005))

    def hit(self):
        self.is_alive = False
        print('You heard a screaming of pain coming from the dark cave before you.')
        print('Then suddenly... Silence.')
