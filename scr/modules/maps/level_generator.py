from .quest.quest_generator import QuestGenerator
from .quest.boss_room_quest import BossRoomQuest
from .terrain.mountain_peak import MountainPeak
from .terrain.terrain_generator import TerrainGenerator
from .temple.temple_generator import TempleGenerator

LAST_LEVEL = 5
GROUND_FLOOR = 0


class Level:
    def __init__(self, game_level):
        self.game_level = game_level
        self.quest_generator = QuestGenerator()
        self.current_map_index = 0

        self.level = []
        self.temple = None
        self._generate_level()

    def _generate_level(self):
        self._generate_temple()
        self._generate_forest()
        self._generate_quest()

    def _generate_temple(self):
        self.temple = TempleGenerator(self.game_level)
        self.level.append(self.temple)

    def _generate_forest(self):
        forest = TerrainGenerator().generate_terrain(self.game_level)
        self.level.append(forest)

    def _generate_quest(self):
        if self.game_level == LAST_LEVEL:
            quest = BossRoomQuest()
        else:
            quest = self.quest_generator.generate_quest(self.game_level)
        self.level.append(quest)

    def get_floor_map_from_temple(self, number_floor):
        return self.temple.get_floor(number_floor)

    def get_map(self):
        map = self.level[self.current_map_index]
        if isinstance(map, TempleGenerator): map = self.get_floor_map_from_temple(GROUND_FLOOR)
        return map

    def increase_current_map_index(self):
        self.current_map_index += 1

    def decrease_current_map_index(self):
        self.current_map_index -= 1
