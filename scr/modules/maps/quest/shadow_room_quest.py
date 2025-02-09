from .door_choice_quest import DoorChoiceQuest
from ...creatures.creature_factory import CreatureFactory

SHADOW_COUNT = 10
MAX_MAP_LEVEL = 5


class ShadowRoomQuest(DoorChoiceQuest):
    def __init__(self, map_level):
        super().__init__()
        self.map_level = map_level
        self._setup_rooms()

    def _setup_rooms(self):
        self._place_shadows()
        self.place_creatures(self.map_level)

    def _place_shadows(self):
        for _ in range(SHADOW_COUNT):
            shadow = CreatureFactory.create_creature("Shadow")
            self.place_creature_in_room(shadow, 0)
