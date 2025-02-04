from ..quest.chamber_quest import ChamberQuest
from ...creatures.creature_factory import CreatureFactory

WIDTH = 35
HEIGHT = 18


class BossRoomQuest(ChamberQuest):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT)
        self._setup_room()

    def _setup_room(self):
        center_position = self.get_center_room_position()
        creature = CreatureFactory.create_creature("Temple Guardian")
        self.place_creature(creature, center_position)
