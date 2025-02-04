from modules.maps.quest.boss_room_quest import BossRoomQuest
from modules.maps.terrain.mountain_peak import MountainPeak

# quest_generator = QuestGenerator()
# for i in range(5):
#     quest = quest_generator.generate_quest(i)
#     quest.print_map()


# game_level = 3
# floor_count = game_level + 2
# temple = TempleGenerator(floor_count, game_level)
# for i in range(floor_count):
#     floor = temple.get_floor(i)
#     floor.print_map()


# forest = TerrainGenerator().generate_terrain(game_level)
# forest.print_map()

quest = MountainPeak()
quest.print_map()
mountain_peak = BossRoomQuest()
mountain_peak.print_map()

# temple = Floor(31,21,True)
# item = ItemFactory().create_item("Statue with a Cup")
# creature = CreatureFactory().create_creature("Human")
# position = Position(temple.rooms[0].get_x_upper_left_angle(), temple.rooms[0].get_y_upper_left_angle())
# temple.place_creature(creature, position)
# temple.place_item(item,position)
# temple.print_map()

# Fight.test_healing()
# Fight.test_combat()
