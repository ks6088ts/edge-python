from . import mock


def test_mock():
    driver = mock.Mock()
    driver.initialize()
    timestamp, states = driver.get_states()
    assert isinstance(timestamp, float)
    assert states is not None
    driver.finalize()
