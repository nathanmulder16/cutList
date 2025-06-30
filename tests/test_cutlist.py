import pytest
from cutlist_app.cutlist import addSomeNumbers, subSomeNumbers

# to run pytest:    uv run pytest
@pytest.fixture
def numbers():
    return [1,2,3]

def test_addSomeNumbers(numbers):
    assert addSomeNumbers(numbers) == 6
    assert addSomeNumbers([2,3,4]) == 9

def test_subSomeNumbers(numbers):
    assert subSomeNumbers(numbers) == -6