from ..core.game_entity import _load_data_from_file, _parse_attribute
from ..creature.creature import Creature
from ..creature.psychological import Psychological
from ..creature.hero import Hero
from ..creature.angry_guardian import AngryGuardian
from ..creature.rat import Rat
from ..creature.broken_marionette import BrokenMarionette
from ..creature.poisoned_monk import PoisonedMonk
from ..creature.withering_acolyte import WitheringAcolyte
from ..creature.fire_choker import FireChoker
from ..creature.rotting_flesh import RottingFlesh


def _select_type(type, title):
    if type == "psychological":
        return Psychological(title)
    elif type == "special":
        return _init_special_creature(title)
    else:
        return Creature(title)


def _init_special_creature(title):
    if title == "Mark":
        return Hero(title)
    elif title == "Angry Guardian":
        return AngryGuardian(title)
    elif title == "Rat":
        return Rat(title)
    elif title == "Broken Marionette":
        return BrokenMarionette(title)
    elif title == "Poisoned Monk":
        return PoisonedMonk(title)
    elif title == "Withering Acolyte":
        return WitheringAcolyte(title)
    elif title == "Fire Choker":
        return FireChoker(title)
    elif title == "Rotting Flesh":
        return RottingFlesh(title)
    else:
        return Creature(title)


class CreatureFactory:
    @staticmethod
    def create_creature(title):
        data_creatures = _load_data_from_file("./creatures.json", title)
        type = _parse_attribute(data_creatures, "type")
        return _select_type(type, title)
