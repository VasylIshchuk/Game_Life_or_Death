from modules.tests.fight_test import Fight
from modules.maps.terrain.forest import Forest
from modules.maps.temple.temple_generator import TempleGenerator
from modules.maps.temple.floor import Floor
from modules.maps.temple.floor_creature_spawner import FloorCreatureSpawner
from modules.maps.terrain.forest_creature_spawner import ForestCreatureSpawner
from modules.maps.temple.floor_item_spawner import FloorItemSpawner
from modules.maps.terrain.forest_item_spawner import ForestItemSwamper
from modules.maps.quest.door_choice_quest import DoorChoiceQuest
from modules.maps.quest.chamber_quest import ChamberQuest
from modules.maps.quest.quest_generator import QuestGenerator
from modules.maps.position import Position
from modules.items.item_factory import ItemFactory
from modules.creatures.creature_factory import CreatureFactory

# quest_generator = QuestGenerator()
# for i in range(5):
#     quest = quest_generator.generate_quest(i)
#     quest.print_map()


# forest = Forest(43, 71)
# ForestCreatureSpawner(2, forest)
# ForestItemSwamper(forest)
# forest.print_map()


# game_level = 1
# floor_count = game_level + 2
# temple = TempleGenerator(floor_count, game_level)
# for i in range(floor_count):
#     floor = temple.get_floor(i)
#     floor.print_map()

# temple = Floor(31,21,True)
# item = ItemFactory().create_item("Statue with a Cup")
# creature = CreatureFactory().create_creature("Human")
# position = Position(temple.rooms[0].get_x_upper_left_angle(), temple.rooms[0].get_y_upper_left_angle())
# temple.place_creature(creature, position)
# temple.place_item(item,position)
# temple.print_map()

# Fight.test_healing()
# Fight.test_combat()
