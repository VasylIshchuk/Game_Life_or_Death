from ..creatures.creature_factory import CreatureFactory
from ..maps.direction import Direction, get_position_toward_direction
from ..core.icons import Icon
from ..core.input_handler import InputHandler, refresh_display
from .temple.temple import Temple
from ..core.user_prompt import UserPrompt
from ..creatures.AI_controller import AIController

TRANSITION_TILES = (Icon.GATEWAY_EXIT, Icon.GATEWAY_ENTRANCE, Icon.STAIRS,
                    Icon.LEVEL_EXIT, Icon.LEVEL_ENTRANCE, Icon.CLOSED_LEVEL_EXIT,
                    Icon.DOOR, Icon.QUEST_DOOR)

GROUND_FLOOR = 0
MAP_INDEXES = {
    "Temple": 0,
    "Forest": 1,
    "Quest": 2
}


def _get_map_index(map_title):
    return MAP_INDEXES[map_title]


class LevelManager:
    def __init__(self, level):
        self.current_floor = 0
        self.current_map_index = 0
        self.current_map = None
        self.level = level
        self.is_level_active = True
        self.move_to_next_level = False
        self.move_to_previous_level = False
        self.hero = CreatureFactory.create_creature("Mark")
        self.input_handler = InputHandler(self)
        self.user_prompt = UserPrompt(self.hero)

    def set_current_map(self):
        self.current_map = self._get_current_map()

    def _get_current_map(self):
        current_section = self.level.get_section(self.current_map_index)
        return self.get_temple_floor(GROUND_FLOOR) if isinstance(current_section, Temple) else current_section

    def get_temple_floor(self, floor_number):
        temple = self._get_temple()
        return temple.get_floor(floor_number)

    def get_temple_total_floors(self):
        temple = self._get_temple()
        return temple.get_total_floors()

    def _get_temple(self):
        temple_index = _get_map_index("Temple")
        return self.level.get_section(temple_index)

    def put_hero_near_entrance(self):
        self.current_map.place_hero_near_entrance(self.hero)

    def put_hero_near_exit(self):
        self.current_map.place_hero_near_exit(self.hero)

    def reset_level_state(self):
        self.is_level_active = True
        self.move_to_next_level = False
        self.move_to_previous_level = False

    def is_level_in_progress(self):
        return self.is_level_active

    def deactivate_level(self):
        self.is_level_active = False

    def enable_move_to_next_level(self):
        self.move_to_next_level = True

    def enable_move_to_previous_level(self):
        self.move_to_previous_level = True

    def should_move_to_next_level(self):
        return self.move_to_next_level

    def should_move_to_previous_level(self):
        return self.move_to_previous_level

    def display(self):
        refresh_display()
        map_text = self.current_map.generate_map_text()
        text = self.user_prompt.get_text()

        max_map_width = self.get_current_map_width() * 3
        text_width = 10
        separator = "             "

        for i in range(max(len(map_text), len(text))):
            map_part = map_text[i] if i < len(map_text) else " " * max_map_width
            text_part = text[i] if i < len(text) else ""
            print(map_part.ljust(max_map_width) + separator + text_part.ljust(text_width))

        self.user_prompt.reset_text()

    def get_current_map_width(self):
        return self.current_map.get_map_width()

    def move_hero(self, direction):
        new_position = get_position_toward_direction(self.hero.get_position(), direction)
        self.current_map.place_creature(self.hero, new_position)

    def find_adjacent_transition_tile(self):
        hero_pos = self.hero.get_position()
        for direction in Direction.CARDINAL_DIRECTIONS:
            new_position = get_position_toward_direction(hero_pos, direction)
            cell_icon = self._get_tile_icon(new_position)
            if cell_icon in TRANSITION_TILES:
                return cell_icon
        return None

    def _get_tile_icon(self, position):
        return self.current_map.get_cell_icon(position)

    def handle_transition_level(self, cell_icon):
        if cell_icon == Icon.GATEWAY_EXIT:
            self._set_next_map()
        elif cell_icon == Icon.GATEWAY_ENTRANCE:
            self._set_previous_map()
        elif cell_icon == Icon.STAIRS:
            self._move_to_adjacent_floor()
        elif cell_icon == Icon.LEVEL_ENTRANCE:
            self.enable_move_to_previous_level()
            self.deactivate_level()
        elif cell_icon == Icon.LEVEL_EXIT:
            self.enable_move_to_next_level()
            self.deactivate_level()
        elif cell_icon == Icon.CLOSED_LEVEL_EXIT:
            if not self.current_map.is_completed_quest(): return
            self.current_map.open_quest_room()
            points = self.hero.calculate_xp_for_map_level_up(self.level.get_level_number())
            self.hero.add_experience_points(points)

    def _set_next_map(self):
        self._set_index_in_next_map()
        self.set_current_map()
        self.put_hero_near_entrance()

    def _set_index_in_next_map(self):
        self.current_map_index = min(self.current_map_index + 1, len(MAP_INDEXES) - 1)

    def _set_previous_map(self):
        self._set_index_in_previous_map()
        self.set_current_map()
        self.put_hero_near_exit()

    def _set_index_in_previous_map(self):
        self.current_map_index = max(self.current_map_index - 1, 0)

    def _move_to_adjacent_floor(self):
        direction = ""
        if 0 < self.current_floor < self.get_temple_total_floors() - 1:
            self.user_prompt.show_floor_direction_menu()
            self.display()
            direction = self.input_handler.get_floor_movement_input()

        if direction == "up" or self._is_ground_floor():
            self.load_next_floor()
        elif direction == "down" or self._is_top_floor():
            self.load_previous_floor()

        self.current_map.put_hero_near_stairs(self.hero)

    def _is_ground_floor(self):
        return self.current_floor == GROUND_FLOOR

    def _is_top_floor(self):
        return self.current_floor == self.get_temple_total_floors() - 1

    def load_next_floor(self):
        self.current_floor += 1
        self.current_map = self.get_temple_floor(self.current_floor)

    def load_previous_floor(self):
        self.current_floor -= 1
        self.current_map = self.get_temple_floor(self.current_floor)

    def handle_transition_map(self, cell_icon):
        if cell_icon == Icon.DOOR:
            self._move_through_door()
        elif cell_icon == Icon.QUEST_DOOR:
            door_position = self._move_through_quest_door()
            if door_position is not None:
                self.current_map.closed_quest_room(door_position)

    def _move_through_door(self):
        hero_pos = self.hero.get_position()
        for direction in Direction.CARDINAL_DIRECTIONS:
            door_position = get_position_toward_direction(hero_pos, direction)
            door_icon = self._get_tile_icon(door_position)
            if door_icon in (Icon.DOOR, Icon.QUEST_DOOR):
                position_near_door = get_position_toward_direction(door_position, direction)
                self.current_map.place_creature(self.hero, position_near_door)

    def _move_through_quest_door(self):
        hero_pos = self.hero.get_position()
        for direction in Direction.CARDINAL_DIRECTIONS:
            door_position = get_position_toward_direction(hero_pos, direction)
            door_icon = self._get_tile_icon(door_position)
            if door_icon in (Icon.DOOR, Icon.QUEST_DOOR):
                position_near_door = get_position_toward_direction(door_position, direction)
                if not self.current_map.is_placement_valid(position_near_door): return None
                key = self.hero.get_key_from_slots()
                if key is None or key.get_level_number() != self.level.get_level_number(): return None
                self.hero.delete_key_from_slots()
                self.current_map.place_creature(self.hero, position_near_door)
                return door_position
        return None

    def handle_creatures_action(self):
        for creature in self.current_map.get_creatures():
            AIController(creature).make_decision(self.hero, self.current_map)

    def validate_hero_is_alive(self):
        return self.hero.is_alive

    def find_adjacent_chest(self):
        hero_pos = self.hero.get_position()
        for direction in Direction.CARDINAL_DIRECTIONS:
            new_position = get_position_toward_direction(hero_pos, direction)
            chest = self.current_map.get_item(new_position)
            if chest is not None:
                return chest
        return None

    def handle_chest(self, chest):
        if chest.title == "Ordinary Chest":
            self._loot_chest_items(chest)
        elif chest.title == "Closed Chest":
            """TODO: change"""
            self._loot_chest_items(chest)

    def _loot_chest_items(self, chest):
        while not chest.is_empty():
            item = self._take_item_from_chest(chest)
            if item is None: return
            if not self.hero.add_item_to_backpack(item):
                self.user_prompt.show_backpack_is_full()
                return
            chest.remove_item(item)
        self.user_prompt.show_chest_is_empty()

    def _take_item_from_chest(self, chest):
        self.user_prompt.show_chest_items(chest)
        self.display()
        index = self.input_handler.select_item(chest)
        if index is None: return None
        return chest.get_item(index)

    def handle_attack(self):
        for creature in self.current_map.creatures:
            if self.hero.is_within_range(creature, self.hero.get_attack_range(), self.current_map):
                self.hero.attack(creature)
                if not creature.is_alive: self.current_map.remove_creature(creature)
                return

    def handle_spiritual_attack(self):
        for creature in self.current_map.creatures:
            if self.hero.is_within_range(creature, self.hero.attack_range_spirit_power, self.current_map):
                self.hero.spiritual_attack(creature)
                if not creature.is_alive: self.current_map.remove_creature(creature)
                return

    def handle_backpack(self):
        while True:
            self.user_prompt.show_backpack()
            self.display()
            index = self.input_handler.select_item(self.hero.backpack)
            if index is None: return

            item = self.hero.backpack.get_item(index)

            self.user_prompt.show_backpack()
            self.user_prompt.show_item_action_menu()
            self.display()
            action = self.input_handler.handle_bacpack_action()

            if action == "Equip":
                if not self.hero.validate_is_slot_available(item):
                    item_from_slot = self.hero.get_item_from_slots(item)
                    self.hero.delete_item_from_slots(item_from_slot)
                    self.hero.add_item_to_backpack(item_from_slot)

                self.hero.add_item_to_slots(item)
                self.hero.delete_item_from_backpack(index)
            elif action == "Drop":
                chest = self.find_adjacent_chest()
                if chest is None: continue

                if not chest.put_item(item):
                    print("Chest is Full ;(")
                    continue

                self.hero.delete_item_from_backpack(index)
            elif action == "Exchange":
                chest = self.find_adjacent_chest()
                if chest is None: continue

                chest_item = self._take_item_from_chest(chest)
                if chest_item is None: continue

                backpack_item = self.hero.get_item_from_backpack(index)

                self.hero.delete_item_from_backpack(index)
                self.hero.add_item_to_backpack(chest_item)

                chest.remove_item(chest_item)
                chest.put_item(backpack_item)
            elif action == "Stats":
                self.user_prompt.show_item_stats(item)

    def handle_book_effect(self):
        self.hero.apply_book_effect()

    def handle_food_effect(self):
        self.hero.apply_food_effect()
