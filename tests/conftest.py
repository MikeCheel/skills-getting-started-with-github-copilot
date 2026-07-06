from copy import deepcopy

import pytest

from src.app import activities


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original_activities))