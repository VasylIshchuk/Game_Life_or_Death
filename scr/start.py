from modules.tests.fight_test import Fight
from modules.maps.temple.temple import Temple

temple = Temple(63, 7)
temple.print_map()

Fight.test_healing()

Fight.test_combat()
