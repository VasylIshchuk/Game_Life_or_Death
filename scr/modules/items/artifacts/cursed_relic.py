from .artifact import Artifact


class CursedRelic(Artifact):
    def __init__(self, title):
        super().__init__(title)
        self._health_cost: int = 0
        self._initialize_items_attributes()

    @property
    def health_cost(self) -> int:
        return self._health_cost

