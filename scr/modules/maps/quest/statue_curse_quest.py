from .chamber_quest import ChamberQuest
from ...creatures.creature_factory import CreatureFactory


class StatueCurseQuest(ChamberQuest):
    def __init__(self):
        super().__init__()
        self._setup_room()

    def _setup_room(self):
        center_position = self.get_center_room_position()
        creature = CreatureFactory.create_creature("Statue")
        self.place_creature(creature, center_position)
