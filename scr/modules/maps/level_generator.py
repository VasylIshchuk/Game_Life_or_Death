from .quest.quest_generator import QuestGenerator
from .quest.boss_room_quest import BossRoomQuest
from .terrain.forest_generator import ForestGenerator
from .temple.temple_generator import TempleGenerator

LAST_LEVEL = 5


class LevelGenerator:
    def __init__(self, level_number):
        self.level_number = level_number
        self.quest_generator = QuestGenerator()

        self.level_sections = []

    def generate_level(self):
        self._create_temple()
        self._create_forest()
        self._assign_quest()
        return self.level_sections

    def _create_temple(self):
        temple = TempleGenerator.generate_temple(self.level_number)
        self.level_sections.append(temple)

    def _create_forest(self):
        forest = ForestGenerator.generate_forest(self.level_number)
        self.level_sections.append(forest)

    def _assign_quest(self):
        quest = BossRoomQuest() if self.level_number == LAST_LEVEL else self.quest_generator.generate_quest(
            self.level_number)
        self.level_sections.append(quest)
