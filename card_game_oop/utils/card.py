class Card:

    def __init__(self, color, composition, name, points):
        # COACHES' NOTES : Nice use of private names
        self._color = color
        self._composition = composition
        self._name = name
        self._points = points
    
    def __call__(self, *args, **kwargs):
        return f"new card: {self._color} {self._composition} {self._name} {self._points} was created"

    def __str__(self):
        return f'[{self._color} {self._composition} {self._name}: {self._points}]'

    def __repr__(self):
        return f'[{self._color} {self._composition} {self._name}: {self._points}]'

    # COACHES' NOTES : Usually the @property decorator is for single properties, not for
    # a group of properties. https://www.freecodecamp.org/news/python-property-decorator/
    @property
    def get_card_properties(self):
        return self._color, self._composition, self._name, self._points

# COACHES' NOTES : Symbol class missing