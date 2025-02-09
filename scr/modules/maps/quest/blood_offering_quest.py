from .chamber_quest import ChamberQuest
from ...items.item_factory import ItemFactory
from ...creatures.creature_factory import CreatureFactory


class BloodOfferingQuest(ChamberQuest):
    def __init__(self):
        super().__init__()
        self._setup_room()

    def _setup_room(self):
        self._place_statue()
        self._place_human()

    def _place_statue(self):
        center_position = self.get_center_room_position()
        statue = ItemFactory.create_item("Statue with a Cup")
        self.place_item(statue, center_position)

    def _place_human(self):
        human = CreatureFactory.create_creature("Human")
        self.place_creature_in_room(human, 0)
