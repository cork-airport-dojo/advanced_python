import random
from typing import Callable, Iterable, List
from models.character import Character
from models.dwarf import Dwarf
from models.elf import Elf
from models.orc import Orc
from models.human import Human

from enum import Enum, auto

class Action(Enum):
    ATTACK = auto()
    HEAL = auto()

class TargetedAction:
    action: Action
    target: Character

type AttackStrategy = Callable[
    [Character, List[Character], List[Character], List[List[str]]], TargetedAction]

def default_attack_strategy(
        _character: Character, _allies: List[Character],
        enemies: List[Character], _combat_log: List[List[str]]
    ) -> TargetedAction:
    # just attack the first conscious enemy
    output = TargetedAction()

    output.action = Action.ATTACK
    output.target = next((enemy for enemy in enemies if enemy.health > 0), None)
    return output

class Team:
    team_name: str
    members: List[Character]
    attack_strategy: AttackStrategy

    def __init__(self,
                team_name: str, members: List[Character], 
                attack_strategy: AttackStrategy = None):
        self.team_name = team_name
        self.members = members
        # ==
        self.attack_strategy = attack_strategy
        if not attack_strategy:
            self.attack_strategy = default_attack_strategy

    def __repr__(self):
        return self.team_name

class Simulation:

    team_one: Team
    team_two: Team

    turn: int = 0

    initiative_order: List[Character]

    max_turns = 20

    def __init__(self, team_one, team_two):
        self.team_one = team_one
        self.team_two = team_two

def main():
    pass

if __name__ == "__main__":
    main()
