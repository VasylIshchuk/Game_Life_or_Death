import random
from .statue_curse_quest import StatueCurseQuest
from .blood_offering_quest import BloodOfferingQuest
from .shadow_room_quest import ShadowRoomQuest
from .corpse_path_quest import CorpsePathQuest
from .moral_dilemma_quest import MoralDilemmaQuest

QUESTS_WITH_GAME_LEVEL = {2, 3, 4}
QUESTS = {
    1: StatueCurseQuest,
    2: ShadowRoomQuest,
    3: CorpsePathQuest,
    4: MoralDilemmaQuest,
    5: BloodOfferingQuest
}


class QuestGenerator:
    def __init__(self):
        self.quest_indexes = list(QUESTS.keys())

    def generate_quest(self, game_level):
        index_quest = self._pick_random_quest()
        self.quest_indexes.remove(index_quest)
        quest_class = QUESTS[index_quest]

        if index_quest in QUESTS_WITH_GAME_LEVEL:
            return quest_class(game_level)
        return quest_class()

    def _pick_random_quest(self):
        return random.choice(self.quest_indexes)
