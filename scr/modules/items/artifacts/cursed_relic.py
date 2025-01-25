from ..artifact import Artifact


class CursedRelic(Artifact):
    def __init__(self, title):
        super().__init__(title)
        self.health_cost: int = 0
        self._initialize_items_attributes()
