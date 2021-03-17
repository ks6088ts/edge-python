import pytest

from . import imu0


@pytest.mark.skip
def test_mock():
    driver = imu0.Imu0()
    driver.initialize()
    timestamp, states = driver.get_states()
    assert isinstance(timestamp, float)
    assert states is not None
    driver.finalize()
