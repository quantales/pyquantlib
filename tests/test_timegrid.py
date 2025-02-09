import pytest
import pyquantlib as ql

def test_timegrid_regular_constructor():
    """Tests the constructor for a regularly spaced grid."""
    end_time = 2.0
    steps = 4
    grid = ql.TimeGrid(end_time, steps)

    assert not grid.empty()
    assert len(grid) == steps + 1  # steps define intervals, so there are steps+1 points
    assert grid.size() == 5
    
    # Check the grid points
    expected_times = [0.0, 0.5, 1.0, 1.5, 2.0]
    for i, t in enumerate(grid):
        assert t == pytest.approx(expected_times[i])

    # Check sequence access
    assert grid[0] == 0.0
    assert grid[4] == 2.0
    assert grid.back() == 2.0
    
    # Check dt
    assert grid.dt(0) == pytest.approx(0.5)
    assert grid.dt(1) == pytest.approx(0.5)

def test_timegrid_from_list_constructor():
    """Tests the constructor that takes a list of mandatory times."""
    mandatory_times = [0.5, 1.0, 1.5]
    
    # Test without specifying steps
    grid = ql.TimeGrid(mandatory_times)
    # The grid should start at 0.0 and include the mandatory points
    expected_times = [0.0, 0.5, 1.0, 1.5]
    assert list(grid) == pytest.approx(expected_times)
    assert grid.mandatoryTimes() == pytest.approx(mandatory_times)

    # Test with a specified number of steps
    steps = 6
    grid_with_steps = ql.TimeGrid(mandatory_times, steps)
    assert len(grid_with_steps) > len(mandatory_times)
    assert grid_with_steps.size() == 7 # steps=6 -> 7 points
    assert grid_with_steps.back() == 1.5 # The last mandatory time is the end
    
    # Check that all mandatory times are present in the final grid
    for t in mandatory_times:
        # Using closestTime to account for floating point comparisons
        assert grid_with_steps.closestTime(t) == pytest.approx(t)

def test_timegrid_utility_methods():
    """Tests methods like index() and closestIndex()."""
    grid = ql.TimeGrid(1.0, 4) # Grid will be [0.0, 0.25, 0.5, 0.75, 1.0]
    
    # Test index() for an exact time on the grid
    assert grid.index(0.5) == 2
    
    # Test closestIndex()
    assert grid.closestIndex(0.51) == 2
    assert grid.closestIndex(0.60) == 2
    assert grid.closestIndex(0.63) == 3 # 0.63 is closer to 0.75 than 0.5
    assert grid.closestIndex(-0.1) == 0

    # Test closestTime()
    assert grid.closestTime(0.6) == pytest.approx(0.5)
