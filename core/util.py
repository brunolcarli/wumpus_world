"""
General utilities module.
"""
from game.settings import __version__


def get_perception(agent, cave, is_wall=None,):
    """
    Returns a tuple of perceptions over the area with the folowing
    structure:

    (stink, breeze, shine, impact, wumpus)
    """
    x, y = agent.current_position
    stink = cave._map[x][y].stink
    breeze = cave._map[x][y].breeze
    shine = cave._map[x][y].shine
    impact = is_wall
    wumpus = cave._map[x][y].wumpus

    return (stink, breeze, shine, impact, wumpus)


def ascii_banner():
    return r'''

     __      __
     \ \    / /  _ _ __  _ __ _  _ ___
      \ \/\/ / || | '  \| '_ \ || (_-<
     __\_/\_/_\_,_|_|_|_| .__/\_,_/__/
     \ \    / /__ _ _| ||_| |
      \ \/\/ / _ \ '_| / _` |
       \_/\_/\___/_| |_\__,_|
   ''' + f'\n\tversion: {__version__}'
