from .door_choice_quest import DoorChoiceQuest
from ...creatures.creature_factory import CreatureFactory

PEOPLE_COUNT = 5
MAX_MAP_LEVEL = 5


class MoralDilemmaQuest(DoorChoiceQuest):
    def __init__(self, map_level):
        super().__init__()
        self.map_level = map_level
        self._setup_rooms()

    def _setup_rooms(self):
        self._place_people()
        self.place_creatures(self.map_level)

    def _place_people(self):
        for _ in range(PEOPLE_COUNT):
            human = CreatureFactory.create_creature("Human")
            self._place_creature_in_room(human, 0)

