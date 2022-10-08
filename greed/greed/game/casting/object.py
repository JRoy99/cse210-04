from game.casting.actor import Actor

class Object(Actor):
    """A falling object which increment or decrement points when touched in the game. Subclass of Actor.
    
    The responsibility of Object is to keep track of its appearance, position, and text message

    Attributes:
        _scoremod (int): The number of points a given object is worth

        Inherited attributes:
            _text (string): The text to display
            _font_size (int): The font size to use.
            _color (Color): The color of the text.
            _position (Point): The screen coordinates.
            _velocity (Point): The speed and direction.
    """
    
    def __init__(self):
        """Constructs a new Object"""
        pass
