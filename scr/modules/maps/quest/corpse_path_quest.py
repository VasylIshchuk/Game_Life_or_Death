from .door_choice_quest import DoorChoiceQuest
from ...items.item_factory import ItemFactory

CORPSES_COUNT = 45
MAX_MAP_LEVEL = 5


class CorpsePathQuest(DoorChoiceQuest):
    def __init__(self, map_level):
        super().__init__()
        self.map_level = map_level
        self._setup_rooms()

    def _setup_rooms(self):
        self._place_corpses()
        self.place_creatures(self.map_level)

    def _place_corpses(self):
        for _ in range(CORPSES_COUNT):
            corpse = ItemFactory.create_item("Human Corpse")
            self._place_creature_in_room(corpse, 0)

