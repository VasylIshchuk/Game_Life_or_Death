from  modules.core.game_manager import GameManager

GameManager()

# from modules.maps.quest.quest_generator import QuestGenerator
#
# quest_generator = QuestGenerator()
# for i in range(5):
#     quest = quest_generator.generate_quest(i)
#     quest.print_map()
#
#

# from modules.maps.terrain.forest_generator import ForestGenerator
#
# forest = ForestGenerator.generate_forest(5)
# forest.print_map()

# from  modules.maps.temple.temple_generator import TempleGenerator
#
# game_level = 4
# floor_count = game_level + 2
# temple =  TempleGenerator.generate_temple(game_level)
# for i in range(floor_count):
#     floor = temple.get_floor(i)
#     floor.print_map()


# quest = MountainPeak()
# quest.print_map()
# mountain_peak = BossRoomQuest()
# mountain_peak.print_map()

# temple = Floor(31,21,True)
# item = ItemFactory().create_item("Statue with a Cup")
# creature = CreatureFactory().create_creature("Human")
# position = Position(temple.rooms[0].get_x_upper_left_angle(), temple.rooms[0].get_y_upper_left_angle())
# temple.place_creature(creature, position)
# temple.place_item(item,position)
# temple.print_map()

# from  modules.tests.fight_test import Fight
#
# Fight.test_combat()
