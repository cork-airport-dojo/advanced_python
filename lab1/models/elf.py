from models.character import Character

class Elf(Character):
    def __init__(self):
        self.health = 10
        self.attack = 3
        self.armor = 3

        self.heal_action_count = 3
        self.heal_action_method = self.d6

        self.race = "Elf"
