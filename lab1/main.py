from typing import Callable, List, Tuple
from models.character import Character
from models.orc import Orc
from models.human import Human

from enum import Enum, auto

class Action():
    ATTACK = auto()

class TargetedAction:
    action: Action
    target: Character

def attack_strategy(
        character: Character, allies: List[Character], enemies: List[Character], attack_log) -> TargetedAction:
    pass


class Team:

    team_name: str
    members: List[Character]
    attack_strategy: Callable[]

    def __init__(self, team_name: str, members: List[Character]):
        self.team_name = team_name
        self.members = members




def main():
    orc = Orc()
    human = Human()
    turn = 1
    while True:
        if human.health < 1 or orc.health < 1:
            break
        orc_attack = orc.attack_roll()
        if orc_attack == 0 or orc_attack > human.armor:
            orc_dmg = orc.d6()
            if not orc_attack:
                orc_dmg *= 2
                print(f"Orc got a critical hit with {orc_dmg} damage")
            human.health -= orc_dmg
            print(f"Human took {orc_dmg} damage")
            if human.health < 1:
                print(f"Human is dead")

        if human.health > 0:
            human_attack = human.attack_roll()
            if human_attack == 0 or human_attack > orc.armor:
                human_dmg = human.d6()
                if not human_attack:
                    human_dmg *= 2
                    print(f"Human got a critical hit with {human_dmg} damage")

                orc.health -= human_dmg
                print(f"Orc took {human_dmg} damage")
                if orc.health < 1:
                    print(f"Orc is dead")


        turn += 1
    return False

if __name__ == "__main__":
    main()
