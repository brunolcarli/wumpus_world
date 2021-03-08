"""
General utilities module.
"""

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
