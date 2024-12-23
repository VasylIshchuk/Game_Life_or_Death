from ..core.game_entity import load_data_from_file, parse_attribute
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

_SPECIAL_CREATURES = {
    "Mark": Hero,
    "Angry Guardian": AngryGuardian,
    "Rat": Rat,
    "Broken Marionette": BrokenMarionette,
    "Poisoned Monk": PoisonedMonk,
    "Withering Acolyte": WitheringAcolyte,
    "Fire Choker": FireChoker,
    "Rotting Flesh": RottingFlesh,
}


def _select_type(type_creature, title):
    if type_creature == "psychological":
        return Psychological(title)
    elif type_creature == "special":
        return _init_special_creature(title)
    else:
        return Creature(title)


def _init_special_creature(title: str) -> Creature:
    creature_class = _SPECIAL_CREATURES.get(title, Creature)
    return creature_class(title)


class CreatureFactory:
    @staticmethod
    def create_creature(title):
        data_creature = load_data_from_file("./creatures.json", title)
        type_creature = parse_attribute(data_creature, "type")
        return _select_type(type_creature, title)
