import pytest


def test_a(live_server):
    assert live_server._process
    assert live_server._process.is_alive()
