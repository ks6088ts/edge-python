import numpy as np
from scipy.spatial.transform import Rotation as R


class Imu:
    STATE_NAMES = [
        "p_x",
        "p_y",
        "p_z",
        "q_x",
        "q_y",
        "q_z",
        "q_w",
    ]
    INITIAL_STATE_VALUES = [
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ]

    def __init__(self):
        self.states = dict(zip(self.STATE_NAMES, self.INITIAL_STATE_VALUES))

    def update(self, acc, angv, dt):  # pylint: disable=unused-argument
        if len(acc) != 3:
            raise AssertionError(f"len(acc)={len(acc)} should be 3")
        if len(angv) != 3:
            raise AssertionError(f"len(angv)={len(angv)} should be 3")
        if dt < 0:
            raise AssertionError(f"dt={dt} should be more than 0")
        dq = R.from_quat([0, 0, 1, np.cos(np.pi / 4)])
        q = R.from_quat(list(self.states.values())[3:7])
        q = q * dq
        dict_q = dict(zip(self.STATE_NAMES[3:7], q.as_quat().tolist()))
        self.states.update(dict_q)

    def get_state(self):
        return self.states
