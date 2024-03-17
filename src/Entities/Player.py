from pydantic import BaseModel
class Player(BaseModel):
    id: int
    name: str
    nickname: str
    walk_on_music: str