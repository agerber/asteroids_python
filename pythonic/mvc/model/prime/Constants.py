from pythonic.mvc.model.prime.Dimension import Dimension
import os

def getEnvInt(varName: str):
    """Return integer value of environment variable or raise."""
    value = os.getenv(varName)
    if value is None:
        raise ValueError(f"{varName} not set")
    return int(value)

def setDimFromEnv():
    try:
        width = getEnvInt("WIDTH")
        height = getEnvInt("HEIGHT")
        return Dimension(width, height)
    except (ValueError, TypeError):
        # default fallback
        return Dimension(900, 700)

DIM = setDimFromEnv()
PIXELS = 400
SPAWN_SHIELD_FLOATER = 1000   ## in java G_FRAMES_PER_SECOND/ANIMATION_DELAY * 40
SPAWN_NEW_WALL_FLOATER = 1120
SPAWN_NUKE_FLOATER = 350
INITIAL_SPAWN_TIME = 46
MAX_SHIELD = 200
MAX_NUKE = 600
