from dataclasses import dataclass

@dataclass
class Player():
    id: int
    name: str
    nickname: str
    walk_on_music: str

    def __hash__(self) -> int:
        return self.id