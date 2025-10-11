import random
from typing import Any, Callable

class Character:
    """
    Character base class
    """

    health: int
    armor: int
    attack: int

    heal_action_count: int = 0
    heal_action_method: Callable[[Any], int]

    race: str = "Unspecified"
    class_name: str = "Fighter"

    def attack_roll(self):
        """Rolls a d20 + attack modifier, 
        returns 0 for a critical hit.
        """
        roll = self.d20()
        if roll == 20: # natural 20
            return 0
        return roll + self.attack

    def d20(self):
        return random.randint(1, 20)
    
    def d12(self):
        return random.randint(1, 12)

    def d8(self):
        return random.randint(1, 8)
    
    def d6(self):
        return random.randint(1, 6)
    
    def d4(self):
        return random.randint(1, 4)
    

    def damage_roll(self):
        return self.d6() + self.attack

    def __repr__(self):
        return self.race + " " + self.class_name
