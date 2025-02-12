from .quest.quest_generator import QuestGenerator
from .quest.boss_room_quest import BossRoomQuest
from .terrain.forest_generator import ForestGenerator
from .temple.temple_generator import TempleGenerator

LAST_LEVEL = 5


class Level:
    def __init__(self, level_number):
        self._level_number = level_number
        self.quest_generator = QuestGenerator()

        self._level_sections = []
        self._generate_level()

    def get_section(self, index):
        return self._level_sections[index]

    def get_level_number(self):
        return self._level_number

    def _generate_level(self):
        self._create_temple()
        self._create_forest()
        self._assign_quest()

    def _create_temple(self):
        temple = TempleGenerator.generate_temple(self._level_number)
        self._level_sections.append(temple)

    def _create_forest(self):
        forest = ForestGenerator.generate_forest(self._level_number)
        self._level_sections.append(forest)

    def _assign_quest(self):
        quest = BossRoomQuest() if self._level_number == LAST_LEVEL else self.quest_generator.generate_quest(
            self._level_number)
        self._level_sections.append(quest)
