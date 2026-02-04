"""
Abstract base classes
"""
from __future__ import annotations
import collections.abc
import pyquantlib._pyquantlib
import typing
__all__: list[str] = ['AffineModel', 'BasketPayoff', 'BlackCalibrationHelper', 'BlackVarianceTermStructure', 'BlackVolTermStructure', 'BlackVolatilityTermStructure', 'CalibratedModel', 'CalibrationHelper', 'CashFlow', 'Constraint', 'CostFunction', 'Coupon', 'Event', 'Extrapolator', 'GenericHestonModelEngine', 'Index', 'Instrument', 'InterestRateIndex', 'Interpolation', 'LazyObject', 'LocalVolTermStructure', 'MultiAssetOption', 'Observer', 'OneAssetOption', 'OneAssetOptionGenericEngine', 'OneFactorAffineModel', 'OneFactorModel', 'OptimizationMethod', 'Option', 'Payoff', 'PricingEngine', 'Quote', 'ShortRateModel', 'SmileSection', 'SpreadBlackScholesVanillaEngine', 'StochasticProcess', 'StochasticProcess1D', 'StrikedTypePayoff', 'SwapGenericEngine', 'SwaptionGenericEngine', 'TermStructure', 'TermStructureConsistentModel', 'TwoFactorModel', 'VolatilityTermStructure', 'YieldTermStructure']
class AffineModel(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for affine models.
    """
    def discount(self, t: typing.SupportsFloat) -> float:
        """
        Returns implied discount factor at time t.
        """
    def discountBondOption(self, type: pyquantlib._pyquantlib.OptionType, strike: typing.SupportsFloat, maturity: typing.SupportsFloat, bondMaturity: typing.SupportsFloat) -> float:
        """
        Returns discount bond option price.
        """
class BasketPayoff(Payoff):
    """
    Abstract base class for basket payoffs.
    """
    @typing.overload
    def __call__(self, price: typing.SupportsFloat) -> float:
        """
        Calculates payoff for a single price.
        """
    @typing.overload
    def __call__(self, prices: pyquantlib._pyquantlib.Array) -> float:
        """
        Calculates payoff for an array of prices.
        """
    @typing.overload
    def __call__(self, prices: collections.abc.Sequence[typing.SupportsFloat]) -> float:
        """
        Calculates payoff for a list of prices.
        """
    def __init__(self, basePayoff: Payoff) -> None:
        """
        Constructs with base payoff.
        """
    @typing.overload
    def accumulate(self, prices: pyquantlib._pyquantlib.Array) -> float:
        """
        Accumulates prices into a single value.
        """
    @typing.overload
    def accumulate(self, prices: collections.abc.Sequence[typing.SupportsFloat]) -> float:
        """
        Accumulates a list of prices into a single value.
        """
    def basePayoff(self) -> Payoff:
        """
        Returns the underlying payoff.
        """
    def description(self) -> str:
        """
        Returns the payoff description.
        """
    def name(self) -> str:
        """
        Returns the payoff name.
        """
class BlackCalibrationHelper(CalibrationHelper, LazyObject):
    """
    Base class for Black76-based calibration helpers.
    """
    def blackPrice(self, volatility: typing.SupportsFloat) -> float:
        """
        Returns Black price for given volatility.
        """
    def calibrationError(self) -> float:
        """
        Returns the calibration error.
        """
    def impliedVolatility(self, targetValue: typing.SupportsFloat, accuracy: typing.SupportsFloat = 0.0001, maxEvaluations: typing.SupportsInt = 100, minVol: typing.SupportsFloat = 1e-07, maxVol: typing.SupportsFloat = 4.0) -> float:
        """
        Returns implied Black volatility.
        """
    def marketValue(self) -> float:
        """
        Returns the market value from quoted volatility.
        """
    def modelValue(self) -> float:
        """
        Returns the model value.
        """
    def setPricingEngine(self, engine: PricingEngine) -> None:
        """
        Sets the pricing engine.
        """
    def volatility(self) -> pyquantlib._pyquantlib.QuoteHandle:
        """
        Returns the volatility handle.
        """
    def volatilityType(self) -> pyquantlib._pyquantlib.VolatilityType:
        """
        Returns the volatility type.
        """
class BlackVarianceTermStructure(BlackVolTermStructure):
    """
    Abstract adapter for Black volatility term structures (variance-based).
    """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with reference date.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with settlement days.
        """
class BlackVolTermStructure(VolatilityTermStructure):
    """
    Abstract base class for Black volatility term structures.
    """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with reference date.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with settlement days.
        """
    @typing.overload
    def blackForwardVariance(self, date1: pyquantlib._pyquantlib.Date, date2: pyquantlib._pyquantlib.Date, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black forward variance between two dates.
        """
    @typing.overload
    def blackForwardVariance(self, time1: typing.SupportsFloat, time2: typing.SupportsFloat, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black forward variance between two times.
        """
    @typing.overload
    def blackForwardVol(self, date1: pyquantlib._pyquantlib.Date, date2: pyquantlib._pyquantlib.Date, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black forward volatility between two dates.
        """
    @typing.overload
    def blackForwardVol(self, time1: typing.SupportsFloat, time2: typing.SupportsFloat, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black forward volatility between two times.
        """
    @typing.overload
    def blackVariance(self, date: pyquantlib._pyquantlib.Date, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black variance for the given date and strike.
        """
    @typing.overload
    def blackVariance(self, time: typing.SupportsFloat, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black variance for the given time and strike.
        """
    @typing.overload
    def blackVol(self, date: pyquantlib._pyquantlib.Date, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black volatility for the given date and strike.
        """
    @typing.overload
    def blackVol(self, time: typing.SupportsFloat, strike: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the Black volatility for the given time and strike.
        """
class BlackVolatilityTermStructure(BlackVolTermStructure):
    """
    Abstract adapter for Black volatility term structures (volatility-based).
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor for Python subclassing.
        """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with reference date.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with settlement days.
        """
class CalibratedModel(Observer, pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for calibrated models.
    """
    def calibrate(self, instruments: collections.abc.Sequence[...], method: OptimizationMethod, endCriteria: pyquantlib._pyquantlib.EndCriteria, constraint: Constraint = ..., weights: collections.abc.Sequence[typing.SupportsFloat] = [], fixParameters: collections.abc.Sequence[bool] = []) -> None:
        """
        Calibrate model to market instruments.
        """
    def constraint(self) -> Constraint:
        """
        Returns parameter constraint.
        """
    def endCriteria(self) -> pyquantlib._pyquantlib.EndCriteria.Type:
        """
        Returns end criteria from last calibration.
        """
    def functionEvaluation(self) -> int:
        """
        Returns number of function evaluations.
        """
    def params(self) -> pyquantlib._pyquantlib.Array:
        """
        Returns model parameters.
        """
    def problemValues(self) -> pyquantlib._pyquantlib.Array:
        """
        Returns problem values from last calibration.
        """
    def setParams(self, params: pyquantlib._pyquantlib.Array) -> None:
        """
        Sets model parameters.
        """
    def value(self, params: pyquantlib._pyquantlib.Array, instruments: collections.abc.Sequence[...]) -> float:
        """
        Returns objective function value.
        """
class CalibrationHelper:
    """
    Abstract base class for model calibration helpers.
    """
    def calibrationError(self) -> float:
        """
        Returns the calibration error.
        """
class CashFlow(Event, LazyObject):
    """
    Abstract base class for a single cash flow.
    """
    def __init__(self) -> None:
        ...
    def amount(self) -> float:
        """
        Returns the cash flow amount.
        """
    def hasOccurred(self, refDate: pyquantlib._pyquantlib.Date = ..., includeRefDate: bool | None = None) -> bool:
        """
        Returns true if the cash flow has occurred by the reference date.
        """
class Constraint:
    """
    Abstract constraint for optimization.
    """
    def empty(self) -> bool:
        """
        Returns true if the constraint is empty.
        """
    def test(self, params: pyquantlib._pyquantlib.Array) -> bool:
        """
        Tests if parameters satisfy the constraint.
        """
class CostFunction:
    """
    Abstract cost function for optimization.
    """
    def __init__(self) -> None:
        ...
    def value(self, x: pyquantlib._pyquantlib.Array) -> float:
        """
        Returns the cost for the given parameters.
        """
    def values(self, x: pyquantlib._pyquantlib.Array) -> pyquantlib._pyquantlib.Array:
        """
        Returns the cost values for the given parameters.
        """
class Coupon(CashFlow):
    """
    Abstract base class for coupon payments.
    """
    def __init__(self) -> None:
        ...
    def accrualDays(self) -> int:
        """
        Returns the number of accrual days.
        """
    def accrualEndDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the accrual end date.
        """
    def accrualPeriod(self) -> float:
        """
        Returns the accrual period as a year fraction.
        """
    def accrualStartDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the accrual start date.
        """
    def accruedAmount(self, date: pyquantlib._pyquantlib.Date) -> float:
        """
        Returns the accrued amount at the given date.
        """
    def date(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the payment date.
        """
    def dayCounter(self) -> pyquantlib._pyquantlib.DayCounter:
        """
        Returns the day counter.
        """
    def nominal(self) -> float:
        """
        Returns the nominal amount.
        """
    def rate(self) -> float:
        """
        Returns the accrual rate.
        """
    def referencePeriodEnd(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the reference period end date.
        """
    def referencePeriodStart(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the reference period start date.
        """
class Event(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for events with a date.
    """
    def __init__(self) -> None:
        ...
    def date(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the date of the event.
        """
class Extrapolator:
    """
    Base class for term structures supporting extrapolation.
    """
    def allowsExtrapolation(self) -> bool:
        """
        Returns true if extrapolation is enabled.
        """
    def disableExtrapolation(self, b: bool = True) -> None:
        """
        Disables or enables extrapolation.
        """
    def enableExtrapolation(self, b: bool = True) -> None:
        """
        Enables or disables extrapolation.
        """
class GenericHestonModelEngine(PricingEngine):
    """
    Generic pricing engine for Heston model.
    """
    @typing.overload
    def __init__(self, model: pyquantlib._pyquantlib.HestonModelHandle = ...) -> None:
        ...
    @typing.overload
    def __init__(self, model: pyquantlib._pyquantlib.HestonModel) -> None:
        ...
class Index(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for market indexes.
    """
    def __init__(self) -> None:
        ...
    def addFixing(self, fixingDate: pyquantlib._pyquantlib.Date, fixing: typing.SupportsFloat, forceOverwrite: bool = False) -> None:
        """
        Stores a fixing for the given date.
        """
    def clearFixings(self) -> None:
        """
        Clears all stored fixings.
        """
    def fixing(self, fixingDate: pyquantlib._pyquantlib.Date, forecastTodaysFixing: bool = False) -> float:
        """
        Returns the fixing for the given date.
        """
    def fixingCalendar(self) -> pyquantlib._pyquantlib.Calendar:
        """
        Returns the calendar used for fixing dates.
        """
    def isValidFixingDate(self, fixingDate: pyquantlib._pyquantlib.Date) -> bool:
        """
        Returns true if the fixing date is valid.
        """
    def name(self) -> str:
        """
        Returns the name of the index.
        """
class Instrument(LazyObject):
    """
    Abstract base class for financial instruments.
    """
    class results(PricingEngine.results):
        """
        Results from instrument valuation.
        """
        def __init__(self) -> None:
            ...
        @property
        def value(self) -> float:
            """
            The calculated NPV.
            """
        @value.setter
        def value(self, arg0: typing.SupportsFloat) -> None:
            ...
    def NPV(self) -> float:
        """
        Returns the net present value of the instrument.
        """
    def __init__(self) -> None:
        ...
    def isExpired(self) -> bool:
        """
        Returns true if the instrument has expired.
        """
    def setPricingEngine(self, engine: PricingEngine) -> None:
        """
        Sets the pricing engine for valuation.
        """
class InterestRateIndex(Index):
    """
    Base class for interest rate indexes.
    """
    def __init__(self, familyName: str, tenor: pyquantlib._pyquantlib.Period, fixingDays: typing.SupportsInt, currency: pyquantlib._pyquantlib.Currency, fixingCalendar: pyquantlib._pyquantlib.Calendar, dayCounter: pyquantlib._pyquantlib.DayCounter) -> None:
        ...
    def currency(self) -> pyquantlib._pyquantlib.Currency:
        """
        Returns the currency.
        """
    def dayCounter(self) -> pyquantlib._pyquantlib.DayCounter:
        """
        Returns the day counter.
        """
    def familyName(self) -> str:
        """
        Returns the family name.
        """
    def fixing(self, fixingDate: pyquantlib._pyquantlib.Date, forecastTodaysFixing: bool = False) -> float:
        """
        Returns the fixing for the given date.
        """
    def fixingCalendar(self) -> pyquantlib._pyquantlib.Calendar:
        """
        Returns the fixing calendar.
        """
    def fixingDate(self, valueDate: pyquantlib._pyquantlib.Date) -> pyquantlib._pyquantlib.Date:
        """
        Returns the fixing date for the given value date.
        """
    def fixingDays(self) -> int:
        """
        Returns the number of fixing days.
        """
    def forecastFixing(self, fixingDate: pyquantlib._pyquantlib.Date) -> float:
        """
        Returns the forecasted fixing for the given date.
        """
    def isValidFixingDate(self, fixingDate: pyquantlib._pyquantlib.Date) -> bool:
        """
        Returns true if the fixing date is valid.
        """
    def maturityDate(self, valueDate: pyquantlib._pyquantlib.Date) -> pyquantlib._pyquantlib.Date:
        """
        Returns the maturity date for the given value date.
        """
    def name(self) -> str:
        """
        Returns the index name.
        """
    def tenor(self) -> pyquantlib._pyquantlib.Period:
        """
        Returns the tenor.
        """
    def valueDate(self, fixingDate: pyquantlib._pyquantlib.Date) -> pyquantlib._pyquantlib.Date:
        """
        Returns the value date for the given fixing date.
        """
class Interpolation(Extrapolator):
    """
    Base class for 1-D interpolations.
    """
    def __call__(self, x: typing.SupportsFloat, allowExtrapolation: bool = False) -> float:
        """
        Returns interpolated value at x.
        """
    def derivative(self, x: typing.SupportsFloat, allowExtrapolation: bool = False) -> float:
        """
        Returns first derivative at x.
        """
    def empty(self) -> bool:
        """
        Returns true if interpolation is not initialized.
        """
    def isInRange(self, x: typing.SupportsFloat) -> bool:
        """
        Returns true if x is in the interpolation range.
        """
    def primitive(self, x: typing.SupportsFloat, allowExtrapolation: bool = False) -> float:
        """
        Returns primitive (integral) at x.
        """
    def secondDerivative(self, x: typing.SupportsFloat, allowExtrapolation: bool = False) -> float:
        """
        Returns second derivative at x.
        """
    def update(self) -> None:
        """
        Updates the interpolation after data changes.
        """
    def xMax(self) -> float:
        """
        Returns maximum x value.
        """
    def xMin(self) -> float:
        """
        Returns minimum x value.
        """
class LazyObject(Observer, pyquantlib._pyquantlib.Observable):
    """
    Framework for lazy object calculation.
    
    Derived classes must implement performCalculations().
    """
    multiple_inheritance: typing.ClassVar[bool] = True
    def __init__(self) -> None:
        ...
    def freeze(self) -> None:
        """
        Freeze the object, preventing automatic recalculation.
        """
    def recalculate(self) -> None:
        """
        Force recalculation of the object.
        """
    def unfreeze(self) -> None:
        """
        Unfreeze the object, allowing automatic recalculation.
        """
class LocalVolTermStructure(VolatilityTermStructure):
    """
    Abstract base class for local volatility term structures.
    """
    @typing.overload
    def __init__(self, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with business day convention and day counter.
        """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with reference date.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with settlement days.
        """
    @typing.overload
    def localVol(self, date: pyquantlib._pyquantlib.Date, underlyingLevel: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the local volatility for the given date and underlying level.
        """
    @typing.overload
    def localVol(self, time: typing.SupportsFloat, underlyingLevel: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the local volatility for the given time and underlying level.
        """
class MultiAssetOption(Option):
    """
    Base class for options on multiple assets.
    """
    class results(Instrument.results, pyquantlib._pyquantlib.Greeks):
        """
        Results from multi-asset option calculation.
        """
        def __init__(self) -> None:
            ...
        def reset(self) -> None:
            """
            Resets all results.
            """
    def __init__(self, payoff: Payoff, exercise: pyquantlib._pyquantlib.Exercise) -> None:
        """
        Constructs with payoff and exercise.
        """
    def delta(self) -> float:
        """
        Returns delta.
        """
    def dividendRho(self) -> float:
        """
        Returns dividend rho.
        """
    def gamma(self) -> float:
        """
        Returns gamma.
        """
    def isExpired(self) -> bool:
        """
        Returns whether the option has expired.
        """
    def rho(self) -> float:
        """
        Returns rho.
        """
    def theta(self) -> float:
        """
        Returns theta.
        """
    def vega(self) -> float:
        """
        Returns vega.
        """
class Observer:
    """
    Observer in QuantLib's Observer pattern
    
    Receives updates from Observable objects. Must implement update().
    """
    def __init__(self) -> None:
        ...
    def registerWith(self, observable: ...) -> None:
        """
        Register this observer with the given observable. The observer will then be notified when the observable changes.
        """
    def unregisterWith(self, observable: ...) -> int:
        """
        Unregister this observer from the given observable. The observer will no longer be notified by this observable.
        """
    def unregisterWithAll(self) -> None:
        """
        Unregister this observer from all observables it is currently registered with.
        """
    def update(self) -> None:
        """
        This method is called by the observable when it changes. Derived classes must implement this method.
        """
class OneAssetOption(Option):
    """
    Abstract base class for options on a single asset.
    """
    class engine(OneAssetOptionGenericEngine):
        """
        Pricing engine for one-asset options.
        """
        def __init__(self) -> None:
            ...
    class results(Instrument.results, pyquantlib._pyquantlib.Greeks, pyquantlib._pyquantlib.MoreGreeks):
        """
        Results from one-asset option pricing.
        """
        def __init__(self) -> None:
            ...
        def reset(self) -> None:
            """
            Resets all results.
            """
    def __init__(self, payoff: Payoff, exercise: pyquantlib._pyquantlib.Exercise) -> None:
        ...
    def delta(self) -> float:
        """
        Returns delta sensitivity.
        """
    def deltaForward(self) -> float:
        """
        Returns forward delta.
        """
    def dividendRho(self) -> float:
        """
        Returns dividend rho sensitivity.
        """
    def elasticity(self) -> float:
        """
        Returns elasticity (leverage).
        """
    def gamma(self) -> float:
        """
        Returns gamma sensitivity.
        """
    def itmCashProbability(self) -> float:
        """
        Returns probability of finishing in the money.
        """
    def rho(self) -> float:
        """
        Returns rho sensitivity.
        """
    def strikeSensitivity(self) -> float:
        """
        Returns strike sensitivity.
        """
    def theta(self) -> float:
        """
        Returns theta sensitivity.
        """
    def thetaPerDay(self) -> float:
        """
        Returns theta per day.
        """
    def vega(self) -> float:
        """
        Returns vega sensitivity.
        """
class OneAssetOptionGenericEngine(PricingEngine, Observer):
    """
    Generic base engine for one-asset options.
    """
    def __init__(self) -> None:
        ...
class OneFactorAffineModel(OneFactorModel, AffineModel):
    """
    Abstract base class for single-factor affine short-rate models.
    """
    def discountBond(self, now: typing.SupportsFloat, maturity: typing.SupportsFloat, rate: typing.SupportsFloat) -> float:
        """
        Returns the discount bond price P(now, maturity, rate).
        """
class OneFactorModel(ShortRateModel):
    """
    Abstract base class for single-factor short-rate models.
    """
class OptimizationMethod:
    """
    Abstract base class for optimization methods.
    """
    def __init__(self) -> None:
        ...
    def minimize(self, problem: ..., endCriteria: ...) -> ...:
        """
        Minimizes the problem using the given end criteria.
        """
class Option(Instrument):
    """
    Abstract base class for options.
    """
    class arguments(PricingEngine.arguments):
        """
        Arguments for option pricing engines.
        """
        def __init__(self) -> None:
            ...
        @property
        def exercise(self) -> pyquantlib._pyquantlib.Exercise:
            """
            The exercise style.
            """
        @exercise.setter
        def exercise(self, arg0: pyquantlib._pyquantlib.Exercise) -> None:
            ...
        @property
        def payoff(self) -> ...:
            """
            The option payoff.
            """
        @payoff.setter
        def payoff(self, arg0: ...) -> None:
            ...
    def __init__(self, payoff: ..., exercise: pyquantlib._pyquantlib.Exercise) -> None:
        """
        Constructs with payoff and exercise.
        """
    def exercise(self) -> pyquantlib._pyquantlib.Exercise:
        """
        Returns the exercise style.
        """
    def payoff(self) -> ...:
        """
        Returns the option payoff.
        """
class Payoff:
    """
    Abstract base class for option payoffs.
    """
    def __call__(self, price: typing.SupportsFloat) -> float:
        """
        Calculates the payoff for a given price.
        """
    def __init__(self) -> None:
        ...
    def description(self) -> str:
        """
        Returns the payoff description.
        """
    def name(self) -> str:
        """
        Returns the payoff name.
        """
class PricingEngine(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for pricing engines.
    """
    class arguments:
        """
        Abstract base class for pricing engine arguments.
        """
        def __init__(self) -> None:
            ...
        def validate(self) -> None:
            """
            Validates the arguments.
            """
    class results:
        """
        Abstract base class for pricing engine results.
        """
        def __init__(self) -> None:
            ...
        def reset(self) -> None:
            """
            Resets the results.
            """
    def __init__(self) -> None:
        ...
    def calculate(self) -> None:
        """
        Performs the calculation.
        """
    def getArguments(self) -> ...:
        """
        Returns a pointer to the arguments structure.
        """
    def getResults(self) -> ...:
        """
        Returns a pointer to the results structure.
        """
    def reset(self) -> None:
        """
        Resets the engine results.
        """
class Quote(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for market quotes.
    """
    def isValid(self) -> bool:
        """
        Returns true if the quote holds a valid value.
        """
    def value(self) -> float:
        """
        Returns the current value of the quote.
        """
class ShortRateModel(CalibratedModel):
    """
    Abstract base class for short-rate models.
    """
    def tree(self, grid: pyquantlib._pyquantlib.TimeGrid) -> ...:
        """
        Returns a lattice for the given time grid.
        """
class SmileSection(pyquantlib._pyquantlib.Observable, Observer):
    """
    Abstract base class for volatility smile sections.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor for Python subclassing.
        """
    @typing.overload
    def __init__(self, exerciseTime: typing.SupportsFloat, dc: pyquantlib._pyquantlib.DayCounter, type: pyquantlib._pyquantlib.VolatilityType, shift: typing.SupportsFloat) -> None:
        """
        Constructs with exercise time (all args required).
        """
    @typing.overload
    def __init__(self, exerciseTime: typing.SupportsFloat, dc: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with exercise time.
        """
    def atmLevel(self) -> float:
        """
        Returns ATM level (forward).
        """
    def dayCounter(self) -> pyquantlib._pyquantlib.DayCounter:
        """
        Returns the day counter.
        """
    def density(self, strike: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, gap: typing.SupportsFloat = 0.0001) -> float:
        """
        Returns the probability density at the given strike.
        """
    def digitalOptionPrice(self, strike: typing.SupportsFloat, type: pyquantlib._pyquantlib.OptionType = ..., discount: typing.SupportsFloat = 1.0, gap: typing.SupportsFloat = 1e-05) -> float:
        """
        Returns the digital option price at the given strike.
        """
    def exerciseDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the exercise date.
        """
    def exerciseTime(self) -> float:
        """
        Returns the time to exercise.
        """
    def maxStrike(self) -> float:
        """
        Returns maximum strike.
        """
    def minStrike(self) -> float:
        """
        Returns minimum strike.
        """
    def optionPrice(self, strike: typing.SupportsFloat, type: pyquantlib._pyquantlib.OptionType = ..., discount: typing.SupportsFloat = 1.0) -> float:
        """
        Returns the option price at the given strike.
        """
    def referenceDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the reference date.
        """
    def shift(self) -> float:
        """
        Returns the shift for shifted lognormal volatility.
        """
    def variance(self, strike: typing.SupportsFloat) -> float:
        """
        Returns variance at the given strike.
        """
    def vega(self, strike: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0) -> float:
        """
        Returns the vega at the given strike.
        """
    @typing.overload
    def volatility(self, strike: typing.SupportsFloat) -> float:
        """
        Returns volatility at the given strike.
        """
    @typing.overload
    def volatility(self, strike: typing.SupportsFloat, volatilityType: pyquantlib._pyquantlib.VolatilityType, shift: typing.SupportsFloat = 0.0) -> float:
        """
        Returns volatility at the given strike with specified type.
        """
    def volatilityType(self) -> pyquantlib._pyquantlib.VolatilityType:
        """
        Returns the volatility type.
        """
class SpreadBlackScholesVanillaEngine(pyquantlib._pyquantlib.BasketOptionEngine):
    """
    Abstract base class for spread option pricing engines.
    """
    def __init__(self, process1: pyquantlib._pyquantlib.GeneralizedBlackScholesProcess, process2: pyquantlib._pyquantlib.GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with two Black-Scholes processes and correlation.
        """
class StochasticProcess(Observer, pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for stochastic processes.
    """
    def __init__(self) -> None:
        ...
    def diffusion(self, t: typing.SupportsFloat, x: pyquantlib._pyquantlib.Array) -> pyquantlib._pyquantlib.Matrix:
        """
        Returns the diffusion matrix at time t given state x.
        """
    def drift(self, t: typing.SupportsFloat, x: pyquantlib._pyquantlib.Array) -> pyquantlib._pyquantlib.Array:
        """
        Returns the drift at time t given state x.
        """
    def evolve(self, t0: typing.SupportsFloat, x0: pyquantlib._pyquantlib.Array, dt: typing.SupportsFloat, dw: pyquantlib._pyquantlib.Array) -> pyquantlib._pyquantlib.Array:
        """
        Evolves the process from state x0 at time t0.
        """
    def factors(self) -> int:
        """
        Returns the number of Brownian factors.
        """
    def initialValues(self) -> pyquantlib._pyquantlib.Array:
        """
        Returns the initial values.
        """
    def size(self) -> int:
        """
        Returns the number of dimensions.
        """
class StochasticProcess1D(StochasticProcess):
    """
    Abstract base class for 1D stochastic processes.
    """
    class discretization:
        """
        Discretization scheme for 1D stochastic processes.
        """
        def __init__(self) -> None:
            ...
        def diffusion(self, process: StochasticProcess1D, t0: typing.SupportsFloat, x0: typing.SupportsFloat, dt: typing.SupportsFloat) -> float:
            """
            Returns the discretized diffusion.
            """
        def drift(self, process: StochasticProcess1D, t0: typing.SupportsFloat, x0: typing.SupportsFloat, dt: typing.SupportsFloat) -> float:
            """
            Returns the discretized drift.
            """
        def variance(self, process: StochasticProcess1D, t0: typing.SupportsFloat, x0: typing.SupportsFloat, dt: typing.SupportsFloat) -> float:
            """
            Returns the discretized variance.
            """
    def __init__(self) -> None:
        ...
    def diffusion(self, t: typing.SupportsFloat, x: typing.SupportsFloat) -> float:
        """
        Returns the diffusion at time t given state x.
        """
    def drift(self, t: typing.SupportsFloat, x: typing.SupportsFloat) -> float:
        """
        Returns the drift at time t given state x.
        """
    def evolve(self, t0: typing.SupportsFloat, x0: typing.SupportsFloat, dt: typing.SupportsFloat, dw: typing.SupportsFloat) -> float:
        """
        Evolves the process from state x0 at time t0.
        """
    def x0(self) -> float:
        """
        Returns the initial value.
        """
class StrikedTypePayoff(Payoff):
    """
    Abstract base class for payoffs with strike and option type.
    """
    def optionType(self) -> pyquantlib._pyquantlib.OptionType:
        """
        Returns the option type (Call or Put).
        """
    def strike(self) -> float:
        """
        Returns the strike price.
        """
class SwapGenericEngine(PricingEngine, Observer):
    """
    Generic base engine for swaps.
    """
    def __init__(self) -> None:
        ...
class SwaptionGenericEngine(PricingEngine, Observer):
    """
    Generic base engine for swaptions.
    """
    def __init__(self) -> None:
        ...
class TermStructure(Observer, pyquantlib._pyquantlib.Observable, Extrapolator):
    """
    Abstract base class for term structures.
    """
    @typing.overload
    def __init__(self, dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with day counter (defaults to Actual365Fixed).
        """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with reference date, calendar, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with settlement days, calendar, and day counter.
        """
    def calendar(self) -> pyquantlib._pyquantlib.Calendar:
        """
        Returns the calendar.
        """
    def dayCounter(self) -> pyquantlib._pyquantlib.DayCounter:
        """
        Returns the day counter.
        """
    def maxDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the latest date for which the curve can return values.
        """
    def maxTime(self) -> float:
        """
        Returns the latest time for which the curve can return values.
        """
    def referenceDate(self) -> pyquantlib._pyquantlib.Date:
        """
        Returns the reference date for the term structure.
        """
    def settlementDays(self) -> int:
        """
        Returns the number of settlement days.
        """
    def timeFromReference(self, date: pyquantlib._pyquantlib.Date) -> float:
        """
        Returns the time from the reference date to the given date.
        """
class TermStructureConsistentModel(pyquantlib._pyquantlib.Observable):
    """
    Abstract base class for models consistent with a term structure.
    """
    def termStructure(self) -> pyquantlib._pyquantlib.YieldTermStructureHandle:
        """
        Returns the term structure handle.
        """
class TwoFactorModel(ShortRateModel):
    """
    Abstract base class for two-factor short-rate models.
    """
class VolatilityTermStructure(TermStructure):
    """
    Abstract base class for volatility term structures.
    """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention, dayCounter: pyquantlib._pyquantlib.DayCounter) -> None:
        """
        Constructs with reference date, calendar, convention, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, businessDayConvention: pyquantlib._pyquantlib.BusinessDayConvention, dayCounter: pyquantlib._pyquantlib.DayCounter) -> None:
        """
        Constructs with settlement days, calendar, convention, and day counter.
        """
    def businessDayConvention(self) -> pyquantlib._pyquantlib.BusinessDayConvention:
        """
        Returns the business day convention.
        """
    def maxStrike(self) -> float:
        """
        Returns the maximum strike for which the term structure is defined.
        """
    def minStrike(self) -> float:
        """
        Returns the minimum strike for which the term structure is defined.
        """
    def optionDateFromTenor(self, tenor: pyquantlib._pyquantlib.Period) -> pyquantlib._pyquantlib.Date:
        """
        Returns the option date for the given tenor.
        """
class YieldTermStructure(TermStructure):
    """
    Abstract base class for yield term structures.
    """
    @typing.overload
    def __init__(self, dayCounter: pyquantlib._pyquantlib.DayCounter = ...) -> None:
        """
        Constructs with day counter (defaults to Actual365Fixed).
        """
    @typing.overload
    def __init__(self, referenceDate: pyquantlib._pyquantlib.Date, calendar: pyquantlib._pyquantlib.Calendar = ..., dayCounter: pyquantlib._pyquantlib.DayCounter = ..., jumps: collections.abc.Sequence[pyquantlib._pyquantlib.QuoteHandle] = [], jumpDates: collections.abc.Sequence[pyquantlib._pyquantlib.Date] = []) -> None:
        """
        Constructs with reference date, calendar, day counter, and optional jumps.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: pyquantlib._pyquantlib.Calendar, dayCounter: pyquantlib._pyquantlib.DayCounter = ..., jumps: collections.abc.Sequence[pyquantlib._pyquantlib.QuoteHandle] = [], jumpDates: collections.abc.Sequence[pyquantlib._pyquantlib.Date] = []) -> None:
        """
        Constructs with settlement days, calendar, day counter, and optional jumps.
        """
    @typing.overload
    def discount(self, date: pyquantlib._pyquantlib.Date, extrapolate: bool = False) -> float:
        """
        Returns the discount factor for the given date.
        """
    @typing.overload
    def discount(self, time: typing.SupportsFloat, extrapolate: bool = False) -> float:
        """
        Returns the discount factor for the given time.
        """
    @typing.overload
    def forwardRate(self, date1: pyquantlib._pyquantlib.Date, date2: pyquantlib._pyquantlib.Date, dayCounter: pyquantlib._pyquantlib.DayCounter, compounding: pyquantlib._pyquantlib.Compounding, frequency: pyquantlib._pyquantlib.Frequency = ..., extrapolate: bool = False) -> pyquantlib._pyquantlib.InterestRate:
        """
        Returns the forward rate between two dates.
        """
    @typing.overload
    def forwardRate(self, date: pyquantlib._pyquantlib.Date, period: pyquantlib._pyquantlib.Period, dayCounter: pyquantlib._pyquantlib.DayCounter, compounding: pyquantlib._pyquantlib.Compounding, frequency: pyquantlib._pyquantlib.Frequency = ..., extrapolate: bool = False) -> pyquantlib._pyquantlib.InterestRate:
        """
        Returns the forward rate for a date and period.
        """
    @typing.overload
    def forwardRate(self, time1: typing.SupportsFloat, time2: typing.SupportsFloat, compounding: pyquantlib._pyquantlib.Compounding, frequency: pyquantlib._pyquantlib.Frequency = ..., extrapolate: bool = False) -> pyquantlib._pyquantlib.InterestRate:
        """
        Returns the forward rate between two times.
        """
    def jumpDates(self) -> list[pyquantlib._pyquantlib.Date]:
        """
        Returns the jump dates.
        """
    def jumpTimes(self) -> list[float]:
        """
        Returns the jump times.
        """
    def update(self) -> None:
        """
        Notifies observers of a change.
        """
    @typing.overload
    def zeroRate(self, date: pyquantlib._pyquantlib.Date, dayCounter: pyquantlib._pyquantlib.DayCounter, compounding: pyquantlib._pyquantlib.Compounding, frequency: pyquantlib._pyquantlib.Frequency = ..., extrapolate: bool = False) -> pyquantlib._pyquantlib.InterestRate:
        """
        Returns the zero rate for the given date.
        """
    @typing.overload
    def zeroRate(self, time: typing.SupportsFloat, compounding: pyquantlib._pyquantlib.Compounding, frequency: pyquantlib._pyquantlib.Frequency = ..., extrapolate: bool = False) -> pyquantlib._pyquantlib.InterestRate:
        """
        Returns the zero rate for the given time.
        """
