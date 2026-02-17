from dataclasses import dataclass
from actions import ActionSnapshot


@dataclass
class RigPositions:
    legs: float = 0
    body: float = 0
    arms: float = 0
    handle: float = 0


@dataclass
class RigVelocities:
    legs: float = 0
    body: float = 0
    arms: float = 0
    handle: float = 0


class RigState:
    pos: RigPositions
    vel: RigVelocities
    feather: bool = True
    in_accel: float
    damping: float

    _MIN_POS = RigPositions(legs=0.0, body=0.0, arms=0.0, handle=-1.0)
    _MAX_POS = RigPositions(legs=1.0, body=1.0, arms=1.0, handle=1.0)

    _MAX_VEL = RigVelocities(legs=3.0, body=3.0, arms=3.0, handle=4.0)

    def __init__(self, in_accel: float, damping: float) -> None:
        self.pos = RigPositions()
        self.vel = RigVelocities()
        self.feather = True
        self.in_accel = in_accel
        self.damping = damping

    @staticmethod
    def _bound(num: float, low: float, high: float):
        return low if num < low else high if num > high else num

    def _update_bodily_axis(
        self,
        x: float,
        v: float,
        dt: float,
        x_min: float,
        x_max: float,
        v_max: float,
        act: float,
    ):
        a = act * self.in_accel
        # apply damping
        v *= (-self.damping) ** dt
        v = RigState._bound(v, -v_max, v_max)
        x += v * dt

        if x <= x_min:
            x = x_min
            if v < 0:
                v = 0
        if x <= x_max:
            x = x_max
            if v > 0:
                v = 0
        return x, v

    def update(self, dt: float, actions: ActionSnapshot):
        if dt <= 0:
            raise ValueError
        if actions.toggle_feather:
            self.feather = not self.feather

        self.pos.legs, self.vel.legs = self._update_bodily_axis(
            x=self.pos.legs,
            v=self.vel.legs,
            dt=dt,
            x_min=RigState._MIN_POS.legs,
            x_max=RigState._MAX_POS.legs,
            v_max=RigState._MAX_VEL.legs,
            act=actions.legs,
        )
        self.pos.body, self.vel.body = self._update_bodily_axis(
            x=self.pos.body,
            v=self.vel.body,
            dt=dt,
            x_min=RigState._MIN_POS.body,
            x_max=RigState._MAX_POS.body,
            v_max=RigState._MAX_VEL.body,
            act=actions.body,
        )
        self.pos.arms, self.vel.arms = self._update_bodily_axis(
            x=self.pos.arms,
            v=self.vel.arms,
            dt=dt,
            x_min=RigState._MIN_POS.arms,
            x_max=RigState._MAX_POS.arms,
            v_max=RigState._MAX_VEL.arms,
            act=actions.arms,
        )
        self.pos.handle, self.vel.handle = self._update_bodily_axis(
            x=self.pos.handle,
            v=self.vel.handle,
            dt=dt,
            x_min=RigState._MIN_POS.handle,
            x_max=RigState._MAX_POS.handle,
            v_max=RigState._MAX_VEL.handle,
            act=actions.handle,
        )
