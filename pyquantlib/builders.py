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


# ---------------------------------------------------------------------------
# MakeVanillaSwap
# ---------------------------------------------------------------------------

_MAKEVANILLASWAP_METHODS = {
    "receiveFixed": "receiveFixed",
    "swapType": "withType",
    "nominal": "withNominal",
    "settlementDays": "withSettlementDays",
    "effectiveDate": "withEffectiveDate",
    "terminationDate": "withTerminationDate",
    "rule": "withRule",
    "paymentConvention": "withPaymentConvention",
    "fixedLegTenor": "withFixedLegTenor",
    "fixedLegCalendar": "withFixedLegCalendar",
    "fixedLegConvention": "withFixedLegConvention",
    "fixedLegTerminationDateConvention": "withFixedLegTerminationDateConvention",
    "fixedLegRule": "withFixedLegRule",
    "fixedLegEndOfMonth": "withFixedLegEndOfMonth",
    "fixedLegFirstDate": "withFixedLegFirstDate",
    "fixedLegNextToLastDate": "withFixedLegNextToLastDate",
    "fixedLegDayCount": "withFixedLegDayCount",
    "floatingLegTenor": "withFloatingLegTenor",
    "floatingLegCalendar": "withFloatingLegCalendar",
    "floatingLegConvention": "withFloatingLegConvention",
    "floatingLegTerminationDateConvention": "withFloatingLegTerminationDateConvention",
    "floatingLegRule": "withFloatingLegRule",
    "floatingLegEndOfMonth": "withFloatingLegEndOfMonth",
    "floatingLegFirstDate": "withFloatingLegFirstDate",
    "floatingLegNextToLastDate": "withFloatingLegNextToLastDate",
    "floatingLegDayCount": "withFloatingLegDayCount",
    "floatingLegSpread": "withFloatingLegSpread",
    "discountingTermStructure": "withDiscountingTermStructure",
    "indexedCoupons": "withIndexedCoupons",
    "atParCoupons": "withAtParCoupons",
    "pricingEngine": "withPricingEngine",
}


def MakeVanillaSwap(swapTenor, iborIndex, fixedRate=None,
                    forwardStart=None, **kwargs):
    """Build a VanillaSwap from keyword arguments.

    Parameters
    ----------
    swapTenor : Period
        Tenor of the swap.
    iborIndex : IborIndex
        The floating rate index.
    fixedRate : float, optional
        Fixed rate.  ``None`` for par rate.
    forwardStart : Period, optional
        Forward start period.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``nominal``,
        ``pricingEngine``, ``fixedLegDayCount``, ``floatingLegSpread``, ...).

    Returns
    -------
    VanillaSwap
    """
    if forwardStart is not None:
        builder = _ql.MakeVanillaSwap(swapTenor, iborIndex,
                                      fixedRate, forwardStart)
    else:
        builder = _ql.MakeVanillaSwap(swapTenor, iborIndex, fixedRate)
    _apply_kwargs("MakeVanillaSwap", _MAKEVANILLASWAP_METHODS, builder, kwargs)
    return builder.swap()


# ---------------------------------------------------------------------------
# MakeSwaption
# ---------------------------------------------------------------------------

_MAKESWAPTION_METHODS = {
    "nominal": "withNominal",
    "settlementType": "withSettlementType",
    "settlementMethod": "withSettlementMethod",
    "optionConvention": "withOptionConvention",
    "exerciseDate": "withExerciseDate",
    "underlyingType": "withUnderlyingType",
    "indexedCoupons": "withIndexedCoupons",
    "atParCoupons": "withAtParCoupons",
    "pricingEngine": "withPricingEngine",
}


def MakeSwaption(swapIndex, optionTenor, strike=None, **kwargs):
    """Build a Swaption from keyword arguments.

    Parameters
    ----------
    swapIndex : SwapIndex
        The swap index.
    optionTenor : Period or Date
        Option tenor (Period) or fixing date (Date).
    strike : float, optional
        Strike rate.  ``None`` for ATM.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``nominal``,
        ``pricingEngine``, ``settlementType``, ...).

    Returns
    -------
    Swaption
    """
    builder = _ql.MakeSwaption(swapIndex, optionTenor, strike)
    _apply_kwargs("MakeSwaption", _MAKESWAPTION_METHODS, builder, kwargs)
    return builder.swaption()


# ---------------------------------------------------------------------------
# MakeYoYInflationCapFloor
# ---------------------------------------------------------------------------

_MAKEYOYINFLATIONCAPFLOOR_METHODS = {
    "nominal": "withNominal",
    "effectiveDate": "withEffectiveDate",
    "paymentDayCounter": "withPaymentDayCounter",
    "paymentAdjustment": "withPaymentAdjustment",
    "fixingDays": "withFixingDays",
    "pricingEngine": "withPricingEngine",
    "asOptionlet": "asOptionlet",
    "strike": "withStrike",
    "atmStrike": "withAtmStrike",
    "forwardStart": "withForwardStart",
}


def MakeYoYInflationCapFloor(capFloorType, index, length, calendar,
                             observationLag, interpolation, **kwargs):
    """Build a YoYInflationCapFloor from keyword arguments.

    Parameters
    ----------
    capFloorType : YoYInflationCapFloorType
        Cap, Floor, or Collar.
    index : YoYInflationIndex
        The YoY inflation index.
    length : int
        Length in years.
    calendar : Calendar
        Payment calendar.
    observationLag : Period
        Observation lag.
    interpolation : CPI.InterpolationType
        Interpolation type.
    **kwargs
        Builder options mapped to ``with*`` methods (e.g. ``nominal``,
        ``pricingEngine``, ``strike``, ``paymentDayCounter``, ...).

    Returns
    -------
    YoYInflationCapFloor
    """
    builder = _ql.MakeYoYInflationCapFloor(
        capFloorType, index, length, calendar,
        observationLag, interpolation)
    _apply_kwargs("MakeYoYInflationCapFloor",
                  _MAKEYOYINFLATIONCAPFLOOR_METHODS, builder, kwargs)
    return builder.capFloor()


# ---------------------------------------------------------------------------
# MakeFdHestonVanillaEngine
# ---------------------------------------------------------------------------

_MAKEFDHESTONVANILLAENGINE_METHODS = {
    "tGrid": "withTGrid",
    "xGrid": "withXGrid",
    "vGrid": "withVGrid",
    "dampingSteps": "withDampingSteps",
    "fdmSchemeDesc": "withFdmSchemeDesc",
}


def MakeFdHestonVanillaEngine(hestonModel, **kwargs):
    """Build an FdHestonVanillaEngine from keyword arguments.

    Parameters
    ----------
    hestonModel
        The Heston model.
    **kwargs
        Builder options: ``tGrid``, ``xGrid``, ``vGrid``,
        ``dampingSteps``, ``fdmSchemeDesc``.
        ``cashDividends`` expects a tuple of (dates, amounts).

    Returns
    -------
    PricingEngine
    """
    cash_divs = kwargs.pop("cashDividends", None)
    builder = _ql.MakeFdHestonVanillaEngine(hestonModel)
    _apply_kwargs("MakeFdHestonVanillaEngine",
                  _MAKEFDHESTONVANILLAENGINE_METHODS, builder, kwargs)
    if cash_divs is not None:
        dates, amounts = cash_divs
        builder.withCashDividends(dates, amounts)
    return builder.engine()
