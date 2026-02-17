import math
import unittest
from dataclasses import FrozenInstanceError

from frust_row_tion.model.actions import ActionSnapshot


class TestActionSnapShot(unittest.TestCase):

    def make_valid_act_snap(self, **overrides):
        data = dict(
            legs=0.0,
            body=0.0,
            arms=0.0,
            handle=0.0,
            toggle_feather=False,
        )
        data.update(overrides)
        return ActionSnapshot(**data)

    def test_constructor_with_valid_values(self):
        action_snapshot = self.make_valid_act_snap(
            legs=-1.0, body=-0.5, arms=0.5, handle=1.0, toggle_feather=True
        )
        self.assertEqual(action_snapshot.legs, -1.0)
        self.assertEqual(action_snapshot.body, -0.5)
        self.assertEqual(action_snapshot.arms, 0.5)
        self.assertEqual(action_snapshot.handle, 1.0)
        self.assertTrue(action_snapshot.toggle_feather)

    def test_axis_boundaries_allowed(self):
        for v in (-1.0, 0.0, 1.0):
            with self.subTest(v=v):
                self.make_valid_act_snap(
                    legs=v,
                    body=v,
                    arms=v,
                    handle=v,
                    toggle_feather=False,
                )

    def test_out_of_range_rejected(self):
        bad_cases = [
            ("legs", 1.0001),
            ("legs", -1.0001),
            ("body", 2.0),
            ("arms", -2.0),
            ("handle_height", 999.0),
            ("handle_height", -999.0),
        ]
        for field, value in bad_cases:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    self.make_valid_act_snap(**{field: value})

    def test_nan_inf_rejected(self):
        bad_cases = [
            ("legs", math.nan),
            ("body", math.inf),
            ("arms", -math.inf),
            ("handle_height", math.nan),
        ]
        for field, value in bad_cases:
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValueError):
                    self.make_valid_act_snap(**{field: value})

    def test_toggle_feather_must_be_bool(self):
        bad_values = (1, 0, 0.0, "true", None, [], {})
        for bad in bad_values:
            with self.subTest(bad=bad):
                with self.assertRaises((TypeError, ValueError)):
                    self.make_valid_act_snap(toggle_feather=bad)

    def test_value_equality(self):
        a1 = self.make_valid_act_snap(legs=0.25, toggle_feather=True)
        a2 = self.make_valid_act_snap(legs=0.25, toggle_feather=True)
        self.assertEqual(a1, a2)

    def test_immutability_if_frozen(self):
        params = getattr(ActionSnapshot, "__dataclass_params__", None)
        if params is None or not params.frozen:
            self.skipTest("ActionSnapshot is not a frozen dataclass")

        a = self.make_valid_act_snap()
        with self.assertRaises(FrozenInstanceError):
            a.legs = 1.0


if __name__ == "__main__":
    unittest.main()
