import random

from ..core.game_entity import load_entity_data_from_file, load_data_from_file, get_attribute_from_data
from .creature import Creature
from .special_creatures.psychological import Psychological
from .hero import Hero
from .special_creatures.angry_guardian import AngryGuardian
from .special_creatures.rat import Rat
from .special_creatures.broken_marionette import BrokenMarionette
from .special_creatures.poisoned_monk import PoisonedMonk
from .special_creatures.withering_acolyte import WitheringAcolyte
from .special_creatures.fire_choker import FireChoker
from .special_creatures.rotting_flesh import RottingFlesh

CREATURES_FILE_PATH = "./creatures.json"
EXCLUDED_CREATURES = {"Mark", "Statue", "Shadow", "Human"}

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


def _select_creature_by_type(type_creature, title):
    if type_creature == "psychological":
        return Psychological(title)
    elif type_creature == "special":
        return _init_special_creature(title)
    else:
        return Creature(title)


def _init_special_creature(title):
    creature_class = _SPECIAL_CREATURES.get(title)
    return creature_class(title)


def _get_random_creature(creatures):
    return random.choice(creatures)


class CreatureFactory:
    @staticmethod
    def create_creature(title):
        data_creature = load_entity_data_from_file(CREATURES_FILE_PATH, title)
        type_creature = get_attribute_from_data(data_creature, "type")
        return _select_creature_by_type(type_creature, title)

    @staticmethod
    def create_random_creature_by_level(level):
        creatures = load_data_from_file(CREATURES_FILE_PATH)
        filtered_creatures = [name for name, data in creatures.items() if
                              data["level"] == level and name not in EXCLUDED_CREATURES]
        creature_title = _get_random_creature(filtered_creatures)
        creature = CreatureFactory().create_creature(creature_title)
        return creature
