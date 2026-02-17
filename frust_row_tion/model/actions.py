from dataclasses import dataclass


@dataclass(frozen=True)
class ActionSnapshot:
    legs: float
    body: float
    arms: float
    handle_height: float
    toggle_feather: bool

    def __post_init__(self):
        for attr in (self.legs, self.body, self.arms, self.handle_height):
            if type(attr) != float:
                raise TypeError
            if not -1.0 <= attr <= 1.0:
                raise ValueError
        if type(self.toggle_feather) != bool:
            raise TypeError
