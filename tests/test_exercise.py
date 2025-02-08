import pytest
import pyquantlib as ql

def test_concrete_european_exercise():
    exercise_date = ql.Date(15, 6, 2025)
    exercise = ql.EuropeanExercise(exercise_date)

    assert isinstance(exercise, ql.EuropeanExercise)
    assert isinstance(exercise, ql.Exercise)
    assert len(exercise.dates()) == 1
    assert exercise.dates()[0] == exercise_date
    assert exercise.lastDate() == exercise_date


def test_concrete_american_exercise():
    earliest_date = ql.Date(15, 2, 2025)
    latest_date = ql.Date(15, 8, 2025)
    exercise = ql.AmericanExercise(earliest_date, latest_date)

    assert isinstance(exercise, ql.AmericanExercise)
    assert exercise.dates() == [earliest_date, latest_date]
    assert exercise.lastDate() == latest_date


def test_concrete_bermudan_exercise():
    dates = [
        ql.Date(1, 3, 2025),
        ql.Date(1, 6, 2025),
        ql.Date(1, 9, 2025),
        ql.Date(1, 12, 2025)
    ]
    exercise = ql.BermudanExercise(dates)

    assert isinstance(exercise, ql.BermudanExercise)
    assert exercise.dates() == dates
    assert exercise.lastDate() == ql.Date(1, 12, 2025)

