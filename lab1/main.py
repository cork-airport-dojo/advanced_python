import random

import time
from typing import Callable, Iterable, List, Literal

from models.character import Character
from models.dwarf import Dwarf
from models.elf import Elf
from models.orc import Orc
from models.human import Human

from enum import Enum, auto

class Action(Enum):
    ATTACK = auto()
    HEAL = auto()
    DODGE = auto() # unimplemented
    GRAPPLE = auto() # unimplemented
    HELP = auto() # unimplemented

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

    def __get_team(self, character: Character):
        for team in [self.team_one, self.team_two]:
            for member in team.members:
                if member is character:
                    return team

    def __get_first_alive(self, characters: Iterable[Character]) -> Character:
        return next(char for char in characters if char.health > 0)

    def __calculate_initiative(self):
        members = self.team_one.members + self.team_two.members
        random.shuffle(members)
        self.initiative_order = members


    def simulate(self):
        """
        Perform a DnD encounter simulation
        """
        self.__calculate_initiative()

        print("=== Rolled initiative ===")
        print('\n'.join(f"{i}: {char}" for i, char in enumerate(self.initiative_order)))

        combat_log = []

        while True:
            current_turn = [] # the combat log strings for this turn.
            self.turn += 1

            # ensure each team has active members
            if not all([
                any(member.health > 0 for member in self.team_one.members),
                any(member.health > 0 for member in self.team_two.members),
            ]):
                current_turn.append("The fight is over")
                current_turn.append(
                    str(self.__get_team(self.__get_first_alive(self.initiative_order))) 
                    + " team wins!"
                )

                alive_fighters = [char for char in self.initiative_order if char.health > 0]
                current_turn.append(', '.join(
                    [str(fighter) for fighter in alive_fighters]) + " are left standing.")
                break

            print(f"== Turn {self.turn} ==")
            for fighter in self.initiative_order:
                if fighter.health > 0:
                    # generate a targeted action
                    team = self.__get_team(fighter)
                    enemies = set(self.initiative_order).difference(set(team.members))
                    targeted_action = team.attack_strategy(
                        fighter, team.members, enemies, [*combat_log, current_turn])

                    match targeted_action.action:                                                       
                        case Action.HEAL:
                            # if the target exists and the fighter has healing items left
                            if targeted_action.target and fighter.heal_action_count > 0:
                                # remove their healing item
                                fighter.heal_action_count -= 1

                                # now we roll the healing item dice, before adding the
                                # result to the target's health
                                heal_points = fighter.heal_action_method()
                                targeted_action.target.health += heal_points

                                current_turn.append(
                                    f"{fighter} healed {targeted_action.target} for {heal_points} points"
                                )                

                        case Action.ATTACK:
                            target = targeted_action.target
                            if target:
                                attack_roll = fighter.attack_roll()
                                current_turn.append(
                                    f"{fighter} rolled a {attack_roll} against enemy {target}'s {target.armor} AC"
                                )

                                # check the enemy's AC against the roll
                                if not attack_roll or attack_roll >= target.armor:
                                    # if the attack is critical or just hits normally

                                    # roll damage
                                    damage = fighter.damage_roll()
                                    if attack_roll == 0:
                                        damage *= 2

                                    target.health -= damage
                                    current_turn.append(
                                        f"{fighter} dealt {damage} damage against enemy {target}"
                                    )
                                else:
                                    current_turn.append(
                                        f"{fighter} missed {target}"
                                    )
                        case _:
                            current_turn.append(
                                f"{fighter} did not act or is confused"
                            )
                            print(f"Unhandled Action: {targeted_action}")
                print("\n".join(current_turn))
                combat_log.extend(current_turn)

                if self.turn >= self.max_turns:
                    print("Max turns reached!")
                    break

                # optional wait a little bit between turns
                time.sleep(0.1)

            print("Game over!")
def main():
    team_one = Team("Good guys", [Human(), Dwarf(), Elf()], default_attack_strategy)
    team_two = Team("Bad guys", [Orc(), Orc(), Orc()], default_attack_strategy)

    simulator = Simulation(team_one, team_two)
    simulator.simulate()

if __name__ == "__main__":
    main()