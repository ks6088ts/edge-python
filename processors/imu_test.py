import pytest

from . import imu


def test_imu():
    acc = [0, 0, 0]
    angv = [0, 0, 0]
    dt = 0.005
    processor = imu.Imu()
    processor.update(acc=acc, angv=angv, dt=dt)
    assert len(processor.get_state()) == 7

    with pytest.raises(AssertionError):
        processor.update(acc=acc, angv=angv, dt=-1)
    with pytest.raises(AssertionError):
        processor.update(acc=acc, angv=[0, 0], dt=dt)
    with pytest.raises(AssertionError):
        processor.update(acc=[0, 0], angv=angv, dt=dt)
