"""
Pythonic wrapper functions for QuantLib Make* builders.

Each function accepts the builder's constructor arguments as positional
parameters and all builder options as keyword arguments, returning the
built object directly.

See docs/design/builder-pattern.md for the design rationale.
"""

from . import _pyquantlib as _ql

# ---------------------------------------------------------------------------
# Shared helper
# ---------------------------------------------------------------------------

def _apply_kwargs(func_name, method_map, builder, kwargs):
    """Apply keyword arguments to a builder via its with* methods."""
    for name, value in kwargs.items():
        try:
            method = method_map[name]
        except KeyError:
            raise TypeError(
                f"{func_name}() got an unexpected keyword argument {name!r}"
            ) from None
        getattr(builder, method)(value)


# ---------------------------------------------------------------------------
# MakeSchedule
# ---------------------------------------------------------------------------

_MAKESCHEDULE_METHODS = {
    "tenor": "withTenor",
    "frequency": "withFrequency",
    "calendar": "withCalendar",
    "convention": "withConvention",
    "terminationDateConvention": "withTerminationDateConvention",
    "rule": "withRule",
    "endOfMonth": "endOfMonth",
    "firstDate": "withFirstDate",
    "nextToLastDate": "withNextToLastDate",
}


def MakeSchedule(effectiveDate=None, terminationDate=None, *,
                 forwards=False, backwards=False, **kwargs):
    """Build a Schedule from keyword arguments.

    Parameters
    ----------
    effectiveDate : Date, optional
        Start date of the schedule.
    terminationDate : Date, optional
        End date of the schedule.
    forwards : bool
        Use forward date generation.
    backwards : bool
        Use backward date generation.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``tenor``,
        ``frequency``, ``calendar``, ``convention``, ``rule``, ...).

    Returns
    -------
    Schedule
    """
    ms = _ql.MakeSchedule()
    if effectiveDate is not None:
        ms.from_(effectiveDate)
    if terminationDate is not None:
        ms.to(terminationDate)
    if forwards:
        ms.forwards()
    if backwards:
        ms.backwards()
    _apply_kwargs("MakeSchedule", _MAKESCHEDULE_METHODS, ms, kwargs)
    return ms.schedule()


# ---------------------------------------------------------------------------
# MakeCapFloor
# ---------------------------------------------------------------------------

_MAKECAPFLOOR_METHODS = {
    "nominal": "withNominal",
    "effectiveDate": "withEffectiveDate",
    "tenor": "withTenor",
    "calendar": "withCalendar",
    "convention": "withConvention",
    "terminationDateConvention": "withTerminationDateConvention",
    "rule": "withRule",
    "endOfMonth": "withEndOfMonth",
    "firstDate": "withFirstDate",
    "nextToLastDate": "withNextToLastDate",
    "dayCount": "withDayCount",
    "asOptionlet": "asOptionlet",
    "pricingEngine": "withPricingEngine",
}


def MakeCapFloor(capFloorType, tenor, index, strike=None,
                 forwardStart=None, **kwargs):
    """Build a CapFloor from keyword arguments.

    Parameters
    ----------
    capFloorType : CapFloorType
        Cap, Floor, or Collar.
    tenor : Period
        Tenor of the cap/floor.
    index : IborIndex
        The floating rate index.
    strike : float, optional
        Strike rate.  ``None`` for ATM.
    forwardStart : Period, optional
        Forward start period.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``nominal``,
        ``pricingEngine``, ``calendar``, ``dayCount``, ...).

    Returns
    -------
    CapFloor
    """
    if forwardStart is not None:
        builder = _ql.MakeCapFloor(capFloorType, tenor, index,
                                   strike, forwardStart)
    else:
        builder = _ql.MakeCapFloor(capFloorType, tenor, index, strike)
    _apply_kwargs("MakeCapFloor", _MAKECAPFLOOR_METHODS, builder, kwargs)
    return builder.capFloor()


# ---------------------------------------------------------------------------
# MakeOIS
# ---------------------------------------------------------------------------

_MAKEOIS_METHODS = {
    "receiveFixed": "receiveFixed",
    "swapType": "withType",
    "nominal": "withNominal",
    "settlementDays": "withSettlementDays",
    "effectiveDate": "withEffectiveDate",
    "terminationDate": "withTerminationDate",
    "rule": "withRule",
    "fixedLegRule": "withFixedLegRule",
    "overnightLegRule": "withOvernightLegRule",
    "paymentFrequency": "withPaymentFrequency",
    "fixedLegPaymentFrequency": "withFixedLegPaymentFrequency",
    "overnightLegPaymentFrequency": "withOvernightLegPaymentFrequency",
    "paymentAdjustment": "withPaymentAdjustment",
    "paymentLag": "withPaymentLag",
    "paymentCalendar": "withPaymentCalendar",
    "calendar": "withCalendar",
    "fixedLegCalendar": "withFixedLegCalendar",
    "overnightLegCalendar": "withOvernightLegCalendar",
    "convention": "withConvention",
    "fixedLegConvention": "withFixedLegConvention",
    "overnightLegConvention": "withOvernightLegConvention",
    "terminationDateConvention": "withTerminationDateConvention",
    "fixedLegTerminationDateConvention": "withFixedLegTerminationDateConvention",
    "overnightLegTerminationDateConvention": "withOvernightLegTerminationDateConvention",
    "endOfMonth": "withEndOfMonth",
    "fixedLegEndOfMonth": "withFixedLegEndOfMonth",
    "overnightLegEndOfMonth": "withOvernightLegEndOfMonth",
    "fixedLegDayCount": "withFixedLegDayCount",
    "overnightLegSpread": "withOvernightLegSpread",
    "discountingTermStructure": "withDiscountingTermStructure",
    "telescopicValueDates": "withTelescopicValueDates",
    "averagingMethod": "withAveragingMethod",
    "lookbackDays": "withLookbackDays",
    "lockoutDays": "withLockoutDays",
    "observationShift": "withObservationShift",
    "pricingEngine": "withPricingEngine",
}


def MakeOIS(swapTenor, overnightIndex, fixedRate=None,
            fwdStart=None, **kwargs):
    """Build an OvernightIndexedSwap from keyword arguments.

    Parameters
    ----------
    swapTenor : Period
        Tenor of the swap.
    overnightIndex : OvernightIndex
        The overnight rate index.
    fixedRate : float, optional
        Fixed rate.  ``None`` for ATM.
    fwdStart : Period, optional
        Forward start period.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``nominal``,
        ``pricingEngine``, ``fixedLegDayCount``, ...).

    Returns
    -------
    OvernightIndexedSwap
    """
    if fwdStart is not None:
        builder = _ql.MakeOIS(swapTenor, overnightIndex, fixedRate, fwdStart)
    else:
        builder = _ql.MakeOIS(swapTenor, overnightIndex, fixedRate)
    _apply_kwargs("MakeOIS", _MAKEOIS_METHODS, builder, kwargs)
    return builder.ois()
