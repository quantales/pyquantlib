import pyquantlib as ql


def test_evaluation_date_get_set():
    settings = ql.Settings.instance()

    today = ql.Date.todaysDate()
    custom_date = ql.Date(30, ql.Month.January, 2025)

    # Set evaluation date
    settings.evaluationDate = custom_date
    assert settings.evaluationDate == custom_date

    # Reset it to today
    settings.evaluationDate = today
    assert settings.evaluationDate == today


def test_set_evaluation_date():
    s = ql.Settings.instance()
    today = ql.Date(30, 1, 2025)
    s.setEvaluationDate(today)
    assert s.evaluationDate == today


def test_include_reference_date_events():
    settings = ql.Settings.instance()

    settings.includeReferenceDateEvents = True
    assert settings.includeReferenceDateEvents is True

    settings.includeReferenceDateEvents = False
    assert settings.includeReferenceDateEvents is False


def test_include_todays_cash_flows():
    settings = ql.Settings.instance()

    settings.includeTodaysCashFlows = True
    assert settings.includeTodaysCashFlows is True

    settings.includeTodaysCashFlows = False
    assert settings.includeTodaysCashFlows is False

    settings.includeTodaysCashFlows = None
    assert settings.includeTodaysCashFlows is None


def test_enforces_todays_historic_fixings():
    settings = ql.Settings.instance()

    settings.enforcesTodaysHistoricFixings = True
    assert settings.enforcesTodaysHistoricFixings is True

    settings.enforcesTodaysHistoricFixings = False
    assert settings.enforcesTodaysHistoricFixings is False
