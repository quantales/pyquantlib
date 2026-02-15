"""
PyQuantLib: Python bindings for QuantLib
"""
from __future__ import annotations
import collections.abc
import numpy
import numpy.typing
import typing
from . import base
__all__: list[str] = ['AEDCurrency', 'AOACurrency', 'ARSCurrency', 'ATSCurrency', 'AUDCurrency', 'Abs', 'Actual360', 'Actual364', 'Actual36525', 'Actual365Fixed', 'Actual366', 'ActualActual', 'Akima', 'AmericanExercise', 'AmortizingPayment', 'AnalyticBarrierEngine', 'AnalyticBlackVasicekEngine', 'AnalyticContinuousGeometricAveragePriceAsianEngine', 'AnalyticDiscreteGeometricAveragePriceAsianEngine', 'AnalyticDoubleBarrierEngine', 'AnalyticEuropeanEngine', 'AnalyticHestonEngine', 'Annual', 'Apr', 'April', 'Argentina', 'Array', 'AssetOrNothingPayoff', 'AssetSwap', 'Aug', 'August', 'Australia', 'AustraliaRegion', 'Austria', 'AverageBasketPayoff', 'AverageType', 'BCHCurrency', 'BDTCurrency', 'BEFCurrency', 'BGLCurrency', 'BGNCurrency', 'BHDCurrency', 'BOOST_VERSION', 'BRLCurrency', 'BTCCurrency', 'BWPCurrency', 'BYRCurrency', 'BachelierCapFloorEngine', 'BachelierSwaptionEngine', 'BackwardFlatInterpolation', 'BaroneAdesiWhaleyApproximationEngine', 'BarrierOption', 'BarrierType', 'BasketOption', 'BasketOptionEngine', 'BatesEngine', 'BatesModel', 'BatesProcess', 'BermudanExercise', 'BespokeCalendar', 'Bimonthly', 'BinomialVanillaEngine', 'Bisection', 'BivariateCumulativeNormalDistribution', 'Biweekly', 'BjerksundStenslandApproximationEngine', 'BjerksundStenslandSpreadEngine', 'BlackCapFloorEngine', 'BlackConstantVol', 'BlackIborCouponPricer', 'BlackKarasinski', 'BlackProcess', 'BlackScholesMertonProcess', 'BlackScholesProcess', 'BlackSwaptionEngine', 'BlackVarianceSurface', 'BlackVarianceSurfaceExtrapolation', 'BlackVolTermStructureHandle', 'Bond', 'BondFunctions', 'BondHelper', 'BondPrice', 'BondPriceType', 'Botswana', 'BoundaryConstraint', 'Brazil', 'Brent', 'Business252', 'BusinessDayConvention', 'CADCurrency', 'CHFCurrency', 'CLFCurrency', 'CLPCurrency', 'CNHCurrency', 'CNYCurrency', 'COPCurrency', 'COUCurrency', 'CPI', 'CYPCurrency', 'CZKCurrency', 'Calendar', 'CalendarVector', 'CalibrationErrorType', 'Call', 'Canada', 'Cap', 'CapFloor', 'CapFloorTermVolSurface', 'CapFloorType', 'CashDividendModel', 'CashOrNothingPayoff', 'CdsPricingModel', 'CeilingTruncation', 'Chebyshev', 'Chebyshev2nd', 'ChfLiborSwapIsdaFix', 'Chile', 'China', 'ClosestRounding', 'CmsCoupon', 'CmsLeg', 'Collar', 'ComplexLogFormula', 'CompositeConstraint', 'CompositeInstrument', 'CompositeQuote', 'Compounded', 'CompoundedThenSimple', 'Compounding', 'ConstantOptionletVolatility', 'ConstantParameter', 'ConstantSwaptionVolatility', 'Continuous', 'ContinuousAveragingAsianOption', 'CraigSneyd', 'CrankNicolson', 'CreditDefaultSwap', 'CubicBSplinesFitting', 'CubicBoundaryCondition', 'CubicDerivativeApprox', 'CubicInterpolation', 'CubicNaturalSpline', 'CumulativeNormalDistribution', 'Currency', 'CustomRegion', 'CzechRepublic', 'DASHCurrency', 'DEMCurrency', 'DKKCurrency', 'Daily', 'Date', 'DateGeneration', 'DayCounter', 'Days', 'Dec', 'December', 'DefaultProbabilityTermStructureHandle', 'DengLiZhouBasketEngine', 'Denmark', 'DepositRateHelper', 'DerivedQuote', 'DiscountCurve', 'DiscountingBondEngine', 'DiscountingSwapEngine', 'DiscreteAveragingAsianOption', 'DotProduct', 'DoubleBarrierOption', 'DoubleBarrierType', 'Douglas', 'DownRounding', 'DurationType', 'EEKCurrency', 'EGPCurrency', 'EPSILON', 'ESPCurrency', 'ETBCurrency', 'ETCCurrency', 'ETHCurrency', 'EUHICP', 'EUHICPXT', 'EURCurrency', 'EURegion', 'EndCriteria', 'Eonia', 'Error', 'Escrowed', 'Estr', 'EulerDiscretization', 'EurLiborSwapIfrFix', 'EurLiborSwapIsdaFixA', 'EurLiborSwapIsdaFixB', 'Euribor', 'Euribor1M', 'Euribor1W', 'Euribor1Y', 'Euribor365', 'Euribor3M', 'Euribor6M', 'EuriborSwapIfrFix', 'EuriborSwapIsdaFixA', 'EuriborSwapIsdaFixB', 'EuropeanExercise', 'EveryFourthMonth', 'EveryFourthWeek', 'ExchangeRate', 'ExchangeRateManager', 'Exercise', 'Exp', 'ExplicitEuler', 'ExponentialSplinesFitting', 'FIMCurrency', 'FRFCurrency', 'FaceValueAccrualClaim', 'FaceValueClaim', 'Fd2dBlackScholesVanillaEngine', 'FdBlackScholesBarrierEngine', 'FdBlackScholesVanillaEngine', 'FdG2SwaptionEngine', 'FdHullWhiteSwaptionEngine', 'FdmSchemeDesc', 'FdmSchemeType', 'Feb', 'February', 'Finland', 'FirstDerivative', 'FittedBondDiscountCurve', 'FixedLocalVolExtrapolation', 'FixedLocalVolSurface', 'FixedRateBond', 'FixedRateBondHelper', 'FixedRateCoupon', 'FixedRateLeg', 'FixedVsFloatingSwap', 'FixedVsFloatingSwapArguments', 'FixedVsFloatingSwapResults', 'FlatForward', 'FlatHazardRate', 'FloatingRateBond', 'FloatingRateCoupon', 'Floor', 'FloorTruncation', 'Following', 'ForwardCurve', 'ForwardRateAgreement', 'FourthOrder', 'FraRateHelper', 'France', 'FranceRegion', 'Frequency', 'Fri', 'Friday', 'FritschButland', 'G2', 'G2SwaptionEngine', 'GBPCurrency', 'GELCurrency', 'GHSCurrency', 'GRDCurrency', 'GapPayoff', 'GarmanKohlhagenProcess', 'GbpLiborSwapIsdaFix', 'GeneralizedBlackScholesProcess', 'Germany', 'Greeks', 'HKDCurrency', 'HRKCurrency', 'HUFCurrency', 'HalfMonthModifiedFollowing', 'Harmonic', 'Hermite', 'HestonModel', 'HestonModelHandle', 'HestonProcess', 'HongKong', 'Hours', 'HullWhite', 'Hundsdorfer', 'Hungary', 'Hyperbolic', 'IDRCurrency', 'IEPCurrency', 'ILSCurrency', 'INRCurrency', 'IQDCurrency', 'IRRCurrency', 'ISKCurrency', 'ITLCurrency', 'IborCoupon', 'IborCouponSettings', 'IborIndex', 'IborLeg', 'Iceland', 'ImplicitEuler', 'India', 'Indonesia', 'IntegralEngine', 'Integration', 'InterestRate', 'InverseCumulativeNormal', 'IsdaAccrualBias', 'IsdaCdsEngine', 'IsdaForwardsInCouponPeriod', 'IsdaNumericalFix', 'Israel', 'Italy', 'JODCurrency', 'JPYCurrency', 'JamshidianSwaptionEngine', 'Jan', 'January', 'Japan', 'JoinBusinessDays', 'JoinHolidays', 'JointCalendar', 'JointCalendarRule', 'JpyLiborSwapIsdaFixAm', 'JpyLiborSwapIsdaFixPm', 'Jul', 'July', 'Jun', 'June', 'KESCurrency', 'KRWCurrency', 'KWDCurrency', 'KZTCurrency', 'KirkEngine', 'Kruger', 'LKRCurrency', 'LTCCurrency', 'LTLCurrency', 'LUFCurrency', 'LVLCurrency', 'Lagrange', 'Laguerre', 'Legendre', 'LevenbergMarquardt', 'LinearInterpolation', 'LinearTsrPricer', 'LinearTsrPricerSettings', 'LinearTsrPricerStrategy', 'LocalConstantVol', 'LocalVolSurface', 'LocalVolTermStructureHandle', 'Log', 'LogLinearInterpolation', 'MADCurrency', 'MAX_INTEGER', 'MAX_REAL', 'MCAmericanEngine', 'MCDiscreteArithmeticAPEngine', 'MCEuropeanBasketEngine', 'MCEuropeanEngine', 'MCLDEuropeanBasketEngine', 'MIN_INTEGER', 'MIN_POSITIVE_REAL', 'MIN_REAL', 'MTLCurrency', 'MURCurrency', 'MXNCurrency', 'MXVCurrency', 'MYRCurrency', 'MakeCapFloor', 'MakeOIS', 'MakeSchedule', 'MakeSwaption', 'MakeVanillaSwap', 'Mar', 'March', 'Matrix', 'MaxBasketPayoff', 'May', 'MethodOfLines', 'Mexico', 'Microseconds', 'MidPointCdsEngine', 'Milliseconds', 'MinBasketPayoff', 'Minutes', 'ModifiedCraigSneyd', 'ModifiedFollowing', 'ModifiedPreceding', 'Mon', 'Monday', 'Money', 'Monomial', 'MonotonicCubicNaturalSpline', 'Month', 'Monthly', 'Months', 'MoreGreeks', 'NGNCurrency', 'NLGCurrency', 'NOKCurrency', 'NPRCurrency', 'NZDCurrency', 'Nearest', 'NelsonSiegelFitting', 'NewZealand', 'Newton', 'NoConstraint', 'NoExceptLocalVolSurface', 'NoFrequency', 'NormalDistribution', 'Norway', 'NotAKnot', 'Nov', 'November', 'NullCalendar', 'NullReal', 'NullSize', 'OISRateHelper', 'OMRCurrency', 'Observable', 'ObservableValue_Date', 'Oct', 'October', 'Once', 'OneDayCounter', 'OperatorSplittingSpreadEngine', 'OptionType', 'OptionletStripper1', 'OptionletVolatilityStructureHandle', 'OtherFrequency', 'OvernightIndex', 'OvernightIndexedCoupon', 'OvernightIndexedSwap', 'OvernightIndexedSwapIndex', 'OvernightLeg', 'PEHCurrency', 'PEICurrency', 'PENCurrency', 'PHPCurrency', 'PKRCurrency', 'PLNCurrency', 'PTECurrency', 'Parabolic', 'Parameter', 'PercentageStrikePayoff', 'Period', 'Periodic', 'PiecewiseBackwardFlatForward', 'PiecewiseBackwardFlatHazard', 'PiecewiseCubicDiscount', 'PiecewiseCubicZero', 'PiecewiseFlatForward', 'PiecewiseFlatHazardRate', 'PiecewiseLinearDefaultDensity', 'PiecewiseLinearDiscount', 'PiecewiseLinearForward', 'PiecewiseLinearZero', 'PiecewiseLogLinearDiscount', 'PiecewiseLogLinearSurvival', 'PiecewiseTimeDependentHestonModel', 'Pillar', 'PlainVanillaPayoff', 'Poland', 'PolynomialType', 'PositionType', 'PositiveConstraint', 'Pow', 'Preceding', 'Problem', 'ProtectionSide', 'Put', 'QARCurrency', 'QL_VERSION', 'QL_VERSION_HEX', 'QdFpAmericanEngine', 'QdFpFixedPointEquation', 'QdFpIterationScheme', 'QdFpLegendreScheme', 'QdFpLegendreTanhSinhScheme', 'QdFpTanhSinhIterationScheme', 'Quarterly', 'QuoteHandle', 'ROLCurrency', 'RONCurrency', 'RSDCurrency', 'RUBCurrency', 'RateAveraging', 'Redemption', 'Region', 'RelinkableBlackVolTermStructureHandle', 'RelinkableDefaultProbabilityTermStructureHandle', 'RelinkableLocalVolTermStructureHandle', 'RelinkableOptionletVolatilityStructureHandle', 'RelinkableQuoteHandle', 'RelinkableShortRateModelHandle', 'RelinkableSwaptionVolatilityStructureHandle', 'RelinkableYieldTermStructureHandle', 'RelinkableYoYInflationTermStructureHandle', 'RelinkableZeroInflationTermStructureHandle', 'Romania', 'Rounding', 'Russia', 'SARCurrency', 'SEKCurrency', 'SGDCurrency', 'SITCurrency', 'SKKCurrency', 'SabrInterpolatedSmileSection', 'SabrSmileSection', 'SabrSwaptionVolatilityCube', 'Sat', 'Saturday', 'SaudiArabia', 'SavedSettings', 'Schedule', 'Secant', 'SecondDerivative', 'Seconds', 'Semiannual', 'Sep', 'September', 'Settings', 'SettlementMethod', 'SettlementType', 'ShortRateModelHandle', 'Simple', 'SimpleCashFlow', 'SimpleDayCounter', 'SimplePolynomialFitting', 'SimpleQuote', 'SimpleThenCompounded', 'Singapore', 'Slovakia', 'Sofr', 'Sonia', 'SouthAfrica', 'SouthKorea', 'Spline', 'SplineOM1', 'SplineOM2', 'Spot', 'SpreadBasketPayoff', 'SpreadCdsHelper', 'SpreadFittingMethod', 'Sqrt', 'StochasticProcessArray', 'StrippedOptionletAdapter', 'StulzEngine', 'Sun', 'Sunday', 'SuperFundPayoff', 'SuperSharePayoff', 'SvenssonFitting', 'SviSmileSection', 'Swap', 'SwapArguments', 'SwapIndex', 'SwapRateHelper', 'SwapResults', 'SwapType', 'Swaption', 'SwaptionArguments', 'SwaptionHelper', 'SwaptionPriceType', 'SwaptionVolatilityCube', 'SwaptionVolatilityMatrix', 'SwaptionVolatilityStructureHandle', 'Sweden', 'Switzerland', 'TARGET', 'THBCurrency', 'TNDCurrency', 'TRLCurrency', 'TRYCurrency', 'TTDCurrency', 'TWDCurrency', 'Taiwan', 'Thailand', 'Thirty360', 'Thirty365', 'Thu', 'Thursday', 'TimeGrid', 'TimeUnit', 'TrBDF2', 'TreeSwaptionEngine', 'Tue', 'Tuesday', 'Turkey', 'TurnbullWakemanAsianEngine', 'UAHCurrency', 'UGXCurrency', 'UKRPI', 'UKRegion', 'USCPI', 'USDCurrency', 'USRegion', 'UYUCurrency', 'Ukraine', 'Unadjusted', 'UnitedKingdom', 'UnitedStates', 'UpRounding', 'UpfrontCdsHelper', 'UsdLiborSwapIsdaFixAm', 'UsdLiborSwapIsdaFixPm', 'VEBCurrency', 'VNDCurrency', 'VanillaOption', 'VanillaSwap', 'Vasicek', 'VolatilityType', 'Wed', 'Wednesday', 'Weekday', 'WeekendsOnly', 'Weekly', 'Weeks', 'XOFCurrency', 'XRPCurrency', 'YYEUHICP', 'YYEUHICPXT', 'YYUKRPI', 'YYUSCPI', 'Years', 'YieldTermStructureHandle', 'YoYInflationIndex', 'YoYInflationTermStructureHandle', 'ZARCurrency', 'ZARegion', 'ZECCurrency', 'ZMWCurrency', 'ZeroCouponBond', 'ZeroCouponSwap', 'ZeroCurve', 'ZeroInflationIndex', 'ZeroInflationTermStructureHandle', 'ZeroSpreadedTermStructure', 'bachelierBlackFormula', 'bachelierBlackFormulaImpliedVol', 'bachelierBlackFormulaStdDevDerivative', 'base', 'blackFormula', 'blackFormulaAssetItmProbability', 'blackFormulaCashItmProbability', 'blackFormulaForwardDerivative', 'blackFormulaImpliedStdDev', 'blackFormulaImpliedStdDevApproximation', 'blackFormulaStdDevDerivative', 'blackFormulaVolDerivative', 'cdsMaturity', 'checkSviParameters', 'close', 'close_enough', 'days', 'daysBetween', 'inflationPeriod', 'months', 'outerProduct', 'sabrVolatility', 'setCouponPricer', 'shiftedSabrVolatility', 'sviTotalVariance', 'transpose', 'validateSabrParameters', 'weeks', 'yearFractionToDate', 'years']
class AEDCurrency(Currency):
    """
    ! United Arab Emirates dirham
    /*! The ISO three-letter code is AED; the numeric code is 784.
         It is divided into 100 fils.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class AOACurrency(Currency):
    """
     Angolan kwanza
    /*! The ISO three-letter code is AOA; the numeric code is 973.
         It is divided into 100 c�ntimo.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class ARSCurrency(Currency):
    """
    ! The ISO three-letter code is ARS; the numeric code is 32.
            It is divided in 100 centavos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ATSCurrency(Currency):
    """
    ! The ISO three-letter code was ATS; the numeric code was 40.
            It was divided in 100 groschen.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class AUDCurrency(Currency):
    """
    ! The ISO three-letter code is AUD; the numeric code is 36.
            It is divided into 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class Actual360(DayCounter):
    """
    Actual/360 day count convention, also known as 'Act/360' or 'A/360'.
    """
    def __init__(self) -> None:
        ...
class Actual364(DayCounter):
    """
    Actual/364 day count convention.
    """
    def __init__(self) -> None:
        ...
class Actual36525(DayCounter):
    """
    Actual/365.25 day count convention.
    """
    def __init__(self) -> None:
        ...
class Actual365Fixed(DayCounter):
    """
    Actual/365 (Fixed) day count convention, also known as 'Act/365 (Fixed)' or 'A/365F'.
    """
    class Convention:
        """
        Members:
        
          Standard
        
          Canadian
        
          NoLeap
        """
        Canadian: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.Canadian: 1>
        NoLeap: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.NoLeap: 2>
        Standard: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.Standard: 0>
        __members__: typing.ClassVar[dict[str, Actual365Fixed.Convention]]  # value = {'Standard': <Convention.Standard: 0>, 'Canadian': <Convention.Canadian: 1>, 'NoLeap': <Convention.NoLeap: 2>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Canadian: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.Canadian: 1>
    NoLeap: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.NoLeap: 2>
    Standard: typing.ClassVar[Actual365Fixed.Convention]  # value = <Convention.Standard: 0>
    def __init__(self, c: Actual365Fixed.Convention = ...) -> None:
        ...
class Actual366(DayCounter):
    """
    Actual/366 day count convention.
    """
    def __init__(self) -> None:
        ...
class ActualActual(DayCounter):
    """
    Actual/Actual day count convention with ISDA, ISMA (Bond), and AFB (Euro) variants.
    """
    class Convention:
        """
        Members:
        
          ISMA
        
          Bond
        
          ISDA
        
          Historical
        
          Actual365
        
          AFB
        
          Euro
        """
        AFB: typing.ClassVar[ActualActual.Convention]  # value = <Convention.AFB: 5>
        Actual365: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Actual365: 4>
        Bond: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Bond: 1>
        Euro: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Euro: 6>
        Historical: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Historical: 3>
        ISDA: typing.ClassVar[ActualActual.Convention]  # value = <Convention.ISDA: 2>
        ISMA: typing.ClassVar[ActualActual.Convention]  # value = <Convention.ISMA: 0>
        __members__: typing.ClassVar[dict[str, ActualActual.Convention]]  # value = {'ISMA': <Convention.ISMA: 0>, 'Bond': <Convention.Bond: 1>, 'ISDA': <Convention.ISDA: 2>, 'Historical': <Convention.Historical: 3>, 'Actual365': <Convention.Actual365: 4>, 'AFB': <Convention.AFB: 5>, 'Euro': <Convention.Euro: 6>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    AFB: typing.ClassVar[ActualActual.Convention]  # value = <Convention.AFB: 5>
    Actual365: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Actual365: 4>
    Bond: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Bond: 1>
    Euro: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Euro: 6>
    Historical: typing.ClassVar[ActualActual.Convention]  # value = <Convention.Historical: 3>
    ISDA: typing.ClassVar[ActualActual.Convention]  # value = <Convention.ISDA: 2>
    ISMA: typing.ClassVar[ActualActual.Convention]  # value = <Convention.ISMA: 0>
    def __init__(self, c: ActualActual.Convention = ...) -> None:
        ...
class AmericanExercise(Exercise):
    """
    American-style exercise (date range).
    """
    def __init__(self, earliestDate: Date, latestDate: Date) -> None:
        """
        Constructs with earliest and latest exercise dates.
        """
class AmortizingPayment(SimpleCashFlow):
    """
    Amortizing payment cash flow.
    """
    def __init__(self, amount: typing.SupportsFloat, date: Date) -> None:
        """
        Constructs an amortizing payment with the given amount and date.
        """
class AnalyticBarrierEngine(base.PricingEngine):
    """
    Analytic barrier option engine (Haug).
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs AnalyticBarrierEngine.
        """
class AnalyticBlackVasicekEngine(base.PricingEngine):
    """
    European option engine with stochastic Vasicek interest rates.
    """
    def __init__(self, bsProcess: GeneralizedBlackScholesProcess, vasicekProcess: Vasicek, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with BS process, Vasicek model, and correlation.
        """
class AnalyticContinuousGeometricAveragePriceAsianEngine(base.PricingEngine):
    """
    Analytic continuous geometric average price Asian engine.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs engine.
        """
class AnalyticDiscreteGeometricAveragePriceAsianEngine(base.PricingEngine):
    """
    Analytic discrete geometric average price Asian engine.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs engine.
        """
class AnalyticDoubleBarrierEngine(base.PricingEngine):
    """
    Analytic double barrier option engine (Ikeda-Kunitomo).
    """
    def __init__(self, process: GeneralizedBlackScholesProcess, series: typing.SupportsInt = 5) -> None:
        """
        Constructs AnalyticDoubleBarrierEngine.
        """
class AnalyticEuropeanEngine(base.OneAssetOption.engine):
    """
    Analytic pricing engine for European vanilla options.
    """
    @typing.overload
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs engine with a Black-Scholes process.
        """
    @typing.overload
    def __init__(self, process: GeneralizedBlackScholesProcess, discountCurve: YieldTermStructureHandle) -> None:
        """
        Constructs engine with separate discount curve.
        """
    @typing.overload
    def __init__(self, process: GeneralizedBlackScholesProcess, discountCurve: base.YieldTermStructure) -> None:
        """
        Constructs engine with separate discount curve (handle created internally).
        """
class AnalyticHestonEngine(base.GenericHestonModelEngine):
    """
    Analytic pricing engine for Heston stochastic volatility model.
    """
    @typing.overload
    def __init__(self, model: HestonModel, relTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt) -> None:
        """
        Constructs with adaptive Gauss-Lobatto integration.
        """
    @typing.overload
    def __init__(self, model: HestonModel, integrationOrder: typing.SupportsInt = 144) -> None:
        """
        Constructs with Gauss-Laguerre integration.
        """
    @typing.overload
    def __init__(self, model: HestonModel, cpxLog: ComplexLogFormula, integration: Integration, andersenPiterbargEpsilon: typing.SupportsFloat = 1e-25, alpha: typing.SupportsFloat = -0.5) -> None:
        """
        Constructs with full control over integration method.
        """
    def numberOfEvaluations(self) -> int:
        """
        Returns number of integration evaluations.
        """
    def priceVanillaPayoff(self, payoff: PlainVanillaPayoff, maturity: typing.SupportsFloat) -> float:
        """
        Prices vanilla payoff for given maturity.
        """
class Argentina(Calendar):
    """
    ! Holidays for the Buenos Aires stock exchange
            (data from <http://www.merval.sba.com.ar/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Holy Thursday</li>
            <li>Good Friday</li>
            <li>Labour Day, May 1st</li>
            <li>May Revolution, May 25th</li>
            <li>Death of General Manuel Belgrano, third Monday of June</li>
            <li>Independence Day, July 9th</li>
            <li>Death of General Jos� de San Mart�n, third Monday of August</li>
            <li>Columbus Day, October 12th (moved to preceding Monday if
                on Tuesday or Wednesday and to following if on Thursday
                or Friday)</li>
            <li>Immaculate Conception, December 8th</li>
            <li>Christmas Eve, December 24th</li>
            <li>New Year's Eve, December 31th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Merval : !< Buenos Aires stock exchange calendar
        """
        Merval: typing.ClassVar[Argentina.Market]  # value = <Market.Merval: 0>
        __members__: typing.ClassVar[dict[str, Argentina.Market]]  # value = {'Merval': <Market.Merval: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Merval: typing.ClassVar[Argentina.Market]  # value = <Market.Merval: 0>
    def __init__(self, m: Argentina.Market = ...) -> None:
        ...
class Array:
    """
    1-dimensional array of Real values.
    """
    __hash__: typing.ClassVar[None] = None
    @typing.overload
    def __add__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __add__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __eq__(self, arg0: Array) -> bool:
        ...
    def __getitem__(self, i: typing.SupportsInt) -> float:
        ...
    @typing.overload
    def __iadd__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __iadd__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    @typing.overload
    def __imul__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __imul__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor (empty array).
        """
    @typing.overload
    def __init__(self, size: typing.SupportsInt) -> None:
        """
        Creates an array of given size.
        """
    @typing.overload
    def __init__(self, size: typing.SupportsInt, value: typing.SupportsFloat) -> None:
        """
        Creates an array of given size with all elements set to value.
        """
    @typing.overload
    def __init__(self, iterable: collections.abc.Iterable) -> None:
        """
        Creates an array from a Python iterable.
        """
    @typing.overload
    def __init__(self, numpy_array: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        """
        Creates an array from a 1D NumPy array.
        """
    @typing.overload
    def __isub__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __isub__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __iter__(self) -> collections.abc.Iterator[float]:
        ...
    @typing.overload
    def __itruediv__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __itruediv__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __mul__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __mul__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __ne__(self, arg0: Array) -> bool:
        ...
    def __neg__(self) -> Array:
        ...
    def __radd__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __repr__(self) -> str:
        ...
    def __rmul__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __rsub__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __rtruediv__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def __setitem__(self, i: typing.SupportsInt, value: typing.SupportsFloat) -> None:
        ...
    @typing.overload
    def __sub__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __sub__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    @typing.overload
    def __truediv__(self, arg0: Array) -> Array:
        ...
    @typing.overload
    def __truediv__(self, arg0: typing.SupportsFloat) -> Array:
        ...
    def at(self, i: typing.SupportsInt) -> float:
        """
        Access element with bounds checking.
        """
    def back(self) -> float:
        """
        Returns the last element.
        """
    def empty(self) -> bool:
        """
        Returns true if the array is empty.
        """
    def fill(self, value: typing.SupportsFloat) -> None:
        """
        Fills the array with a value.
        """
    def front(self) -> float:
        """
        Returns the first element.
        """
    @typing.overload
    def resize(self, size: typing.SupportsInt) -> None:
        """
        Resizes the array.
        """
    @typing.overload
    def resize(self, size: typing.SupportsInt, value: typing.SupportsFloat) -> None:
        """
        Resizes the array, filling new elements with value.
        """
    def size(self) -> int:
        """
        Returns the number of elements.
        """
    def swap(self, other: Array) -> None:
        """
        Swaps contents with another array.
        """
class AssetOrNothingPayoff(base.StrikedTypePayoff):
    """
    Binary payoff: asset value if in the money, zero otherwise.
    """
    def __init__(self, type: OptionType, strike: typing.SupportsFloat) -> None:
        ...
class AssetSwap(Swap):
    """
    Bullet bond vs Libor swap.
    """
    def __init__(self, payBondCoupon: bool, bond: Bond, bondCleanPrice: typing.SupportsFloat, iborIndex: IborIndex, spread: typing.SupportsFloat, floatSchedule: Schedule = ..., floatingDayCount: typing.Any = None, parAssetSwap: bool = True) -> None:
        """
        Constructs an asset swap.
        """
    def bond(self) -> Bond:
        """
        Underlying bond.
        """
    def bondLeg(self) -> list[base.CashFlow]:
        """
        Bond leg.
        """
    def cleanPrice(self) -> float:
        """
        Clean price.
        """
    def fairCleanPrice(self) -> float:
        """
        Fair clean price.
        """
    def fairNonParRepayment(self) -> float:
        """
        Fair non-par repayment.
        """
    def fairSpread(self) -> float:
        """
        Fair spread.
        """
    def floatingLeg(self) -> list[base.CashFlow]:
        """
        Floating leg.
        """
    def floatingLegBPS(self) -> float:
        """
        Floating leg BPS.
        """
    def floatingLegNPV(self) -> float:
        """
        Floating leg NPV.
        """
    def nonParRepayment(self) -> float:
        """
        Non-par repayment.
        """
    def parSwap(self) -> bool:
        """
        Whether this is a par swap.
        """
    def payBondCoupon(self) -> bool:
        """
        Whether bond coupons are paid.
        """
    def spread(self) -> float:
        """
        Spread.
        """
class Australia(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Australia Day, January 26th (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>ANZAC Day. April 25th (possibly moved to Monday)</li>
            <li>Queen's Birthday, second Monday in June</li>
            <li>Bank Holiday, first Monday in August</li>
            <li>Labour Day, first Monday in October</li>
            <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            <li>National Day of Mourning for Her Majesty, September 22, 2022</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          ASX : !< Australia ASX calendar
        """
        ASX: typing.ClassVar[Australia.Market]  # value = <Market.ASX: 1>
        Settlement: typing.ClassVar[Australia.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, Australia.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'ASX': <Market.ASX: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    ASX: typing.ClassVar[Australia.Market]  # value = <Market.ASX: 1>
    Settlement: typing.ClassVar[Australia.Market]  # value = <Market.Settlement: 0>
    def __init__(self, market: Australia.Market = ...) -> None:
        ...
class AustraliaRegion(Region):
    """
    Australia region.
    """
    def __init__(self) -> None:
        ...
class Austria(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th</li>
            <li>Easter Monday</li>
            <li>Ascension Thursday</li>
            <li>Whit Monday</li>
            <li>Corpus Christi</li>
            <li>Labour Day, May 1st</li>
            <li>Assumption Day, August 15th</li>
            <li>National Holiday, October 26th, since 1967</li>
            <li>All Saints Day, November 1st</li>
            <li>National Holiday, November 12th, 1919-1934</li>
            <li>Immaculate Conception Day, December 8th</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen, December 26th</li>
            </ul>
    
            Holidays for the stock exchange (data from https://www.wienerborse.at/en/trading/trading-information/trading-calendar/):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Whit Monday</li>
            <li>Labour Day, May 1st</li>
            <li>National Holiday, October 26th, since 1967</li>
            <li>National Holiday, November 12th, 1919-1934</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen, December 26th</li>
            <li>Exchange Holiday</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        ! Austrian calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          Exchange : !< Vienna stock-exchange calendar
        """
        Exchange: typing.ClassVar[Austria.Market]  # value = <Market.Exchange: 1>
        Settlement: typing.ClassVar[Austria.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, Austria.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'Exchange': <Market.Exchange: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Exchange: typing.ClassVar[Austria.Market]  # value = <Market.Exchange: 1>
    Settlement: typing.ClassVar[Austria.Market]  # value = <Market.Settlement: 0>
    def __init__(self) -> None:
        ...
class AverageBasketPayoff(base.BasketPayoff):
    """
    Payoff based on weighted average of basket prices.
    """
    @typing.overload
    def __init__(self, basePayoff: base.Payoff, weights: Array) -> None:
        """
        Constructs with base payoff and weights.
        """
    @typing.overload
    def __init__(self, basePayoff: base.Payoff, n: typing.SupportsInt) -> None:
        """
        Constructs with base payoff and equal weights for n assets.
        """
    def weights(self) -> Array:
        """
        Returns the weights.
        """
class AverageType:
    """
    Averaging type.
    
    Members:
    
      Arithmetic
    
      Geometric
    """
    Arithmetic: typing.ClassVar[AverageType]  # value = <AverageType.Arithmetic: 0>
    Geometric: typing.ClassVar[AverageType]  # value = <AverageType.Geometric: 1>
    __members__: typing.ClassVar[dict[str, AverageType]]  # value = {'Arithmetic': <AverageType.Arithmetic: 0>, 'Geometric': <AverageType.Geometric: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BCHCurrency(Currency):
    """
    ! https://www.bitcoincash.org/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BDTCurrency(Currency):
    """
    ! The ISO three-letter code is BDT; the numeric code is 50.
            It is divided in 100 paisa.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BEFCurrency(Currency):
    """
    ! The ISO three-letter code was BEF; the numeric code was 56.
            It had no subdivisions.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BGLCurrency(Currency):
    """
    ! The ISO three-letter code is BGL; the numeric code is 100.
            It is divided in 100 stotinki.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BGNCurrency(Currency):
    """
    ! The ISO three-letter code is BGN; the numeric code is 975.
            It is divided into 100 stotinki.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BHDCurrency(Currency):
    """
    ! Bahraini dinar
    /*! The ISO three-letter code is BHD; the numeric code is 048.
         It is divided into 1000 fils.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class BRLCurrency(Currency):
    """
    ! The ISO three-letter code is BRL; the numeric code is 986.
            It is divided in 100 centavos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BTCCurrency(Currency):
    """
    ! https://bitcoin.org/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BWPCurrency(Currency):
    """
     Botswanan Pula
    /*! The ISO three-letter code is BWP; the numeric code is 72.
         It is divided into 100 thebe.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class BYRCurrency(Currency):
    """
    ! The ISO three-letter code is BYR; the numeric code is 974.
            It has no subdivisions.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class BachelierCapFloorEngine(base.PricingEngine):
    """
    Bachelier (normal) cap/floor engine.
    """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: typing.SupportsFloat, dayCounter: DayCounter = ...) -> None:
        """
        Constructs with flat normal volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: typing.SupportsFloat, dayCounter: DayCounter = ...) -> None:
        """
        Constructs with flat normal volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: QuoteHandle, dayCounter: DayCounter = ...) -> None:
        """
        Constructs with quote normal volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: base.Quote, dayCounter: DayCounter = ...) -> None:
        """
        Constructs with quote normal volatility.
        """
class BachelierSwaptionEngine(base.PricingEngine):
    """
    Normal Bachelier-formula swaption engine.
    """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: typing.SupportsFloat, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from constant normal volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: base.Quote, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from quote normal volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: typing.SupportsFloat, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from constant normal volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: QuoteHandle, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from quote normal volatility (handle).
        """
class BackwardFlatInterpolation(base.Interpolation):
    """
    Backward-flat interpolation between discrete points.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs interpolation from x and y arrays.
        """
class BaroneAdesiWhaleyApproximationEngine(base.PricingEngine):
    """
    Barone-Adesi and Whaley approximation engine for American options (1987).
    """
    @staticmethod
    def criticalPrice(payoff: base.StrikedTypePayoff, riskFreeDiscount: typing.SupportsFloat, dividendDiscount: typing.SupportsFloat, variance: typing.SupportsFloat, tolerance: typing.SupportsFloat = 1e-06) -> float:
        """
        Computes the critical price for early exercise.
        """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs from a Black-Scholes process.
        """
class BarrierOption(base.OneAssetOption):
    """
    Barrier option on a single asset.
    """
    def __init__(self, barrierType: BarrierType, barrier: typing.SupportsFloat, rebate: typing.SupportsFloat, payoff: base.StrikedTypePayoff, exercise: Exercise) -> None:
        """
        Constructs BarrierOption.
        """
    def impliedVolatility(self, price: typing.SupportsFloat, process: GeneralizedBlackScholesProcess, accuracy: typing.SupportsFloat = 0.0001, maxEvaluations: typing.SupportsInt = 100, minVol: typing.SupportsFloat = 1e-07, maxVol: typing.SupportsFloat = 4.0) -> float:
        """
        Returns implied volatility.
        """
class BarrierType:
    """
    Barrier type.
    
    Members:
    
      DownIn
    
      UpIn
    
      DownOut
    
      UpOut
    """
    DownIn: typing.ClassVar[BarrierType]  # value = <BarrierType.DownIn: 0>
    DownOut: typing.ClassVar[BarrierType]  # value = <BarrierType.DownOut: 2>
    UpIn: typing.ClassVar[BarrierType]  # value = <BarrierType.UpIn: 1>
    UpOut: typing.ClassVar[BarrierType]  # value = <BarrierType.UpOut: 3>
    __members__: typing.ClassVar[dict[str, BarrierType]]  # value = {'DownIn': <BarrierType.DownIn: 0>, 'UpIn': <BarrierType.UpIn: 1>, 'DownOut': <BarrierType.DownOut: 2>, 'UpOut': <BarrierType.UpOut: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BasketOption(base.MultiAssetOption):
    """
    Basket option on multiple assets.
    """
    def __init__(self, payoff: base.BasketPayoff, exercise: Exercise) -> None:
        """
        Constructs with basket payoff and exercise.
        """
class BasketOptionEngine(base.PricingEngine):
    """
    Base class for basket option engines.
    """
class BatesEngine(AnalyticHestonEngine):
    """
    Analytic pricing engine for the Bates model.
    """
    @typing.overload
    def __init__(self, model: BatesModel, integrationOrder: typing.SupportsInt = 144) -> None:
        """
        Constructs with Bates model and integration order.
        """
    @typing.overload
    def __init__(self, model: BatesModel, relTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt) -> None:
        """
        Constructs with Bates model, relative tolerance, and max evaluations.
        """
class BatesModel(HestonModel):
    """
    Bates stochastic volatility model with jumps.
    """
    def __init__(self, process: BatesProcess) -> None:
        """
        Constructs from a Bates process.
        """
    def delta(self) -> float:
        """
        Returns jump size volatility.
        """
    def lambda_(self) -> float:
        """
        Returns jump intensity.
        """
    def nu(self) -> float:
        """
        Returns mean jump size.
        """
class BatesProcess(HestonProcess):
    """
    Bates stochastic volatility process with jumps.
    """
    @typing.overload
    def __init__(self, riskFreeRate: YieldTermStructureHandle, dividendYield: YieldTermStructureHandle, s0: QuoteHandle, v0: typing.SupportsFloat, kappa: typing.SupportsFloat, theta: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, lambda: typing.SupportsFloat, nu: typing.SupportsFloat, delta: typing.SupportsFloat, discretization: HestonProcess.Discretization = ...) -> None:
        """
        Constructs Bates process with Heston parameters plus jump parameters.
        """
    @typing.overload
    def __init__(self, riskFreeRate: base.YieldTermStructure, dividendYield: base.YieldTermStructure, s0: base.Quote, v0: typing.SupportsFloat, kappa: typing.SupportsFloat, theta: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, lambda: typing.SupportsFloat, nu: typing.SupportsFloat, delta: typing.SupportsFloat, discretization: HestonProcess.Discretization = ...) -> None:
        """
        Constructs with term structures and quote (handles created internally).
        """
    def delta(self) -> float:
        """
        Returns jump size volatility.
        """
    def lambda_(self) -> float:
        """
        Returns jump intensity.
        """
    def nu(self) -> float:
        """
        Returns mean jump size.
        """
class BermudanExercise(Exercise):
    """
    Bermudan-style exercise (discrete dates).
    """
    def __init__(self, dates: collections.abc.Sequence[Date]) -> None:
        """
        Constructs with a list of exercise dates.
        """
class BespokeCalendar(Calendar):
    """
    ! This calendar has no predefined set of business days. Holidays
            and weekdays can be defined by means of the provided
            interface. Instances constructed by copying remain linked to
            the original one; adding a new holiday or weekday will affect
            all linked instances.
    
            \\ingroup calendars
    """
    def __init__(self, name: str = '') -> None:
        ...
    def addWeekend(self, param_0: Weekday) -> None:
        """
        ! marks the passed day as part of the weekend
        """
class Bisection:
    """
    Bisection 1-D solver.
    """
    def __init__(self) -> None:
        ...
    def setLowerBound(self, lowerBound: typing.SupportsFloat) -> None:
        """
        Sets lower bound for the function domain.
        """
    def setMaxEvaluations(self, evaluations: typing.SupportsInt) -> None:
        """
        Sets maximum number of function evaluations.
        """
    def setUpperBound(self, upperBound: typing.SupportsFloat) -> None:
        """
        Sets upper bound for the function domain.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, step: typing.SupportsFloat) -> float:
        """
        Finds root with automatic bracketing.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, xMin: typing.SupportsFloat, xMax: typing.SupportsFloat) -> float:
        """
        Finds root within explicit bracket.
        """
class BivariateCumulativeNormalDistribution:
    """
    Cumulative bivariate normal distribution (West 2004).
    """
    def __call__(self, x: typing.SupportsFloat, y: typing.SupportsFloat) -> float:
        """
        Returns the cumulative bivariate normal probability.
        """
    def __init__(self, rho: typing.SupportsFloat) -> None:
        """
        Constructs BivariateCumulativeNormalDistribution with correlation rho.
        """
class BjerksundStenslandApproximationEngine(base.PricingEngine):
    """
    Bjerksund and Stensland approximation engine for American options (1993).
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs from a Black-Scholes process.
        """
class BjerksundStenslandSpreadEngine(base.SpreadBlackScholesVanillaEngine):
    """
    Bjerksund-Stensland analytical approximation for spread options.
    """
    def __init__(self, process1: GeneralizedBlackScholesProcess, process2: GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with two Black-Scholes processes and correlation.
        """
class BlackCapFloorEngine(base.PricingEngine):
    """
    Black-formula cap/floor engine.
    """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: typing.SupportsFloat, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs with flat volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: typing.SupportsFloat, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs with flat volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: QuoteHandle, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs with quote volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: base.Quote, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs with quote volatility.
        """
class BlackConstantVol(base.BlackVolatilityTermStructure):
    """
    Constant Black volatility term structure.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, volatility: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and constant volatility.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, volatility: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, volatility: base.Quote, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and constant volatility.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: base.Quote, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and quote (handle created internally).
        """
class BlackIborCouponPricer(base.FloatingRateCouponPricer):
    """
    Black-formula pricer for capped/floored Ibor coupons.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs with no optionlet volatility.
        """
    @typing.overload
    def __init__(self, volatility: ...) -> None:
        """
        Constructs with optionlet volatility.
        """
class BlackKarasinski(base.OneFactorModel, base.TermStructureConsistentModel):
    """
    Black-Karasinski model: d(ln r) = (theta(t) - a*ln(r))dt + sigma*dW.
    """
    @typing.overload
    def __init__(self, termStructure: YieldTermStructureHandle, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.1) -> None:
        """
        Constructs Black-Karasinski model with term structure, mean reversion, and volatility.
        """
    @typing.overload
    def __init__(self, termStructure: base.YieldTermStructure, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.1) -> None:
        """
        Constructs Black-Karasinski model from term structure.
        """
class BlackProcess(GeneralizedBlackScholesProcess):
    """
    Black process for forward price dynamics.
    """
    @typing.overload
    def __init__(self, x0: QuoteHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle) -> None:
        ...
    @typing.overload
    def __init__(self, x0: QuoteHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, x0: base.Quote, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    @typing.overload
    def __init__(self, x0: base.Quote, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        """
        Constructs from term structures with discretization (handles created internally).
        """
class BlackScholesProcess(GeneralizedBlackScholesProcess):
    """
    Black-Scholes process with no dividend yield.
    """
    @typing.overload
    def __init__(self, x0: QuoteHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle) -> None:
        ...
    @typing.overload
    def __init__(self, x0: QuoteHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, x0: base.Quote, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    @typing.overload
    def __init__(self, x0: base.Quote, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        """
        Constructs from term structures with discretization (handles created internally).
        """
class BlackSwaptionEngine(base.PricingEngine):
    """
    Shifted lognormal Black-formula swaption engine.
    """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: typing.SupportsFloat, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from constant volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, vol: base.Quote, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from quote volatility.
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: typing.SupportsFloat, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from constant volatility (handle).
        """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, vol: QuoteHandle, dayCounter: DayCounter = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from quote volatility (handle).
        """
class BlackVarianceSurface(base.BlackVarianceTermStructure):
    """
    Black volatility surface modelled as a variance surface.
    """
    def __init__(self, referenceDate: Date, calendar: Calendar, dates: collections.abc.Sequence[Date], strikes: collections.abc.Sequence[typing.SupportsFloat], blackVolMatrix: Matrix, dayCounter: DayCounter, lowerExtrapolation: BlackVarianceSurfaceExtrapolation = ..., upperExtrapolation: BlackVarianceSurfaceExtrapolation = ...) -> None:
        """
        Constructs from date/strike grid and volatility matrix.
        """
    def dayCounter(self) -> DayCounter:
        """
        Returns the day counter.
        """
    def maxDate(self) -> Date:
        """
        Returns the maximum date.
        """
    def maxStrike(self) -> float:
        """
        Returns the maximum strike.
        """
    def minStrike(self) -> float:
        """
        Returns the minimum strike.
        """
    def setInterpolation(self, interpolator: str) -> None:
        """
        Sets interpolation method. Supported: 'bilinear', 'bicubic'.
        """
class BlackVarianceSurfaceExtrapolation:
    """
    Extrapolation type for BlackVarianceSurface.
    
    Members:
    
      ConstantExtrapolation
    
      InterpolatorDefaultExtrapolation
    """
    ConstantExtrapolation: typing.ClassVar[BlackVarianceSurfaceExtrapolation]  # value = <BlackVarianceSurfaceExtrapolation.ConstantExtrapolation: 0>
    InterpolatorDefaultExtrapolation: typing.ClassVar[BlackVarianceSurfaceExtrapolation]  # value = <BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation: 1>
    __members__: typing.ClassVar[dict[str, BlackVarianceSurfaceExtrapolation]]  # value = {'ConstantExtrapolation': <BlackVarianceSurfaceExtrapolation.ConstantExtrapolation: 0>, 'InterpolatorDefaultExtrapolation': <BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BlackVolTermStructureHandle:
    """
    Handle to BlackVolTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: BlackVolTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: BlackVolTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: BlackVolTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.BlackVolTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.BlackVolTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class Bond(base.Instrument):
    """
    Base class for bonds.
    """
    class engine(base.BondGenericEngine):
        """
        Pricing engine for bonds.
        """
        def __init__(self) -> None:
            ...
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, issueDate: Date = ..., coupons: collections.abc.Sequence[base.CashFlow] = []) -> None:
        """
        Constructs from settlement days, calendar, issue date, and coupons.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, faceAmount: typing.SupportsFloat, maturityDate: Date, issueDate: Date = ..., cashflows: collections.abc.Sequence[base.CashFlow] = []) -> None:
        """
        Constructs from settlement days, calendar, face amount, maturity, issue date, and cashflows.
        """
    def accruedAmount(self, d: Date = ...) -> float:
        """
        Returns the accrued amount at date d.
        """
    @typing.overload
    def bondYield(self, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, accuracy: typing.SupportsFloat = 1e-08, maxEvaluations: typing.SupportsInt = 100, guess: typing.SupportsFloat = 0.05, priceType: BondPriceType = ...) -> float:
        """
        Calculates the yield from the engine price.
        """
    @typing.overload
    def bondYield(self, price: BondPrice, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlement: Date = ..., accuracy: typing.SupportsFloat = 1e-08, maxEvaluations: typing.SupportsInt = 100, guess: typing.SupportsFloat = 0.05) -> float:
        """
        Calculates the yield from a given price.
        """
    def calendar(self) -> Calendar:
        """
        Returns the calendar.
        """
    def cashflows(self) -> list[base.CashFlow]:
        """
        Returns all cash flows.
        """
    @typing.overload
    def cleanPrice(self) -> float:
        """
        Returns the clean price (requires pricing engine).
        """
    @typing.overload
    def cleanPrice(self, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlement: Date = ...) -> float:
        """
        Returns the clean price given a yield.
        """
    @typing.overload
    def dirtyPrice(self) -> float:
        """
        Returns the dirty price (requires pricing engine).
        """
    @typing.overload
    def dirtyPrice(self, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlement: Date = ...) -> float:
        """
        Returns the dirty price given a yield.
        """
    def isExpired(self) -> bool:
        """
        Returns True if the bond has expired.
        """
    def isTradable(self, d: Date = ...) -> bool:
        """
        Returns True if the bond is tradable at date d.
        """
    def issueDate(self) -> Date:
        """
        Returns the issue date.
        """
    def maturityDate(self) -> Date:
        """
        Returns the maturity date.
        """
    def nextCouponRate(self, d: Date = ...) -> float:
        """
        Returns the next coupon rate at date d.
        """
    def notional(self, d: Date = ...) -> float:
        """
        Returns the notional amount at date d.
        """
    def notionals(self) -> list[float]:
        """
        Returns the notional amounts.
        """
    def previousCouponRate(self, d: Date = ...) -> float:
        """
        Returns the previous coupon rate at date d.
        """
    def redemption(self) -> base.CashFlow:
        """
        Returns the single redemption cash flow.
        """
    def redemptions(self) -> list[base.CashFlow]:
        """
        Returns the redemption cash flows.
        """
    def settlementDate(self, d: Date = ...) -> Date:
        """
        Returns the settlement date for trade date d.
        """
    def settlementDays(self) -> int:
        """
        Returns the number of settlement days.
        """
    @typing.overload
    def settlementValue(self) -> float:
        """
        Returns the settlement value (requires pricing engine).
        """
    @typing.overload
    def settlementValue(self, cleanPrice: typing.SupportsFloat) -> float:
        """
        Returns the settlement value for a given clean price.
        """
    def startDate(self) -> Date:
        """
        Returns the start date.
        """
class BondFunctions:
    """
    Static bond analytics functions.
    """
    @staticmethod
    def accrualDays(bond: Bond, settlementDate: Date = ...) -> int:
        """
        Accrual days.
        """
    @staticmethod
    def accrualEndDate(bond: Bond, settlementDate: Date = ...) -> Date:
        """
        Accrual end date.
        """
    @staticmethod
    def accrualPeriod(bond: Bond, settlementDate: Date = ...) -> float:
        """
        Accrual period as a year fraction.
        """
    @staticmethod
    def accrualStartDate(bond: Bond, settlementDate: Date = ...) -> Date:
        """
        Accrual start date.
        """
    @staticmethod
    def accruedAmount(bond: Bond, settlementDate: Date = ...) -> float:
        """
        Accrued amount.
        """
    @staticmethod
    def accruedDays(bond: Bond, settlementDate: Date = ...) -> int:
        """
        Accrued days.
        """
    @staticmethod
    def accruedPeriod(bond: Bond, settlementDate: Date = ...) -> float:
        """
        Accrued period as a year fraction.
        """
    @staticmethod
    def basisPointValue(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ...) -> float:
        """
        Basis point value (DV01).
        """
    @staticmethod
    def bondYield(bond: Bond, price: BondPrice, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ..., accuracy: typing.SupportsFloat = 1e-10, maxIterations: typing.SupportsInt = 100, guess: typing.SupportsFloat = 0.05) -> float:
        """
        Bond yield (IRR) from price.
        """
    @staticmethod
    def bps(bond: Bond, discountCurve: base.YieldTermStructure, settlementDate: Date = ...) -> float:
        """
        Basis point sensitivity from discount curve.
        """
    @staticmethod
    def cleanPrice(bond: Bond, discountCurve: base.YieldTermStructure, settlementDate: Date = ...) -> float:
        """
        Clean price from discount curve.
        """
    @staticmethod
    def cleanPriceFromYield(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ...) -> float:
        """
        Clean price from yield.
        """
    @staticmethod
    def convexity(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ...) -> float:
        """
        Bond convexity.
        """
    @staticmethod
    def dirtyPrice(bond: Bond, discountCurve: base.YieldTermStructure, settlementDate: Date = ...) -> float:
        """
        Dirty price from discount curve.
        """
    @staticmethod
    def dirtyPriceFromYield(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ...) -> float:
        """
        Dirty price from yield.
        """
    @staticmethod
    def duration(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, type: DurationType = ..., settlementDate: Date = ...) -> float:
        """
        Bond duration.
        """
    @staticmethod
    def isTradable(bond: Bond, settlementDate: Date = ...) -> bool:
        """
        Whether the bond is tradable at the given date.
        """
    @staticmethod
    def maturityDate(bond: Bond) -> Date:
        """
        Maturity date of the bond.
        """
    @staticmethod
    def nextCashFlowAmount(bond: Bond, refDate: Date = ...) -> float:
        """
        Amount of the next cash flow.
        """
    @staticmethod
    def nextCashFlowDate(bond: Bond, refDate: Date = ...) -> Date:
        """
        Date of the next cash flow.
        """
    @staticmethod
    def nextCouponRate(bond: Bond, settlementDate: Date = ...) -> float:
        """
        Next coupon rate.
        """
    @staticmethod
    def previousCashFlowAmount(bond: Bond, refDate: Date = ...) -> float:
        """
        Amount of the previous cash flow.
        """
    @staticmethod
    def previousCashFlowDate(bond: Bond, refDate: Date = ...) -> Date:
        """
        Date of the previous cash flow.
        """
    @staticmethod
    def previousCouponRate(bond: Bond, settlementDate: Date = ...) -> float:
        """
        Previous coupon rate.
        """
    @staticmethod
    def startDate(bond: Bond) -> Date:
        """
        Start date of the bond.
        """
    @staticmethod
    def yieldValueBasisPoint(bond: Bond, yield: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ...) -> float:
        """
        Yield value of a basis point.
        """
    @staticmethod
    def zSpread(bond: Bond, price: BondPrice, discountCurve: base.YieldTermStructure, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, settlementDate: Date = ..., accuracy: typing.SupportsFloat = 1e-10, maxIterations: typing.SupportsInt = 100, guess: typing.SupportsFloat = 0.0) -> float:
        """
        Z-spread over a discount curve.
        """
class BondHelper(base.RateHelper):
    """
    Bond helper for bootstrapping yield curves.
    """
    @typing.overload
    def __init__(self, price: QuoteHandle, bond: ..., priceType: typing.Any = None) -> None:
        """
        Constructs from price handle and bond.
        """
    @typing.overload
    def __init__(self, price: base.Quote, bond: ..., priceType: typing.Any = None) -> None:
        """
        Constructs from quote and bond (handle created internally).
        """
    def bond(self) -> ...:
        """
        Returns the underlying bond.
        """
    def priceType(self) -> ...:
        """
        Returns the price type (Clean or Dirty).
        """
class BondPrice:
    """
    Bond price with type (clean or dirty).
    """
    def __init__(self, amount: typing.SupportsFloat, type: BondPriceType) -> None:
        """
        Constructs a bond price.
        """
    def amount(self) -> float:
        """
        Returns the price amount.
        """
    def type(self) -> BondPriceType:
        """
        Returns the price type (Clean or Dirty).
        """
class BondPriceType:
    """
    Bond price type: Clean or Dirty.
    
    Members:
    
      Clean : Clean price (excluding accrued interest).
    
      Dirty : Dirty price (including accrued interest).
    """
    Clean: typing.ClassVar[BondPriceType]  # value = <BondPriceType.Clean: 1>
    Dirty: typing.ClassVar[BondPriceType]  # value = <BondPriceType.Dirty: 0>
    __members__: typing.ClassVar[dict[str, BondPriceType]]  # value = {'Clean': <BondPriceType.Clean: 1>, 'Dirty': <BondPriceType.Dirty: 0>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Botswana(Calendar):
    """
    ! Holidays:
        From the Botswana <a href="http://www.ilo.org/dyn/travail/docs/1766/Public%20Holidays%20Act.pdf">Public Holidays Act</a>
        The days named in the Schedule shall be public holidays within Botswana:
        Provided that
        <ul>
        <li>when any of the said days fall on a Sunday the following Monday shall be observed as a public holiday;</li>
        <li>if 2nd January, 1st October or Boxing Day falls on a Monday, the following Tuesday shall be observed as a public holiday;</li>
        <li>when Botswana Day referred to in the Schedule falls on a Saturday, the next following Monday shall be observed as a public holiday.</li>
        </ul>
        <ul>
        <li>Saturdays</li>
        <li>Sundays</li>
        <li>New Year's Day, January 1st</li>
        <li>Good Friday</li>
        <li>Easter Monday</li>
        <li>Labour Day, May 1st</li>
        <li>Ascension</li>
        <li>Sir Seretse Khama Day, July 1st</li>
        <li>Presidents' Day</li>
        <li>Independence Day, September 30th</li>
        <li>Botswana Day, October 1st</li>
        <li>Christmas, December 25th </li>
        <li>Boxing Day, December 26th</li>
        </ul>
    
        \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class BoundaryConstraint(base.Constraint):
    """
    Constraint enforcing values within bounds.
    """
    def __init__(self, low: typing.SupportsFloat, high: typing.SupportsFloat) -> None:
        ...
class Brazil(Calendar):
    """
    ! Banking holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Tiradentes's Day, April 21th</li>
            <li>Labour Day, May 1st</li>
            <li>Independence Day, September 7th</li>
            <li>Nossa Sra. Aparecida Day, October 12th</li>
            <li>All Souls Day, November 2nd</li>
            <li>Republic Day, November 15th</li>
            <li>Black Awareness Day, November 20th (since 2024)</li>
            <li>Christmas, December 25th</li>
            <li>Passion of Christ</li>
            <li>Carnival</li>
            <li>Corpus Christi</li>
            </ul>
    
            Holidays for the Bovespa stock exchange
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Sao Paulo City Day, January 25th (up to 2021 included)</li>
            <li>Tiradentes's Day, April 21th</li>
            <li>Labour Day, May 1st</li>
            <li>Revolution Day, July 9th (up to 2021 included)</li>
            <li>Independence Day, September 7th</li>
            <li>Nossa Sra. Aparecida Day, October 12th</li>
            <li>All Souls Day, November 2nd</li>
            <li>Republic Day, November 15th</li>
            <li>Black Consciousness Day, November 20th (since 2007, except 2022 and 2023)</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Passion of Christ</li>
            <li>Carnival</li>
            <li>Corpus Christi</li>
            <li>the last business day of the year</li>
            </ul>
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested
                  against a list of known holidays.
    """
    class Market:
        """
        ! Brazilian calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          Exchange : !< BOVESPA calendar
        """
        Exchange: typing.ClassVar[Brazil.Market]  # value = <Market.Exchange: 1>
        Settlement: typing.ClassVar[Brazil.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, Brazil.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'Exchange': <Market.Exchange: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Exchange: typing.ClassVar[Brazil.Market]  # value = <Market.Exchange: 1>
    Settlement: typing.ClassVar[Brazil.Market]  # value = <Market.Settlement: 0>
    def __init__(self, market: Brazil.Market = ...) -> None:
        ...
class Brent:
    """
    Brent 1-D solver.
    """
    def __init__(self) -> None:
        ...
    def setLowerBound(self, lowerBound: typing.SupportsFloat) -> None:
        """
        Sets lower bound for the function domain.
        """
    def setMaxEvaluations(self, evaluations: typing.SupportsInt) -> None:
        """
        Sets maximum number of function evaluations.
        """
    def setUpperBound(self, upperBound: typing.SupportsFloat) -> None:
        """
        Sets upper bound for the function domain.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, step: typing.SupportsFloat) -> float:
        """
        Finds root with automatic bracketing.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, xMin: typing.SupportsFloat, xMax: typing.SupportsFloat) -> float:
        """
        Finds root within explicit bracket.
        """
class Business252(DayCounter):
    """
    Business/252 day count convention.
    """
    def __init__(self, c: Calendar = ...) -> None:
        ...
class BusinessDayConvention:
    """
    Conventions for adjusting dates that fall on non-business days.
    
    Members:
    
      Following : Choose the first business day after the given holiday.
    
      ModifiedFollowing : Choose the first business day after the holiday unless it belongs to a different month, in which case choose the first before.
    
      Preceding : Choose the first business day before the given holiday.
    
      ModifiedPreceding : Choose the first business day before the holiday unless it belongs to a different month, in which case choose the first after.
    
      Unadjusted : Do not adjust.
    
      HalfMonthModifiedFollowing : Choose the first business day after the holiday unless that day crosses mid-month (15th) or end of month, then choose before.
    
      Nearest : Choose the nearest business day. If equidistant, default to following.
    """
    Following: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.Following: 0>
    HalfMonthModifiedFollowing: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.HalfMonthModifiedFollowing: 5>
    ModifiedFollowing: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.ModifiedFollowing: 1>
    ModifiedPreceding: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.ModifiedPreceding: 3>
    Nearest: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.Nearest: 6>
    Preceding: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.Preceding: 2>
    Unadjusted: typing.ClassVar[BusinessDayConvention]  # value = <BusinessDayConvention.Unadjusted: 4>
    __members__: typing.ClassVar[dict[str, BusinessDayConvention]]  # value = {'Following': <BusinessDayConvention.Following: 0>, 'ModifiedFollowing': <BusinessDayConvention.ModifiedFollowing: 1>, 'Preceding': <BusinessDayConvention.Preceding: 2>, 'ModifiedPreceding': <BusinessDayConvention.ModifiedPreceding: 3>, 'Unadjusted': <BusinessDayConvention.Unadjusted: 4>, 'HalfMonthModifiedFollowing': <BusinessDayConvention.HalfMonthModifiedFollowing: 5>, 'Nearest': <BusinessDayConvention.Nearest: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CADCurrency(Currency):
    """
    ! The ISO three-letter code is CAD; the numeric code is 124.
            It is divided into 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class CHFCurrency(Currency):
    """
    ! The ISO three-letter code is CHF; the numeric code is 756.
            It is divided into 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class CLFCurrency(Currency):
    """
    ! Unidad de Fomento (funds code)
    /*! The ISO three-letter code is CLF; the numeric code is 990.
         A unit of account used in Chile.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class CLPCurrency(Currency):
    """
    ! The ISO three-letter code is CLP; the numeric code is 152.
            It is divided in 100 centavos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class CNHCurrency(Currency):
    """
    ! Chinese yuan (Hong Kong)
    /*! The ISO three-letter code is CNH; there is no numeric code.
         It is divided in 100 fen.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class CNYCurrency(Currency):
    """
    ! The ISO three-letter code is CNY; the numeric code is 156.
            It is divided in 100 fen.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class COPCurrency(Currency):
    """
    ! The ISO three-letter code is COP; the numeric code is 170.
            It is divided in 100 centavos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class COUCurrency(Currency):
    """
    ! Unidad de Valor Real
    /*! The ISO three-letter code is COU; the numeric code is 970.
         A unit of account used in Colombia.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class CPI:
    """
    CPI interpolation methods and utilities.
    """
    class InterpolationType:
        """
        CPI interpolation type.
        
        Members:
        
          AsIndex : Same interpolation as the index.
        
          Flat : Flat from previous fixing.
        
          Linear : Linearly between bracketing fixings.
        """
        AsIndex: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.AsIndex: 0>
        Flat: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.Flat: 1>
        Linear: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.Linear: 2>
        __members__: typing.ClassVar[dict[str, CPI.InterpolationType]]  # value = {'AsIndex': <InterpolationType.AsIndex: 0>, 'Flat': <InterpolationType.Flat: 1>, 'Linear': <InterpolationType.Linear: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    AsIndex: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.AsIndex: 0>
    Flat: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.Flat: 1>
    Linear: typing.ClassVar[CPI.InterpolationType]  # value = <InterpolationType.Linear: 2>
    @staticmethod
    def laggedFixing(index: ..., date: Date, observationLag: Period, interpolationType: CPI.InterpolationType) -> float:
        """
        Returns the lagged CPI fixing.
        """
class CYPCurrency(Currency):
    """
    ! The ISO three-letter code is CYP; the numeric code is 196.
            It is divided in 100 cents.
    
            Obsoleted by the Euro since 2008.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class CZKCurrency(Currency):
    """
    ! The ISO three-letter code is CZK; the numeric code is 203.
            It is divided in 100 haleru.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class Calendar:
    """
    Calendar class for determining business days and holidays for a given market.
    """
    def __eq__(self, arg0: Calendar) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self) -> None:
        ...
    def __ne__(self, arg0: Calendar) -> bool:
        ...
    def __str__(self) -> str:
        ...
    def addHoliday(self, d: Date) -> None:
        """
        Adds a date to the set of holidays for the given calendar.
        """
    def addedHolidays(self) -> set[Date]:
        """
        Returns the set of added holidays for the given calendar.
        """
    def adjust(self, d: Date, convention: BusinessDayConvention = ...) -> Date:
        """
        Adjusts a non-business day to the appropriate nearby business day.
        """
    @typing.overload
    def advance(self, d: Date, n: typing.SupportsInt, unit: TimeUnit, convention: BusinessDayConvention = ..., endOfMonth: bool = False) -> Date:
        """
        Advances the date by the given number of time units.
        """
    @typing.overload
    def advance(self, d: Date, period: Period, convention: BusinessDayConvention = ..., endOfMonth: bool = False) -> Date:
        """
        Advances the date by the given period.
        """
    def businessDayList(self, from_: Date, to: Date) -> list[Date]:
        """
        Returns the business days between two dates.
        """
    def businessDaysBetween(self, from_: Date, to: Date, includeFirst: bool = True, includeLast: bool = False) -> int:
        """
        Calculates the number of business days between two dates.
        """
    def empty(self) -> bool:
        """
        Returns whether or not the calendar is initialized.
        """
    def endOfMonth(self, d: Date) -> Date:
        """
        Last business day of the month to which the given date belongs.
        """
    def holidayList(self, from_: Date, to: Date, includeWeekEnds: bool = False) -> list[Date]:
        """
        Returns the holidays between two dates.
        """
    def isBusinessDay(self, d: Date) -> bool:
        """
        Returns True if the date is a business day.
        """
    def isEndOfMonth(self, d: Date) -> bool:
        """
        Returns True if the date is on or after the last business day of its month.
        """
    def isHoliday(self, d: Date) -> bool:
        """
        Returns True if the date is a holiday.
        """
    def isStartOfMonth(self, d: Date) -> bool:
        """
        Returns True if the date is on or before the first business day of its month.
        """
    def isWeekend(self, w: Weekday) -> bool:
        """
        Returns True if the weekday is part of the weekend.
        """
    def name(self) -> str:
        """
        Returns the name of the calendar.
        """
    def removeHoliday(self, d: Date) -> None:
        """
        Removes a date from the set of holidays for the given calendar.
        """
    def removedHolidays(self) -> set[Date]:
        """
        Returns the set of removed holidays for the given calendar.
        """
    def resetAddedAndRemovedHolidays(self) -> None:
        """
        Clear the set of added and removed holidays.
        """
    def startOfMonth(self, d: Date) -> Date:
        """
        First business day of the month to which the given date belongs.
        """
class CalendarVector:
    """
    A vector of Calendar objects, exposed as a Python list.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Calendar) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, arg0: CalendarVector) -> bool:
        ...
    @typing.overload
    def __getitem__(self, s: slice) -> CalendarVector:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> Calendar:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: CalendarVector) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator[Calendar]:
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, arg0: CalendarVector) -> bool:
        ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: Calendar) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CalendarVector) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Calendar) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Calendar) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: CalendarVector) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: typing.SupportsInt, x: Calendar) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Calendar:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> Calendar:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Calendar) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
class CalibrationErrorType:
    """
    Type of calibration error calculation.
    
    Members:
    
      RelativePriceError
    
      PriceError
    
      ImpliedVolError
    """
    ImpliedVolError: typing.ClassVar[CalibrationErrorType]  # value = <CalibrationErrorType.ImpliedVolError: 2>
    PriceError: typing.ClassVar[CalibrationErrorType]  # value = <CalibrationErrorType.PriceError: 1>
    RelativePriceError: typing.ClassVar[CalibrationErrorType]  # value = <CalibrationErrorType.RelativePriceError: 0>
    __members__: typing.ClassVar[dict[str, CalibrationErrorType]]  # value = {'RelativePriceError': <CalibrationErrorType.RelativePriceError: 0>, 'PriceError': <CalibrationErrorType.PriceError: 1>, 'ImpliedVolError': <CalibrationErrorType.ImpliedVolError: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Canada(Calendar):
    """
    ! Banking holidays
            (data from <http://www.bankofcanada.ca/en/about/holiday.html>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Family Day, third Monday of February (since 2008)</li>
            <li>Good Friday</li>
            <li>Victoria Day, the Monday on or preceding May 24th</li>
            <li>Canada Day, July 1st (possibly moved to Monday)</li>
            <li>Provincial Holiday, first Monday of August</li>
            <li>Labour Day, first Monday of September</li>
            <li>National Day for Truth and Reconciliation, September 30th (possibly moved to Monday)</li>
            <li>Thanksgiving Day, second Monday of October</li>
            <li>Remembrance Day, November 11th (possibly moved to Monday)</li>
            <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            </ul>
    
            Holidays for the Toronto stock exchange
            (data from <http://www.tsx.com/en/about_tsx/market_hours.html>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Family Day, third Monday of February (since 2008)</li>
            <li>Good Friday</li>
            <li>Victoria Day, the Monday on or preceding May 24th</li>
            <li>Canada Day, July 1st (possibly moved to Monday)</li>
            <li>Provincial Holiday, first Monday of August</li>
            <li>Labour Day, first Monday of September</li>
            <li>Thanksgiving Day, second Monday of October</li>
            <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          TSX : !< Toronto stock exchange calendar
        """
        Settlement: typing.ClassVar[Canada.Market]  # value = <Market.Settlement: 0>
        TSX: typing.ClassVar[Canada.Market]  # value = <Market.TSX: 1>
        __members__: typing.ClassVar[dict[str, Canada.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'TSX': <Market.TSX: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Settlement: typing.ClassVar[Canada.Market]  # value = <Market.Settlement: 0>
    TSX: typing.ClassVar[Canada.Market]  # value = <Market.TSX: 1>
    def __init__(self, market: Canada.Market = ...) -> None:
        ...
class Cap(CapFloor):
    """
    Interest rate cap.
    """
    def __init__(self, floatingLeg: collections.abc.Sequence[base.CashFlow], exerciseRates: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs a cap.
        """
class CapFloor(base.Instrument):
    """
    Interest rate cap, floor, or collar.
    """
    @typing.overload
    def __init__(self, type: CapFloorType, floatingLeg: collections.abc.Sequence[base.CashFlow], capRates: collections.abc.Sequence[typing.SupportsFloat], floorRates: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs a cap/floor/collar.
        """
    @typing.overload
    def __init__(self, type: CapFloorType, floatingLeg: collections.abc.Sequence[base.CashFlow], strikes: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs a cap or floor with uniform strikes.
        """
    def atmRate(self, discountCurve: base.YieldTermStructure) -> float:
        """
        Returns the ATM rate.
        """
    def capRates(self) -> list[float]:
        """
        Returns the cap rates.
        """
    def floatingLeg(self) -> list[base.CashFlow]:
        """
        Returns the floating leg.
        """
    def floorRates(self) -> list[float]:
        """
        Returns the floor rates.
        """
    def impliedVolatility(self, price: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, guess: typing.SupportsFloat, accuracy: typing.SupportsFloat = 0.0001, maxEvaluations: typing.SupportsInt = 100, minVol: typing.SupportsFloat = 1e-07, maxVol: typing.SupportsFloat = 4.0, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> float:
        """
        Returns the implied volatility.
        """
    def isExpired(self) -> bool:
        """
        Returns True if expired.
        """
    def maturityDate(self) -> Date:
        """
        Returns the maturity date.
        """
    def startDate(self) -> Date:
        """
        Returns the start date.
        """
    def type(self) -> CapFloorType:
        """
        Returns the cap/floor type.
        """
class CapFloorTermVolSurface(base.LazyObject, base.CapFloorTermVolatilityStructure):
    """
    Cap/floor smile volatility surface.
    """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], strikes: collections.abc.Sequence[typing.SupportsFloat], volatilities: Matrix, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from settlement days and volatility matrix.
        """
    @typing.overload
    def __init__(self, settlementDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], strikes: collections.abc.Sequence[typing.SupportsFloat], volatilities: Matrix, dayCounter: DayCounter = ...) -> None:
        """
        Constructs from settlement date and volatility matrix.
        """
    def maxDate(self) -> Date:
        """
        Returns the maximum date.
        """
    def maxStrike(self) -> float:
        """
        Returns the maximum strike.
        """
    def minStrike(self) -> float:
        """
        Returns the minimum strike.
        """
    def optionDates(self) -> list[Date]:
        """
        Returns the option dates.
        """
    def optionTenors(self) -> list[Period]:
        """
        Returns the option tenors.
        """
    def optionTimes(self) -> list[float]:
        """
        Returns the option times.
        """
    def strikes(self) -> list[float]:
        """
        Returns the strikes.
        """
class CapFloorType:
    """
    Cap/floor type.
    
    Members:
    
      Cap
    
      Floor
    
      Collar
    """
    Cap: typing.ClassVar[CapFloorType]  # value = <CapFloorType.Cap: 0>
    Collar: typing.ClassVar[CapFloorType]  # value = <CapFloorType.Collar: 2>
    Floor: typing.ClassVar[CapFloorType]  # value = <CapFloorType.Floor: 1>
    __members__: typing.ClassVar[dict[str, CapFloorType]]  # value = {'Cap': <CapFloorType.Cap: 0>, 'Floor': <CapFloorType.Floor: 1>, 'Collar': <CapFloorType.Collar: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CashDividendModel:
    """
    Cash dividend model for finite difference engines.
    
    Members:
    
      Spot : Spot adjustment model.
    
      Escrowed : Escrowed dividend model.
    """
    Escrowed: typing.ClassVar[CashDividendModel]  # value = <CashDividendModel.Escrowed: 1>
    Spot: typing.ClassVar[CashDividendModel]  # value = <CashDividendModel.Spot: 0>
    __members__: typing.ClassVar[dict[str, CashDividendModel]]  # value = {'Spot': <CashDividendModel.Spot: 0>, 'Escrowed': <CashDividendModel.Escrowed: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CashOrNothingPayoff(base.StrikedTypePayoff):
    """
    Binary payoff: fixed cash amount if in the money, zero otherwise.
    """
    def __init__(self, type: OptionType, strike: typing.SupportsFloat, cashPayoff: typing.SupportsFloat) -> None:
        ...
    def cashPayoff(self) -> float:
        """
        Returns the cash payoff amount.
        """
class CdsPricingModel:
    """
    CDS pricing model.
    
    Members:
    
      Midpoint : Midpoint model.
    
      ISDA : ISDA standard model.
    """
    ISDA: typing.ClassVar[CdsPricingModel]  # value = <CdsPricingModel.ISDA: 1>
    Midpoint: typing.ClassVar[CdsPricingModel]  # value = <CdsPricingModel.Midpoint: 0>
    __members__: typing.ClassVar[dict[str, CdsPricingModel]]  # value = {'Midpoint': <CdsPricingModel.Midpoint: 0>, 'ISDA': <CdsPricingModel.ISDA: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CeilingTruncation(Rounding):
    """
    Ceiling truncation.
    """
    def __init__(self, precision: typing.SupportsInt, digit: typing.SupportsInt = 5) -> None:
        ...
class ChfLiborSwapIsdaFix(SwapIndex):
    """
    CHF LIBOR swap rate (ISDA fix).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class Chile(Calendar):
    """
    ! Holidays for the Santiago Stock Exchange
            (data from <https://en.wikipedia.org/wiki/Public_holidays_in_Chile>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>January 2nd, when falling on a Monday (since 2017)</li>
            <li>Good Friday</li>
            <li>Easter Saturday</li>
            <li>Labour Day, May 1st</li>
            <li>Navy Day, May 21st</li>
            <li>Day of Aboriginal People, around June 21st (observed on each Winter Solstice) (since 2021)</li>
            <li>Saint Peter and Saint Paul, June 29th (moved to the nearest Monday if it falls on a weekday)</li>
            <li>Our Lady of Mount Carmel, July 16th</li>
            <li>Assumption Day, August 15th</li>
            <li>Independence Day, September 18th (also the 17th if the latter falls on a Monday or Friday)</li>
            <li>Army Day, September 19th (also the 20th if the latter falls on a Friday)</li>
            <li>Discovery of Two Worlds, October 12th (moved to the nearest Monday if it falls on a weekday)</li>
            <li>Reformation Day, October 31st (since 2008; moved to the preceding Friday if it falls on a Tuesday,
                or to the following Friday if it falls on a Wednesday)</li>
            <li>All Saints' Day, November 1st</li>
            <li>Immaculate Conception, December 8th</li>
            <li>Christmas Day, December 25th</li>
            <li>New Year's Eve, December 31st; (see https://www.cmfchile.cl/portal/prensa/615/w3-article-49984.html)</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          SSE : !< Santiago Stock Exchange
        """
        SSE: typing.ClassVar[Chile.Market]  # value = <Market.SSE: 0>
        __members__: typing.ClassVar[dict[str, Chile.Market]]  # value = {'SSE': <Market.SSE: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    SSE: typing.ClassVar[Chile.Market]  # value = <Market.SSE: 0>
    def __init__(self, m: Chile.Market = ...) -> None:
        ...
class China(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's day, January 1st (possibly followed by one or
                two more holidays)</li>
            <li>Labour Day, first week in May</li>
            <li>National Day, one week from October 1st</li>
            </ul>
    
            Other holidays for which no rule is given (data available for
            2004-2019 only):
            <ul>
            <li>Chinese New Year</li>
            <li>Ching Ming Festival</li>
            <li>Tuen Ng Festival</li>
            <li>Mid-Autumn Festival</li>
            <li>70th anniversary of the victory of anti-Japaneses war</li>
            </ul>
    
            SSE data from <http://www.sse.com.cn/>
            IB data from <http://www.chinamoney.com.cn/>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          SSE : !< Shanghai stock exchange
        
          IB : !< Interbank calendar
        """
        IB: typing.ClassVar[China.Market]  # value = <Market.IB: 1>
        SSE: typing.ClassVar[China.Market]  # value = <Market.SSE: 0>
        __members__: typing.ClassVar[dict[str, China.Market]]  # value = {'SSE': <Market.SSE: 0>, 'IB': <Market.IB: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    IB: typing.ClassVar[China.Market]  # value = <Market.IB: 1>
    SSE: typing.ClassVar[China.Market]  # value = <Market.SSE: 0>
    def __init__(self, m: China.Market = ...) -> None:
        ...
class ClosestRounding(Rounding):
    """
    Closest-rounding.
    """
    def __init__(self, precision: typing.SupportsInt, digit: typing.SupportsInt = 5) -> None:
        ...
class CmsCoupon(FloatingRateCoupon):
    """
    Coupon paying a CMS swap rate.
    """
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, startDate: Date, endDate: Date, fixingDays: typing.SupportsInt, index: ..., gearing: typing.SupportsFloat = 1.0, spread: typing.SupportsFloat = 0.0, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., dayCounter: typing.Any = None, isInArrears: bool = False, exCouponDate: Date = ...) -> None:
        """
        Constructs a CMS coupon.
        """
    def swapIndex(self) -> ...:
        """
        Returns the underlying swap index.
        """
class CmsLeg:
    """
    Helper class for building a leg of CMS coupons.
    """
    def __init__(self, schedule: Schedule, swapIndex: ...) -> None:
        """
        Constructs a CmsLeg from a schedule and swap index.
        """
    def build(self) -> list[base.CashFlow]:
        """
        Builds and returns the leg of cash flows.
        """
    def inArrears(self, flag: bool = True) -> CmsLeg:
        ...
    @typing.overload
    def withCaps(self, cap: typing.SupportsFloat) -> CmsLeg:
        ...
    @typing.overload
    def withCaps(self, caps: collections.abc.Sequence[typing.SupportsFloat]) -> CmsLeg:
        ...
    def withExCouponPeriod(self, period: Period, calendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool = False) -> CmsLeg:
        ...
    @typing.overload
    def withFixingDays(self, fixingDays: typing.SupportsInt) -> CmsLeg:
        ...
    @typing.overload
    def withFixingDays(self, fixingDays: collections.abc.Sequence[typing.SupportsInt]) -> CmsLeg:
        ...
    @typing.overload
    def withFloors(self, floor: typing.SupportsFloat) -> CmsLeg:
        ...
    @typing.overload
    def withFloors(self, floors: collections.abc.Sequence[typing.SupportsFloat]) -> CmsLeg:
        ...
    @typing.overload
    def withGearings(self, gearing: typing.SupportsFloat) -> CmsLeg:
        ...
    @typing.overload
    def withGearings(self, gearings: collections.abc.Sequence[typing.SupportsFloat]) -> CmsLeg:
        ...
    @typing.overload
    def withNotionals(self, nominal: typing.SupportsFloat) -> CmsLeg:
        ...
    @typing.overload
    def withNotionals(self, nominals: collections.abc.Sequence[typing.SupportsFloat]) -> CmsLeg:
        ...
    def withPaymentAdjustment(self, convention: BusinessDayConvention) -> CmsLeg:
        ...
    def withPaymentDayCounter(self, dayCounter: DayCounter) -> CmsLeg:
        ...
    @typing.overload
    def withSpreads(self, spread: typing.SupportsFloat) -> CmsLeg:
        ...
    @typing.overload
    def withSpreads(self, spreads: collections.abc.Sequence[typing.SupportsFloat]) -> CmsLeg:
        ...
    def withZeroPayments(self, flag: bool = True) -> CmsLeg:
        ...
class Collar(CapFloor):
    """
    Interest rate collar.
    """
    def __init__(self, floatingLeg: collections.abc.Sequence[base.CashFlow], capRates: collections.abc.Sequence[typing.SupportsFloat], floorRates: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs a collar.
        """
class ComplexLogFormula:
    """
    Formula for complex logarithm in Heston integration.
    
    Members:
    
      Gatheral
    
      BranchCorrection
    
      AndersenPiterbarg
    
      AndersenPiterbargOptCV
    
      AsymptoticChF
    
      AngledContour
    
      AngledContourNoCV
    
      OptimalCV
    """
    AndersenPiterbarg: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.AndersenPiterbarg: 2>
    AndersenPiterbargOptCV: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.AndersenPiterbargOptCV: 3>
    AngledContour: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.AngledContour: 5>
    AngledContourNoCV: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.AngledContourNoCV: 6>
    AsymptoticChF: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.AsymptoticChF: 4>
    BranchCorrection: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.BranchCorrection: 1>
    Gatheral: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.Gatheral: 0>
    OptimalCV: typing.ClassVar[ComplexLogFormula]  # value = <ComplexLogFormula.OptimalCV: 7>
    __members__: typing.ClassVar[dict[str, ComplexLogFormula]]  # value = {'Gatheral': <ComplexLogFormula.Gatheral: 0>, 'BranchCorrection': <ComplexLogFormula.BranchCorrection: 1>, 'AndersenPiterbarg': <ComplexLogFormula.AndersenPiterbarg: 2>, 'AndersenPiterbargOptCV': <ComplexLogFormula.AndersenPiterbargOptCV: 3>, 'AsymptoticChF': <ComplexLogFormula.AsymptoticChF: 4>, 'AngledContour': <ComplexLogFormula.AngledContour: 5>, 'AngledContourNoCV': <ComplexLogFormula.AngledContourNoCV: 6>, 'OptimalCV': <ComplexLogFormula.OptimalCV: 7>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CompositeConstraint(base.Constraint):
    """
    Composite of two constraints.
    """
    def __init__(self, c1: base.Constraint, c2: base.Constraint) -> None:
        ...
class CompositeInstrument(base.Instrument):
    """
    Aggregate of instruments with weighted NPVs.
    """
    def __init__(self) -> None:
        """
        Constructs an empty composite instrument.
        """
    def add(self, instrument: base.Instrument, multiplier: typing.SupportsFloat = 1.0) -> None:
        """
        Adds an instrument with a multiplier.
        """
    def isExpired(self) -> bool:
        """
        Returns whether all components are expired.
        """
    def subtract(self, instrument: base.Instrument, multiplier: typing.SupportsFloat = 1.0) -> None:
        """
        Subtracts an instrument with a multiplier.
        """
class CompositeQuote(base.Quote):
    """
    Quote composed from two quotes using a binary function.
    """
    def __init__(self, quote1: QuoteHandle, quote2: QuoteHandle, function: collections.abc.Callable) -> None:
        """
        Creates a composite quote from two quotes and a Python function.
        """
class Compounding:
    """
    Interest rate compounding rule.
    
    Members:
    
      Simple : 1 + r*t
    
      Compounded : (1 + r)^t
    
      Continuous : e^(r*t)
    
      SimpleThenCompounded : Simple up to the first period, then Compounded.
    
      CompoundedThenSimple : Compounded up to the first period, then Simple.
    """
    Compounded: typing.ClassVar[Compounding]  # value = <Compounding.Compounded: 1>
    CompoundedThenSimple: typing.ClassVar[Compounding]  # value = <Compounding.CompoundedThenSimple: 4>
    Continuous: typing.ClassVar[Compounding]  # value = <Compounding.Continuous: 2>
    Simple: typing.ClassVar[Compounding]  # value = <Compounding.Simple: 0>
    SimpleThenCompounded: typing.ClassVar[Compounding]  # value = <Compounding.SimpleThenCompounded: 3>
    __members__: typing.ClassVar[dict[str, Compounding]]  # value = {'Simple': <Compounding.Simple: 0>, 'Compounded': <Compounding.Compounded: 1>, 'Continuous': <Compounding.Continuous: 2>, 'SimpleThenCompounded': <Compounding.SimpleThenCompounded: 3>, 'CompoundedThenSimple': <Compounding.CompoundedThenSimple: 4>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ConstantOptionletVolatility(base.OptionletVolatilityStructure):
    """
    Constant optionlet volatility, no time-strike dependence.
    """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: typing.SupportsFloat, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and constant volatility.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: typing.SupportsFloat, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and constant volatility.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: QuoteHandle, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: QuoteHandle, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: base.Quote, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: base.Quote, dayCounter: DayCounter, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and quote (handle created internally).
        """
class ConstantParameter(Parameter):
    """
    Time-constant parameter.
    """
    @typing.overload
    def __init__(self, constraint: base.Constraint) -> None:
        ...
    @typing.overload
    def __init__(self, value: typing.SupportsFloat, constraint: base.Constraint) -> None:
        ...
class ConstantSwaptionVolatility(base.SwaptionVolatilityStructure):
    """
    Constant swaption volatility, no time-strike dependence.
    """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: typing.SupportsFloat, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and constant volatility.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: typing.SupportsFloat, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and constant volatility.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: QuoteHandle, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: QuoteHandle, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: base.Quote, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from settlement days and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, volatility: base.Quote, dayCounter: DayCounter, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs from reference date and quote (handle created internally).
        """
    def volatilityType(self) -> VolatilityType:
        """
        Returns the volatility type.
        """
class ContinuousAveragingAsianOption(base.OneAssetOption):
    """
    Continuous-averaging Asian option.
    """
    def __init__(self, averageType: AverageType, payoff: base.StrikedTypePayoff, exercise: Exercise) -> None:
        """
        Constructs ContinuousAveragingAsianOption.
        """
class CreditDefaultSwap(base.Instrument):
    """
    Credit default swap.
    """
    @typing.overload
    def __init__(self, side: ProtectionSide, notional: typing.SupportsFloat, spread: typing.SupportsFloat, schedule: Schedule, paymentConvention: BusinessDayConvention, dayCounter: DayCounter, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, protectionStart: Date = ..., claim: base.Claim = None, lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, tradeDate: Date = ..., cashSettlementDays: typing.SupportsInt = 3) -> None:
        """
        Constructs CDS quoted as running spread only.
        """
    @typing.overload
    def __init__(self, side: ProtectionSide, notional: typing.SupportsFloat, upfront: typing.SupportsFloat, spread: typing.SupportsFloat, schedule: Schedule, paymentConvention: BusinessDayConvention, dayCounter: DayCounter, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, protectionStart: Date = ..., upfrontDate: Date = ..., claim: base.Claim = None, lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, tradeDate: Date = ..., cashSettlementDays: typing.SupportsInt = 3) -> None:
        """
        Constructs CDS quoted as upfront and running spread.
        """
    def accrualRebateNPV(self) -> float:
        """
        Accrual rebate NPV.
        """
    def conventionalSpread(self, conventionalRecovery: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, dayCounter: DayCounter, model: CdsPricingModel = ...) -> float:
        """
        Conventional spread.
        """
    def couponLegBPS(self) -> float:
        """
        Coupon leg BPS.
        """
    def couponLegNPV(self) -> float:
        """
        Coupon leg NPV.
        """
    def coupons(self) -> list[base.CashFlow]:
        """
        Coupon leg.
        """
    def defaultLegNPV(self) -> float:
        """
        Default leg NPV.
        """
    def fairSpread(self) -> float:
        """
        Fair running spread.
        """
    def fairUpfront(self) -> float:
        """
        Fair upfront.
        """
    def impliedHazardRate(self, targetNPV: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, dayCounter: DayCounter, recoveryRate: typing.SupportsFloat = 0.4, accuracy: typing.SupportsFloat = 1e-08, model: CdsPricingModel = ...) -> float:
        """
        Implied hazard rate.
        """
    def isExpired(self) -> bool:
        """
        Whether the CDS has expired.
        """
    def notional(self) -> float:
        """
        Notional.
        """
    def paysAtDefaultTime(self) -> bool:
        """
        Whether default payment is at default time.
        """
    def protectionEndDate(self) -> Date:
        """
        Protection end date.
        """
    def protectionStartDate(self) -> Date:
        """
        Protection start date.
        """
    def rebatesAccrual(self) -> bool:
        """
        Whether accrual is rebated.
        """
    def runningSpread(self) -> float:
        """
        Running spread.
        """
    def settlesAccrual(self) -> bool:
        """
        Whether accrual is settled on default.
        """
    def side(self) -> ProtectionSide:
        """
        Protection side.
        """
    def upfrontBPS(self) -> float:
        """
        Upfront BPS.
        """
    def upfrontNPV(self) -> float:
        """
        Upfront NPV.
        """
class CubicBSplinesFitting(base.FittingMethod):
    """
    Cubic B-splines fitting method.
    """
    def __init__(self, knotVector: collections.abc.Sequence[typing.SupportsFloat], constrainAtZero: bool = True, weights: Array = ..., optimizationMethod: base.OptimizationMethod = None, l2: Array = ..., minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308, constraint: base.Constraint = ...) -> None:
        """
        Constructs a cubic B-splines fitting method.
        """
    def basisFunction(self, i: typing.SupportsInt, t: typing.SupportsFloat) -> float:
        """
        Returns the i-th basis function value at time t.
        """
class CubicBoundaryCondition:
    """
    Boundary conditions for cubic interpolation.
    
    Members:
    
      NotAKnot
    
      FirstDerivative
    
      SecondDerivative
    
      Periodic
    
      Lagrange
    """
    FirstDerivative: typing.ClassVar[CubicBoundaryCondition]  # value = <CubicBoundaryCondition.FirstDerivative: 1>
    Lagrange: typing.ClassVar[CubicBoundaryCondition]  # value = <CubicBoundaryCondition.Lagrange: 4>
    NotAKnot: typing.ClassVar[CubicBoundaryCondition]  # value = <CubicBoundaryCondition.NotAKnot: 0>
    Periodic: typing.ClassVar[CubicBoundaryCondition]  # value = <CubicBoundaryCondition.Periodic: 3>
    SecondDerivative: typing.ClassVar[CubicBoundaryCondition]  # value = <CubicBoundaryCondition.SecondDerivative: 2>
    __members__: typing.ClassVar[dict[str, CubicBoundaryCondition]]  # value = {'NotAKnot': <CubicBoundaryCondition.NotAKnot: 0>, 'FirstDerivative': <CubicBoundaryCondition.FirstDerivative: 1>, 'SecondDerivative': <CubicBoundaryCondition.SecondDerivative: 2>, 'Periodic': <CubicBoundaryCondition.Periodic: 3>, 'Lagrange': <CubicBoundaryCondition.Lagrange: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CubicDerivativeApprox:
    """
    Derivative approximation methods for cubic interpolation.
    
    Members:
    
      Spline
    
      SplineOM1
    
      SplineOM2
    
      FourthOrder
    
      Parabolic
    
      FritschButland
    
      Akima
    
      Kruger
    
      Harmonic
    """
    Akima: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.Akima: 6>
    FourthOrder: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.FourthOrder: 3>
    FritschButland: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.FritschButland: 5>
    Harmonic: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.Harmonic: 8>
    Kruger: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.Kruger: 7>
    Parabolic: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.Parabolic: 4>
    Spline: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.Spline: 0>
    SplineOM1: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.SplineOM1: 1>
    SplineOM2: typing.ClassVar[CubicDerivativeApprox]  # value = <CubicDerivativeApprox.SplineOM2: 2>
    __members__: typing.ClassVar[dict[str, CubicDerivativeApprox]]  # value = {'Spline': <CubicDerivativeApprox.Spline: 0>, 'SplineOM1': <CubicDerivativeApprox.SplineOM1: 1>, 'SplineOM2': <CubicDerivativeApprox.SplineOM2: 2>, 'FourthOrder': <CubicDerivativeApprox.FourthOrder: 3>, 'Parabolic': <CubicDerivativeApprox.Parabolic: 4>, 'FritschButland': <CubicDerivativeApprox.FritschButland: 5>, 'Akima': <CubicDerivativeApprox.Akima: 6>, 'Kruger': <CubicDerivativeApprox.Kruger: 7>, 'Harmonic': <CubicDerivativeApprox.Harmonic: 8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class CubicInterpolation(base.Interpolation):
    """
    Cubic interpolation between discrete points.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat], derivativeApprox: CubicDerivativeApprox = ..., monotonic: bool = False, leftCondition: CubicBoundaryCondition = ..., leftConditionValue: typing.SupportsFloat = 0.0, rightCondition: CubicBoundaryCondition = ..., rightConditionValue: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs cubic interpolation from x and y arrays.
        """
class CubicNaturalSpline(base.Interpolation):
    """
    Natural cubic spline interpolation.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs interpolation from x and y arrays.
        """
class CumulativeNormalDistribution:
    """
    Cumulative normal distribution function.
    """
    def __call__(self, x: typing.SupportsFloat) -> float:
        """
        Returns the cumulative probability at x.
        """
    def __init__(self, average: typing.SupportsFloat = 0.0, sigma: typing.SupportsFloat = 1.0) -> None:
        """
        Constructs CumulativeNormalDistribution.
        """
    def derivative(self, x: typing.SupportsFloat) -> float:
        """
        Returns the derivative (density) at x.
        """
class Currency:
    """
    Currency specification.
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Currency) -> bool:
        ...
    def __init__(self) -> None:
        """
        Default constructor, creates an empty currency.
        """
    def __ne__(self, arg0: Currency) -> bool:
        ...
    def code(self) -> str:
        """
        Returns the ISO 4217 three-letter code, e.g., 'USD'.
        """
    def empty(self) -> bool:
        """
        Returns true if this is an empty (uninitialized) currency.
        """
    def fractionSymbol(self) -> str:
        """
        Returns the fraction symbol, e.g., 'c' for cents.
        """
    def fractionsPerUnit(self) -> int:
        """
        Returns the number of fractional units per currency unit, e.g., 100.
        """
    def name(self) -> str:
        """
        Returns the full currency name, e.g., 'U.S. Dollar'.
        """
    def numericCode(self) -> int:
        """
        Returns the ISO 4217 numeric code, e.g., 840.
        """
    def rounding(self) -> Rounding:
        """
        Returns the rounding convention for this currency.
        """
    def symbol(self) -> str:
        """
        Returns the currency symbol, e.g., '$'.
        """
    def triangulationCurrency(self) -> Currency:
        """
        Returns the triangulation currency, if any.
        """
class CustomRegion(Region):
    """
    Custom region with user-defined name and code.
    """
    def __init__(self, name: str, code: str) -> None:
        """
        Constructs a custom region.
        """
class CzechRepublic(Calendar):
    """
    ! Holidays for the Prague stock exchange (see http://www.pse.cz/):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Liberation Day, May 8th</li>
            <li>SS. Cyril and Methodius, July 5th</li>
            <li>Jan Hus Day, July 6th</li>
            <li>Czech Statehood Day, September 28th</li>
            <li>Independence Day, October 28th</li>
            <li>Struggle for Freedom and Democracy Day, November 17th</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          PSE : !< Prague stock exchange
        """
        PSE: typing.ClassVar[CzechRepublic.Market]  # value = <Market.PSE: 0>
        __members__: typing.ClassVar[dict[str, CzechRepublic.Market]]  # value = {'PSE': <Market.PSE: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    PSE: typing.ClassVar[CzechRepublic.Market]  # value = <Market.PSE: 0>
    def __init__(self, m: CzechRepublic.Market = ...) -> None:
        ...
class DASHCurrency(Currency):
    """
    ! https://www.dash.org/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class DEMCurrency(Currency):
    """
    ! The ISO three-letter code was DEM; the numeric code was 276.
            It was divided into 100 pfennig.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class DKKCurrency(Currency):
    """
    ! The ISO three-letter code is DKK; the numeric code is 208.
            It is divided in 100 �re.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class Date:
    """
    Date class for date algebra and calendar operations.
    """
    @staticmethod
    def endOfMonth(d: Date) -> Date:
        """
        Last day of the month to which the given date belongs.
        """
    @staticmethod
    def from_date(arg0: typing.Any) -> Date:
        ...
    @staticmethod
    def isEndOfMonth(d: Date) -> bool:
        """
        Whether a date is the last day of its month.
        """
    @staticmethod
    def isLeap(y: typing.SupportsInt) -> bool:
        """
        Whether the given year is a leap one.
        """
    @staticmethod
    def isStartOfMonth(d: Date) -> bool:
        """
        Whether a date is the first day of its month.
        """
    @staticmethod
    def maxDate() -> Date:
        """
        Latest allowed date.
        """
    @staticmethod
    def minDate() -> Date:
        """
        Earliest allowed date.
        """
    @staticmethod
    def nextWeekday(d: Date, w: Weekday) -> Date:
        """
        Next given weekday following the given date.
        """
    @staticmethod
    def nthWeekday(n: typing.SupportsInt, w: Weekday, m: Month, y: typing.SupportsInt) -> Date:
        """
        The n-th given weekday in the given month and year.
        """
    @staticmethod
    def startOfMonth(d: Date) -> Date:
        """
        First day of the month to which the given date belongs.
        """
    @staticmethod
    def todaysDate() -> Date:
        """
        Today's date.
        """
    @typing.overload
    def __add__(self, days: typing.SupportsInt) -> Date:
        """
        Return a new date incremented by the given number of days.
        """
    @typing.overload
    def __add__(self, period: ...) -> Date:
        """
        Return a new date incremented by the given period.
        """
    def __eq__(self, arg0: Date) -> bool:
        ...
    def __ge__(self, arg0: Date) -> bool:
        ...
    def __gt__(self, arg0: Date) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def __iadd__(self, days: typing.SupportsInt) -> Date:
        """
        Increment date by the given number of days.
        """
    @typing.overload
    def __iadd__(self, period: ...) -> Date:
        """
        Increment date by the given period.
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor returning a null date.
        """
    @typing.overload
    def __init__(self, serialNumber: typing.SupportsInt) -> None:
        """
        Constructor taking a serial number as given by Excel.
        """
    @typing.overload
    def __init__(self, d: typing.SupportsInt, m: Month, y: typing.SupportsInt) -> None:
        """
        Constructor taking day, month, year.
        """
    @typing.overload
    def __init__(self, arg0: typing.Any) -> None:
        ...
    @typing.overload
    def __isub__(self, days: typing.SupportsInt) -> Date:
        """
        Decrement date by the given number of days.
        """
    @typing.overload
    def __isub__(self, period: ...) -> Date:
        """
        Decrement date by the given period.
        """
    def __le__(self, arg0: Date) -> bool:
        ...
    def __lt__(self, arg0: Date) -> bool:
        ...
    def __ne__(self, arg0: Date) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def __sub__(self, days: typing.SupportsInt) -> Date:
        """
        Return a new date decremented by the given number of days.
        """
    @typing.overload
    def __sub__(self, period: ...) -> Date:
        """
        Return a new date decremented by the given period.
        """
    def dayOfMonth(self) -> int:
        ...
    def dayOfYear(self) -> int:
        ...
    def month(self) -> Month:
        ...
    def serialNumber(self) -> int:
        ...
    def to_date(self) -> typing.Any:
        ...
    def weekday(self) -> Weekday:
        ...
    def year(self) -> int:
        ...
class DateGeneration:
    """
    Date generation rules for Schedule construction.
    """
    class Rule:
        """
        Members:
        
          Backward : Backward from termination date to effective date.
        
          Forward : Forward from effective date to termination date.
        
          Zero : No intermediate dates between effective date and termination date.
        
          ThirdWednesday : All dates but effective/termination are third Wednesday of their month.
        
          ThirdWednesdayInclusive : All dates including effective/termination are third Wednesday of their month.
        
          Twentieth : All dates but effective are the twentieth of their month (CDS in emerging markets).
        
          TwentiethIMM : All dates but effective are the twentieth of an IMM month (CDS schedules).
        
          OldCDS : Same as TwentiethIMM with unrestricted date ends (old CDS convention).
        
          CDS : Credit derivatives standard rule since 'Big Bang' changes in 2009.
        
          CDS2015 : Credit derivatives standard rule since December 20th, 2015.
        """
        Backward: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Backward: 0>
        CDS: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.CDS: 8>
        CDS2015: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.CDS2015: 9>
        Forward: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Forward: 1>
        OldCDS: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.OldCDS: 7>
        ThirdWednesday: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.ThirdWednesday: 3>
        ThirdWednesdayInclusive: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.ThirdWednesdayInclusive: 4>
        Twentieth: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Twentieth: 5>
        TwentiethIMM: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.TwentiethIMM: 6>
        Zero: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Zero: 2>
        __members__: typing.ClassVar[dict[str, DateGeneration.Rule]]  # value = {'Backward': <Rule.Backward: 0>, 'Forward': <Rule.Forward: 1>, 'Zero': <Rule.Zero: 2>, 'ThirdWednesday': <Rule.ThirdWednesday: 3>, 'ThirdWednesdayInclusive': <Rule.ThirdWednesdayInclusive: 4>, 'Twentieth': <Rule.Twentieth: 5>, 'TwentiethIMM': <Rule.TwentiethIMM: 6>, 'OldCDS': <Rule.OldCDS: 7>, 'CDS': <Rule.CDS: 8>, 'CDS2015': <Rule.CDS2015: 9>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Backward: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Backward: 0>
    CDS: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.CDS: 8>
    CDS2015: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.CDS2015: 9>
    Forward: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Forward: 1>
    OldCDS: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.OldCDS: 7>
    ThirdWednesday: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.ThirdWednesday: 3>
    ThirdWednesdayInclusive: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.ThirdWednesdayInclusive: 4>
    Twentieth: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Twentieth: 5>
    TwentiethIMM: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.TwentiethIMM: 6>
    Zero: typing.ClassVar[DateGeneration.Rule]  # value = <Rule.Zero: 2>
    def __init__(self) -> None:
        ...
class DayCounter:
    """
    Day counter base class, providing methods for time period calculations according to market conventions.
    """
    def __eq__(self, arg0: DayCounter) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __init__(self) -> None:
        """
        Default (null) day counter constructor.
        """
    def __ne__(self, arg0: DayCounter) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def dayCount(self, d1: Date, d2: Date) -> int:
        """
        Returns the number of days between two dates.
        """
    def empty(self) -> bool:
        """
        Returns True if the day counter is not initialized.
        """
    def name(self) -> str:
        """
        Returns the name of the day counter.
        """
    def yearFraction(self, d1: Date, d2: Date, refPeriodStart: Date = ..., refPeriodEnd: Date = ...) -> float:
        """
        Returns the period between two dates as a fraction of year.
        """
class DefaultProbabilityTermStructureHandle:
    """
    Handle to DefaultProbabilityTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: DefaultProbabilityTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: DefaultProbabilityTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: DefaultProbabilityTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.DefaultProbabilityTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.DefaultProbabilityTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class DengLiZhouBasketEngine(BasketOptionEngine):
    """
    Deng-Li-Zhou analytical approximation for N-dim basket options.
    """
    def __init__(self, processes: collections.abc.Sequence[GeneralizedBlackScholesProcess], correlation: Matrix) -> None:
        """
        Constructs with vector of Black-Scholes processes and correlation matrix.
        """
class Denmark(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Maunday Thursday</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>General Prayer Day, 25 days after Easter Monday (up until 2023)</li>
            <li>Ascension</li>
            <li>Day after Ascension (from 2009)</li>
            <li>Whit (Pentecost) Monday </li>
            <li>New Year's Day, January 1st</li>
            <li>Constitution Day, June 5th</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            <li>New Year's Eve, December 31st</li>
            </ul>
    
            See: https://www.nasdaqomxnordic.com/tradinghours,
            and: https://www.nationalbanken.dk/da/Kontakt/aabningstider/Sider/default.aspx
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class DepositRateHelper(base.RelativeDateRateHelper):
    """
    Rate helper for bootstrapping over deposit rates.
    """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, index: IborIndex) -> None:
        """
        Constructs from rate and Ibor index.
        """
    @typing.overload
    def __init__(self, rate: QuoteHandle, index: IborIndex) -> None:
        """
        Constructs from quote handle and Ibor index.
        """
    @typing.overload
    def __init__(self, rate: base.Quote, index: IborIndex) -> None:
        """
        Constructs from quote and Ibor index (handle created internally).
        """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, tenor: Period, fixingDays: typing.SupportsInt, calendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool, dayCounter: DayCounter) -> None:
        """
        Constructs from rate and explicit market conventions.
        """
class DerivedQuote(base.Quote):
    """
    Quote derived from another quote using a unary function.
    """
    def __init__(self, quote: QuoteHandle, function: collections.abc.Callable) -> None:
        """
        Creates a derived quote from another quote and a Python function.
        """
class DiscountCurve(base.YieldTermStructure):
    """
    Yield curve based on discount factors with log-linear interpolation.
    """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], discounts: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter) -> None:
        """
        Constructs from dates, discount factors, and day counter.
        """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], discounts: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, calendar: Calendar) -> None:
        """
        Constructs from dates, discount factors, day counter, and calendar.
        """
    def data(self) -> list[float]:
        """
        Returns the discount factors.
        """
    def dates(self) -> list[Date]:
        """
        Returns the curve dates.
        """
    def discounts(self) -> list[float]:
        """
        Returns the discount factors.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns the (date, discount factor) pairs.
        """
    def times(self) -> list[float]:
        """
        Returns the curve times.
        """
class DiscountingBondEngine(Bond.engine):
    """
    Discounting engine for bonds.
    """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle = ..., includeSettlementDateFlows: bool | None = None) -> None:
        """
        Constructs discounting bond engine.
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, includeSettlementDateFlows: bool | None = None) -> None:
        """
        Constructs discounting bond engine from term structure.
        """
    def discountCurve(self) -> YieldTermStructureHandle:
        """
        Returns the discount curve handle.
        """
class DiscountingSwapEngine(Swap.engine):
    """
    Discounting engine for swaps.
    """
    @typing.overload
    def __init__(self, discountCurve: YieldTermStructureHandle, includeSettlementDateFlows: bool | None = None, settlementDate: Date = ..., npvDate: Date = ...) -> None:
        """
        Constructs discounting swap engine.
        """
    @typing.overload
    def __init__(self, discountCurve: base.YieldTermStructure, includeSettlementDateFlows: bool | None = None, settlementDate: Date = ..., npvDate: Date = ...) -> None:
        """
        Constructs discounting swap engine from term structure.
        """
    def discountCurve(self) -> YieldTermStructureHandle:
        """
        Returns the discount curve handle.
        """
class DiscreteAveragingAsianOption(base.OneAssetOption):
    """
    Discrete-averaging Asian option.
    """
    @typing.overload
    def __init__(self, averageType: AverageType, runningAccumulator: typing.SupportsFloat, pastFixings: typing.SupportsInt, fixingDates: collections.abc.Sequence[Date], payoff: base.StrikedTypePayoff, exercise: Exercise) -> None:
        """
        Constructs with running accumulator and past fixings count.
        """
    @typing.overload
    def __init__(self, averageType: AverageType, fixingDates: collections.abc.Sequence[Date], payoff: base.StrikedTypePayoff, exercise: Exercise, allPastFixings: collections.abc.Sequence[typing.SupportsFloat] = []) -> None:
        """
        Constructs with all fixing dates.
        """
class DoubleBarrierOption(base.OneAssetOption):
    """
    Double barrier option on a single asset.
    """
    def __init__(self, barrierType: DoubleBarrierType, barrier_lo: typing.SupportsFloat, barrier_hi: typing.SupportsFloat, rebate: typing.SupportsFloat, payoff: base.StrikedTypePayoff, exercise: Exercise) -> None:
        """
        Constructs DoubleBarrierOption.
        """
    def impliedVolatility(self, price: typing.SupportsFloat, process: GeneralizedBlackScholesProcess, accuracy: typing.SupportsFloat = 0.0001, maxEvaluations: typing.SupportsInt = 100, minVol: typing.SupportsFloat = 1e-07, maxVol: typing.SupportsFloat = 4.0) -> float:
        """
        Returns implied volatility.
        """
class DoubleBarrierType:
    """
    Double barrier type.
    
    Members:
    
      KnockIn
    
      KnockOut
    
      KIKO : Lower barrier KI, upper KO.
    
      KOKI : Lower barrier KO, upper KI.
    """
    KIKO: typing.ClassVar[DoubleBarrierType]  # value = <DoubleBarrierType.KIKO: 2>
    KOKI: typing.ClassVar[DoubleBarrierType]  # value = <DoubleBarrierType.KOKI: 3>
    KnockIn: typing.ClassVar[DoubleBarrierType]  # value = <DoubleBarrierType.KnockIn: 0>
    KnockOut: typing.ClassVar[DoubleBarrierType]  # value = <DoubleBarrierType.KnockOut: 1>
    __members__: typing.ClassVar[dict[str, DoubleBarrierType]]  # value = {'KnockIn': <DoubleBarrierType.KnockIn: 0>, 'KnockOut': <DoubleBarrierType.KnockOut: 1>, 'KIKO': <DoubleBarrierType.KIKO: 2>, 'KOKI': <DoubleBarrierType.KOKI: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class DownRounding(Rounding):
    """
    Down-rounding.
    """
    def __init__(self, precision: typing.SupportsInt, digit: typing.SupportsInt = 5) -> None:
        ...
class DurationType:
    """
    Duration calculation type.
    
    Members:
    
      Simple : Simple duration.
    
      Macaulay : Macaulay duration.
    
      Modified : Modified duration.
    """
    Macaulay: typing.ClassVar[DurationType]  # value = <DurationType.Macaulay: 1>
    Modified: typing.ClassVar[DurationType]  # value = <DurationType.Modified: 2>
    Simple: typing.ClassVar[DurationType]  # value = <DurationType.Simple: 0>
    __members__: typing.ClassVar[dict[str, DurationType]]  # value = {'Simple': <DurationType.Simple: 0>, 'Macaulay': <DurationType.Macaulay: 1>, 'Modified': <DurationType.Modified: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EEKCurrency(Currency):
    """
    ! The ISO three-letter code is EEK; the numeric code is 233.
            It is divided in 100 senti.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class EGPCurrency(Currency):
    """
    ! Egyptian pound
    /*! The ISO three-letter code is EGP; the numeric code is 818.
         It is divided into 100 piastres.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class ESPCurrency(Currency):
    """
    ! The ISO three-letter code was ESP; the numeric code was 724.
            It was divided in 100 centimos.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ETBCurrency(Currency):
    """
     Ethiopian birr
    /*! The ISO three-letter code is ETB; the numeric code is 230.
         It is divided into 100 santim.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class ETCCurrency(Currency):
    """
    ! https://ethereumclassic.github.io/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ETHCurrency(Currency):
    """
    ! https://www.ethereum.org/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class EUHICP(ZeroInflationIndex):
    """
    EU Harmonised Index of Consumer Prices.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs EUHICP without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs EUHICP with a term structure handle.
        """
    @typing.overload
    def __init__(self, zeroInflationTermStructure: ...) -> None:
        """
        Constructs EUHICP with a term structure.
        """
class EUHICPXT(ZeroInflationIndex):
    """
    EU HICP Excluding Tobacco.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs EUHICPXT without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs EUHICPXT with a term structure handle.
        """
    @typing.overload
    def __init__(self, zeroInflationTermStructure: ...) -> None:
        """
        Constructs EUHICPXT with a term structure.
        """
class EURCurrency(Currency):
    """
    ! The ISO three-letter code is EUR; the numeric code is 978.
            It is divided into 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class EURegion(Region):
    """
    European Union region.
    """
    def __init__(self) -> None:
        ...
class EndCriteria:
    """
    Criteria to end optimization processes.
    """
    class Type:
        """
        End criteria type enumeration.
        
        Members:
        
          None_
        
          MaxIterations
        
          StationaryPoint
        
          StationaryFunctionValue
        
          StationaryFunctionAccuracy
        
          ZeroGradientNorm
        
          FunctionEpsilonTooSmall
        
          Unknown
        """
        FunctionEpsilonTooSmall: typing.ClassVar[EndCriteria.Type]  # value = <Type.FunctionEpsilonTooSmall: 6>
        MaxIterations: typing.ClassVar[EndCriteria.Type]  # value = <Type.MaxIterations: 1>
        None_: typing.ClassVar[EndCriteria.Type]  # value = <Type.None_: 0>
        StationaryFunctionAccuracy: typing.ClassVar[EndCriteria.Type]  # value = <Type.StationaryFunctionAccuracy: 4>
        StationaryFunctionValue: typing.ClassVar[EndCriteria.Type]  # value = <Type.StationaryFunctionValue: 3>
        StationaryPoint: typing.ClassVar[EndCriteria.Type]  # value = <Type.StationaryPoint: 2>
        Unknown: typing.ClassVar[EndCriteria.Type]  # value = <Type.Unknown: 7>
        ZeroGradientNorm: typing.ClassVar[EndCriteria.Type]  # value = <Type.ZeroGradientNorm: 5>
        __members__: typing.ClassVar[dict[str, EndCriteria.Type]]  # value = {'None_': <Type.None_: 0>, 'MaxIterations': <Type.MaxIterations: 1>, 'StationaryPoint': <Type.StationaryPoint: 2>, 'StationaryFunctionValue': <Type.StationaryFunctionValue: 3>, 'StationaryFunctionAccuracy': <Type.StationaryFunctionAccuracy: 4>, 'ZeroGradientNorm': <Type.ZeroGradientNorm: 5>, 'FunctionEpsilonTooSmall': <Type.FunctionEpsilonTooSmall: 6>, 'Unknown': <Type.Unknown: 7>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @staticmethod
    def succeeded(ecType: EndCriteria.Type) -> bool:
        """
        Returns true if the optimization succeeded.
        """
    def __init__(self, maxIterations: typing.SupportsInt, maxStationaryStateIterations: typing.SupportsInt, rootEpsilon: typing.SupportsFloat, functionEpsilon: typing.SupportsFloat, gradientNormEpsilon: typing.SupportsFloat) -> None:
        """
        Creates end criteria for optimization.
        """
    def checkMaxIterations(self, iteration: typing.SupportsInt, ecType: EndCriteria.Type) -> tuple:
        """
        Checks if maximum iterations reached. Returns (bool, ecType).
        """
    def checkStationaryFunctionAccuracy(self, f: typing.SupportsFloat, positiveOptimization: bool, ecType: EndCriteria.Type) -> tuple:
        """
        Checks for stationary function accuracy. Returns (bool, ecType).
        """
    def checkStationaryFunctionValue(self, fxOld: typing.SupportsFloat, fxNew: typing.SupportsFloat, statStateIterations: typing.SupportsInt, ecType: EndCriteria.Type) -> tuple:
        """
        Checks for stationary function value. Returns (bool, statStateIterations, ecType).
        """
    def checkStationaryPoint(self, xOld: typing.SupportsFloat, xNew: typing.SupportsFloat, statState: typing.SupportsInt, ecType: EndCriteria.Type) -> tuple:
        """
        Checks for stationary point. Returns (bool, ecType).
        """
    def checkZeroGradientNorm(self, gNorm: typing.SupportsFloat, ecType: EndCriteria.Type) -> tuple:
        """
        Checks for zero gradient norm. Returns (bool, ecType).
        """
    @property
    def functionEpsilon(self) -> float:
        """
        Returns the function epsilon.
        """
    @property
    def gradientNormEpsilon(self) -> float:
        """
        Returns the gradient norm epsilon.
        """
    @property
    def maxIterations(self) -> int:
        """
        Returns the maximum number of iterations.
        """
    @property
    def maxStationaryStateIterations(self) -> int:
        """
        Returns the maximum stationary state iterations.
        """
    @property
    def rootEpsilon(self) -> float:
        """
        Returns the root epsilon.
        """
class Eonia(OvernightIndex):
    """
    Euro Overnight Index Average (EONIA) rate fixed by the ECB.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs Eonia without forwarding curve.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs Eonia with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        """
        Constructs Eonia with forwarding term structure.
        """
class Error(Exception):
    pass
class Estr(OvernightIndex):
    """
    Euro Short-Term Rate (ESTR) index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs ESTR without forwarding curve.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs ESTR with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        """
        Constructs ESTR with forwarding term structure.
        """
class EulerDiscretization(base.StochasticProcess1D.discretization):
    """
    Euler discretization for 1D stochastic processes.
    """
    def __init__(self) -> None:
        ...
class EurLiborSwapIfrFix(SwapIndex):
    """
    EUR LIBOR swap rate (IFR fix).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class EurLiborSwapIsdaFixA(SwapIndex):
    """
    EUR LIBOR swap rate (ISDA fix A).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class EurLiborSwapIsdaFixB(SwapIndex):
    """
    EUR LIBOR swap rate (ISDA fix B).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class Euribor(IborIndex):
    """
    Euribor index fixed by the ECB.
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs Euribor index with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs Euribor index with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs Euribor index with forwarding term structure.
        """
class Euribor1M(Euribor):
    """
    1-month Euribor index.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, h: ...) -> None:
        ...
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        ...
class Euribor1W(Euribor):
    """
    1-week Euribor index.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, h: ...) -> None:
        ...
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        ...
class Euribor1Y(Euribor):
    """
    1-year Euribor index.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, h: ...) -> None:
        ...
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        ...
class Euribor365(IborIndex):
    """
    Actual/365 Euribor index.
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs Euribor365 index with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs Euribor365 index with forwarding term structure handle.
        """
class Euribor3M(Euribor):
    """
    3-month Euribor index.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, h: ...) -> None:
        ...
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        ...
class Euribor6M(Euribor):
    """
    6-month Euribor index.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, h: ...) -> None:
        ...
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        ...
class EuriborSwapIfrFix(SwapIndex):
    """
    Euribor swap rate (IFR fix).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class EuriborSwapIsdaFixA(SwapIndex):
    """
    Euribor swap rate (ISDA fix A).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class EuriborSwapIsdaFixB(SwapIndex):
    """
    Euribor swap rate (ISDA fix B).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class EuropeanExercise(Exercise):
    """
    European-style exercise (single date).
    """
    def __init__(self, date: Date) -> None:
        """
        Constructs with the exercise date.
        """
class ExchangeRate:
    """
    Exchange rate between two currencies.
    """
    class Type:
        """
        Type of exchange rate.
        
        Members:
        
          Direct : Directly quoted rate.
        
          Derived : Rate derived from other rates.
        """
        Derived: typing.ClassVar[ExchangeRate.Type]  # value = <Type.Derived: 1>
        Direct: typing.ClassVar[ExchangeRate.Type]  # value = <Type.Direct: 0>
        __members__: typing.ClassVar[dict[str, ExchangeRate.Type]]  # value = {'Direct': <Type.Direct: 0>, 'Derived': <Type.Derived: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Derived: typing.ClassVar[ExchangeRate.Type]  # value = <Type.Derived: 1>
    Direct: typing.ClassVar[ExchangeRate.Type]  # value = <Type.Direct: 0>
    @staticmethod
    def chain(r1: ExchangeRate, r2: ExchangeRate) -> ExchangeRate:
        """
        Creates a derived rate by chaining two rates.
        """
    def __init__(self, source: Currency, target: Currency, rate: typing.SupportsFloat) -> None:
        """
        Constructs an exchange rate from source to target currency.
        """
    def rate(self) -> float:
        """
        Returns the exchange rate value.
        """
    def source(self) -> Currency:
        """
        Returns the source currency.
        """
    def target(self) -> Currency:
        """
        Returns the target currency.
        """
    def type(self) -> ExchangeRate.Type:
        """
        Returns the type of the exchange rate.
        """
class ExchangeRateManager:
    """
    Global repository for exchange rates.
    """
    @staticmethod
    def add(*args, **kwargs) -> None:
        """
        Adds an exchange rate.
        """
    @staticmethod
    def instance() -> ExchangeRateManager:
        """
        Returns the singleton instance.
        """
    def clear(self) -> None:
        """
        Clears all stored exchange rates.
        """
    def lookup(self, source: Currency, target: Currency, date: Date = ..., type: ExchangeRate.Type = ...) -> ExchangeRate:
        """
        Looks up an exchange rate between two currencies.
        """
class Exercise:
    """
    Abstract base class for option exercise styles.
    """
    def dates(self) -> list[Date]:
        """
        Returns the list of exercise dates.
        """
    def lastDate(self) -> Date:
        """
        Returns the latest exercise date.
        """
class ExponentialSplinesFitting(base.FittingMethod):
    """
    Exponential splines fitting method.
    """
    def __init__(self, constrainAtZero: bool = True, weights: Array = ..., optimizationMethod: base.OptimizationMethod = None, l2: Array = ..., minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308, numCoeffs: typing.SupportsInt = 9, fixedKappa: typing.Any = None, constraint: base.Constraint = ...) -> None:
        """
        Constructs an exponential splines fitting method.
        """
class FIMCurrency(Currency):
    """
    ! The ISO three-letter code was FIM; the numeric code was 246.
            It was divided in 100 penni�.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class FRFCurrency(Currency):
    """
    ! The ISO three-letter code was FRF; the numeric code was 250.
            It was divided in 100 centimes.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class FaceValueAccrualClaim(base.Claim):
    """
    Claim on the notional of a reference security, including accrual.
    """
    def __init__(self, referenceSecurity: Bond) -> None:
        """
        Constructs from a reference bond.
        """
class FaceValueClaim(base.Claim):
    """
    Claim on a notional.
    """
    def __init__(self) -> None:
        """
        Constructs a face value claim.
        """
class Fd2dBlackScholesVanillaEngine(BasketOptionEngine):
    """
    2D finite-difference Black-Scholes engine for basket options.
    """
    def __init__(self, process1: GeneralizedBlackScholesProcess, process2: GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat, xGrid: typing.SupportsInt = 100, yGrid: typing.SupportsInt = 100, tGrid: typing.SupportsInt = 50, dampingSteps: typing.SupportsInt = 0, schemeDesc: FdmSchemeDesc = ..., localVol: bool = False, illegalLocalVolOverwrite: typing.SupportsFloat = -3.4028234663852886e+38) -> None:
        """
        Constructs with two processes, correlation, and optional grid/scheme parameters.
        """
class FdBlackScholesBarrierEngine(base.PricingEngine):
    """
    Finite-differences Black-Scholes barrier option engine.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess, tGrid: typing.SupportsInt = 100, xGrid: typing.SupportsInt = 100, dampingSteps: typing.SupportsInt = 0, schemeDesc: FdmSchemeDesc = ..., localVol: bool = False, illegalLocalVolOverwrite: typing.SupportsFloat = -3.4028234663852886e+38) -> None:
        """
        Constructs FdBlackScholesBarrierEngine.
        """
class FdBlackScholesVanillaEngine(base.PricingEngine):
    """
    Finite-differences Black-Scholes vanilla option engine.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess, tGrid: typing.SupportsInt = 100, xGrid: typing.SupportsInt = 100, dampingSteps: typing.SupportsInt = 0, schemeDesc: FdmSchemeDesc = ..., localVol: bool = False, illegalLocalVolOverwrite: typing.SupportsFloat = -3.4028234663852886e+38, cashDividendModel: CashDividendModel = ...) -> None:
        """
        Constructs a finite-difference Black-Scholes engine.
        
        Parameters:
          process: Black-Scholes process
          tGrid: Number of time steps
          xGrid: Number of spatial grid points
          dampingSteps: Damping steps near maturity
          schemeDesc: FD scheme (Douglas, CrankNicolson, etc.)
          localVol: Use local volatility
          illegalLocalVolOverwrite: Override for illegal local vol values
          cashDividendModel: Spot or Escrowed
        """
class FdG2SwaptionEngine(base.PricingEngine):
    """
    Finite-differences swaption engine for G2++ two-factor model.
    """
    def __init__(self, model: G2, tGrid: typing.SupportsInt = 100, xGrid: typing.SupportsInt = 50, yGrid: typing.SupportsInt = 50, dampingSteps: typing.SupportsInt = 0, invEps: typing.SupportsFloat = 1e-05, schemeDesc: FdmSchemeDesc = ...) -> None:
        """
        Constructs FD G2 swaption engine.
        """
class FdHullWhiteSwaptionEngine(base.PricingEngine):
    """
    Finite-differences swaption engine for Hull-White model.
    """
    def __init__(self, model: HullWhite, tGrid: typing.SupportsInt = 100, xGrid: typing.SupportsInt = 100, dampingSteps: typing.SupportsInt = 0, invEps: typing.SupportsFloat = 1e-05, schemeDesc: FdmSchemeDesc = ...) -> None:
        """
        Constructs FD Hull-White swaption engine.
        """
class FdmSchemeDesc:
    """
    Finite difference scheme descriptor.
    """
    @staticmethod
    def CraigSneyd() -> FdmSchemeDesc:
        """
        Craig-Sneyd scheme.
        """
    @staticmethod
    def CrankNicolson() -> FdmSchemeDesc:
        """
        Crank-Nicolson scheme.
        """
    @staticmethod
    def Douglas() -> FdmSchemeDesc:
        """
        Douglas scheme (same as Crank-Nicolson in 1D).
        """
    @staticmethod
    def ExplicitEuler() -> FdmSchemeDesc:
        """
        Explicit Euler scheme.
        """
    @staticmethod
    def Hundsdorfer() -> FdmSchemeDesc:
        """
        Hundsdorfer scheme.
        """
    @staticmethod
    def ImplicitEuler() -> FdmSchemeDesc:
        """
        Implicit Euler scheme.
        """
    @staticmethod
    def MethodOfLines(eps: typing.SupportsFloat = 0.001, relInitStepSize: typing.SupportsFloat = 0.01) -> FdmSchemeDesc:
        """
        Method of lines scheme.
        """
    @staticmethod
    def ModifiedCraigSneyd() -> FdmSchemeDesc:
        """
        Modified Craig-Sneyd scheme.
        """
    @staticmethod
    def ModifiedHundsdorfer() -> FdmSchemeDesc:
        """
        Modified Hundsdorfer scheme.
        """
    @staticmethod
    def TrBDF2() -> FdmSchemeDesc:
        """
        TR-BDF2 scheme.
        """
    def __init__(self, type: FdmSchemeType, theta: typing.SupportsFloat, mu: typing.SupportsFloat) -> None:
        """
        Constructs with scheme type, theta, and mu.
        """
    @property
    def mu(self) -> float:
        ...
    @property
    def theta(self) -> float:
        ...
    @property
    def type(self) -> FdmSchemeType:
        ...
class FdmSchemeType:
    """
    Finite difference scheme types.
    
    Members:
    
      Hundsdorfer
    
      Douglas
    
      CraigSneyd
    
      ModifiedCraigSneyd
    
      ImplicitEuler
    
      ExplicitEuler
    
      MethodOfLines
    
      TrBDF2
    
      CrankNicolson
    """
    CraigSneyd: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.CraigSneyd: 2>
    CrankNicolson: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.CrankNicolson: 8>
    Douglas: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.Douglas: 1>
    ExplicitEuler: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.ExplicitEuler: 5>
    Hundsdorfer: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.Hundsdorfer: 0>
    ImplicitEuler: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.ImplicitEuler: 4>
    MethodOfLines: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.MethodOfLines: 6>
    ModifiedCraigSneyd: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.ModifiedCraigSneyd: 3>
    TrBDF2: typing.ClassVar[FdmSchemeType]  # value = <FdmSchemeType.TrBDF2: 7>
    __members__: typing.ClassVar[dict[str, FdmSchemeType]]  # value = {'Hundsdorfer': <FdmSchemeType.Hundsdorfer: 0>, 'Douglas': <FdmSchemeType.Douglas: 1>, 'CraigSneyd': <FdmSchemeType.CraigSneyd: 2>, 'ModifiedCraigSneyd': <FdmSchemeType.ModifiedCraigSneyd: 3>, 'ImplicitEuler': <FdmSchemeType.ImplicitEuler: 4>, 'ExplicitEuler': <FdmSchemeType.ExplicitEuler: 5>, 'MethodOfLines': <FdmSchemeType.MethodOfLines: 6>, 'TrBDF2': <FdmSchemeType.TrBDF2: 7>, 'CrankNicolson': <FdmSchemeType.CrankNicolson: 8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Finland(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Ascension Thursday</li>
            <li>Labour Day, May 1st</li>
            <li>Midsummer Eve (Friday between June 19-25)</li>
            <li>Independence Day, December 6th</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class FittedBondDiscountCurve(base.YieldTermStructure, base.LazyObject):
    """
    Discount curve fitted to a set of bonds.
    """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, bonds: collections.abc.Sequence[BondHelper], dayCounter: DayCounter, fittingMethod: base.FittingMethod, accuracy: typing.SupportsFloat = 1e-10, maxEvaluations: typing.SupportsInt = 10000, guess: Array = ..., simplexLambda: typing.SupportsFloat = 1.0, maxStationaryStateIterations: typing.SupportsInt = 100) -> None:
        """
        Constructs from settlement days with bond fitting.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, bonds: collections.abc.Sequence[BondHelper], dayCounter: DayCounter, fittingMethod: base.FittingMethod, accuracy: typing.SupportsFloat = 1e-10, maxEvaluations: typing.SupportsInt = 10000, guess: Array = ..., simplexLambda: typing.SupportsFloat = 1.0, maxStationaryStateIterations: typing.SupportsInt = 100) -> None:
        """
        Constructs from reference date with bond fitting.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, fittingMethod: base.FittingMethod, parameters: Array, maxDate: Date, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days with precalculated parameters.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, fittingMethod: base.FittingMethod, parameters: Array, maxDate: Date, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date with precalculated parameters.
        """
    def fitResults(self) -> base.FittingMethod:
        """
        Returns the fitting method with calibration results.
        """
    def numberOfBonds(self) -> int:
        """
        Returns the number of bonds used in the fit.
        """
    def resetGuess(self, guess: Array) -> None:
        """
        Resets the initial guess for refitting.
        """
class FixedLocalVolExtrapolation:
    """
    Extrapolation type for FixedLocalVolSurface.
    
    Members:
    
      ConstantExtrapolation
    
      InterpolatorDefaultExtrapolation
    """
    ConstantExtrapolation: typing.ClassVar[FixedLocalVolExtrapolation]  # value = <FixedLocalVolExtrapolation.ConstantExtrapolation: 0>
    InterpolatorDefaultExtrapolation: typing.ClassVar[FixedLocalVolExtrapolation]  # value = <FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation: 1>
    __members__: typing.ClassVar[dict[str, FixedLocalVolExtrapolation]]  # value = {'ConstantExtrapolation': <FixedLocalVolExtrapolation.ConstantExtrapolation: 0>, 'InterpolatorDefaultExtrapolation': <FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class FixedLocalVolSurface(base.LocalVolTermStructure):
    """
    Fixed local volatility surface with strike/time grid.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, dates: collections.abc.Sequence[Date], strikes: collections.abc.Sequence[typing.SupportsFloat], localVolMatrix: Matrix, dayCounter: DayCounter, lowerExtrapolation: FixedLocalVolExtrapolation = ..., upperExtrapolation: FixedLocalVolExtrapolation = ...) -> None:
        """
        Constructs from dates and uniform strikes.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, times: collections.abc.Sequence[typing.SupportsFloat], strikes: collections.abc.Sequence[typing.SupportsFloat], localVolMatrix: Matrix, dayCounter: DayCounter, lowerExtrapolation: FixedLocalVolExtrapolation = ..., upperExtrapolation: FixedLocalVolExtrapolation = ...) -> None:
        """
        Constructs from times and uniform strikes.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, times: collections.abc.Sequence[typing.SupportsFloat], strikes: collections.abc.Sequence[collections.abc.Sequence[typing.SupportsFloat]], localVolMatrix: Matrix, dayCounter: DayCounter, lowerExtrapolation: FixedLocalVolExtrapolation = ..., upperExtrapolation: FixedLocalVolExtrapolation = ...) -> None:
        """
        Constructs from times and varying strikes per time point.
        """
    def maxDate(self) -> Date:
        """
        Returns the maximum date.
        """
    def maxStrike(self) -> float:
        """
        Returns the maximum strike.
        """
    def maxTime(self) -> float:
        """
        Returns the maximum time.
        """
    def minStrike(self) -> float:
        """
        Returns the minimum strike.
        """
class FixedRateBond(Bond):
    """
    Fixed rate bond.
    """
    def __init__(self, settlementDays: typing.SupportsInt, faceAmount: typing.SupportsFloat, schedule: Schedule, coupons: collections.abc.Sequence[typing.SupportsFloat], accrualDayCounter: DayCounter, paymentConvention: BusinessDayConvention = ..., redemption: typing.SupportsFloat = 100.0, issueDate: Date = ..., paymentCalendar: typing.Any = None, exCouponPeriod: Period = ..., exCouponCalendar: typing.Any = None, exCouponConvention: BusinessDayConvention = ..., exCouponEndOfMonth: bool = False, firstPeriodDayCounter: typing.Any = None) -> None:
        """
        Constructs a fixed rate bond.
        """
    def dayCounter(self) -> DayCounter:
        """
        Returns the accrual day counter.
        """
    def frequency(self) -> Frequency:
        """
        Returns the coupon frequency.
        """
class FixedRateBondHelper(BondHelper):
    """
    Fixed-coupon bond helper for bootstrapping yield curves.
    """
    @typing.overload
    def __init__(self, price: QuoteHandle, settlementDays: typing.SupportsInt, faceAmount: typing.SupportsFloat, schedule: Schedule, coupons: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, paymentConvention: BusinessDayConvention = ..., redemption: typing.SupportsFloat = 100.0, issueDate: Date = ..., paymentCalendar: typing.Any = None, exCouponPeriod: Period = ..., exCouponCalendar: typing.Any = None, exCouponConvention: BusinessDayConvention = ..., exCouponEndOfMonth: bool = False, priceType: typing.Any = None) -> None:
        """
        Constructs from price handle and bond parameters.
        """
    @typing.overload
    def __init__(self, price: base.Quote, settlementDays: typing.SupportsInt, faceAmount: typing.SupportsFloat, schedule: Schedule, coupons: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, paymentConvention: BusinessDayConvention = ..., redemption: typing.SupportsFloat = 100.0, issueDate: Date = ..., paymentCalendar: typing.Any = None, exCouponPeriod: Period = ..., exCouponCalendar: typing.Any = None, exCouponConvention: BusinessDayConvention = ..., exCouponEndOfMonth: bool = False, priceType: typing.Any = None) -> None:
        """
        Constructs from quote and bond parameters (handle created internally).
        """
    @typing.overload
    def __init__(self, price: typing.SupportsFloat, settlementDays: typing.SupportsInt, faceAmount: typing.SupportsFloat, schedule: Schedule, coupons: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, paymentConvention: BusinessDayConvention = ..., redemption: typing.SupportsFloat = 100.0, issueDate: Date = ..., paymentCalendar: typing.Any = None, exCouponPeriod: Period = ..., exCouponCalendar: typing.Any = None, exCouponConvention: BusinessDayConvention = ..., exCouponEndOfMonth: bool = False, priceType: typing.Any = None) -> None:
        """
        Constructs from price value and bond parameters.
        """
class FixedRateCoupon(base.Coupon):
    """
    Coupon paying a fixed interest rate.
    """
    @typing.overload
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, interestRate: InterestRate, accrualStartDate: Date, accrualEndDate: Date, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., exCouponDate: Date = ...) -> None:
        """
        Constructs a fixed-rate coupon from an InterestRate.
        """
    @typing.overload
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, rate: typing.SupportsFloat, dayCounter: DayCounter, accrualStartDate: Date, accrualEndDate: Date, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., exCouponDate: Date = ...) -> None:
        """
        Constructs a fixed-rate coupon from rate and day counter.
        """
    def interestRate(self) -> InterestRate:
        """
        Returns the interest rate.
        """
class FixedRateLeg:
    """
    Helper class for building a leg of fixed-rate coupons.
    """
    def __init__(self, schedule: Schedule) -> None:
        """
        Constructs a FixedRateLeg from a schedule.
        """
    def build(self) -> list[base.CashFlow]:
        """
        Builds and returns the leg of cash flows.
        """
    @typing.overload
    def withCouponRates(self, rate: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> FixedRateLeg:
        ...
    @typing.overload
    def withCouponRates(self, interestRate: InterestRate) -> FixedRateLeg:
        ...
    @typing.overload
    def withCouponRates(self, rates: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> FixedRateLeg:
        ...
    @typing.overload
    def withCouponRates(self, interestRates: collections.abc.Sequence[InterestRate]) -> FixedRateLeg:
        ...
    def withExCouponPeriod(self, period: Period, calendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool = False) -> FixedRateLeg:
        ...
    def withFirstPeriodDayCounter(self, dayCounter: DayCounter) -> FixedRateLeg:
        ...
    def withLastPeriodDayCounter(self, dayCounter: DayCounter) -> FixedRateLeg:
        ...
    @typing.overload
    def withNotionals(self, nominal: typing.SupportsFloat) -> FixedRateLeg:
        ...
    @typing.overload
    def withNotionals(self, nominals: collections.abc.Sequence[typing.SupportsFloat]) -> FixedRateLeg:
        ...
    def withPaymentAdjustment(self, convention: BusinessDayConvention) -> FixedRateLeg:
        ...
    def withPaymentCalendar(self, calendar: Calendar) -> FixedRateLeg:
        ...
    def withPaymentLag(self, lag: typing.SupportsInt) -> FixedRateLeg:
        ...
class FixedVsFloatingSwap(Swap):
    """
    Fixed vs floating swap base class.
    """
    def fairRate(self) -> float:
        """
        Returns the fair fixed rate.
        """
    def fairSpread(self) -> float:
        """
        Returns the fair spread.
        """
    def fixedDayCount(self) -> DayCounter:
        """
        Returns the fixed leg day counter.
        """
    def fixedLeg(self) -> list[base.CashFlow]:
        """
        Returns the fixed leg cash flows.
        """
    def fixedLegBPS(self) -> float:
        """
        Returns the BPS of the fixed leg.
        """
    def fixedLegNPV(self) -> float:
        """
        Returns the NPV of the fixed leg.
        """
    def fixedNominals(self) -> list[float]:
        """
        Returns the fixed leg nominals.
        """
    def fixedRate(self) -> float:
        """
        Returns the fixed rate.
        """
    def fixedSchedule(self) -> Schedule:
        """
        Returns the fixed leg schedule.
        """
    def floatingDayCount(self) -> DayCounter:
        """
        Returns the floating leg day counter.
        """
    def floatingLeg(self) -> list[base.CashFlow]:
        """
        Returns the floating leg cash flows.
        """
    def floatingLegBPS(self) -> float:
        """
        Returns the BPS of the floating leg.
        """
    def floatingLegNPV(self) -> float:
        """
        Returns the NPV of the floating leg.
        """
    def floatingNominals(self) -> list[float]:
        """
        Returns the floating leg nominals.
        """
    def floatingSchedule(self) -> Schedule:
        """
        Returns the floating leg schedule.
        """
    def iborIndex(self) -> IborIndex:
        """
        Returns the IBOR index.
        """
    def nominal(self) -> float:
        """
        Returns the nominal (throws if not constant).
        """
    def nominals(self) -> list[float]:
        """
        Returns the nominals (throws if different for legs).
        """
    def paymentConvention(self) -> BusinessDayConvention:
        """
        Returns the payment business day convention.
        """
    def spread(self) -> float:
        """
        Returns the floating leg spread.
        """
    def type(self) -> SwapType:
        """
        Returns the swap type (Payer or Receiver).
        """
class FixedVsFloatingSwapArguments(SwapArguments):
    """
    Arguments for fixed vs floating swap pricing.
    """
    type: SwapType
    def __init__(self) -> None:
        ...
    @property
    def fixedCoupons(self) -> list[float]:
        ...
    @fixedCoupons.setter
    def fixedCoupons(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def fixedNominals(self) -> list[float]:
        ...
    @fixedNominals.setter
    def fixedNominals(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def fixedPayDates(self) -> list[Date]:
        ...
    @fixedPayDates.setter
    def fixedPayDates(self, arg0: collections.abc.Sequence[Date]) -> None:
        ...
    @property
    def fixedResetDates(self) -> list[Date]:
        ...
    @fixedResetDates.setter
    def fixedResetDates(self, arg0: collections.abc.Sequence[Date]) -> None:
        ...
    @property
    def floatingAccrualTimes(self) -> list[float]:
        ...
    @floatingAccrualTimes.setter
    def floatingAccrualTimes(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def floatingCoupons(self) -> list[float]:
        ...
    @floatingCoupons.setter
    def floatingCoupons(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def floatingFixingDates(self) -> list[Date]:
        ...
    @floatingFixingDates.setter
    def floatingFixingDates(self, arg0: collections.abc.Sequence[Date]) -> None:
        ...
    @property
    def floatingNominals(self) -> list[float]:
        ...
    @floatingNominals.setter
    def floatingNominals(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def floatingPayDates(self) -> list[Date]:
        ...
    @floatingPayDates.setter
    def floatingPayDates(self, arg0: collections.abc.Sequence[Date]) -> None:
        ...
    @property
    def floatingResetDates(self) -> list[Date]:
        ...
    @floatingResetDates.setter
    def floatingResetDates(self, arg0: collections.abc.Sequence[Date]) -> None:
        ...
    @property
    def floatingSpreads(self) -> list[float]:
        ...
    @floatingSpreads.setter
    def floatingSpreads(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def nominal(self) -> float:
        ...
    @nominal.setter
    def nominal(self, arg0: typing.SupportsFloat) -> None:
        ...
class FixedVsFloatingSwapResults(SwapResults):
    """
    Results from fixed vs floating swap pricing.
    """
    def __init__(self) -> None:
        ...
    @property
    def fairRate(self) -> float:
        ...
    @fairRate.setter
    def fairRate(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def fairSpread(self) -> float:
        ...
    @fairSpread.setter
    def fairSpread(self, arg0: typing.SupportsFloat) -> None:
        ...
class FlatForward(base.YieldTermStructure):
    """
    Flat interest-rate curve.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, forward: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from reference date and forward rate.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, forward: QuoteHandle, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from reference date and quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, forward: base.Quote, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from reference date and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, forward: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from settlement days and forward rate.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, forward: QuoteHandle, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from settlement days and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, forward: base.Quote, dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from settlement days and quote (handle created internally).
        """
    def compounding(self) -> Compounding:
        """
        Returns the compounding convention.
        """
    def compoundingFrequency(self) -> Frequency:
        """
        Returns the compounding frequency.
        """
class FlatHazardRate(base.DefaultProbabilityTermStructure):
    """
    Flat hazard rate term structure.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, hazardRate: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from date and hazard rate.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, hazardRate: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from date and hazard rate quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, hazardRate: base.Quote, dayCounter: DayCounter) -> None:
        """
        Constructs from date and hazard rate quote.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, hazardRate: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and hazard rate.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, hazardRate: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and hazard rate quote handle.
        """
    def maxDate(self) -> Date:
        """
        Maximum date.
        """
class FloatingRateBond(Bond):
    """
    Floating rate bond.
    """
    def __init__(self, settlementDays: typing.SupportsInt, faceAmount: typing.SupportsFloat, schedule: Schedule, iborIndex: IborIndex, accrualDayCounter: DayCounter, paymentConvention: BusinessDayConvention = ..., fixingDays: typing.Any = None, gearings: collections.abc.Sequence[typing.SupportsFloat] = [1.0], spreads: collections.abc.Sequence[typing.SupportsFloat] = [0.0], caps: collections.abc.Sequence[typing.SupportsFloat] = [], floors: collections.abc.Sequence[typing.SupportsFloat] = [], inArrears: bool = False, redemption: typing.SupportsFloat = 100.0, issueDate: Date = ..., exCouponPeriod: Period = ..., exCouponCalendar: typing.Any = None, exCouponConvention: BusinessDayConvention = ..., exCouponEndOfMonth: bool = False) -> None:
        """
        Constructs a floating rate bond.
        """
class FloatingRateCoupon(base.Coupon):
    """
    Coupon paying a variable index-based rate.
    """
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, startDate: Date, endDate: Date, fixingDays: typing.SupportsInt, index: ..., gearing: typing.SupportsFloat = 1.0, spread: typing.SupportsFloat = 0.0, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., dayCounter: typing.Any = None, isInArrears: bool = False, exCouponDate: Date = ...) -> None:
        """
        Constructs a floating-rate coupon.
        """
    def adjustedFixing(self) -> float:
        """
        Returns the convexity-adjusted fixing.
        """
    def convexityAdjustment(self) -> float:
        """
        Returns the convexity adjustment.
        """
    def fixingDate(self) -> Date:
        """
        Returns the fixing date.
        """
    def fixingDays(self) -> int:
        """
        Returns the number of fixing days.
        """
    def gearing(self) -> float:
        """
        Returns the index gearing.
        """
    def index(self) -> ...:
        """
        Returns the floating index.
        """
    def indexFixing(self) -> float:
        """
        Returns the fixing of the underlying index.
        """
    def isInArrears(self) -> bool:
        """
        Returns whether the coupon fixes in arrears.
        """
    def pricer(self) -> base.FloatingRateCouponPricer:
        """
        Returns the coupon pricer.
        """
    def setPricer(self, pricer: base.FloatingRateCouponPricer) -> None:
        """
        Sets the coupon pricer.
        """
    def spread(self) -> float:
        """
        Returns the spread over the index fixing.
        """
class Floor(CapFloor):
    """
    Interest rate floor.
    """
    def __init__(self, floatingLeg: collections.abc.Sequence[base.CashFlow], exerciseRates: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs a floor.
        """
class FloorTruncation(Rounding):
    """
    Floor truncation.
    """
    def __init__(self, precision: typing.SupportsInt, digit: typing.SupportsInt = 5) -> None:
        ...
class ForwardCurve(base.YieldTermStructure):
    """
    Yield curve based on forward rates with backward-flat interpolation.
    """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], forwards: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter) -> None:
        """
        Constructs from dates, forward rates, and day counter.
        """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], forwards: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, calendar: Calendar) -> None:
        """
        Constructs from dates, forward rates, day counter, and calendar.
        """
    def data(self) -> list[float]:
        """
        Returns the forward rates.
        """
    def dates(self) -> list[Date]:
        """
        Returns the curve dates.
        """
    def forwards(self) -> list[float]:
        """
        Returns the forward rates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns the (date, forward rate) pairs.
        """
    def times(self) -> list[float]:
        """
        Returns the curve times.
        """
class ForwardRateAgreement(base.Instrument):
    """
    Forward rate agreement (FRA).
    """
    @typing.overload
    def __init__(self, index: IborIndex, valueDate: Date, type: PositionType, strikeForwardRate: typing.SupportsFloat, notionalAmount: typing.SupportsFloat, discountCurve: YieldTermStructureHandle = ...) -> None:
        """
        Constructs FRA using indexed coupon.
        """
    @typing.overload
    def __init__(self, index: IborIndex, valueDate: Date, type: PositionType, strikeForwardRate: typing.SupportsFloat, notionalAmount: typing.SupportsFloat, discountCurve: base.YieldTermStructure) -> None:
        """
        Constructs FRA with term structure (handle created internally).
        """
    @typing.overload
    def __init__(self, index: IborIndex, valueDate: Date, maturityDate: Date, type: PositionType, strikeForwardRate: typing.SupportsFloat, notionalAmount: typing.SupportsFloat, discountCurve: YieldTermStructureHandle = ...) -> None:
        """
        Constructs FRA using par-rate approximation.
        """
    def amount(self) -> float:
        """
        Returns the payoff on the value date.
        """
    def businessDayConvention(self) -> BusinessDayConvention:
        """
        Returns the business day convention.
        """
    def calendar(self) -> Calendar:
        """
        Returns the calendar.
        """
    def dayCounter(self) -> DayCounter:
        """
        Returns the day counter.
        """
    def fixingDate(self) -> Date:
        """
        Returns the fixing date.
        """
    def forwardRate(self) -> InterestRate:
        """
        Returns the market forward rate.
        """
    def isExpired(self) -> bool:
        """
        Returns True if expired.
        """
class FraRateHelper(base.RelativeDateRateHelper):
    """
    Rate helper for bootstrapping over FRA rates.
    """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, monthsToStart: typing.SupportsInt, index: IborIndex, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., useIndexedCoupon: bool = True) -> None:
        """
        Constructs from rate, months to start, and Ibor index.
        """
    @typing.overload
    def __init__(self, rate: QuoteHandle, monthsToStart: typing.SupportsInt, index: IborIndex, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., useIndexedCoupon: bool = True) -> None:
        """
        Constructs from quote handle, months to start, and Ibor index.
        """
    @typing.overload
    def __init__(self, rate: base.Quote, monthsToStart: typing.SupportsInt, index: IborIndex, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., useIndexedCoupon: bool = True) -> None:
        """
        Constructs from quote, months to start, and Ibor index (handle created internally).
        """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, periodToStart: Period, index: IborIndex, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., useIndexedCoupon: bool = True) -> None:
        """
        Constructs from rate, period to start, and Ibor index.
        """
class France(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Armistice 1945, May 8th</li>
            <li>Ascension, May 10th</li>
            <li>Pentec�te, May 21st</li>
            <li>F�te nationale, July 14th</li>
            <li>Assumption, August 15th</li>
            <li>All Saint's Day, November 1st</li>
            <li>Armistice 1918, November 11th</li>
            <li>Christmas Day, December 25th</li>
            </ul>
    
            Holidays for the stock exchange (data from https://www.stockmarketclock.com/exchanges/euronext-paris/market-holidays/):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas Day, December 25th</li>
            <li>Boxing Day, December 26th</li>
            <li>New Year's Eve, December 31st</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        ! French calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          Exchange : !< Paris stock-exchange calendar
        """
        Exchange: typing.ClassVar[France.Market]  # value = <Market.Exchange: 1>
        Settlement: typing.ClassVar[France.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, France.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'Exchange': <Market.Exchange: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Exchange: typing.ClassVar[France.Market]  # value = <Market.Exchange: 1>
    Settlement: typing.ClassVar[France.Market]  # value = <Market.Settlement: 0>
    def __init__(self) -> None:
        ...
class FranceRegion(Region):
    """
    France region.
    """
    def __init__(self) -> None:
        ...
class Frequency:
    """
    Frequency of events.
    
    Members:
    
      NoFrequency : Null frequency
    
      Once : Only once, e.g., a zero-coupon
    
      Annual : Once a year
    
      Semiannual : Twice a year
    
      EveryFourthMonth : Every fourth month
    
      Quarterly : Every third month
    
      Bimonthly : Every second month
    
      Monthly : Once a month
    
      EveryFourthWeek : Every fourth week
    
      Biweekly : Every second week
    
      Weekly : Once a week
    
      Daily : Once a day
    
      OtherFrequency : Some other unknown frequency
    """
    Annual: typing.ClassVar[Frequency]  # value = <Frequency.Annual: 1>
    Bimonthly: typing.ClassVar[Frequency]  # value = <Frequency.Bimonthly: 6>
    Biweekly: typing.ClassVar[Frequency]  # value = <Frequency.Biweekly: 26>
    Daily: typing.ClassVar[Frequency]  # value = <Frequency.Daily: 365>
    EveryFourthMonth: typing.ClassVar[Frequency]  # value = <Frequency.EveryFourthMonth: 3>
    EveryFourthWeek: typing.ClassVar[Frequency]  # value = <Frequency.EveryFourthWeek: 13>
    Monthly: typing.ClassVar[Frequency]  # value = <Frequency.Monthly: 12>
    NoFrequency: typing.ClassVar[Frequency]  # value = <Frequency.NoFrequency: -1>
    Once: typing.ClassVar[Frequency]  # value = <Frequency.Once: 0>
    OtherFrequency: typing.ClassVar[Frequency]  # value = <Frequency.OtherFrequency: 999>
    Quarterly: typing.ClassVar[Frequency]  # value = <Frequency.Quarterly: 4>
    Semiannual: typing.ClassVar[Frequency]  # value = <Frequency.Semiannual: 2>
    Weekly: typing.ClassVar[Frequency]  # value = <Frequency.Weekly: 52>
    __members__: typing.ClassVar[dict[str, Frequency]]  # value = {'NoFrequency': <Frequency.NoFrequency: -1>, 'Once': <Frequency.Once: 0>, 'Annual': <Frequency.Annual: 1>, 'Semiannual': <Frequency.Semiannual: 2>, 'EveryFourthMonth': <Frequency.EveryFourthMonth: 3>, 'Quarterly': <Frequency.Quarterly: 4>, 'Bimonthly': <Frequency.Bimonthly: 6>, 'Monthly': <Frequency.Monthly: 12>, 'EveryFourthWeek': <Frequency.EveryFourthWeek: 13>, 'Biweekly': <Frequency.Biweekly: 26>, 'Weekly': <Frequency.Weekly: 52>, 'Daily': <Frequency.Daily: 365>, 'OtherFrequency': <Frequency.OtherFrequency: 999>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class G2(base.TwoFactorModel, base.AffineModel, base.TermStructureConsistentModel):
    """
    Two-additive-factor Gaussian model G2++.
    """
    @typing.overload
    def __init__(self, termStructure: YieldTermStructureHandle, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.01, b: typing.SupportsFloat = 0.1, eta: typing.SupportsFloat = 0.01, rho: typing.SupportsFloat = -0.75) -> None:
        """
        Constructs G2++ model with term structure and parameters.
        """
    @typing.overload
    def __init__(self, termStructure: base.YieldTermStructure, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.01, b: typing.SupportsFloat = 0.1, eta: typing.SupportsFloat = 0.01, rho: typing.SupportsFloat = -0.75) -> None:
        """
        Constructs G2++ model from term structure.
        """
    def a(self) -> float:
        """
        Returns first factor mean reversion speed.
        """
    def b(self) -> float:
        """
        Returns second factor mean reversion speed.
        """
    def discountBond(self, t: typing.SupportsFloat, T: typing.SupportsFloat, x: typing.SupportsFloat, y: typing.SupportsFloat) -> float:
        """
        Returns discount bond price P(t,T) given state variables x and y.
        """
    def discountBondOption(self, type: OptionType, strike: typing.SupportsFloat, maturity: typing.SupportsFloat, bondMaturity: typing.SupportsFloat) -> float:
        """
        Returns discount bond option price.
        """
    def eta(self) -> float:
        """
        Returns second factor volatility.
        """
    def rho(self) -> float:
        """
        Returns correlation between factors.
        """
    def sigma(self) -> float:
        """
        Returns first factor volatility.
        """
class G2SwaptionEngine(base.PricingEngine):
    """
    Swaption engine for two-factor G2++ model.
    """
    def __init__(self, model: G2, range: typing.SupportsFloat, intervals: typing.SupportsInt) -> None:
        """
        Constructs G2 swaption engine with integration parameters.
        """
class GBPCurrency(Currency):
    """
    ! The ISO three-letter code is GBP; the numeric code is 826.
            It is divided into 100 pence.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class GELCurrency(Currency):
    """
    ! The ISO three-letter code is GEL; the numeric code is 981.
            It is divided into 100 tetri.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class GHSCurrency(Currency):
    """
    ! Ghanaian cedi
    /*! The ISO three-letter code is GHS; the numeric code is 936.
         It is divided into 100 pesewas.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class GRDCurrency(Currency):
    """
    ! The ISO three-letter code was GRD; the numeric code was 300.
            It was divided in 100 lepta.
    
            Obsoleted by the Euro since 2001.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class GapPayoff(base.StrikedTypePayoff):
    """
    Gap payoff: vanilla minus digital, with two strikes.
    """
    def __init__(self, type: OptionType, strike: typing.SupportsFloat, secondStrike: typing.SupportsFloat) -> None:
        ...
    def secondStrike(self) -> float:
        """
        Returns the second (payoff) strike.
        """
class GarmanKohlhagenProcess(GeneralizedBlackScholesProcess):
    """
    Garman-Kohlhagen process for FX options.
    """
    @typing.overload
    def __init__(self, x0: QuoteHandle, foreignRiskFreeTS: YieldTermStructureHandle, domesticRiskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle) -> None:
        ...
    @typing.overload
    def __init__(self, x0: QuoteHandle, foreignRiskFreeTS: YieldTermStructureHandle, domesticRiskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        ...
    @typing.overload
    def __init__(self, x0: base.Quote, foreignRiskFreeTS: base.YieldTermStructure, domesticRiskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    @typing.overload
    def __init__(self, x0: base.Quote, foreignRiskFreeTS: base.YieldTermStructure, domesticRiskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure, discretization: base.StochasticProcess1D.discretization, forceDiscretization: bool = False) -> None:
        """
        Constructs from term structures with discretization (handles created internally).
        """
class GbpLiborSwapIsdaFix(SwapIndex):
    """
    GBP LIBOR swap rate (ISDA fix).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class GeneralizedBlackScholesProcess(base.StochasticProcess1D):
    """
    Generalized Black-Scholes-Merton stochastic process.
    """
    @typing.overload
    def __init__(self, x0: QuoteHandle, dividendTS: YieldTermStructureHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle) -> None:
        ...
    @typing.overload
    def __init__(self, x0: QuoteHandle, dividendTS: YieldTermStructureHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle, discretization: base.StochasticProcess1D.discretization) -> None:
        ...
    @typing.overload
    def __init__(self, x0: base.Quote, dividendTS: base.YieldTermStructure, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    @typing.overload
    def __init__(self, x0: base.Quote, dividendTS: base.YieldTermStructure, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure, discretization: base.StochasticProcess1D.discretization) -> None:
        """
        Constructs from term structures with discretization (handles created internally).
        """
    @typing.overload
    def __init__(self, x0: QuoteHandle, dividendTS: YieldTermStructureHandle, riskFreeTS: YieldTermStructureHandle, blackVolTS: BlackVolTermStructureHandle, localVolTS: LocalVolTermStructureHandle) -> None:
        ...
    @typing.overload
    def __init__(self, x0: base.Quote, dividendTS: base.YieldTermStructure, riskFreeTS: base.YieldTermStructure, blackVolTS: base.BlackVolTermStructure, localVolTS: base.LocalVolTermStructure) -> None:
        """
        Constructs with external local vol (handles created internally).
        """
    def blackVolatility(self) -> BlackVolTermStructureHandle:
        """
        Returns the Black volatility term structure handle.
        """
    def dividendYield(self) -> YieldTermStructureHandle:
        """
        Returns the dividend yield term structure handle.
        """
    def localVolatility(self) -> LocalVolTermStructureHandle:
        """
        Returns the local volatility term structure handle.
        """
    def riskFreeRate(self) -> YieldTermStructureHandle:
        """
        Returns the risk-free rate term structure handle.
        """
    def stateVariable(self) -> QuoteHandle:
        """
        Returns the state variable handle.
        """
class Germany(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Ascension Thursday</li>
            <li>Whit Monday</li>
            <li>Corpus Christi</li>
            <li>Labour Day, May 1st</li>
            <li>National Day, October 3rd</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            </ul>
    
            Holidays for the Frankfurt Stock exchange
            (data from http://deutsche-boerse.com/):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Christmas' Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Christmas Holiday, December 26th</li>
            </ul>
    
            Holidays for the Xetra exchange
            (data from http://deutsche-boerse.com/):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Christmas' Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Christmas Holiday, December 26th</li>
            </ul>
    
            Holidays for the Eurex exchange
            (data from http://www.eurexchange.com/index.html):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Christmas' Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Christmas Holiday, December 26th</li>
            <li>New Year's Eve, December 31st</li>
            </ul>
    
            Holidays for the Euwax exchange
            (data from http://www.boerse-stuttgart.de):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Whit Monday</li>
            <li>Christmas' Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Christmas Holiday, December 26th</li>
            </ul>
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested
                  against a list of known holidays.
    """
    class Market:
        """
        ! German calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          FrankfurtStockExchange : !< Frankfurt stock-exchange
        
          Xetra : !< Xetra
        
          Eurex : !< Eurex
        
          Euwax : !< Euwax
        """
        Eurex: typing.ClassVar[Germany.Market]  # value = <Market.Eurex: 3>
        Euwax: typing.ClassVar[Germany.Market]  # value = <Market.Euwax: 4>
        FrankfurtStockExchange: typing.ClassVar[Germany.Market]  # value = <Market.FrankfurtStockExchange: 1>
        Settlement: typing.ClassVar[Germany.Market]  # value = <Market.Settlement: 0>
        Xetra: typing.ClassVar[Germany.Market]  # value = <Market.Xetra: 2>
        __members__: typing.ClassVar[dict[str, Germany.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'FrankfurtStockExchange': <Market.FrankfurtStockExchange: 1>, 'Xetra': <Market.Xetra: 2>, 'Eurex': <Market.Eurex: 3>, 'Euwax': <Market.Euwax: 4>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Eurex: typing.ClassVar[Germany.Market]  # value = <Market.Eurex: 3>
    Euwax: typing.ClassVar[Germany.Market]  # value = <Market.Euwax: 4>
    FrankfurtStockExchange: typing.ClassVar[Germany.Market]  # value = <Market.FrankfurtStockExchange: 1>
    Settlement: typing.ClassVar[Germany.Market]  # value = <Market.Settlement: 0>
    Xetra: typing.ClassVar[Germany.Market]  # value = <Market.Xetra: 2>
    def __init__(self, market: Germany.Market = ...) -> None:
        ...
class Greeks:
    """
    Container for first-order Greeks.
    """
    def __init__(self) -> None:
        ...
    @property
    def delta(self) -> float:
        """
        Delta sensitivity.
        """
    @delta.setter
    def delta(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def dividendRho(self) -> float:
        """
        Dividend rho sensitivity.
        """
    @dividendRho.setter
    def dividendRho(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def gamma(self) -> float:
        """
        Gamma sensitivity.
        """
    @gamma.setter
    def gamma(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def rho(self) -> float:
        """
        Rho sensitivity.
        """
    @rho.setter
    def rho(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def theta(self) -> float:
        """
        Theta sensitivity.
        """
    @theta.setter
    def theta(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def vega(self) -> float:
        """
        Vega sensitivity.
        """
    @vega.setter
    def vega(self, arg0: typing.SupportsFloat) -> None:
        ...
class HKDCurrency(Currency):
    """
    ! The ISO three-letter code is HKD; the numeric code is 344.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class HRKCurrency(Currency):
    """
    ! The ISO three-letter code was HRK; the numeric code was 191.
            It was divided into 100 lipa.
    
            Obsoleted by the Euro since 2023.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class HUFCurrency(Currency):
    """
    ! The ISO three-letter code is HUF; the numeric code is 348.
            It has no subdivisions.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class HestonModel(base.CalibratedModel):
    """
    Heston stochastic volatility model.
    """
    def __init__(self, process: HestonProcess) -> None:
        """
        Constructs Heston model from process.
        """
    def kappa(self) -> float:
        """
        Returns mean-reversion speed.
        """
    def rho(self) -> float:
        """
        Returns correlation.
        """
    def sigma(self) -> float:
        """
        Returns volatility of volatility.
        """
    def theta(self) -> float:
        """
        Returns long-term variance.
        """
    def v0(self) -> float:
        """
        Returns initial variance.
        """
class HestonModelHandle:
    """
    Handle to HestonModel objects.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: HestonModelHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: HestonModelHandle) -> bool:
        ...
    def __ne__(self, arg0: HestonModelHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> HestonModel:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> HestonModel:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class HestonProcess(base.StochasticProcess):
    """
    Heston stochastic volatility process.
    """
    class Discretization:
        """
        Discretization schemes for Heston process simulation.
        
        Members:
        
          PartialTruncation
        
          FullTruncation
        
          Reflection
        
          NonCentralChiSquareVariance
        
          QuadraticExponential
        
          QuadraticExponentialMartingale
        
          BroadieKayaExactSchemeLobatto
        
          BroadieKayaExactSchemeLaguerre
        
          BroadieKayaExactSchemeTrapezoidal
        """
        BroadieKayaExactSchemeLaguerre: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeLaguerre: 7>
        BroadieKayaExactSchemeLobatto: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeLobatto: 6>
        BroadieKayaExactSchemeTrapezoidal: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeTrapezoidal: 8>
        FullTruncation: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.FullTruncation: 1>
        NonCentralChiSquareVariance: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.NonCentralChiSquareVariance: 3>
        PartialTruncation: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.PartialTruncation: 0>
        QuadraticExponential: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.QuadraticExponential: 4>
        QuadraticExponentialMartingale: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.QuadraticExponentialMartingale: 5>
        Reflection: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.Reflection: 2>
        __members__: typing.ClassVar[dict[str, HestonProcess.Discretization]]  # value = {'PartialTruncation': <Discretization.PartialTruncation: 0>, 'FullTruncation': <Discretization.FullTruncation: 1>, 'Reflection': <Discretization.Reflection: 2>, 'NonCentralChiSquareVariance': <Discretization.NonCentralChiSquareVariance: 3>, 'QuadraticExponential': <Discretization.QuadraticExponential: 4>, 'QuadraticExponentialMartingale': <Discretization.QuadraticExponentialMartingale: 5>, 'BroadieKayaExactSchemeLobatto': <Discretization.BroadieKayaExactSchemeLobatto: 6>, 'BroadieKayaExactSchemeLaguerre': <Discretization.BroadieKayaExactSchemeLaguerre: 7>, 'BroadieKayaExactSchemeTrapezoidal': <Discretization.BroadieKayaExactSchemeTrapezoidal: 8>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BroadieKayaExactSchemeLaguerre: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeLaguerre: 7>
    BroadieKayaExactSchemeLobatto: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeLobatto: 6>
    BroadieKayaExactSchemeTrapezoidal: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.BroadieKayaExactSchemeTrapezoidal: 8>
    FullTruncation: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.FullTruncation: 1>
    NonCentralChiSquareVariance: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.NonCentralChiSquareVariance: 3>
    PartialTruncation: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.PartialTruncation: 0>
    QuadraticExponential: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.QuadraticExponential: 4>
    QuadraticExponentialMartingale: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.QuadraticExponentialMartingale: 5>
    Reflection: typing.ClassVar[HestonProcess.Discretization]  # value = <Discretization.Reflection: 2>
    @typing.overload
    def __init__(self, riskFreeRate: YieldTermStructureHandle, dividendYield: YieldTermStructureHandle, s0: QuoteHandle, v0: typing.SupportsFloat, kappa: typing.SupportsFloat, theta: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, d: HestonProcess.Discretization = ...) -> None:
        ...
    @typing.overload
    def __init__(self, riskFreeRate: base.YieldTermStructure, dividendYield: base.YieldTermStructure, s0: base.Quote, v0: typing.SupportsFloat, kappa: typing.SupportsFloat, theta: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, d: HestonProcess.Discretization = ...) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    def dividendYield(self) -> YieldTermStructureHandle:
        """
        Returns the dividend yield term structure handle.
        """
    def kappa(self) -> float:
        """
        Returns the mean-reversion speed.
        """
    def pdf(self, x: typing.SupportsFloat, v: typing.SupportsFloat, t: typing.SupportsFloat, eps: typing.SupportsFloat = 0.001) -> float:
        """
        Returns the probability density at (x, v) for time t, where x is log-spot.
        """
    def rho(self) -> float:
        """
        Returns the correlation between spot and variance.
        """
    def riskFreeRate(self) -> YieldTermStructureHandle:
        """
        Returns the risk-free rate term structure handle.
        """
    def s0(self) -> QuoteHandle:
        """
        Returns the initial spot price handle.
        """
    def sigma(self) -> float:
        """
        Returns the volatility of volatility.
        """
    def theta(self) -> float:
        """
        Returns the long-term variance.
        """
    def v0(self) -> float:
        """
        Returns the initial variance.
        """
class HongKong(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labor Day, May 1st (possibly moved to Monday)</li>
            <li>SAR Establishment Day, July 1st (possibly moved to Monday)</li>
            <li>National Day, October 1st (possibly moved to Monday)</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2004-2015 only:)
            <ul>
            <li>Lunar New Year</li>
            <li>Chinese New Year</li>
            <li>Ching Ming Festival</li>
            <li>Buddha's birthday</li>
            <li>Tuen NG Festival</li>
            <li>Mid-autumn Festival</li>
            <li>Chung Yeung Festival</li>
            </ul>
    
            Data from <http://www.hkex.com.hk>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          HKEx : !< Hong Kong stock exchange
        """
        HKEx: typing.ClassVar[HongKong.Market]  # value = <Market.HKEx: 0>
        __members__: typing.ClassVar[dict[str, HongKong.Market]]  # value = {'HKEx': <Market.HKEx: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    HKEx: typing.ClassVar[HongKong.Market]  # value = <Market.HKEx: 0>
    def __init__(self, m: HongKong.Market = ...) -> None:
        ...
class HullWhite(Vasicek, base.TermStructureConsistentModel):
    """
    Hull-White extended Vasicek model: dr = (theta(t) - a*r)dt + sigma*dW.
    """
    @staticmethod
    def convexityBias(futurePrice: typing.SupportsFloat, t: typing.SupportsFloat, T: typing.SupportsFloat, sigma: typing.SupportsFloat, a: typing.SupportsFloat) -> float:
        """
        Computes futures convexity bias.
        """
    @typing.overload
    def __init__(self, termStructure: YieldTermStructureHandle, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.01) -> None:
        """
        Constructs Hull-White model with term structure, mean reversion, and volatility.
        """
    @typing.overload
    def __init__(self, termStructure: base.YieldTermStructure, a: typing.SupportsFloat = 0.1, sigma: typing.SupportsFloat = 0.01) -> None:
        """
        Constructs Hull-White model from term structure.
        """
    def discountBondOption(self, type: OptionType, strike: typing.SupportsFloat, maturity: typing.SupportsFloat, bondMaturity: typing.SupportsFloat) -> float:
        """
        Returns discount bond option price.
        """
class Hungary(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Good Friday (since 2017)</li>
            <li>Easter Monday</li>
            <li>Whit(Pentecost) Monday </li>
            <li>New Year's Day, January 1st</li>
            <li>National Day, March 15th</li>
            <li>Labour Day, May 1st</li>
            <li>Constitution Day, August 20th</li>
            <li>Republic Day, October 23rd</li>
            <li>All Saints Day, November 1st</li>
            <li>Christmas, December 25th</li>
            <li>2nd Day of Christmas, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class IDRCurrency(Currency):
    """
    ! The ISO three-letter code is IDR; the numeric code is 360.
            It is divided in 100 sen.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class IEPCurrency(Currency):
    """
    ! The ISO three-letter code was IEP; the numeric code was 372.
            It was divided in 100 pence.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ILSCurrency(Currency):
    """
    ! The ISO three-letter code is ILS; the numeric code is 376.
            It is divided in 100 agorot.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class INRCurrency(Currency):
    """
    ! The ISO three-letter code is INR; the numeric code is 356.
            It is divided in 100 paise.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class IQDCurrency(Currency):
    """
    ! The ISO three-letter code is IQD; the numeric code is 368.
            It is divided in 1000 fils.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class IRRCurrency(Currency):
    """
    ! The ISO three-letter code is IRR; the numeric code is 364.
            It has no subdivisions.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ISKCurrency(Currency):
    """
    ! The ISO three-letter code is ISK; the numeric code is 352.
            It is divided in 100 aurar.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ITLCurrency(Currency):
    """
    ! The ISO three-letter code was ITL; the numeric code was 380.
            It had no subdivisions.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class IborCoupon(FloatingRateCoupon):
    """
    Coupon paying a Libor-type index.
    """
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, startDate: Date, endDate: Date, fixingDays: typing.SupportsInt, index: ..., gearing: typing.SupportsFloat = 1.0, spread: typing.SupportsFloat = 0.0, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., dayCounter: typing.Any = None, isInArrears: bool = False, exCouponDate: Date = ...) -> None:
        """
        Constructs an Ibor coupon.
        """
    def fixingDate(self) -> Date:
        """
        Returns the fixing date.
        """
    def fixingEndDate(self) -> Date:
        """
        Returns the end of the deposit period underlying the coupon fixing.
        """
    def fixingMaturityDate(self) -> Date:
        """
        Returns the end of the deposit period underlying the fixing.
        """
    def fixingValueDate(self) -> Date:
        """
        Returns the start of the deposit period underlying the fixing.
        """
    def iborIndex(self) -> ...:
        """
        Returns the Ibor index.
        """
    def spanningTime(self) -> float:
        """
        Returns the period underlying the coupon fixing as a year fraction.
        """
class IborCouponSettings:
    """
    Per-session settings for IborCoupon class.
    """
    @staticmethod
    def instance() -> IborCouponSettings:
        """
        Returns the singleton instance.
        """
    def createAtParCoupons(self) -> None:
        """
        Switches to par coupon creation.
        """
    def createIndexedCoupons(self) -> None:
        """
        Switches to indexed coupon creation.
        """
    def usingAtParCoupons(self) -> bool:
        """
        Returns whether par coupons are being used.
        """
class IborIndex(base.InterestRateIndex):
    """
    Base class for IBOR indexes (e.g. Euribor, Libor).
    """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool, dayCounter: DayCounter) -> None:
        """
        Constructs an IBOR index without forwarding curve.
        """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool, dayCounter: DayCounter, h: ...) -> None:
        """
        Constructs an IBOR index with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool, dayCounter: DayCounter, forwardingTermStructure: ...) -> None:
        """
        Constructs an IBOR index with forwarding term structure.
        """
    def businessDayConvention(self) -> BusinessDayConvention:
        """
        Returns the business day convention.
        """
    def clone(self, forwardingTermStructure: ...) -> IborIndex:
        """
        Returns a copy linked to a different forwarding curve.
        """
    def endOfMonth(self) -> bool:
        """
        Returns True if end-of-month adjustment applies.
        """
    def forwardingTermStructure(self) -> ...:
        """
        Returns the forwarding term structure handle.
        """
class IborLeg:
    """
    Helper class for building a leg of Ibor coupons.
    """
    def __init__(self, schedule: Schedule, index: ...) -> None:
        """
        Constructs an IborLeg from a schedule and index.
        """
    def build(self) -> list[base.CashFlow]:
        """
        Builds and returns the leg of cash flows.
        """
    def inArrears(self, flag: bool = True) -> IborLeg:
        ...
    @typing.overload
    def withCaps(self, cap: typing.SupportsFloat) -> IborLeg:
        ...
    @typing.overload
    def withCaps(self, caps: collections.abc.Sequence[typing.SupportsFloat]) -> IborLeg:
        ...
    def withExCouponPeriod(self, period: Period, calendar: Calendar, convention: BusinessDayConvention, endOfMonth: bool = False) -> IborLeg:
        ...
    @typing.overload
    def withFixingDays(self, fixingDays: typing.SupportsInt) -> IborLeg:
        ...
    @typing.overload
    def withFixingDays(self, fixingDays: collections.abc.Sequence[typing.SupportsInt]) -> IborLeg:
        ...
    @typing.overload
    def withFloors(self, floor: typing.SupportsFloat) -> IborLeg:
        ...
    @typing.overload
    def withFloors(self, floors: collections.abc.Sequence[typing.SupportsFloat]) -> IborLeg:
        ...
    @typing.overload
    def withGearings(self, gearing: typing.SupportsFloat) -> IborLeg:
        ...
    @typing.overload
    def withGearings(self, gearings: collections.abc.Sequence[typing.SupportsFloat]) -> IborLeg:
        ...
    @typing.overload
    def withNotionals(self, nominal: typing.SupportsFloat) -> IborLeg:
        ...
    @typing.overload
    def withNotionals(self, nominals: collections.abc.Sequence[typing.SupportsFloat]) -> IborLeg:
        ...
    def withPaymentAdjustment(self, convention: BusinessDayConvention) -> IborLeg:
        ...
    def withPaymentCalendar(self, calendar: Calendar) -> IborLeg:
        ...
    def withPaymentDayCounter(self, dayCounter: DayCounter) -> IborLeg:
        ...
    def withPaymentLag(self, lag: typing.SupportsInt) -> IborLeg:
        ...
    @typing.overload
    def withSpreads(self, spread: typing.SupportsFloat) -> IborLeg:
        ...
    @typing.overload
    def withSpreads(self, spreads: collections.abc.Sequence[typing.SupportsFloat]) -> IborLeg:
        ...
    def withZeroPayments(self, flag: bool = True) -> IborLeg:
        ...
class Iceland(Calendar):
    """
    ! Holidays for the Iceland stock exchange
            (data from <http://www.icex.is/is/calendar?languageID=1>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Holy Thursday</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>First day of Summer (third or fourth Thursday in April)</li>
            <li>Labour Day, May 1st</li>
            <li>Ascension Thursday</li>
            <li>Pentecost Monday</li>
            <li>Independence Day, June 17th</li>
            <li>Commerce Day, first Monday in August</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          ICEX : !< Iceland stock exchange
        """
        ICEX: typing.ClassVar[Iceland.Market]  # value = <Market.ICEX: 0>
        __members__: typing.ClassVar[dict[str, Iceland.Market]]  # value = {'ICEX': <Market.ICEX: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    ICEX: typing.ClassVar[Iceland.Market]  # value = <Market.ICEX: 0>
    def __init__(self, m: Iceland.Market = ...) -> None:
        ...
class India(Calendar):
    """
    ! Clearing holidays for the National Stock Exchange
            (data from <http://www.nse-india.com/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Republic Day, January 26th</li>
            <li>Good Friday</li>
            <li>Ambedkar Jayanti, April 14th</li>
            <li>May Day, May 1st</li>
            <li>Independence Day, August 15th</li>
            <li>Gandhi Jayanti, October 2nd</li>
            <li>Christmas, December 25th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2005-2014, 2019-2025 only:)
            <ul>
            <li>Bakri Id</li>
            <li>Moharram</li>
            <li>Mahashivratri</li>
            <li>Holi</li>
            <li>Ram Navami</li>
            <li>Mahavir Jayanti</li>
            <li>Id-E-Milad</li>
            <li>Maharashtra Day</li>
            <li>Buddha Pournima</li>
            <li>Ganesh Chaturthi</li>
            <li>Dasara</li>
            <li>Laxmi Puja</li>
            <li>Bhaubeej</li>
            <li>Ramzan Id</li>
            <li>Guru Nanak Jayanti</li>
            </ul>
    
            Note: The holidays Ramzan Id, Bakri Id and Id-E-Milad rely on estimates for 2024-2025.
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          NSE : !< National Stock Exchange
        """
        NSE: typing.ClassVar[India.Market]  # value = <Market.NSE: 0>
        __members__: typing.ClassVar[dict[str, India.Market]]  # value = {'NSE': <Market.NSE: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    NSE: typing.ClassVar[India.Market]  # value = <Market.NSE: 0>
    def __init__(self, m: India.Market = ...) -> None:
        ...
class Indonesia(Calendar):
    """
    ! Holidays for the Indonesia stock exchange
            (data from <http://www.idx.co.id/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Ascension of Jesus Christ</li>
            <li>Independence Day, August 17th</li>
            <li>Christmas, December 25th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2005-2014 only:)
            <ul>
            <li>Idul Adha</li>
            <li>Ied Adha</li>
            <li>Imlek</li>
            <li>Moslem's New Year Day</li>
            <li>Chinese New Year</li>
            <li>Nyepi (Saka's New Year)</li>
            <li>Birthday of Prophet Muhammad SAW</li>
            <li>Waisak</li>
            <li>Ascension of Prophet Muhammad SAW</li>
            <li>Idul Fitri</li>
            <li>Ied Fitri</li>
            <li>Other national leaves</li>
            </ul>
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          BEJ : !< Jakarta stock exchange (merged into IDX)
        
          JSX : !< Jakarta stock exchange (merged into IDX)
        
          IDX : !< Indonesia stock exchange
        """
        BEJ: typing.ClassVar[Indonesia.Market]  # value = <Market.BEJ: 0>
        IDX: typing.ClassVar[Indonesia.Market]  # value = <Market.IDX: 2>
        JSX: typing.ClassVar[Indonesia.Market]  # value = <Market.JSX: 1>
        __members__: typing.ClassVar[dict[str, Indonesia.Market]]  # value = {'BEJ': <Market.BEJ: 0>, 'JSX': <Market.JSX: 1>, 'IDX': <Market.IDX: 2>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BEJ: typing.ClassVar[Indonesia.Market]  # value = <Market.BEJ: 0>
    IDX: typing.ClassVar[Indonesia.Market]  # value = <Market.IDX: 2>
    JSX: typing.ClassVar[Indonesia.Market]  # value = <Market.JSX: 1>
    def __init__(self, m: Indonesia.Market = ...) -> None:
        ...
class IntegralEngine(base.PricingEngine):
    """
    Pricing engine for European options using integral approach.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs with a Black-Scholes process.
        """
class Integration:
    """
    Integration methods for Heston engine.
    """
    @staticmethod
    def discreteSimpson(evaluations: typing.SupportsInt = 1000) -> Integration:
        ...
    @staticmethod
    def discreteTrapezoid(evaluations: typing.SupportsInt = 1000) -> Integration:
        ...
    @staticmethod
    def expSinh(relTolerance: typing.SupportsFloat = 1e-08) -> Integration:
        ...
    @staticmethod
    def gaussChebyshev(integrationOrder: typing.SupportsInt = 128) -> Integration:
        ...
    @staticmethod
    def gaussChebyshev2nd(integrationOrder: typing.SupportsInt = 128) -> Integration:
        ...
    @staticmethod
    def gaussKronrod(absTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt = 1000) -> Integration:
        ...
    @staticmethod
    def gaussLaguerre(integrationOrder: typing.SupportsInt = 128) -> Integration:
        ...
    @staticmethod
    def gaussLegendre(integrationOrder: typing.SupportsInt = 128) -> Integration:
        ...
    @staticmethod
    def gaussLobatto(relTolerance: typing.SupportsFloat, absTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt = 1000, useConvergenceEstimate: bool = False) -> Integration:
        ...
    @staticmethod
    def simpson(absTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt = 1000) -> Integration:
        ...
    @staticmethod
    def trapezoid(absTolerance: typing.SupportsFloat, maxEvaluations: typing.SupportsInt = 1000) -> Integration:
        ...
    def isAdaptiveIntegration(self) -> bool:
        ...
    def numberOfEvaluations(self) -> int:
        ...
class InterestRate:
    """
    Interest rate with compounding algebra.
    """
    @staticmethod
    @typing.overload
    def impliedRate(compound: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, time: typing.SupportsFloat) -> InterestRate:
        """
        Implied rate from a compound factor over a time period.
        """
    @staticmethod
    @typing.overload
    def impliedRate(compound: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, startDate: Date, endDate: Date, refStart: Date = ..., refEnd: Date = ...) -> InterestRate:
        """
        Implied rate from a compound factor between two dates.
        """
    def __eq__(self, arg0: InterestRate) -> bool:
        ...
    def __float__(self) -> float:
        ...
    def __hash__(self) -> int:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor returning a null interest rate.
        """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency) -> None:
        """
        Construct an interest rate with the given parameters.
        """
    def __ne__(self, arg0: InterestRate) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @typing.overload
    def compoundFactor(self, time: typing.SupportsFloat) -> float:
        """
        Compound factor for a given time period.
        """
    @typing.overload
    def compoundFactor(self, startDate: Date, endDate: Date, refStart: Date = ..., refEnd: Date = ...) -> float:
        """
        Compound factor between two dates.
        """
    def compounding(self) -> Compounding:
        """
        Returns the compounding convention.
        """
    def dayCounter(self) -> DayCounter:
        """
        Returns the day counter.
        """
    @typing.overload
    def discountFactor(self, time: typing.SupportsFloat) -> float:
        """
        Discount factor for a given time period.
        """
    @typing.overload
    def discountFactor(self, startDate: Date, endDate: Date, refStart: Date = ..., refEnd: Date = ...) -> float:
        """
        Discount factor between two dates.
        """
    @typing.overload
    def equivalentRate(self, compounding: Compounding, frequency: Frequency, time: typing.SupportsFloat) -> InterestRate:
        """
        Equivalent rate with different compounding over a time period.
        """
    @typing.overload
    def equivalentRate(self, dayCounter: DayCounter, compounding: Compounding, frequency: Frequency, startDate: Date, endDate: Date, refStart: Date = ..., refEnd: Date = ...) -> InterestRate:
        """
        Equivalent rate with different compounding between two dates.
        """
    def frequency(self) -> Frequency:
        """
        Returns the compounding frequency.
        """
    def isNull(self) -> bool:
        """
        Returns true if the rate is null (uninitialized).
        """
    def rate(self) -> float:
        """
        Returns the rate value.
        """
class InverseCumulativeNormal:
    """
    Inverse cumulative normal distribution function.
    """
    @staticmethod
    def standard_value(x: typing.SupportsFloat) -> float:
        """
        Returns the inverse for standard normal (average=0, sigma=1).
        """
    def __call__(self, x: typing.SupportsFloat) -> float:
        """
        Returns the inverse cumulative normal at x.
        """
    def __init__(self, average: typing.SupportsFloat = 0.0, sigma: typing.SupportsFloat = 1.0) -> None:
        """
        Constructs InverseCumulativeNormal.
        """
class IsdaAccrualBias:
    """
    ISDA CDS engine accrual bias.
    
    Members:
    
      HalfDayBias : Half day bias.
    
      NoBias : No bias.
    """
    HalfDayBias: typing.ClassVar[IsdaAccrualBias]  # value = <IsdaAccrualBias.HalfDayBias: 0>
    NoBias: typing.ClassVar[IsdaAccrualBias]  # value = <IsdaAccrualBias.NoBias: 1>
    __members__: typing.ClassVar[dict[str, IsdaAccrualBias]]  # value = {'HalfDayBias': <IsdaAccrualBias.HalfDayBias: 0>, 'NoBias': <IsdaAccrualBias.NoBias: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class IsdaCdsEngine(base.PricingEngine):
    """
    ISDA-compliant CDS engine.
    """
    @typing.overload
    def __init__(self, probability: DefaultProbabilityTermStructureHandle, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, includeSettlementDateFlows: bool | None = None, numericalFix: IsdaNumericalFix = ..., accrualBias: IsdaAccrualBias = ..., forwardsInCouponPeriod: IsdaForwardsInCouponPeriod = ...) -> None:
        """
        Constructs from handles.
        """
    @typing.overload
    def __init__(self, probability: base.DefaultProbabilityTermStructure, recoveryRate: typing.SupportsFloat, discountCurve: base.YieldTermStructure, includeSettlementDateFlows: bool | None = None, numericalFix: IsdaNumericalFix = ..., accrualBias: IsdaAccrualBias = ..., forwardsInCouponPeriod: IsdaForwardsInCouponPeriod = ...) -> None:
        """
        Constructs from term structures (handles created internally).
        """
    def isdaCreditCurve(self) -> DefaultProbabilityTermStructureHandle:
        """
        ISDA credit curve.
        """
    def isdaRateCurve(self) -> YieldTermStructureHandle:
        """
        ISDA rate curve.
        """
class IsdaForwardsInCouponPeriod:
    """
    ISDA CDS forwards in coupon period.
    
    Members:
    
      Flat : Flat forwards.
    
      Piecewise : Piecewise forwards.
    """
    Flat: typing.ClassVar[IsdaForwardsInCouponPeriod]  # value = <IsdaForwardsInCouponPeriod.Flat: 0>
    Piecewise: typing.ClassVar[IsdaForwardsInCouponPeriod]  # value = <IsdaForwardsInCouponPeriod.Piecewise: 1>
    __members__: typing.ClassVar[dict[str, IsdaForwardsInCouponPeriod]]  # value = {'Flat': <IsdaForwardsInCouponPeriod.Flat: 0>, 'Piecewise': <IsdaForwardsInCouponPeriod.Piecewise: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class IsdaNumericalFix:
    """
    ISDA CDS engine numerical fix.
    
    Members:
    
      IsdaNone : No fix.
    
      Taylor : Taylor expansion fix.
    """
    IsdaNone: typing.ClassVar[IsdaNumericalFix]  # value = <IsdaNumericalFix.IsdaNone: 0>
    Taylor: typing.ClassVar[IsdaNumericalFix]  # value = <IsdaNumericalFix.Taylor: 1>
    __members__: typing.ClassVar[dict[str, IsdaNumericalFix]]  # value = {'IsdaNone': <IsdaNumericalFix.IsdaNone: 0>, 'Taylor': <IsdaNumericalFix.Taylor: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Israel(Calendar):
    """
    ! Due to the lack of reliable sources, the settlement calendar
            has the same holidays as the Tel Aviv stock-exchange.
    
            Holidays for the Tel-Aviv Stock Exchange
            (data from <http://www.tase.co.il>):
            <ul>
            <li>Friday</li>
            <li>Saturday</li>
            </ul>
            Other holidays for wich no rule is given
            (data available for 2013-2044 only:)
            <ul>
            <li>Purim, Adar 14th (between Feb 24th & Mar 26th)</li>
            <li>Passover I, Nisan 15th (between Mar 26th & Apr 25th)</li>
            <li>Passover VII, Nisan 21st (between Apr 1st & May 1st)</li>
            <li>Memorial Day, Nisan 27th (between Apr 7th & May 7th)</li>
            <li>Indipendence Day, Iyar 5th (between Apr 15th & May 15th)</li>
            <li>Pentecost (Shavuot), Sivan 6th (between May 15th & June 14th)</li>
            <li>Fast Day</li>
            <li>Jewish New Year, Tishrei 1st & 2nd (between Sep 5th & Oct 5th)</li>
            <li>Yom Kippur, Tishrei 10th (between Sep 14th & Oct 14th)</li>
            <li>Sukkoth, Tishrei 15th (between Sep 19th & Oct 19th)</li>
            <li>Simchat Tora, Tishrei 22nd (between Sep 26th & Oct 26th)</li>
            </ul>
    
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          TASE : !< Tel-Aviv stock exchange calendar
        """
        Settlement: typing.ClassVar[Israel.Market]  # value = <Market.Settlement: 0>
        TASE: typing.ClassVar[Israel.Market]  # value = <Market.TASE: 1>
        __members__: typing.ClassVar[dict[str, Israel.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'TASE': <Market.TASE: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Settlement: typing.ClassVar[Israel.Market]  # value = <Market.Settlement: 0>
    TASE: typing.ClassVar[Israel.Market]  # value = <Market.TASE: 1>
    def __init__(self, market: Israel.Market = ...) -> None:
        ...
class Italy(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th</li>
            <li>Easter Monday</li>
            <li>Liberation Day, April 25th</li>
            <li>Labour Day, May 1st</li>
            <li>Republic Day, June 2nd (since 2000)</li>
            <li>Assumption, August 15th</li>
            <li>All Saint's Day, November 1st</li>
            <li>Immaculate Conception Day, December 8th</li>
            <li>Christmas Day, December 25th</li>
            <li>St. Stephen's Day, December 26th</li>
            </ul>
    
            Holidays for the stock exchange (data from http://www.borsaitalia.it):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Labour Day, May 1st</li>
            <li>Assumption, August 15th</li>
            <li>Christmas' Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen, December 26th</li>
            <li>New Year's Eve, December 31st</li>
            </ul>
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested against a
                  list of known holidays.
    """
    class Market:
        """
        ! Italian calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          Exchange : !< Milan stock-exchange calendar
        """
        Exchange: typing.ClassVar[Italy.Market]  # value = <Market.Exchange: 1>
        Settlement: typing.ClassVar[Italy.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, Italy.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'Exchange': <Market.Exchange: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Exchange: typing.ClassVar[Italy.Market]  # value = <Market.Exchange: 1>
    Settlement: typing.ClassVar[Italy.Market]  # value = <Market.Settlement: 0>
    def __init__(self, market: Italy.Market = ...) -> None:
        ...
class JODCurrency(Currency):
    """
    ! Jordanian dinar
    /*! The ISO three-letter code is JOD; the numeric code is 400.
         It is divided into 100 qirshes.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class JPYCurrency(Currency):
    """
    ! The ISO three-letter code is JPY; the numeric code is 392.
            It is divided into 100 sen.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class JamshidianSwaptionEngine(base.PricingEngine):
    """
    Jamshidian swaption engine using bond option decomposition.
    """
    @typing.overload
    def __init__(self, model: base.OneFactorAffineModel, termStructure: YieldTermStructureHandle = ...) -> None:
        """
        Constructs Jamshidian engine with one-factor affine model.
        """
    @typing.overload
    def __init__(self, model: base.OneFactorAffineModel, termStructure: base.YieldTermStructure) -> None:
        """
        Constructs Jamshidian engine with model and term structure.
        """
class Japan(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Bank Holiday, January 2nd</li>
            <li>Bank Holiday, January 3rd</li>
            <li>Coming of Age Day, 2nd Monday in January</li>
            <li>National Foundation Day, February 11th</li>
            <li>Emperor's Birthday, February 23rd since 2020 and December 23rd before</li>
            <li>Vernal Equinox</li>
            <li>Greenery Day, April 29th</li>
            <li>Constitution Memorial Day, May 3rd</li>
            <li>Holiday for a Nation, May 4th</li>
            <li>Children's Day, May 5th</li>
            <li>Marine Day, 3rd Monday in July</li>
            <li>Mountain Day, August 11th (from 2016 onwards)</li>
            <li>Respect for the Aged Day, 3rd Monday in September</li>
            <li>Autumnal Equinox</li>
            <li>Health and Sports Day, 2nd Monday in October</li>
            <li>National Culture Day, November 3rd</li>
            <li>Labor Thanksgiving Day, November 23rd</li>
            <li>Bank Holiday, December 31st</li>
            <li>a few one-shot holidays</li>
            </ul>
            Holidays falling on a Sunday are observed on the Monday following
            except for the bank holidays associated with the new year.
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class JointCalendar(Calendar):
    """
    ! Depending on the chosen rule, this calendar has a set of
            business days given by either the union or the intersection
            of the sets of business days of the given calendars.
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested by
                  reproducing the calculations.
    """
    @typing.overload
    def __init__(self, param_0: Calendar, param_1: Calendar, param_2: JointCalendarRule = ...) -> None:
        ...
    @typing.overload
    def __init__(self, param_0: Calendar, param_1: Calendar, param_2: Calendar, param_3: JointCalendarRule = ...) -> None:
        ...
    @typing.overload
    def __init__(self, param_0: Calendar, param_1: Calendar, param_2: Calendar, param_3: Calendar, param_4: JointCalendarRule = ...) -> None:
        ...
    @typing.overload
    def __init__(self, calendars: list, rule: JointCalendarRule = ...) -> None:
        ...
class JointCalendarRule:
    """
    ! rules for joining calendars
    
    Members:
    
      JoinHolidays : !< A date is a holiday
                                                       for the joint calendar
                                                       if it is a holiday
                                                       for any of the given
                                                       calendars
    
      JoinBusinessDays : !< A date is a business day
                                                       for the joint calendar
                                                       if it is a business day
                                                       for any of the given
                                                       calendars
    """
    JoinBusinessDays: typing.ClassVar[JointCalendarRule]  # value = <JointCalendarRule.JoinBusinessDays: 1>
    JoinHolidays: typing.ClassVar[JointCalendarRule]  # value = <JointCalendarRule.JoinHolidays: 0>
    __members__: typing.ClassVar[dict[str, JointCalendarRule]]  # value = {'JoinHolidays': <JointCalendarRule.JoinHolidays: 0>, 'JoinBusinessDays': <JointCalendarRule.JoinBusinessDays: 1>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class JpyLiborSwapIsdaFixAm(SwapIndex):
    """
    JPY LIBOR swap rate (ISDA fix AM).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class JpyLiborSwapIsdaFixPm(SwapIndex):
    """
    JPY LIBOR swap rate (ISDA fix PM).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class KESCurrency(Currency):
    """
    ! Kenyan shilling
    /*! The ISO three-letter code is KES; the numeric code is 404.
         It is divided into 100 cents.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class KRWCurrency(Currency):
    """
    ! The ISO three-letter code is KRW; the numeric code is 410.
            It is divided in 100 chon.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class KWDCurrency(Currency):
    """
    ! The ISO three-letter code is KWD; the numeric code is 414.
            It is divided in 1000 fils.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class KZTCurrency(Currency):
    """
    """
    def __init__(self) -> None:
        ...
class KirkEngine(base.SpreadBlackScholesVanillaEngine):
    """
    Kirk engine for spread option pricing on two futures.
    """
    def __init__(self, process1: GeneralizedBlackScholesProcess, process2: GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with two Black-Scholes processes and correlation.
        """
class LKRCurrency(Currency):
    """
    ! Sri Lankan rupee
    /*! The ISO three-letter code is LKR; there numeric code is 144.
         It is divided into 100 cents.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class LTCCurrency(Currency):
    """
    ! https://litecoin.com/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class LTLCurrency(Currency):
    """
    ! The ISO three-letter code is LTL; the numeric code is 440.
            It is divided in 100 centu.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class LUFCurrency(Currency):
    """
    ! The ISO three-letter code was LUF; the numeric code was 442.
            It was divided in 100 centimes.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class LVLCurrency(Currency):
    """
    ! The ISO three-letter code is LVL; the numeric code is 428.
            It is divided in 100 santims.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class LevenbergMarquardt(base.OptimizationMethod):
    """
    Levenberg-Marquardt optimization method.
    """
    def __init__(self, epsfcn: typing.SupportsFloat = 1e-08, xtol: typing.SupportsFloat = 1e-08, gtol: typing.SupportsFloat = 1e-08) -> None:
        """
        Creates a Levenberg-Marquardt optimizer.
        """
class LinearInterpolation(base.Interpolation):
    """
    Linear interpolation between discrete points.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs interpolation from x and y arrays.
        """
class LinearTsrPricer(base.CmsCouponPricer, base.MeanRevertingPricer):
    """
    CMS coupon pricer using linear terminal swap rate model.
    """
    @typing.overload
    def __init__(self, swaptionVol: ..., meanReversion: QuoteHandle, couponDiscountCurve: typing.Any = None, settings: LinearTsrPricerSettings = ...) -> None:
        """
        Constructs with explicit handles.
        """
    @typing.overload
    def __init__(self, swaptionVol: ..., meanReversion: base.Quote, couponDiscountCurve: typing.Any = None, settings: LinearTsrPricerSettings = ...) -> None:
        """
        Constructs from shared pointers (handles created internally).
        """
    def capletPrice(self, effectiveCap: typing.SupportsFloat) -> float:
        """
        Returns the caplet price.
        """
    def capletRate(self, effectiveCap: typing.SupportsFloat) -> float:
        """
        Returns the caplet rate.
        """
    def floorletPrice(self, effectiveFloor: typing.SupportsFloat) -> float:
        """
        Returns the floorlet price.
        """
    def floorletRate(self, effectiveFloor: typing.SupportsFloat) -> float:
        """
        Returns the floorlet rate.
        """
    def meanReversion(self) -> float:
        """
        Returns the mean reversion value.
        """
    def setMeanReversion(self, meanReversion: QuoteHandle) -> None:
        """
        Sets the mean reversion handle.
        """
    def swapletPrice(self) -> float:
        """
        Returns the swaplet price.
        """
    def swapletRate(self) -> float:
        """
        Returns the swaplet rate.
        """
class LinearTsrPricerSettings:
    """
    Settings for LinearTsrPricer integration bounds.
    """
    def __init__(self) -> None:
        """
        Constructs default settings (RateBound strategy).
        """
    @typing.overload
    def withBSStdDevs(self, stdDevs: typing.SupportsFloat = 3.0) -> LinearTsrPricerSettings:
        """
        Sets Black-Scholes std devs strategy with default bounds.
        """
    @typing.overload
    def withBSStdDevs(self, stdDevs: typing.SupportsFloat, lowerRateBound: typing.SupportsFloat, upperRateBound: typing.SupportsFloat) -> LinearTsrPricerSettings:
        """
        Sets Black-Scholes std devs strategy with explicit bounds.
        """
    @typing.overload
    def withPriceThreshold(self, priceThreshold: typing.SupportsFloat = 1e-08) -> LinearTsrPricerSettings:
        """
        Sets price threshold strategy with default bounds.
        """
    @typing.overload
    def withPriceThreshold(self, priceThreshold: typing.SupportsFloat, lowerRateBound: typing.SupportsFloat, upperRateBound: typing.SupportsFloat) -> LinearTsrPricerSettings:
        """
        Sets price threshold strategy with explicit bounds.
        """
    def withRateBound(self, lowerRateBound: typing.SupportsFloat = 0.0, upperRateBound: typing.SupportsFloat = 2.0) -> LinearTsrPricerSettings:
        """
        Sets rate bound strategy with explicit bounds.
        """
    @typing.overload
    def withVegaRatio(self, vegaRatio: typing.SupportsFloat = 0.01) -> LinearTsrPricerSettings:
        """
        Sets vega ratio strategy with default bounds.
        """
    @typing.overload
    def withVegaRatio(self, vegaRatio: typing.SupportsFloat, lowerRateBound: typing.SupportsFloat, upperRateBound: typing.SupportsFloat) -> LinearTsrPricerSettings:
        """
        Sets vega ratio strategy with explicit bounds.
        """
class LinearTsrPricerStrategy:
    """
    Integration boundary determination strategy.
    
    Members:
    
      RateBound
    
      VegaRatio
    
      PriceThreshold
    
      BSStdDevs
    """
    BSStdDevs: typing.ClassVar[LinearTsrPricerStrategy]  # value = <LinearTsrPricerStrategy.BSStdDevs: 3>
    PriceThreshold: typing.ClassVar[LinearTsrPricerStrategy]  # value = <LinearTsrPricerStrategy.PriceThreshold: 2>
    RateBound: typing.ClassVar[LinearTsrPricerStrategy]  # value = <LinearTsrPricerStrategy.RateBound: 0>
    VegaRatio: typing.ClassVar[LinearTsrPricerStrategy]  # value = <LinearTsrPricerStrategy.VegaRatio: 1>
    __members__: typing.ClassVar[dict[str, LinearTsrPricerStrategy]]  # value = {'RateBound': <LinearTsrPricerStrategy.RateBound: 0>, 'VegaRatio': <LinearTsrPricerStrategy.VegaRatio: 1>, 'PriceThreshold': <LinearTsrPricerStrategy.PriceThreshold: 2>, 'BSStdDevs': <LinearTsrPricerStrategy.BSStdDevs: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LocalConstantVol(base.LocalVolTermStructure):
    """
    Constant local volatility term structure.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, volatility: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and constant volatility.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, volatility: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and quote handle.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, volatility: base.Quote, dayCounter: DayCounter) -> None:
        """
        Constructs from reference date and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: typing.SupportsFloat, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and constant volatility.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: QuoteHandle, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, volatility: base.Quote, dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days and quote (handle created internally).
        """
class LocalVolSurface(base.LocalVolTermStructure):
    """
    Local volatility surface derived from a Black volatility surface.
    """
    @typing.overload
    def __init__(self, blackVolTS: BlackVolTermStructureHandle, riskFreeTS: YieldTermStructureHandle, dividendTS: YieldTermStructureHandle, underlying: QuoteHandle) -> None:
        """
        Constructs from Black vol surface and quote handle for underlying.
        """
    @typing.overload
    def __init__(self, blackVolTS: BlackVolTermStructureHandle, riskFreeTS: YieldTermStructureHandle, dividendTS: YieldTermStructureHandle, underlying: typing.SupportsFloat) -> None:
        """
        Constructs from Black vol surface and fixed underlying value.
        """
    @typing.overload
    def __init__(self, blackVolTS: base.BlackVolTermStructure, riskFreeTS: base.YieldTermStructure, dividendTS: base.YieldTermStructure, underlying: base.Quote) -> None:
        """
        Constructs from term structures and quote (handles created internally).
        """
    @typing.overload
    def __init__(self, blackVolTS: base.BlackVolTermStructure, riskFreeTS: base.YieldTermStructure, dividendTS: base.YieldTermStructure, underlying: typing.SupportsFloat) -> None:
        """
        Constructs from term structures and fixed value (handles created internally).
        """
class LocalVolTermStructureHandle:
    """
    Handle to LocalVolTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: LocalVolTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: LocalVolTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: LocalVolTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.LocalVolTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.LocalVolTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class LogLinearInterpolation(base.Interpolation):
    """
    Log-linear interpolation between discrete points.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs interpolation from x and y arrays.
        """
class MADCurrency(Currency):
    """
    ! Moroccan dirham
    /*! The ISO three-letter code is MAD; the numeric code is 504.
         It is divided into 100 santim.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class MCEuropeanBasketEngine(base.PricingEngine):
    """
    Monte Carlo pricing engine for European basket options (pseudo-random).
    """
    def __init__(self, process: StochasticProcessArray, timeSteps: typing.SupportsInt = ..., timeStepsPerYear: typing.SupportsInt = ..., brownianBridge: bool = False, antitheticVariate: bool = False, requiredSamples: typing.SupportsInt = ..., requiredTolerance: typing.SupportsFloat = ..., maxSamples: typing.SupportsInt = ..., seed: typing.SupportsInt = 0) -> None:
        """
        Constructs MC European basket engine with pseudo-random numbers.
        """
class MCLDEuropeanBasketEngine(base.PricingEngine):
    """
    Monte Carlo pricing engine for European basket options (low-discrepancy/Sobol).
    """
    def __init__(self, process: StochasticProcessArray, timeSteps: typing.SupportsInt = ..., timeStepsPerYear: typing.SupportsInt = ..., brownianBridge: bool = False, antitheticVariate: bool = False, requiredSamples: typing.SupportsInt = ..., requiredTolerance: typing.SupportsFloat = ..., maxSamples: typing.SupportsInt = ..., seed: typing.SupportsInt = 0) -> None:
        """
        Constructs MC European basket engine with low-discrepancy sequences.
        """
class MTLCurrency(Currency):
    """
    ! The ISO three-letter code is MTL; the numeric code is 470.
            It was divided in 100 cents.
    
            Obsoleted by the Euro since 2008.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class MURCurrency(Currency):
    """
    ! Mauritian rupee
    /*! The ISO three-letter code is MUR; the numeric code is 480.
         It is divided into 100 cents.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class MXNCurrency(Currency):
    """
    ! The ISO three-letter code is MXN; the numeric code is 484.
            It is divided in 100 centavos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class MXVCurrency(Currency):
    """
    ! Mexican Unidad de Inversion
    /*! The ISO three-letter code is MXV; the numeric code is 979.
         A unit of account used in Mexico.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class MYRCurrency(Currency):
    """
    ! The ISO three-letter code is MYR; the numeric code is 458.
            It is divided in 100 sen.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class MakeCapFloor:
    """
    Helper class for constructing standard market caps and floors.
    """
    def __init__(self, type: CapFloorType, tenor: Period, index: IborIndex, strike: typing.Any = None, forwardStart: Period = ...) -> None:
        """
        Constructs a cap/floor builder.
        """
    def asOptionlet(self, flag: bool = True) -> MakeCapFloor:
        """
        Gets only the last coupon.
        """
    def capFloor(self) -> CapFloor:
        """
        Builds and returns the CapFloor.
        """
    def withCalendar(self, calendar: Calendar) -> MakeCapFloor:
        """
        Sets the calendar.
        """
    def withConvention(self, convention: BusinessDayConvention) -> MakeCapFloor:
        """
        Sets the business day convention.
        """
    def withDayCount(self, dayCount: DayCounter) -> MakeCapFloor:
        """
        Sets the day count convention.
        """
    def withEffectiveDate(self, effectiveDate: Date, firstCapletExcluded: bool) -> MakeCapFloor:
        """
        Sets the effective date.
        """
    def withEndOfMonth(self, flag: bool = True) -> MakeCapFloor:
        """
        Sets the end-of-month flag.
        """
    def withFirstDate(self, date: Date) -> MakeCapFloor:
        """
        Sets the first date.
        """
    def withNextToLastDate(self, date: Date) -> MakeCapFloor:
        """
        Sets the next-to-last date.
        """
    def withNominal(self, nominal: typing.SupportsFloat) -> MakeCapFloor:
        """
        Sets the nominal amount.
        """
    def withPricingEngine(self, engine: base.PricingEngine) -> MakeCapFloor:
        """
        Sets the pricing engine.
        """
    def withRule(self, rule: DateGeneration.Rule) -> MakeCapFloor:
        """
        Sets the date generation rule.
        """
    def withTenor(self, tenor: Period) -> MakeCapFloor:
        """
        Sets the coupon tenor.
        """
    def withTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeCapFloor:
        """
        Sets the termination date convention.
        """
class MakeOIS:
    """
    Helper class for constructing overnight indexed swaps.
    """
    def __init__(self, swapTenor: Period, overnightIndex: OvernightIndex, fixedRate: typing.Any = None, fwdStart: Period = ...) -> None:
        """
        Constructs an OIS builder.
        """
    def ois(self) -> OvernightIndexedSwap:
        """
        Builds and returns the OvernightIndexedSwap.
        """
    def receiveFixed(self, flag: bool = True) -> MakeOIS:
        """
        Sets whether to receive fixed.
        """
    def withAveragingMethod(self, averagingMethod: RateAveraging.Type) -> MakeOIS:
        """
        Sets the rate averaging method.
        """
    def withCalendar(self, calendar: Calendar) -> MakeOIS:
        """
        Sets the calendar for both legs.
        """
    def withConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the business day convention for both legs.
        """
    @typing.overload
    def withDiscountingTermStructure(self, discountCurve: base.YieldTermStructure) -> MakeOIS:
        """
        Sets the discounting term structure.
        """
    @typing.overload
    def withDiscountingTermStructure(self, discountCurve: YieldTermStructureHandle) -> MakeOIS:
        """
        Sets the discounting term structure (handle).
        """
    def withEffectiveDate(self, date: Date) -> MakeOIS:
        """
        Sets the effective date.
        """
    def withEndOfMonth(self, flag: bool = True) -> MakeOIS:
        """
        Sets the end-of-month flag for both legs.
        """
    def withFixedLegCalendar(self, calendar: Calendar) -> MakeOIS:
        """
        Sets the calendar for the fixed leg.
        """
    def withFixedLegConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the business day convention for the fixed leg.
        """
    def withFixedLegDayCount(self, dayCount: DayCounter) -> MakeOIS:
        """
        Sets the day count convention for the fixed leg.
        """
    def withFixedLegEndOfMonth(self, flag: bool = True) -> MakeOIS:
        """
        Sets the end-of-month flag for the fixed leg.
        """
    def withFixedLegPaymentFrequency(self, frequency: Frequency) -> MakeOIS:
        """
        Sets the payment frequency for the fixed leg.
        """
    def withFixedLegRule(self, rule: DateGeneration.Rule) -> MakeOIS:
        """
        Sets the date generation rule for the fixed leg.
        """
    def withFixedLegTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the termination date convention for the fixed leg.
        """
    def withLockoutDays(self, lockoutDays: typing.SupportsInt) -> MakeOIS:
        """
        Sets the lockout days.
        """
    def withLookbackDays(self, lookbackDays: typing.SupportsInt) -> MakeOIS:
        """
        Sets the lookback days.
        """
    def withNominal(self, nominal: typing.SupportsFloat) -> MakeOIS:
        """
        Sets the nominal amount.
        """
    def withObservationShift(self, flag: bool = True) -> MakeOIS:
        """
        Enables observation shift.
        """
    def withOvernightLegCalendar(self, calendar: Calendar) -> MakeOIS:
        """
        Sets the calendar for the overnight leg.
        """
    def withOvernightLegConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the business day convention for the overnight leg.
        """
    def withOvernightLegEndOfMonth(self, flag: bool = True) -> MakeOIS:
        """
        Sets the end-of-month flag for the overnight leg.
        """
    def withOvernightLegPaymentFrequency(self, frequency: Frequency) -> MakeOIS:
        """
        Sets the payment frequency for the overnight leg.
        """
    def withOvernightLegRule(self, rule: DateGeneration.Rule) -> MakeOIS:
        """
        Sets the date generation rule for the overnight leg.
        """
    def withOvernightLegSpread(self, spread: typing.SupportsFloat) -> MakeOIS:
        """
        Sets the spread on the overnight leg.
        """
    def withOvernightLegTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the termination date convention for the overnight leg.
        """
    def withPaymentAdjustment(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the payment adjustment convention.
        """
    def withPaymentCalendar(self, calendar: Calendar) -> MakeOIS:
        """
        Sets the payment calendar.
        """
    def withPaymentFrequency(self, frequency: Frequency) -> MakeOIS:
        """
        Sets the payment frequency for both legs.
        """
    def withPaymentLag(self, lag: typing.SupportsInt) -> MakeOIS:
        """
        Sets the payment lag in days.
        """
    def withPricingEngine(self, engine: base.PricingEngine) -> MakeOIS:
        """
        Sets the pricing engine.
        """
    def withRule(self, rule: DateGeneration.Rule) -> MakeOIS:
        """
        Sets the date generation rule for both legs.
        """
    def withSettlementDays(self, settlementDays: typing.SupportsInt) -> MakeOIS:
        """
        Sets the settlement days.
        """
    def withTelescopicValueDates(self, flag: bool) -> MakeOIS:
        """
        Enables telescopic value dates.
        """
    def withTerminationDate(self, date: Date) -> MakeOIS:
        """
        Sets the termination date.
        """
    def withTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeOIS:
        """
        Sets the termination date convention for both legs.
        """
    def withType(self, type: SwapType) -> MakeOIS:
        """
        Sets the swap type.
        """
class MakeSchedule:
    """
    Helper class providing a fluent interface for Schedule construction.
    """
    def __init__(self) -> None:
        ...
    def backwards(self) -> MakeSchedule:
        ...
    def endOfMonth(self, flag: bool = True) -> MakeSchedule:
        ...
    def forwards(self) -> MakeSchedule:
        ...
    def from_(self, effectiveDate: Date) -> MakeSchedule:
        ...
    def schedule(self) -> Schedule:
        ...
    def to(self, terminationDate: Date) -> MakeSchedule:
        ...
    def withCalendar(self, calendar: Calendar) -> MakeSchedule:
        ...
    def withConvention(self, convention: BusinessDayConvention) -> MakeSchedule:
        ...
    def withFirstDate(self, d: Date) -> MakeSchedule:
        ...
    def withFrequency(self, frequency: Frequency) -> MakeSchedule:
        ...
    def withNextToLastDate(self, d: Date) -> MakeSchedule:
        ...
    def withRule(self, rule: DateGeneration.Rule) -> MakeSchedule:
        ...
    def withTenor(self, tenor: Period) -> MakeSchedule:
        ...
    def withTerminationDateConvention(self, terminationDateConvention: BusinessDayConvention) -> MakeSchedule:
        ...
class MakeSwaption:
    """
    Helper class for constructing standard market swaptions.
    """
    @typing.overload
    def __init__(self, swapIndex: SwapIndex, optionTenor: Period, strike: typing.Any = None) -> None:
        """
        Constructs a swaption builder from option tenor.
        """
    @typing.overload
    def __init__(self, swapIndex: SwapIndex, fixingDate: Date, strike: typing.Any = None) -> None:
        """
        Constructs a swaption builder from fixing date.
        """
    def swaption(self) -> Swaption:
        """
        Builds and returns the Swaption.
        """
    def withAtParCoupons(self, flag: bool = True) -> MakeSwaption:
        """
        Uses at-par coupons for the underlying swap.
        """
    def withExerciseDate(self, date: Date) -> MakeSwaption:
        """
        Sets the exercise date.
        """
    def withIndexedCoupons(self, flag: ... = True) -> MakeSwaption:
        """
        Uses indexed coupons for the underlying swap.
        """
    def withNominal(self, nominal: typing.SupportsFloat) -> MakeSwaption:
        """
        Sets the nominal amount.
        """
    def withOptionConvention(self, convention: BusinessDayConvention) -> MakeSwaption:
        """
        Sets the option convention.
        """
    def withPricingEngine(self, engine: base.PricingEngine) -> MakeSwaption:
        """
        Sets the pricing engine.
        """
    def withSettlementMethod(self, method: SettlementMethod) -> MakeSwaption:
        """
        Sets the settlement method.
        """
    def withSettlementType(self, type: SettlementType) -> MakeSwaption:
        """
        Sets the settlement type.
        """
    def withUnderlyingType(self, type: SwapType) -> MakeSwaption:
        """
        Sets the underlying swap type.
        """
class MakeVanillaSwap:
    """
    Helper class for constructing standard market swaps.
    """
    def __init__(self, swapTenor: Period, iborIndex: IborIndex, fixedRate: typing.Any = None, forwardStart: Period = ...) -> None:
        """
        Constructs a vanilla swap builder.
        """
    def receiveFixed(self, flag: bool = True) -> MakeVanillaSwap:
        """
        Sets whether to receive fixed.
        """
    def swap(self) -> VanillaSwap:
        """
        Builds and returns the VanillaSwap.
        """
    def withAtParCoupons(self, flag: bool = True) -> MakeVanillaSwap:
        """
        Uses at-par coupons for the floating leg.
        """
    @typing.overload
    def withDiscountingTermStructure(self, discountCurve: base.YieldTermStructure) -> MakeVanillaSwap:
        """
        Sets the discounting term structure.
        """
    @typing.overload
    def withDiscountingTermStructure(self, discountCurve: YieldTermStructureHandle) -> MakeVanillaSwap:
        """
        Sets the discounting term structure (handle).
        """
    def withEffectiveDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the effective date.
        """
    def withFixedLegCalendar(self, calendar: Calendar) -> MakeVanillaSwap:
        """
        Sets the fixed leg calendar.
        """
    def withFixedLegConvention(self, convention: BusinessDayConvention) -> MakeVanillaSwap:
        """
        Sets the fixed leg business day convention.
        """
    def withFixedLegDayCount(self, dayCount: DayCounter) -> MakeVanillaSwap:
        """
        Sets the fixed leg day count convention.
        """
    def withFixedLegEndOfMonth(self, flag: bool = True) -> MakeVanillaSwap:
        """
        Sets the fixed leg end-of-month flag.
        """
    def withFixedLegFirstDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the fixed leg first date.
        """
    def withFixedLegNextToLastDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the fixed leg next-to-last date.
        """
    def withFixedLegRule(self, rule: DateGeneration.Rule) -> MakeVanillaSwap:
        """
        Sets the fixed leg date generation rule.
        """
    def withFixedLegTenor(self, tenor: Period) -> MakeVanillaSwap:
        """
        Sets the fixed leg tenor.
        """
    def withFixedLegTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeVanillaSwap:
        """
        Sets the fixed leg termination date convention.
        """
    def withFloatingLegCalendar(self, calendar: Calendar) -> MakeVanillaSwap:
        """
        Sets the floating leg calendar.
        """
    def withFloatingLegConvention(self, convention: BusinessDayConvention) -> MakeVanillaSwap:
        """
        Sets the floating leg business day convention.
        """
    def withFloatingLegDayCount(self, dayCount: DayCounter) -> MakeVanillaSwap:
        """
        Sets the floating leg day count convention.
        """
    def withFloatingLegEndOfMonth(self, flag: bool = True) -> MakeVanillaSwap:
        """
        Sets the floating leg end-of-month flag.
        """
    def withFloatingLegFirstDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the floating leg first date.
        """
    def withFloatingLegNextToLastDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the floating leg next-to-last date.
        """
    def withFloatingLegRule(self, rule: DateGeneration.Rule) -> MakeVanillaSwap:
        """
        Sets the floating leg date generation rule.
        """
    def withFloatingLegSpread(self, spread: typing.SupportsFloat) -> MakeVanillaSwap:
        """
        Sets the floating leg spread.
        """
    def withFloatingLegTenor(self, tenor: Period) -> MakeVanillaSwap:
        """
        Sets the floating leg tenor.
        """
    def withFloatingLegTerminationDateConvention(self, convention: BusinessDayConvention) -> MakeVanillaSwap:
        """
        Sets the floating leg termination date convention.
        """
    def withIndexedCoupons(self, flag: ... = True) -> MakeVanillaSwap:
        """
        Uses indexed coupons for the floating leg.
        """
    def withNominal(self, nominal: typing.SupportsFloat) -> MakeVanillaSwap:
        """
        Sets the nominal amount.
        """
    def withPaymentConvention(self, convention: BusinessDayConvention) -> MakeVanillaSwap:
        """
        Sets the payment convention.
        """
    def withPricingEngine(self, engine: base.PricingEngine) -> MakeVanillaSwap:
        """
        Sets the pricing engine.
        """
    def withRule(self, rule: DateGeneration.Rule) -> MakeVanillaSwap:
        """
        Sets the date generation rule.
        """
    def withSettlementDays(self, settlementDays: typing.SupportsInt) -> MakeVanillaSwap:
        """
        Sets the settlement days.
        """
    def withTerminationDate(self, date: Date) -> MakeVanillaSwap:
        """
        Sets the termination date.
        """
    def withType(self, type: SwapType) -> MakeVanillaSwap:
        """
        Sets the swap type.
        """
class Matrix:
    """
    2-dimensional matrix of Real values.
    """
    def __add__(self, arg0: Matrix) -> Matrix:
        ...
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> numpy.typing.NDArray[numpy.float64]:
        """
        Gets a row as a NumPy array view.
        """
    @typing.overload
    def __getitem__(self, arg0: tuple[typing.SupportsInt, typing.SupportsInt]) -> float:
        """
        Gets element at (row, column).
        """
    def __iadd__(self, arg0: Matrix) -> Matrix:
        ...
    def __imul__(self, arg0: typing.SupportsFloat) -> Matrix:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor (empty matrix).
        """
    @typing.overload
    def __init__(self, rows: typing.SupportsInt, columns: typing.SupportsInt) -> None:
        """
        Creates a zero-filled matrix.
        """
    @typing.overload
    def __init__(self, rows: typing.SupportsInt, columns: typing.SupportsInt, value: typing.SupportsFloat) -> None:
        """
        Creates a matrix filled with value.
        """
    @typing.overload
    def __init__(self, numpy_array: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        """
        Creates a matrix from a 2D NumPy array.
        """
    @typing.overload
    def __init__(self, list_of_lists: list) -> None:
        """
        Creates a matrix from a list of lists.
        """
    def __isub__(self, arg0: Matrix) -> Matrix:
        ...
    def __iter__(self) -> collections.abc.Iterator[float]:
        """
        Iterates over elements in row-major order.
        """
    def __itruediv__(self, arg0: typing.SupportsFloat) -> Matrix:
        ...
    @typing.overload
    def __mul__(self, arg0: Matrix) -> Matrix:
        ...
    @typing.overload
    def __mul__(self, arg0: typing.SupportsFloat) -> Matrix:
        ...
    def __repr__(self) -> str:
        ...
    def __rmul__(self, arg0: typing.SupportsFloat) -> Matrix:
        ...
    def __setitem__(self, arg0: tuple[typing.SupportsInt, typing.SupportsInt], arg1: typing.SupportsFloat) -> None:
        """
        Sets element at (row, column).
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: Matrix) -> Matrix:
        ...
    def __truediv__(self, arg0: typing.SupportsFloat) -> Matrix:
        ...
    def column(self, index: typing.SupportsInt) -> Array:
        """
        Returns a column as an Array.
        """
    def columns(self) -> int:
        """
        Returns the number of columns.
        """
    def diagonal(self) -> Array:
        """
        Returns the diagonal as an Array.
        """
    def empty(self) -> bool:
        """
        Returns true if the matrix is empty.
        """
    def rows(self) -> int:
        """
        Returns the number of rows.
        """
    def swap(self, other: Matrix) -> None:
        """
        Swaps contents with another matrix.
        """
    @property
    def shape(self) -> tuple:
        """
        Returns (rows, columns) tuple.
        """
class MaxBasketPayoff(base.BasketPayoff):
    """
    Payoff based on maximum of basket prices.
    """
    def __init__(self, basePayoff: base.Payoff) -> None:
        """
        Constructs with base payoff.
        """
class Mexico(Calendar):
    """
    ! Holidays for the Mexican stock exchange
            (data from <http://www.bmv.com.mx/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Constitution Day, first Monday in February
                (February 5th before 2006)</li>
            <li>Birthday of Benito Juarez, third Monday in February
                (March 21st before 2006)</li>
            <li>Holy Thursday</li>
            <li>Good Friday</li>
            <li>Labour Day, May 1st</li>
            <li>National Day, September 16th</li>
            <li>Inauguration Day, October 1st, every sixth year starting 2024</li>
            <li>All Souls Day, November 2nd (bank holiday, not a public one)</li>
            <li>Revolution Day, third Monday in November
                (November 20th before 2006)</li>
            <li>Our Lady of Guadalupe, December 12th</li>
            <li>Christmas, December 25th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          BMV : !< Mexican stock exchange
        """
        BMV: typing.ClassVar[Mexico.Market]  # value = <Market.BMV: 0>
        __members__: typing.ClassVar[dict[str, Mexico.Market]]  # value = {'BMV': <Market.BMV: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BMV: typing.ClassVar[Mexico.Market]  # value = <Market.BMV: 0>
    def __init__(self, m: Mexico.Market = ...) -> None:
        ...
class MidPointCdsEngine(base.PricingEngine):
    """
    Mid-point engine for credit default swaps.
    """
    @typing.overload
    def __init__(self, probability: DefaultProbabilityTermStructureHandle, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, includeSettlementDateFlows: bool | None = None) -> None:
        """
        Constructs from handles.
        """
    @typing.overload
    def __init__(self, probability: base.DefaultProbabilityTermStructure, recoveryRate: typing.SupportsFloat, discountCurve: base.YieldTermStructure, includeSettlementDateFlows: bool | None = None) -> None:
        """
        Constructs from term structures (handles created internally).
        """
class MinBasketPayoff(base.BasketPayoff):
    """
    Payoff based on minimum of basket prices.
    """
    def __init__(self, basePayoff: base.Payoff) -> None:
        """
        Constructs with base payoff.
        """
class Money:
    """
    Amount of cash in a specific currency.
    """
    class ConversionType:
        """
        Conversion type for money arithmetic.
        
        Members:
        
          NoConversion : Do not perform conversions.
        
          BaseCurrencyConversion : Convert both operands to base currency.
        
          AutomatedConversion : Return result in the currency of the first operand.
        """
        AutomatedConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.AutomatedConversion: 2>
        BaseCurrencyConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.BaseCurrencyConversion: 1>
        NoConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.NoConversion: 0>
        __members__: typing.ClassVar[dict[str, Money.ConversionType]]  # value = {'NoConversion': <ConversionType.NoConversion: 0>, 'BaseCurrencyConversion': <ConversionType.BaseCurrencyConversion: 1>, 'AutomatedConversion': <ConversionType.AutomatedConversion: 2>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class Settings:
        """
        Per-session settings for Money arithmetic.
        """
        @staticmethod
        def instance() -> Money.Settings:
            """
            Returns the singleton instance.
            """
        @property
        def baseCurrency(self) -> Currency:
            """
            The base currency used for conversions.
            """
        @baseCurrency.setter
        def baseCurrency(self, arg1: Currency) -> None:
            ...
        @property
        def conversionType(self) -> Money.ConversionType:
            """
            The conversion type used for money arithmetic.
            """
        @conversionType.setter
        def conversionType(self, arg1: Money.ConversionType) -> None:
            ...
    AutomatedConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.AutomatedConversion: 2>
    BaseCurrencyConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.BaseCurrencyConversion: 1>
    NoConversion: typing.ClassVar[Money.ConversionType]  # value = <ConversionType.NoConversion: 0>
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Money) -> bool:
        ...
    def __ge__(self, arg0: Money) -> bool:
        ...
    def __gt__(self, arg0: Money) -> bool:
        ...
    def __iadd__(self, other: Money) -> Money:
        ...
    def __imul__(self, factor: typing.SupportsFloat) -> Money:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor.
        """
    @typing.overload
    def __init__(self, currency: Currency, value: typing.SupportsFloat) -> None:
        """
        Constructs from currency and value.
        """
    @typing.overload
    def __init__(self, value: typing.SupportsFloat, currency: Currency) -> None:
        """
        Constructs from value and currency.
        """
    def __isub__(self, other: Money) -> Money:
        ...
    def __itruediv__(self, divisor: typing.SupportsFloat) -> Money:
        ...
    def __le__(self, arg0: Money) -> bool:
        ...
    def __lt__(self, arg0: Money) -> bool:
        ...
    def __ne__(self, arg0: Money) -> bool:
        ...
    def __neg__(self) -> Money:
        ...
    def __pos__(self) -> Money:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def currency(self) -> Currency:
        """
        Returns the currency.
        """
    def rounded(self) -> Money:
        """
        Returns the amount rounded according to the currency.
        """
    def value(self) -> float:
        """
        Returns the amount.
        """
class MonotonicCubicNaturalSpline(base.Interpolation):
    """
    Monotonic natural cubic spline interpolation.
    """
    def __init__(self, x: collections.abc.Sequence[typing.SupportsFloat], y: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs interpolation from x and y arrays.
        """
class Month:
    """
    Month names enumeration.
    
    Members:
    
      January
    
      February
    
      March
    
      April
    
      May
    
      June
    
      July
    
      August
    
      September
    
      October
    
      November
    
      December
    
      Jan
    
      Feb
    
      Mar
    
      Apr
    
      Jun
    
      Jul
    
      Aug
    
      Sep
    
      Oct
    
      Nov
    
      Dec
    """
    Apr: typing.ClassVar[Month]  # value = <Month.April: 4>
    April: typing.ClassVar[Month]  # value = <Month.April: 4>
    Aug: typing.ClassVar[Month]  # value = <Month.August: 8>
    August: typing.ClassVar[Month]  # value = <Month.August: 8>
    Dec: typing.ClassVar[Month]  # value = <Month.December: 12>
    December: typing.ClassVar[Month]  # value = <Month.December: 12>
    Feb: typing.ClassVar[Month]  # value = <Month.February: 2>
    February: typing.ClassVar[Month]  # value = <Month.February: 2>
    Jan: typing.ClassVar[Month]  # value = <Month.January: 1>
    January: typing.ClassVar[Month]  # value = <Month.January: 1>
    Jul: typing.ClassVar[Month]  # value = <Month.July: 7>
    July: typing.ClassVar[Month]  # value = <Month.July: 7>
    Jun: typing.ClassVar[Month]  # value = <Month.June: 6>
    June: typing.ClassVar[Month]  # value = <Month.June: 6>
    Mar: typing.ClassVar[Month]  # value = <Month.March: 3>
    March: typing.ClassVar[Month]  # value = <Month.March: 3>
    May: typing.ClassVar[Month]  # value = <Month.May: 5>
    Nov: typing.ClassVar[Month]  # value = <Month.November: 11>
    November: typing.ClassVar[Month]  # value = <Month.November: 11>
    Oct: typing.ClassVar[Month]  # value = <Month.October: 10>
    October: typing.ClassVar[Month]  # value = <Month.October: 10>
    Sep: typing.ClassVar[Month]  # value = <Month.September: 9>
    September: typing.ClassVar[Month]  # value = <Month.September: 9>
    __members__: typing.ClassVar[dict[str, Month]]  # value = {'January': <Month.January: 1>, 'February': <Month.February: 2>, 'March': <Month.March: 3>, 'April': <Month.April: 4>, 'May': <Month.May: 5>, 'June': <Month.June: 6>, 'July': <Month.July: 7>, 'August': <Month.August: 8>, 'September': <Month.September: 9>, 'October': <Month.October: 10>, 'November': <Month.November: 11>, 'December': <Month.December: 12>, 'Jan': <Month.January: 1>, 'Feb': <Month.February: 2>, 'Mar': <Month.March: 3>, 'Apr': <Month.April: 4>, 'Jun': <Month.June: 6>, 'Jul': <Month.July: 7>, 'Aug': <Month.August: 8>, 'Sep': <Month.September: 9>, 'Oct': <Month.October: 10>, 'Nov': <Month.November: 11>, 'Dec': <Month.December: 12>}
    def __add__(self, arg0: typing.SupportsInt) -> Month:
        ...
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __radd__(self: typing.SupportsInt, arg0: Month) -> Month:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rsub__(self: typing.SupportsInt, arg0: Month) -> Month:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: typing.SupportsInt) -> Month:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MoreGreeks:
    """
    Container for additional Greeks.
    """
    def __init__(self) -> None:
        ...
    @property
    def itmCashProbability(self) -> float:
        """
        ITM cash probability.
        """
    @itmCashProbability.setter
    def itmCashProbability(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def strikeSensitivity(self) -> float:
        """
        Strike sensitivity.
        """
    @strikeSensitivity.setter
    def strikeSensitivity(self, arg0: typing.SupportsFloat) -> None:
        ...
class NGNCurrency(Currency):
    """
    ! Nigerian Naira
    /*! The ISO three-letter code is NGN; the numeric code is 566.
         It is divided into 100 kobo.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class NLGCurrency(Currency):
    """
    ! The ISO three-letter code was NLG; the numeric code was 528.
            It was divided in 100 cents.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class NOKCurrency(Currency):
    """
    ! The ISO three-letter code is NOK; the numeric code is 578.
            It is divided in 100 �re.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class NPRCurrency(Currency):
    """
    ! The ISO three-letter code is NPR; the numeric code is 524.
            It is divided in 100 paise.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class NZDCurrency(Currency):
    """
    ! The ISO three-letter code is NZD; the numeric code is 554.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class NelsonSiegelFitting(base.FittingMethod):
    """
    Nelson-Siegel fitting method.
    """
    def __init__(self, weights: Array = ..., optimizationMethod: base.OptimizationMethod = None, l2: Array = ..., minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308, constraint: base.Constraint = ...) -> None:
        """
        Constructs a Nelson-Siegel fitting method.
        """
class NewZealand(Calendar):
    """
    ! Common holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday or Tuesday)</li>
            <li>Day after New Year's Day, January 2st (possibly moved to Monday or Tuesday)</li>
            <li>Waitangi Day. February 6th (possibly moved to Monday since 2013)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>ANZAC Day. April 25th (possibly moved to Monday since 2013)</li>
            <li>Queen's Birthday, first Monday in June</li>
            <li>Labour Day, fourth Monday in October</li>
            <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or Tuesday)</li>
            <li>Matariki, in June or July, official calendar released for years 2022-2052</li>
            </ul>
    
            Additional holidays for Wellington:
            <ul>
            <li>Anniversary Day, Monday nearest January 22nd</li>
            </ul>
    
            Additional holidays for Auckland:
            <ul>
            <li>Anniversary Day, Monday nearest January 29nd</li>
            </ul>
    
            
    ote The holiday rules for New Zealand were documented by
                  David Gilbert for IDB (http://www.jrefinery.com/ibd/)
                  The Matariki holiday calendar has been released by the NZ Government
                  (https://www.legislation.govt.nz/act/public/2022/0014/latest/LMS557893.html)
    
            \\ingroup calendars
    """
    class Market:
        """
        ! NZ calendars
        
        Members:
        
          Wellington : 
        
          Auckland : 
        """
        Auckland: typing.ClassVar[NewZealand.Market]  # value = <Market.Auckland: 1>
        Wellington: typing.ClassVar[NewZealand.Market]  # value = <Market.Wellington: 0>
        __members__: typing.ClassVar[dict[str, NewZealand.Market]]  # value = {'Wellington': <Market.Wellington: 0>, 'Auckland': <Market.Auckland: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Auckland: typing.ClassVar[NewZealand.Market]  # value = <Market.Auckland: 1>
    Wellington: typing.ClassVar[NewZealand.Market]  # value = <Market.Wellington: 0>
    def __init__(self) -> None:
        ...
class Newton:
    """
    Newton 1-D solver (requires derivative function).
    """
    def __init__(self) -> None:
        ...
    def setLowerBound(self, lowerBound: typing.SupportsFloat) -> None:
        """
        Sets lower bound for the function domain.
        """
    def setMaxEvaluations(self, evaluations: typing.SupportsInt) -> None:
        """
        Sets maximum number of function evaluations.
        """
    def setUpperBound(self, upperBound: typing.SupportsFloat) -> None:
        """
        Sets upper bound for the function domain.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, derivative: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, step: typing.SupportsFloat) -> float:
        """
        Finds root with automatic bracketing.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, derivative: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, xMin: typing.SupportsFloat, xMax: typing.SupportsFloat) -> float:
        """
        Finds root within explicit bracket.
        """
class NoConstraint(base.Constraint):
    """
    No constraint (always satisfied).
    """
    def __init__(self) -> None:
        ...
class NoExceptLocalVolSurface(LocalVolSurface):
    """
    Local volatility surface that returns a fallback value instead of throwing.
    """
    @typing.overload
    def __init__(self, blackTS: BlackVolTermStructureHandle, riskFreeTS: YieldTermStructureHandle, dividendTS: YieldTermStructureHandle, underlying: QuoteHandle, illegalLocalVolOverwrite: typing.SupportsFloat) -> None:
        """
        Constructs with quote handle for underlying.
        """
    @typing.overload
    def __init__(self, blackTS: BlackVolTermStructureHandle, riskFreeTS: YieldTermStructureHandle, dividendTS: YieldTermStructureHandle, underlying: typing.SupportsFloat, illegalLocalVolOverwrite: typing.SupportsFloat) -> None:
        """
        Constructs with fixed underlying value.
        """
    @typing.overload
    def __init__(self, blackTS: base.BlackVolTermStructure, riskFreeTS: base.YieldTermStructure, dividendTS: base.YieldTermStructure, underlying: base.Quote, illegalLocalVolOverwrite: typing.SupportsFloat) -> None:
        """
        Constructs from term structures and quote (handles created internally).
        """
    @typing.overload
    def __init__(self, blackTS: base.BlackVolTermStructure, riskFreeTS: base.YieldTermStructure, dividendTS: base.YieldTermStructure, underlying: typing.SupportsFloat, illegalLocalVolOverwrite: typing.SupportsFloat) -> None:
        """
        Constructs from term structures and fixed value (handles created internally).
        """
class NormalDistribution:
    """
    Normal (Gaussian) distribution function.
    """
    def __call__(self, x: typing.SupportsFloat) -> float:
        """
        Returns the probability density at x.
        """
    def __init__(self, average: typing.SupportsFloat = 0.0, sigma: typing.SupportsFloat = 1.0) -> None:
        """
        Constructs NormalDistribution.
        """
    def derivative(self, x: typing.SupportsFloat) -> float:
        """
        Returns the derivative of the density at x.
        """
class Norway(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Holy Thursday</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Ascension</li>
            <li>Whit(Pentecost) Monday </li>
            <li>New Year's Day, January 1st</li>
            <li>May Day, May 1st</li>
            <li>National Independence Day, May 17th</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>Boxing Day, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class NullCalendar(Calendar):
    """
    ! This calendar has no holidays. It ensures that dates at
            whole-month distances have the same day of month.
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class NullReal:
    def __float__(self) -> float:
        ...
    def __init__(self) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
class NullSize:
    def __float__(self) -> float:
        ...
    def __init__(self) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __repr__(self) -> str:
        ...
class OISRateHelper(base.RelativeDateRateHelper):
    """
    Rate helper for bootstrapping over OIS rates.
    """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, tenor: Period, fixedRate: typing.SupportsFloat, overnightIndex: OvernightIndex, discountingCurve: YieldTermStructureHandle = ..., telescopicValueDates: bool = False, paymentLag: typing.SupportsInt = 0, paymentConvention: BusinessDayConvention = ..., paymentFrequency: Frequency = ..., paymentCalendar: typing.Any = None, forwardStart: Period = ..., overnightSpread: typing.SupportsFloat = 0.0, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs from settlement days, tenor, and overnight index.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, tenor: Period, fixedRate: QuoteHandle, overnightIndex: OvernightIndex, discountingCurve: YieldTermStructureHandle = ..., telescopicValueDates: bool = False, paymentLag: typing.SupportsInt = 0, paymentConvention: BusinessDayConvention = ..., paymentFrequency: Frequency = ..., paymentCalendar: typing.Any = None, forwardStart: Period = ..., overnightSpread: typing.SupportsFloat = 0.0, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs from settlement days, tenor, and quote handle.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, tenor: Period, fixedRate: base.Quote, overnightIndex: OvernightIndex, discountingCurve: YieldTermStructureHandle = ..., telescopicValueDates: bool = False, paymentLag: typing.SupportsInt = 0, paymentConvention: BusinessDayConvention = ..., paymentFrequency: Frequency = ..., paymentCalendar: typing.Any = None, forwardStart: Period = ..., overnightSpread: typing.SupportsFloat = 0.0, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs from settlement days, tenor, and quote (handle created internally).
        """
    @typing.overload
    def __init__(self, startDate: Date, endDate: Date, fixedRate: typing.SupportsFloat, overnightIndex: OvernightIndex, discountingCurve: YieldTermStructureHandle = ..., telescopicValueDates: bool = False, paymentLag: typing.SupportsInt = 0, paymentConvention: BusinessDayConvention = ..., paymentFrequency: Frequency = ..., paymentCalendar: typing.Any = None, overnightSpread: typing.SupportsFloat = 0.0, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs from start date, end date, rate, and overnight index.
        """
    @typing.overload
    def __init__(self, startDate: Date, endDate: Date, fixedRate: QuoteHandle, overnightIndex: OvernightIndex, discountingCurve: YieldTermStructureHandle = ..., telescopicValueDates: bool = False, paymentLag: typing.SupportsInt = 0, paymentConvention: BusinessDayConvention = ..., paymentFrequency: Frequency = ..., paymentCalendar: typing.Any = None, overnightSpread: typing.SupportsFloat = 0.0, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs from start date, end date, quote handle, and overnight index.
        """
    def swap(self) -> ...:
        """
        Returns the underlying OIS swap.
        """
class OMRCurrency(Currency):
    """
    ! Omani rial
    /*! The ISO three-letter code is OMR; the numeric code is 512.
         It is divided into 1000 baisa.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class Observable:
    """
    Core observable class in QuantLib's Observer pattern
    
    Maintains a list of observers and notifies them of state changes.
    """
    def __init__(self) -> None:
        """
        Default constructor for the Observable.
        """
    def notifyObservers(self) -> None:
        """
        Notify all registered observers of state changes.
        This version broadcasts a generic notification without event details.
        """
class ObservableValue_Date:
    """
    Observable and assignable proxy to a Date value.
    
    Observers can be registered with instances of this class so that they are notified when a different value is assigned. Client code can copy the contained value or pass it to functions via implicit conversion.
    
    Note: It is not possible to call non-const methods on the returned value. This is by design, as this would bypass the notification mechanism; modify the value via re-assignment instead.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, date: ...) -> None:
        ...
    @typing.overload
    def __init__(self, other: ObservableValue_Date) -> None:
        ...
    def value(self) -> ...:
        """
        Returns the current value.
        """
class OneDayCounter(DayCounter):
    """
    1/1 day count convention.
    """
    def __init__(self) -> None:
        ...
class OperatorSplittingSpreadEngine(base.SpreadBlackScholesVanillaEngine):
    """
    Operator splitting analytical approximation for spread options.
    """
    def __init__(self, process1: GeneralizedBlackScholesProcess, process2: GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with two Black-Scholes processes and correlation.
        """
class OptionType:
    """
    Option type (call or put).
    
    Members:
    
      Call : Call option.
    
      Put : Put option.
    """
    Call: typing.ClassVar[OptionType]  # value = <OptionType.Call: 1>
    Put: typing.ClassVar[OptionType]  # value = <OptionType.Put: -1>
    __members__: typing.ClassVar[dict[str, OptionType]]  # value = {'Call': <OptionType.Call: 1>, 'Put': <OptionType.Put: -1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class OptionletStripper1(base.OptionletStripper):
    """
    Strips optionlet volatilities from a cap/floor term volatility surface.
    """
    @typing.overload
    def __init__(self, termVolSurface: CapFloorTermVolSurface, index: IborIndex, switchStrike: typing.Any = None, accuracy: typing.SupportsFloat = 1e-06, maxIter: typing.SupportsInt = 100, discount: YieldTermStructureHandle = ..., type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0, dontThrow: bool = False, optionletFrequency: typing.Any = None) -> None:
        """
        Constructs an optionlet stripper.
        """
    @typing.overload
    def __init__(self, termVolSurface: CapFloorTermVolSurface, index: IborIndex, switchStrike: typing.Any = None, accuracy: typing.SupportsFloat = 1e-06, maxIter: typing.SupportsInt = 100, discount: base.YieldTermStructure, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0, dontThrow: bool = False, optionletFrequency: typing.Any = None) -> None:
        """
        Constructs an optionlet stripper (handle created internally).
        """
    def capFloorPrices(self) -> Matrix:
        """
        Returns the cap/floor prices matrix.
        """
    def capFloorVolatilities(self) -> Matrix:
        """
        Returns the cap/floor volatilities matrix.
        """
    def capletVols(self) -> Matrix:
        """
        Returns the caplet volatilities matrix.
        """
    def optionletPrices(self) -> Matrix:
        """
        Returns the optionlet prices matrix.
        """
    def switchStrike(self) -> float:
        """
        Returns the switch strike.
        """
class OptionletVolatilityStructureHandle:
    """
    Handle to OptionletVolatilityStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: OptionletVolatilityStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: OptionletVolatilityStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: OptionletVolatilityStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.OptionletVolatilityStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.OptionletVolatilityStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class OvernightIndex(IborIndex):
    """
    Base class for overnight indexes.
    """
    @typing.overload
    def __init__(self, familyName: str, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, dayCounter: DayCounter) -> None:
        """
        Constructs an overnight index without forwarding curve.
        """
    @typing.overload
    def __init__(self, familyName: str, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, dayCounter: DayCounter, h: ...) -> None:
        """
        Constructs an overnight index with forwarding term structure handle.
        """
class OvernightIndexedCoupon(FloatingRateCoupon):
    """
    Coupon paying the compounded daily overnight rate.
    """
    def __init__(self, paymentDate: Date, nominal: typing.SupportsFloat, startDate: Date, endDate: Date, overnightIndex: ..., gearing: typing.SupportsFloat = 1.0, spread: typing.SupportsFloat = 0.0, refPeriodStart: Date = ..., refPeriodEnd: Date = ..., dayCounter: typing.Any = None, telescopicValueDates: bool = False, averagingMethod: RateAveraging.Type = ..., lookbackDays: typing.Any = None, lockoutDays: typing.SupportsInt = 0, applyObservationShift: bool = False) -> None:
        """
        Constructs an overnight indexed coupon.
        """
    def applyObservationShift(self) -> bool:
        """
        Returns whether observation shift is applied.
        """
    def averagingMethod(self) -> RateAveraging.Type:
        """
        Returns the averaging method.
        """
    def dt(self) -> list[float]:
        """
        Returns the accrual periods.
        """
    def fixingDates(self) -> list[Date]:
        """
        Returns the fixing dates for the rates to be compounded.
        """
    def indexFixings(self) -> list[float]:
        """
        Returns the fixings to be compounded.
        """
    def lockoutDays(self) -> int:
        """
        Returns the number of lockout days.
        """
    def valueDates(self) -> list[Date]:
        """
        Returns the value dates for the rates to be compounded.
        """
class OvernightIndexedSwap(FixedVsFloatingSwap):
    """
    Overnight indexed swap: fixed vs overnight floating leg.
    """
    @typing.overload
    def __init__(self, type: SwapType, nominal: typing.SupportsFloat, schedule: Schedule, fixedRate: typing.SupportsFloat, fixedDC: DayCounter, overnightIndex: OvernightIndex, spread: typing.SupportsFloat = 0.0, paymentLag: typing.SupportsInt = 0, paymentAdjustment: BusinessDayConvention = ..., telescopicValueDates: bool = False, averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs an overnight indexed swap.
        """
    @typing.overload
    def __init__(self, type: SwapType, nominal: typing.SupportsFloat, fixedSchedule: Schedule, fixedRate: typing.SupportsFloat, fixedDC: DayCounter, overnightSchedule: Schedule, overnightIndex: OvernightIndex, spread: typing.SupportsFloat = 0.0, paymentLag: typing.SupportsInt = 0, paymentAdjustment: BusinessDayConvention = ..., telescopicValueDates: bool = False, averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs an OIS with separate fixed and overnight schedules.
        """
    def averagingMethod(self) -> RateAveraging.Type:
        """
        Returns the rate averaging method.
        """
    def overnightIndex(self) -> typing.Any:
        """
        Returns the overnight index.
        """
    def overnightLeg(self) -> list[base.CashFlow]:
        """
        Returns the overnight leg cash flows.
        """
    def overnightLegBPS(self) -> float:
        """
        Returns the BPS of the overnight leg.
        """
    def overnightLegNPV(self) -> float:
        """
        Returns the NPV of the overnight leg.
        """
class OvernightIndexedSwapIndex(SwapIndex):
    """
    OIS swap rate index.
    """
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, overnightIndex: OvernightIndex, telescopicValueDates: bool = False, averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs an OIS swap rate index.
        """
    def overnightIndex(self) -> typing.Any:
        """
        Returns the overnight index.
        """
class OvernightLeg:
    """
    Helper class for building a leg of overnight indexed coupons.
    """
    def __init__(self, schedule: Schedule, overnightIndex: ...) -> None:
        """
        Constructs an OvernightLeg from a schedule and overnight index.
        """
    def build(self) -> list[base.CashFlow]:
        """
        Builds and returns the leg of cash flows.
        """
    def withAveragingMethod(self, averagingMethod: RateAveraging.Type) -> OvernightLeg:
        ...
    @typing.overload
    def withGearings(self, gearing: typing.SupportsFloat) -> OvernightLeg:
        ...
    @typing.overload
    def withGearings(self, gearings: collections.abc.Sequence[typing.SupportsFloat]) -> OvernightLeg:
        ...
    def withLockoutDays(self, lockoutDays: typing.SupportsInt) -> OvernightLeg:
        ...
    def withLookbackDays(self, lookbackDays: typing.SupportsInt) -> OvernightLeg:
        ...
    @typing.overload
    def withNotionals(self, nominal: typing.SupportsFloat) -> OvernightLeg:
        ...
    @typing.overload
    def withNotionals(self, nominals: collections.abc.Sequence[typing.SupportsFloat]) -> OvernightLeg:
        ...
    def withObservationShift(self, applyObservationShift: bool = True) -> OvernightLeg:
        ...
    def withPaymentAdjustment(self, convention: BusinessDayConvention) -> OvernightLeg:
        ...
    def withPaymentCalendar(self, calendar: Calendar) -> OvernightLeg:
        ...
    def withPaymentDayCounter(self, dayCounter: DayCounter) -> OvernightLeg:
        ...
    def withPaymentLag(self, lag: typing.SupportsInt) -> OvernightLeg:
        ...
    @typing.overload
    def withSpreads(self, spread: typing.SupportsFloat) -> OvernightLeg:
        ...
    @typing.overload
    def withSpreads(self, spreads: collections.abc.Sequence[typing.SupportsFloat]) -> OvernightLeg:
        ...
    def withTelescopicValueDates(self, telescopicValueDates: bool) -> OvernightLeg:
        ...
class PEHCurrency(Currency):
    """
    ! The ISO three-letter code was PEH. A numeric code is not available;
            as per ISO 3166-1, we assign 999 as a user-defined code.
            It was divided in 100 centavos.
    
            Obsoleted by the inti since February 1985.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class PEICurrency(Currency):
    """
    ! The ISO three-letter code was PEI.
            It was divided in 100 centimos. A numeric code is not available;
            as per ISO 3166-1, we assign 998 as a user-defined code.
    
            Obsoleted by the nuevo sol since July 1991.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class PENCurrency(Currency):
    """
    ! The ISO three-letter code is PEN; the numeric code is 604.
            It is divided in 100 centimos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class PHPCurrency(Currency):
    """
    ! Philippine peso
    /*! The ISO three-letter code is PHP; the numeric code is 608.
         It is divided into 100 centavo.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class PKRCurrency(Currency):
    """
    ! The ISO three-letter code is PKR; the numeric code is 586.
            It is divided in 100 paisa.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class PLNCurrency(Currency):
    """
    ! The ISO three-letter code is PLN; the numeric code is 985.
            It is divided in 100 groszy.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class PTECurrency(Currency):
    """
    ! The ISO three-letter code was PTE; the numeric code was 620.
            It was divided in 100 centavos.
    
            Obsoleted by the Euro since 1999.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class Parameter:
    """
    Model parameter with constraint.
    """
    def __call__(self, t: typing.SupportsFloat) -> float:
        """
        Returns parameter value at time t.
        """
    def __init__(self) -> None:
        ...
    def constraint(self) -> base.Constraint:
        """
        Returns the parameter constraint.
        """
    def params(self) -> Array:
        """
        Returns parameter values.
        """
    def setParam(self, i: typing.SupportsInt, x: typing.SupportsFloat) -> None:
        """
        Sets the i-th parameter value.
        """
    def size(self) -> int:
        """
        Returns number of parameters.
        """
    def testParams(self, params: Array) -> bool:
        """
        Tests if parameters satisfy constraint.
        """
class PercentageStrikePayoff(base.StrikedTypePayoff):
    """
    Payoff with strike expressed as moneyness percentage.
    """
    def __init__(self, type: OptionType, moneyness: typing.SupportsFloat) -> None:
        ...
class Period:
    """
    Time period represented by length and units.
    """
    def __add__(self, arg0: Period) -> Period:
        ...
    def __eq__(self, arg0: Period) -> bool:
        ...
    def __ge__(self, arg0: Period) -> bool:
        ...
    def __gt__(self, arg0: Period) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __iadd__(self, arg0: Period) -> Period:
        ...
    def __imul__(self, arg0: typing.SupportsInt) -> Period:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, length: typing.SupportsInt, units: TimeUnit) -> None:
        ...
    @typing.overload
    def __init__(self, frequency: Frequency) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: str) -> None:
        """
        Create Period from a string like '3M', '2Y', etc.
        """
    def __isub__(self, arg0: Period) -> Period:
        ...
    def __itruediv__(self, arg0: typing.SupportsInt) -> Period:
        ...
    def __le__(self, arg0: Period) -> bool:
        ...
    def __lt__(self, arg0: Period) -> bool:
        ...
    def __mul__(self, arg0: typing.SupportsInt) -> Period:
        ...
    def __ne__(self, arg0: Period) -> bool:
        ...
    def __neg__(self) -> Period:
        ...
    def __repr__(self) -> str:
        ...
    def __rmul__(self, arg0: typing.SupportsInt) -> Period:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: Period) -> Period:
        ...
    def __truediv__(self, arg0: typing.SupportsInt) -> Period:
        ...
    def frequency(self) -> Frequency:
        ...
    def length(self) -> int:
        ...
    def normalize(self) -> None:
        ...
    def normalized(self) -> Period:
        ...
    def units(self) -> TimeUnit:
        ...
class PiecewiseBackwardFlatForward(base.YieldTermStructure):
    """
    Piecewise yield curve using backward-flat forward-rate interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseBackwardFlatHazard(base.DefaultProbabilityTermStructure):
    """
    Piecewise default curve using backward-flat hazard rate.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseCubicDiscount(base.YieldTermStructure):
    """
    Piecewise yield curve using cubic discount factor interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseCubicZero(base.YieldTermStructure):
    """
    Piecewise yield curve using cubic zero-rate interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLinearDefaultDensity(base.DefaultProbabilityTermStructure):
    """
    Piecewise default curve using linear default density.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLinearDiscount(base.YieldTermStructure):
    """
    Piecewise yield curve using linear discount factor interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLinearForward(base.YieldTermStructure):
    """
    Piecewise yield curve using linear forward-rate interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLinearZero(base.YieldTermStructure):
    """
    Piecewise yield curve using linear zero-rate interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLogLinearDiscount(base.YieldTermStructure):
    """
    Piecewise yield curve using log-linear discount factor interpolation.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.RateHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseLogLinearSurvival(base.DefaultProbabilityTermStructure):
    """
    Piecewise default curve using log-linear survival probability.
    """
    @typing.overload
    def __init__(self, referenceDate: Date, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from reference date, instruments, and day counter.
        """
    @typing.overload
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, instruments: collections.abc.Sequence[base.DefaultProbabilityHelper], dayCounter: DayCounter) -> None:
        """
        Constructs from settlement days, calendar, instruments, and day counter.
        """
    def data(self) -> list[float]:
        """
        Returns the interpolated data values.
        """
    def dates(self) -> list[Date]:
        """
        Returns the interpolation dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns (date, value) pairs for all nodes.
        """
    def times(self) -> list[float]:
        """
        Returns the interpolation times.
        """
class PiecewiseTimeDependentHestonModel(base.CalibratedModel):
    """
    Piecewise time-dependent Heston stochastic volatility model.
    """
    def __init__(self, riskFreeRate: YieldTermStructureHandle, dividendYield: YieldTermStructureHandle, s0: QuoteHandle, v0: typing.SupportsFloat, theta: Parameter, kappa: Parameter, sigma: Parameter, rho: Parameter, timeGrid: TimeGrid) -> None:
        """
        Constructs time-dependent Heston model.
        """
    def dividendYield(self) -> YieldTermStructureHandle:
        """
        Returns dividend yield term structure.
        """
    def kappa(self, t: typing.SupportsFloat) -> float:
        """
        Returns kappa at time t.
        """
    def rho(self, t: typing.SupportsFloat) -> float:
        """
        Returns rho at time t.
        """
    def riskFreeRate(self) -> YieldTermStructureHandle:
        """
        Returns risk-free rate term structure.
        """
    def s0(self) -> float:
        """
        Returns initial spot price.
        """
    def sigma(self, t: typing.SupportsFloat) -> float:
        """
        Returns sigma at time t.
        """
    def theta(self, t: typing.SupportsFloat) -> float:
        """
        Returns theta at time t.
        """
    def timeGrid(self) -> TimeGrid:
        """
        Returns the time grid.
        """
    def v0(self) -> float:
        """
        Returns initial variance.
        """
class Pillar:
    """
    Pillar date calculation types for rate helpers.
    """
    class Choice:
        """
        Pillar choice for rate helper.
        
        Members:
        
          MaturityDate : Use the instrument maturity date.
        
          LastRelevantDate : Use the last relevant date for pricing.
        
          CustomDate : Use a custom pillar date.
        """
        CustomDate: typing.ClassVar[Pillar.Choice]  # value = <Choice.CustomDate: 2>
        LastRelevantDate: typing.ClassVar[Pillar.Choice]  # value = <Choice.LastRelevantDate: 1>
        MaturityDate: typing.ClassVar[Pillar.Choice]  # value = <Choice.MaturityDate: 0>
        __members__: typing.ClassVar[dict[str, Pillar.Choice]]  # value = {'MaturityDate': <Choice.MaturityDate: 0>, 'LastRelevantDate': <Choice.LastRelevantDate: 1>, 'CustomDate': <Choice.CustomDate: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
class PlainVanillaPayoff(base.StrikedTypePayoff):
    """
    Plain vanilla payoff (max(S-K,0) for call, max(K-S,0) for put).
    """
    def __init__(self, type: OptionType, strike: typing.SupportsFloat) -> None:
        ...
class Poland(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Easter Monday</li>
            <li>Corpus Christi</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th (since 2011)</li>
            <li>May Day, May 1st</li>
            <li>Constitution Day, May 3rd</li>
            <li>Assumption of the Blessed Virgin Mary, August 15th</li>
            <li>All Saints Day, November 1st</li>
            <li>Independence Day, November 11th</li>
            <li>Christmas, December 25th</li>
            <li>2nd Day of Christmas, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        ! PL calendars
        
        Members:
        
          Settlement : !< Settlement calendar
        
          WSE : !< Warsaw stock exchange calendar
        """
        Settlement: typing.ClassVar[Poland.Market]  # value = <Market.Settlement: 0>
        WSE: typing.ClassVar[Poland.Market]  # value = <Market.WSE: 1>
        __members__: typing.ClassVar[dict[str, Poland.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'WSE': <Market.WSE: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Settlement: typing.ClassVar[Poland.Market]  # value = <Market.Settlement: 0>
    WSE: typing.ClassVar[Poland.Market]  # value = <Market.WSE: 1>
    def __init__(self) -> None:
        ...
class PolynomialType:
    """
    Polynomial basis types for Longstaff-Schwartz regression.
    
    Members:
    
      Monomial
    
      Laguerre
    
      Hermite
    
      Hyperbolic
    
      Legendre
    
      Chebyshev
    
      Chebyshev2nd
    """
    Chebyshev: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Chebyshev: 5>
    Chebyshev2nd: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Chebyshev2nd: 6>
    Hermite: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Hermite: 2>
    Hyperbolic: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Hyperbolic: 3>
    Laguerre: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Laguerre: 1>
    Legendre: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Legendre: 4>
    Monomial: typing.ClassVar[PolynomialType]  # value = <PolynomialType.Monomial: 0>
    __members__: typing.ClassVar[dict[str, PolynomialType]]  # value = {'Monomial': <PolynomialType.Monomial: 0>, 'Laguerre': <PolynomialType.Laguerre: 1>, 'Hermite': <PolynomialType.Hermite: 2>, 'Hyperbolic': <PolynomialType.Hyperbolic: 3>, 'Legendre': <PolynomialType.Legendre: 4>, 'Chebyshev': <PolynomialType.Chebyshev: 5>, 'Chebyshev2nd': <PolynomialType.Chebyshev2nd: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PositionType:
    """
    Long or short position.
    
    Members:
    
      Long
    
      Short
    """
    Long: typing.ClassVar[PositionType]  # value = <PositionType.Long: 0>
    Short: typing.ClassVar[PositionType]  # value = <PositionType.Short: 1>
    __members__: typing.ClassVar[dict[str, PositionType]]  # value = {'Long': <PositionType.Long: 0>, 'Short': <PositionType.Short: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PositiveConstraint(base.Constraint):
    """
    Constraint enforcing positive values.
    """
    def __init__(self) -> None:
        ...
class Problem:
    """
    Constrained optimization problem.
    """
    def __init__(self, costFunction: base.CostFunction, constraint: base.Constraint, initialValue: Array) -> None:
        """
        Creates an optimization problem.
        """
    def constraint(self) -> base.Constraint:
        """
        Returns the constraint.
        """
    def costFunction(self) -> base.CostFunction:
        """
        Returns the cost function.
        """
    def currentValue(self) -> Array:
        """
        Returns the current parameter values.
        """
    def functionValue(self) -> float:
        """
        Returns the current function value.
        """
    def value(self, x: Array) -> float:
        """
        Evaluates the cost function at the given point.
        """
    def values(self, x: Array) -> Array:
        """
        Evaluates the cost function values at the given point.
        """
class ProtectionSide:
    """
    Protection buyer or seller.
    
    Members:
    
      Buyer : Protection buyer.
    
      Seller : Protection seller.
    """
    Buyer: typing.ClassVar[ProtectionSide]  # value = <ProtectionSide.Buyer: 0>
    Seller: typing.ClassVar[ProtectionSide]  # value = <ProtectionSide.Seller: 1>
    __members__: typing.ClassVar[dict[str, ProtectionSide]]  # value = {'Buyer': <ProtectionSide.Buyer: 0>, 'Seller': <ProtectionSide.Seller: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class QARCurrency(Currency):
    """
    ! Qatari riyal
    /*! The ISO three-letter code is QAR; the numeric code is 634.
         It is divided into 100 diram.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class QdFpAmericanEngine(base.PricingEngine):
    """
    High performance American option engine based on QD+ fixed-point iteration.
    """
    @staticmethod
    def accurateScheme() -> QdFpIterationScheme:
        """
        Returns the accurate iteration scheme (default).
        """
    @staticmethod
    def fastScheme() -> QdFpIterationScheme:
        """
        Returns the fast iteration scheme.
        """
    @staticmethod
    def highPrecisionScheme() -> QdFpIterationScheme:
        """
        Returns the high precision iteration scheme.
        """
    @typing.overload
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs with process using default accurate scheme.
        """
    @typing.overload
    def __init__(self, process: GeneralizedBlackScholesProcess, iterationScheme: QdFpIterationScheme, fpEquation: QdFpFixedPointEquation = ...) -> None:
        """
        Constructs with process, iteration scheme, and fixed-point equation type.
        """
class QdFpFixedPointEquation:
    """
    Fixed point equation type for QD+ American engine.
    
    Members:
    
      FP_A
    
      FP_B
    
      Auto
    """
    Auto: typing.ClassVar[QdFpFixedPointEquation]  # value = <QdFpFixedPointEquation.Auto: 2>
    FP_A: typing.ClassVar[QdFpFixedPointEquation]  # value = <QdFpFixedPointEquation.FP_A: 0>
    FP_B: typing.ClassVar[QdFpFixedPointEquation]  # value = <QdFpFixedPointEquation.FP_B: 1>
    __members__: typing.ClassVar[dict[str, QdFpFixedPointEquation]]  # value = {'FP_A': <QdFpFixedPointEquation.FP_A: 0>, 'FP_B': <QdFpFixedPointEquation.FP_B: 1>, 'Auto': <QdFpFixedPointEquation.Auto: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class QdFpIterationScheme:
    """
    Base class for QD+ fixed-point iteration schemes.
    """
class QdFpLegendreScheme(QdFpIterationScheme):
    """
    Gauss-Legendre (l,m,n)-p iteration scheme.
    """
    def __init__(self, l: typing.SupportsInt, m: typing.SupportsInt, n: typing.SupportsInt, p: typing.SupportsInt) -> None:
        """
        Constructs with integration order l, iteration steps m, Chebyshev nodes n, and final integration order p.
        """
class QdFpLegendreTanhSinhScheme(QdFpLegendreScheme):
    """
    Legendre-Tanh-Sinh (l,m,n)-eps iteration scheme.
    """
    def __init__(self, l: typing.SupportsInt, m: typing.SupportsInt, n: typing.SupportsInt, eps: typing.SupportsFloat) -> None:
        """
        Constructs with integration order l, iteration steps m, Chebyshev nodes n, and tanh-sinh precision eps.
        """
class QdFpTanhSinhIterationScheme(QdFpIterationScheme):
    """
    Tanh-sinh (m,n)-eps iteration scheme.
    """
    def __init__(self, m: typing.SupportsInt, n: typing.SupportsInt, eps: typing.SupportsFloat) -> None:
        """
        Constructs with iteration steps m, Chebyshev nodes n, and tanh-sinh precision eps.
        """
class QuoteHandle:
    """
    Handle to Quote objects
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: QuoteHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: QuoteHandle) -> bool:
        ...
    def __ne__(self, arg0: QuoteHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.Quote:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.Quote:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class ROLCurrency(Currency):
    """
    ! The ISO three-letter code was ROL; the numeric code was 642.
            It was divided in 100 bani.
    
            Obsoleted by the new leu since July 2005.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class RONCurrency(Currency):
    """
    ! The ISO three-letter code is RON; the numeric code is 946.
            It is divided in 100 bani.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class RSDCurrency(Currency):
    """
    ! The ISO three-letter code is RSD; the numeric code is 941.
            It is divided into 100 para/napa.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class RUBCurrency(Currency):
    """
    ! The ISO three-letter code is RUB; the numeric code is 643.
            It is divided in 100 kopeyki.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class RateAveraging:
    """
    Rate averaging methods for multi-fixing coupons.
    """
    class Type:
        """
        Rate averaging type.
        
        Members:
        
          Simple : Simple averaging: sum of sub-period interest amounts.
        
          Compound : Compound averaging: compounded sub-period rates.
        """
        Compound: typing.ClassVar[RateAveraging.Type]  # value = <Type.Compound: 1>
        Simple: typing.ClassVar[RateAveraging.Type]  # value = <Type.Simple: 0>
        __members__: typing.ClassVar[dict[str, RateAveraging.Type]]  # value = {'Simple': <Type.Simple: 0>, 'Compound': <Type.Compound: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
class Redemption(SimpleCashFlow):
    """
    Bond redemption payment.
    """
    def __init__(self, amount: typing.SupportsFloat, date: Date) -> None:
        """
        Constructs a redemption with the given amount and date.
        """
class Region:
    """
    Geographic region for inflation indexes.
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Region) -> bool:
        ...
    def __ne__(self, arg0: Region) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def code(self) -> str:
        """
        Returns the ISO region code.
        """
    def name(self) -> str:
        """
        Returns the region name.
        """
class RelinkableBlackVolTermStructureHandle(BlackVolTermStructureHandle):
    """
    Relinkable handle to BlackVolTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableDefaultProbabilityTermStructureHandle(DefaultProbabilityTermStructureHandle):
    """
    Relinkable handle to DefaultProbabilityTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableLocalVolTermStructureHandle(LocalVolTermStructureHandle):
    """
    Relinkable handle to LocalVolTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableOptionletVolatilityStructureHandle(OptionletVolatilityStructureHandle):
    """
    Relinkable handle to OptionletVolatilityStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableQuoteHandle(QuoteHandle):
    """
    Relinkable handle to Quote objects
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableShortRateModelHandle(ShortRateModelHandle):
    """
    Relinkable handle to a short-rate model.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableSwaptionVolatilityStructureHandle(SwaptionVolatilityStructureHandle):
    """
    Relinkable handle to SwaptionVolatilityStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableYieldTermStructureHandle(YieldTermStructureHandle):
    """
    Relinkable handle to YieldTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableYoYInflationTermStructureHandle(YoYInflationTermStructureHandle):
    """
    Relinkable handle to YoYInflationTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class RelinkableZeroInflationTermStructureHandle(ZeroInflationTermStructureHandle):
    """
    Relinkable handle to ZeroInflationTermStructure.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty relinkable handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a relinkable handle linked to the given object.
        """
    def linkTo(self, ptr: typing.Any = None, registerAsObserver: bool = True) -> None:
        """
        Links the handle to a new object instance. Notifies observers.
        """
class Romania(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li> Day after New Year's Day, January 2nd</li>
            <li>Unification Day, January 24th</li>
            <li>Orthodox Easter (only Sunday and Monday)</li>
            <li>Labour Day, May 1st</li>
            <li>Pentecost with Monday (50th and 51st days after the
                Othodox Easter)</li>
            <li>Children's Day, June 1st (since 2017)</li>
            <li>St Marys Day, August 15th</li>
            <li>Feast of St Andrew, November 30th</li>
            <li>National Day, December 1st</li>
            <li>Christmas, December 25th</li>
            <li>2nd Day of Christmas, December 26th</li>
            </ul>
    
            Holidays for the Bucharest stock exchange
            (data from <http://www.bvb.ro/Marketplace/TradingCalendar/index.aspx>):
            all public holidays, plus a few one-off closing days (2014 only).
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Public : !< Public holidays
        
          BVB : !< Bucharest stock-exchange
        """
        BVB: typing.ClassVar[Romania.Market]  # value = <Market.BVB: 1>
        Public: typing.ClassVar[Romania.Market]  # value = <Market.Public: 0>
        __members__: typing.ClassVar[dict[str, Romania.Market]]  # value = {'Public': <Market.Public: 0>, 'BVB': <Market.BVB: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BVB: typing.ClassVar[Romania.Market]  # value = <Market.BVB: 1>
    Public: typing.ClassVar[Romania.Market]  # value = <Market.Public: 0>
    def __init__(self, market: Romania.Market = ...) -> None:
        ...
class Rounding:
    """
    Basic rounding convention.
    """
    class Type:
        """
        Rounding type enumeration.
        
        Members:
        
          None_ : No rounding.
        
          Up : Round up.
        
          Down : Round down.
        
          Closest : Round to the closest.
        
          Floor : Round to the largest integer not greater than x.
        
          Ceiling : Round to the smallest integer not less than x.
        """
        Ceiling: typing.ClassVar[Rounding.Type]  # value = <Type.Ceiling: 5>
        Closest: typing.ClassVar[Rounding.Type]  # value = <Type.Closest: 3>
        Down: typing.ClassVar[Rounding.Type]  # value = <Type.Down: 2>
        Floor: typing.ClassVar[Rounding.Type]  # value = <Type.Floor: 4>
        None_: typing.ClassVar[Rounding.Type]  # value = <Type.None_: 0>
        Up: typing.ClassVar[Rounding.Type]  # value = <Type.Up: 1>
        __members__: typing.ClassVar[dict[str, Rounding.Type]]  # value = {'None_': <Type.None_: 0>, 'Up': <Type.Up: 1>, 'Down': <Type.Down: 2>, 'Closest': <Type.Closest: 3>, 'Floor': <Type.Floor: 4>, 'Ceiling': <Type.Ceiling: 5>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    def __call__(self, value: typing.SupportsFloat) -> float:
        """
        Rounds the given value.
        """
    def __init__(self, precision: typing.SupportsInt, type: Rounding.Type = ..., digit: typing.SupportsInt = 5) -> None:
        """
        Creates a rounding convention.
        """
    @property
    def precision(self) -> int:
        """
        Returns the precision.
        """
    @property
    def roundingDigit(self) -> int:
        """
        Returns the rounding digit.
        """
    @property
    def type(self) -> Rounding.Type:
        """
        Returns the rounding type.
        """
class Russia(Calendar):
    """
    ! Public holidays (see <http://www.cbr.ru/eng/>:):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year holidays, January 1st to 5th (only 1st and 2nd
                until 2005)</li>
            <li>Christmas, January 7th (possibly moved to Monday)</li>
            <li>Defender of the Fatherland Day, February 23rd (possibly
                moved to Monday)</li>
            <li>International Women's Day, March 8th (possibly moved to
                Monday)</li>
            <li>Labour Day, May 1st (possibly moved to Monday)</li>
            <li>Victory Day, May 9th (possibly moved to Monday)</li>
            <li>Russia Day, June 12th (possibly moved to Monday)</li>
            <li>Unity Day, November 4th (possibly moved to Monday)</li>
            </ul>
    
            Holidays for the Moscow Exchange (MOEX) taken from
            <http://moex.com/s726> and related pages.  These holidays are
            <em>not</em> consistent year-to-year, may or may not correlate
            to public holidays, and are only available for dates since the
            introduction of the MOEX 'brand' (a merger of the stock and
            futures markets).
    
            \\ingroup calendars
    """
    class Market:
        """
        ! Russian calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          MOEX : !< Moscow Exchange calendar
        """
        MOEX: typing.ClassVar[Russia.Market]  # value = <Market.MOEX: 1>
        Settlement: typing.ClassVar[Russia.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, Russia.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'MOEX': <Market.MOEX: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    MOEX: typing.ClassVar[Russia.Market]  # value = <Market.MOEX: 1>
    Settlement: typing.ClassVar[Russia.Market]  # value = <Market.Settlement: 0>
    def __init__(self, param_0: Russia.Market = ...) -> None:
        ...
class SARCurrency(Currency):
    """
    ! The ISO three-letter code is SAR; the numeric code is 682.
            It is divided in 100 halalat.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class SEKCurrency(Currency):
    """
    ! The ISO three-letter code is SEK; the numeric code is 752.
            It is divided in 100 �re.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class SGDCurrency(Currency):
    """
    ! The ISO three-letter code is SGD; the numeric code is 702.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class SITCurrency(Currency):
    """
    ! The ISO three-letter code is SIT; the numeric code is 705.
            It is divided in 100 stotinov.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class SKKCurrency(Currency):
    """
    ! The ISO three-letter code is SKK; the numeric code is 703.
            It was divided in 100 halierov.
    
            Obsoleted by the Euro since 2009.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class SabrInterpolatedSmileSection(base.SmileSection, base.LazyObject):
    """
    Smile section calibrated via SABR interpolation.
    """
    def __init__(self, optionDate: Date, forward: typing.SupportsFloat, strikes: collections.abc.Sequence[typing.SupportsFloat], hasFloatingStrikes: bool, atmVolatility: typing.SupportsFloat, vols: collections.abc.Sequence[typing.SupportsFloat], alpha: typing.SupportsFloat, beta: typing.SupportsFloat, nu: typing.SupportsFloat, rho: typing.SupportsFloat, isAlphaFixed: bool = False, isBetaFixed: bool = False, isNuFixed: bool = False, isRhoFixed: bool = False, vegaWeighted: bool = True, endCriteria: EndCriteria = None, method: base.OptimizationMethod = None, dayCounter: DayCounter = ..., shift: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs and calibrates SABR to market strikes and volatilities.
        """
    def alpha(self) -> float:
        """
        Returns calibrated SABR alpha.
        """
    def beta(self) -> float:
        """
        Returns calibrated SABR beta.
        """
    def endCriteria(self) -> EndCriteria.Type:
        """
        Returns end criteria type from calibration.
        """
    def maxError(self) -> float:
        """
        Returns maximum calibration error.
        """
    def nu(self) -> float:
        """
        Returns calibrated SABR nu.
        """
    def rho(self) -> float:
        """
        Returns calibrated SABR rho.
        """
    def rmsError(self) -> float:
        """
        Returns RMS calibration error.
        """
class SabrSmileSection(base.SmileSection):
    """
    SABR parametric smile section.
    """
    @typing.overload
    def __init__(self, timeToExpiry: typing.SupportsFloat, forward: typing.SupportsFloat, sabrParameters: collections.abc.Sequence[typing.SupportsFloat], shift: typing.SupportsFloat = 0.0, volatilityType: VolatilityType = ...) -> None:
        """
        Constructs from time to expiry, forward, and SABR parameters [alpha, beta, nu, rho].
        """
    @typing.overload
    def __init__(self, expiryDate: Date, forward: typing.SupportsFloat, sabrParameters: collections.abc.Sequence[typing.SupportsFloat], referenceDate: Date = ..., dayCounter: DayCounter = ..., shift: typing.SupportsFloat = 0.0, volatilityType: VolatilityType = ...) -> None:
        """
        Constructs from expiry date, forward, and SABR parameters [alpha, beta, nu, rho].
        """
    def alpha(self) -> float:
        """
        Returns SABR alpha parameter.
        """
    def beta(self) -> float:
        """
        Returns SABR beta parameter.
        """
    def nu(self) -> float:
        """
        Returns SABR nu parameter.
        """
    def rho(self) -> float:
        """
        Returns SABR rho parameter.
        """
class SabrSwaptionVolatilityCube(SwaptionVolatilityCube):
    """
    SABR-parameterized swaption volatility cube.
    """
    def __init__(self, atmVolStructure: SwaptionVolatilityStructureHandle, optionTenors: collections.abc.Sequence[Period], swapTenors: collections.abc.Sequence[Period], strikeSpreads: collections.abc.Sequence[typing.SupportsFloat], volSpreads: collections.abc.Sequence[collections.abc.Sequence[QuoteHandle]], swapIndexBase: SwapIndex, shortSwapIndexBase: SwapIndex, vegaWeightedSmileFit: bool, parametersGuess: collections.abc.Sequence[collections.abc.Sequence[QuoteHandle]], isParameterFixed: collections.abc.Sequence[bool], isAtmCalibrated: bool, endCriteria: EndCriteria = None, maxErrorTolerance: typing.Any = None, optMethod: base.OptimizationMethod = None, errorAccept: typing.Any = None, useMaxError: bool = False, maxGuesses: typing.SupportsInt = 50, backwardFlat: bool = False, cutoffStrike: typing.SupportsFloat = 0.0001) -> None:
        """
        Constructs SABR swaption volatility cube.
        """
    def denseSabrParameters(self) -> Matrix:
        """
        Returns dense SABR parameters matrix.
        """
    def marketVolCube(self) -> Matrix:
        """
        Returns the market volatility cube.
        """
    @typing.overload
    def recalibration(self, beta: typing.SupportsFloat, swapTenor: Period) -> None:
        """
        Recalibrates with fixed beta for a given swap tenor.
        """
    @typing.overload
    def recalibration(self, beta: collections.abc.Sequence[typing.SupportsFloat], swapTenor: Period) -> None:
        """
        Recalibrates with beta vector for a given swap tenor.
        """
    def sparseSabrParameters(self) -> Matrix:
        """
        Returns sparse SABR parameters matrix.
        """
    def updateAfterRecalibration(self) -> None:
        """
        Updates internal state after recalibration.
        """
    def volCubeAtmCalibrated(self) -> Matrix:
        """
        Returns the ATM-calibrated volatility cube.
        """
class SaudiArabia(Calendar):
    """
    ! Holidays for the Tadawul financial market
            (data from <http://www.tadawul.com.sa>):
            <ul>
            <li>Thursdays</li>
            <li>Fridays</li>
            <li>National Day of Saudi Arabia, September 23rd</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available sparsely for 2004-2011 only:)
            <ul>
            <li>Eid Al-Adha</li>
            <li>Eid Al-Fitr</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Tadawul : !< Tadawul financial market
        """
        Tadawul: typing.ClassVar[SaudiArabia.Market]  # value = <Market.Tadawul: 0>
        __members__: typing.ClassVar[dict[str, SaudiArabia.Market]]  # value = {'Tadawul': <Market.Tadawul: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Tadawul: typing.ClassVar[SaudiArabia.Market]  # value = <Market.Tadawul: 0>
    def __init__(self, m: SaudiArabia.Market = ...) -> None:
        ...
class SavedSettings:
    """
    Temporarily stores and restores global settings.
    """
    def __enter__(self) -> SavedSettings:
        ...
    def __exit__(self, arg0: typing.Any, arg1: typing.Any, arg2: typing.Any) -> None:
        ...
    def __init__(self) -> None:
        ...
class Schedule:
    """
    Payment schedule for a financial instrument.
    """
    def __getitem__(self, arg0: typing.SupportsInt) -> Date:
        ...
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], calendar: Calendar = ..., convention: BusinessDayConvention = ..., terminationDateConvention: pyquantlib._pyquantlib.BusinessDayConvention | None = None, tenor: pyquantlib._pyquantlib.Period | None = None, rule: pyquantlib._pyquantlib.DateGeneration.Rule | None = None, endOfMonth: bool | None = None, isRegular: collections.abc.Sequence[bool] = []) -> None:
        ...
    @typing.overload
    def __init__(self, effectiveDate: Date, terminationDate: Date, tenor: Period, calendar: Calendar, convention: BusinessDayConvention, terminationDateConvention: BusinessDayConvention, rule: DateGeneration.Rule, endOfMonth: bool, firstDate: Date = ..., nextToLastDate: Date = ...) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator[Date]:
        ...
    def __len__(self) -> int:
        ...
    def after(self, arg0: Date) -> Schedule:
        ...
    def at(self, arg0: typing.SupportsInt) -> Date:
        ...
    def back(self) -> Date:
        ...
    def businessDayConvention(self) -> BusinessDayConvention:
        ...
    def calendar(self) -> Calendar:
        ...
    def date(self, arg0: typing.SupportsInt) -> Date:
        ...
    def dates(self) -> list[Date]:
        ...
    def empty(self) -> bool:
        ...
    def endDate(self) -> Date:
        ...
    def endOfMonth(self) -> bool:
        ...
    def front(self) -> Date:
        ...
    def hasEndOfMonth(self) -> bool:
        ...
    def hasIsRegular(self) -> bool:
        ...
    def hasRule(self) -> bool:
        ...
    def hasTenor(self) -> bool:
        ...
    def hasTerminationDateBusinessDayConvention(self) -> bool:
        ...
    @typing.overload
    def isRegular(self, arg0: typing.SupportsInt) -> bool:
        ...
    @typing.overload
    def isRegular(self) -> list[bool]:
        ...
    def lower_bound(self, date: Date = ...) -> ...:
        ...
    def nextDate(self, arg0: Date) -> Date:
        ...
    def previousDate(self, arg0: Date) -> Date:
        ...
    def rule(self) -> DateGeneration.Rule:
        ...
    def startDate(self) -> Date:
        ...
    def tenor(self) -> Period:
        ...
    def terminationDateBusinessDayConvention(self) -> BusinessDayConvention:
        ...
    def until(self, arg0: Date) -> Schedule:
        ...
class Secant:
    """
    Secant 1-D solver.
    """
    def __init__(self) -> None:
        ...
    def setLowerBound(self, lowerBound: typing.SupportsFloat) -> None:
        """
        Sets lower bound for the function domain.
        """
    def setMaxEvaluations(self, evaluations: typing.SupportsInt) -> None:
        """
        Sets maximum number of function evaluations.
        """
    def setUpperBound(self, upperBound: typing.SupportsFloat) -> None:
        """
        Sets upper bound for the function domain.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, step: typing.SupportsFloat) -> float:
        """
        Finds root with automatic bracketing.
        """
    @typing.overload
    def solve(self, f: collections.abc.Callable, accuracy: typing.SupportsFloat, guess: typing.SupportsFloat, xMin: typing.SupportsFloat, xMax: typing.SupportsFloat) -> float:
        """
        Finds root within explicit bracket.
        """
class Settings:
    """
    Global repository for run-time library settings.
    """
    @staticmethod
    def instance() -> Settings:
        """
        Returns the singleton instance.
        """
    def anchorEvaluationDate(self) -> None:
        """
        Prevents the evaluation date from advancing automatically.
        """
    def resetEvaluationDate(self) -> None:
        """
        Resets the evaluation date to today and allows automatic advancement.
        """
    def setEvaluationDate(self, date: Date) -> None:
        """
        Sets the evaluation date.
        """
    @property
    def enforcesTodaysHistoricFixings(self) -> bool:
        """
        Whether to enforce historic fixings for today.
        """
    @enforcesTodaysHistoricFixings.setter
    def enforcesTodaysHistoricFixings(self, arg1: bool) -> None:
        ...
    @property
    def evaluationDate(self) -> Date:
        """
        The evaluation date for pricing calculations.
        """
    @evaluationDate.setter
    def evaluationDate(self, arg1: Date) -> None:
        ...
    @property
    def includeReferenceDateEvents(self) -> bool:
        """
        Whether events on the reference date are included.
        """
    @includeReferenceDateEvents.setter
    def includeReferenceDateEvents(self, arg1: bool) -> None:
        ...
    @property
    def includeTodaysCashFlows(self) -> bool | None:
        """
        Whether to include today's cash flows (optional).
        """
    @includeTodaysCashFlows.setter
    def includeTodaysCashFlows(self, arg1: bool | None) -> None:
        ...
class SettlementMethod:
    """
    Swaption settlement method.
    
    Members:
    
      PhysicalOTC
    
      PhysicalCleared
    
      CollateralizedCashPrice
    
      ParYieldCurve
    """
    CollateralizedCashPrice: typing.ClassVar[SettlementMethod]  # value = <SettlementMethod.CollateralizedCashPrice: 2>
    ParYieldCurve: typing.ClassVar[SettlementMethod]  # value = <SettlementMethod.ParYieldCurve: 3>
    PhysicalCleared: typing.ClassVar[SettlementMethod]  # value = <SettlementMethod.PhysicalCleared: 1>
    PhysicalOTC: typing.ClassVar[SettlementMethod]  # value = <SettlementMethod.PhysicalOTC: 0>
    __members__: typing.ClassVar[dict[str, SettlementMethod]]  # value = {'PhysicalOTC': <SettlementMethod.PhysicalOTC: 0>, 'PhysicalCleared': <SettlementMethod.PhysicalCleared: 1>, 'CollateralizedCashPrice': <SettlementMethod.CollateralizedCashPrice: 2>, 'ParYieldCurve': <SettlementMethod.ParYieldCurve: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SettlementType:
    """
    Swaption settlement type.
    
    Members:
    
      Physical
    
      Cash
    """
    Cash: typing.ClassVar[SettlementType]  # value = <SettlementType.Cash: 1>
    Physical: typing.ClassVar[SettlementType]  # value = <SettlementType.Physical: 0>
    __members__: typing.ClassVar[dict[str, SettlementType]]  # value = {'Physical': <SettlementType.Physical: 0>, 'Cash': <SettlementType.Cash: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ShortRateModelHandle:
    """
    Handle to a short-rate model.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: ShortRateModelHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: ShortRateModelHandle) -> bool:
        ...
    def __ne__(self, arg0: ShortRateModelHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.ShortRateModel:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.ShortRateModel:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class SimpleCashFlow(base.CashFlow):
    """
    Simple cash flow paying a fixed amount on a given date.
    """
    def __init__(self, amount: typing.SupportsFloat, date: Date) -> None:
        """
        Constructs a cash flow with the given amount and date.
        """
class SimpleDayCounter(DayCounter):
    """
    Simple day counter returning whole-month distances as simple fractions (1 year = 1.0, 6 months = 0.5, etc.). Use with NullCalendar.
    """
    def __init__(self) -> None:
        ...
class SimplePolynomialFitting(base.FittingMethod):
    """
    Simple polynomial fitting method.
    """
    def __init__(self, degree: typing.SupportsInt, constrainAtZero: bool = True, weights: Array = ..., optimizationMethod: base.OptimizationMethod = None, l2: Array = ..., minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308, constraint: base.Constraint = ...) -> None:
        """
        Constructs a simple polynomial fitting method.
        """
class SimpleQuote(base.Quote):
    """
    Simple quote for market data.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs an invalid SimpleQuote.
        """
    @typing.overload
    def __init__(self, value: typing.SupportsFloat) -> None:
        """
        Constructs a SimpleQuote with the given value.
        """
    def isValid(self) -> bool:
        """
        Returns true if the quote holds a valid value.
        """
    def reset(self) -> None:
        """
        Resets the quote to an invalid state.
        """
    def setValue(self, value: typing.SupportsFloat) -> float:
        """
        Sets the quote value and notifies observers.
        """
    def value(self) -> float:
        """
        Returns the current value.
        """
class Singapore(Calendar):
    """
    ! Holidays for the Singapore exchange
            (data from
             <http://www.sgx.com/wps/portal/sgxweb/home/trading/securities/trading_hours_calendar>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's day, January 1st</li>
            <li>Good Friday</li>
            <li>Labour Day, May 1st</li>
            <li>National Day, August 9th</li>
            <li>Christmas, December 25th </li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2004-2010, 2012-2014, 2019-2024 only:)
            <ul>
            <li>Chinese New Year</li>
            <li>Hari Raya Haji</li>
            <li>Vesak Poya Day</li>
            <li>Deepavali</li>
            <li>Diwali</li>
            <li>Hari Raya Puasa</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          SGX : !< Singapore exchange
        """
        SGX: typing.ClassVar[Singapore.Market]  # value = <Market.SGX: 0>
        __members__: typing.ClassVar[dict[str, Singapore.Market]]  # value = {'SGX': <Market.SGX: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    SGX: typing.ClassVar[Singapore.Market]  # value = <Market.SGX: 0>
    def __init__(self, m: Singapore.Market = ...) -> None:
        ...
class Slovakia(Calendar):
    """
    ! Holidays for the Bratislava stock exchange
            (data from <http://www.bsse.sk/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>May Day, May 1st</li>
            <li>Liberation of the Republic, May 8th</li>
            <li>SS. Cyril and Methodius, July 5th</li>
            <li>Slovak National Uprising, August 29th</li>
            <li>Constitution of the Slovak Republic, September 1st</li>
            <li>Our Lady of the Seven Sorrows, September 15th</li>
            <li>All Saints Day, November 1st</li>
            <li>Freedom and Democracy of the Slovak Republic, November 17th</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          BSSE : !< Bratislava stock exchange
        """
        BSSE: typing.ClassVar[Slovakia.Market]  # value = <Market.BSSE: 0>
        __members__: typing.ClassVar[dict[str, Slovakia.Market]]  # value = {'BSSE': <Market.BSSE: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BSSE: typing.ClassVar[Slovakia.Market]  # value = <Market.BSSE: 0>
    def __init__(self, m: Slovakia.Market = ...) -> None:
        ...
class Sofr(OvernightIndex):
    """
    Secured Overnight Financing Rate (SOFR) index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs SOFR without forwarding curve.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs SOFR with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        """
        Constructs SOFR with forwarding term structure.
        """
class Sonia(OvernightIndex):
    """
    Sterling Overnight Index Average (SONIA) rate.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs SONIA without forwarding curve.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs SONIA with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, forwardingTermStructure: ...) -> None:
        """
        Constructs SONIA with forwarding term structure.
        """
class SouthAfrica(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Family Day, Easter Monday</li>
            <li>Human Rights Day, March 21st (possibly moved to Monday)</li>
            <li>Freedom Day, April 27th (possibly moved to Monday)</li>
            <li>Workers Day, May 1st (possibly moved to Monday)</li>
            <li>Youth Day, June 16th (possibly moved to Monday)</li>
            <li>National Women's Day, August 9th
            (possibly moved to Monday)</li>
            <li>Heritage Day, September 24th (possibly moved to Monday)</li>
            <li>Day of Reconciliation, December 16th
            (possibly moved to Monday)</li>
            <li>Christmas, December 25th </li>
            <li>Day of Goodwill, December 26th (possibly moved to Monday)</li>
            <li>Election Days</li>
            </ul>
    
            Note that there are some one-off holidays not listed above.
            See the implementation for the complete list.
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class SouthKorea(Calendar):
    """
    ! Public holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Independence Day, March 1st</li>
            <li>Arbour Day, April 5th (until 2005)</li>
            <li>Labour Day, May 1st</li>
            <li>Children's Day, May 5th</li>
            <li>Memorial Day, June 6th</li>
            <li>Constitution Day, July 17th (until 2007)</li>
            <li>Liberation Day, August 15th</li>
            <li>National Fondation Day, October 3th</li>
            <li>Hangeul Day, October 9th (from 2013)</li>
            <li>Christmas Day, December 25th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2004-2050 only:)
            <ul>
            <li>Lunar New Year, the last day of the previous lunar year</li>
            <li>Election Days</li>
            <li>National Assemblies</li>
            <li>Presidency</li>
            <li>Regional Election Days</li>
            <li>Buddha's birthday</li>
            <li>Harvest Moon Day</li>
            </ul>
    
            Holidays for the Korea exchange
            (data from
            <http://eng.krx.co.kr/> or
            <http://www.dooriworld.com/daishin/holiday/holiday.html>
            <https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B4%80%EA%B3%B5%EC%84%9C%EC%9D%98%20%EA%B3%B5%ED%9C%B4%EC%9D%BC%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B7%9C%EC%A0%95>):
            <ul>
            <li>Public holidays as listed above</li>
            <li>Year-end closing</li>
            <li>Occasional closing days</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          Settlement : !< Public holidays
        
          KRX : !< Korea exchange
        """
        KRX: typing.ClassVar[SouthKorea.Market]  # value = <Market.KRX: 1>
        Settlement: typing.ClassVar[SouthKorea.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, SouthKorea.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'KRX': <Market.KRX: 1>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    KRX: typing.ClassVar[SouthKorea.Market]  # value = <Market.KRX: 1>
    Settlement: typing.ClassVar[SouthKorea.Market]  # value = <Market.Settlement: 0>
    def __init__(self, m: SouthKorea.Market = ...) -> None:
        ...
class SpreadBasketPayoff(base.BasketPayoff):
    """
    Payoff based on spread between two assets.
    """
    def __init__(self, basePayoff: base.Payoff) -> None:
        """
        Constructs with base payoff.
        """
class SpreadCdsHelper(base.DefaultProbabilityHelper):
    """
    Spread-quoted CDS bootstrap helper.
    """
    @typing.overload
    def __init__(self, runningSpread: typing.SupportsFloat, tenor: Period, settlementDays: typing.SupportsInt, calendar: Calendar, frequency: Frequency, paymentConvention: BusinessDayConvention, rule: DateGeneration.Rule, dayCounter: DayCounter, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, startDate: Date = ..., lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, model: CdsPricingModel = ...) -> None:
        """
        Constructs from running spread.
        """
    @typing.overload
    def __init__(self, runningSpread: QuoteHandle, tenor: Period, settlementDays: typing.SupportsInt, calendar: Calendar, frequency: Frequency, paymentConvention: BusinessDayConvention, rule: DateGeneration.Rule, dayCounter: DayCounter, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, startDate: Date = ..., lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, model: CdsPricingModel = ...) -> None:
        """
        Constructs from running spread quote.
        """
class SpreadFittingMethod(base.FittingMethod):
    """
    Spread fitting method over a reference curve.
    """
    @typing.overload
    def __init__(self, method: base.FittingMethod, discountCurve: YieldTermStructureHandle, minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308) -> None:
        """
        Constructs with a discount curve handle.
        """
    @typing.overload
    def __init__(self, method: base.FittingMethod, discountCurve: typing.Any, minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308) -> None:
        """
        Constructs with a discount curve (handle created internally).
        """
class StochasticProcessArray(base.StochasticProcess):
    """
    Array of correlated 1-D stochastic processes.
    """
    def __init__(self, processes: collections.abc.Sequence[base.StochasticProcess1D], correlation: Matrix) -> None:
        """
        Constructs from a list of 1D processes and correlation matrix.
        """
    def correlation(self) -> Matrix:
        """
        Returns the correlation matrix.
        """
    def covariance(self, t0: typing.SupportsFloat, x0: Array, dt: typing.SupportsFloat) -> Matrix:
        """
        Returns the covariance matrix.
        """
    def diffusion(self, t: typing.SupportsFloat, x: Array) -> Matrix:
        """
        Returns the diffusion matrix at time t and state x.
        """
    def drift(self, t: typing.SupportsFloat, x: Array) -> Array:
        """
        Returns the drift at time t and state x.
        """
    def evolve(self, t0: typing.SupportsFloat, x0: Array, dt: typing.SupportsFloat, dw: Array) -> Array:
        """
        Returns the asset value after a time interval.
        """
    def expectation(self, t0: typing.SupportsFloat, x0: Array, dt: typing.SupportsFloat) -> Array:
        """
        Returns the expectation of the process.
        """
    def initialValues(self) -> Array:
        """
        Returns the initial values of all processes.
        """
    def process(self, i: typing.SupportsInt) -> base.StochasticProcess1D:
        """
        Returns the i-th process.
        """
    def size(self) -> int:
        """
        Returns the number of processes.
        """
    def stdDeviation(self, t0: typing.SupportsFloat, x0: Array, dt: typing.SupportsFloat) -> Matrix:
        """
        Returns the standard deviation matrix.
        """
class StrippedOptionletAdapter(base.OptionletVolatilityStructure, base.LazyObject):
    """
    Adapts stripped optionlet data into an OptionletVolatilityStructure.
    """
    def __init__(self, optionletStripper: base.StrippedOptionletBase) -> None:
        """
        Constructs from a StrippedOptionletBase.
        """
    def displacement(self) -> float:
        """
        Returns the displacement for shifted lognormal volatilities.
        """
    def maxDate(self) -> Date:
        """
        Returns the maximum date.
        """
    def maxStrike(self) -> float:
        """
        Returns the maximum strike.
        """
    def minStrike(self) -> float:
        """
        Returns the minimum strike.
        """
    def volatilityType(self) -> VolatilityType:
        """
        Returns the volatility type.
        """
class StulzEngine(BasketOptionEngine):
    """
    Stulz analytical engine for 2D min/max European basket options.
    """
    def __init__(self, process1: GeneralizedBlackScholesProcess, process2: GeneralizedBlackScholesProcess, correlation: typing.SupportsFloat) -> None:
        """
        Constructs with two Black-Scholes processes and correlation.
        """
class SuperFundPayoff(base.StrikedTypePayoff):
    """
    Binary superfund payoff between two strikes (normalized by lower strike).
    """
    def __init__(self, strike: typing.SupportsFloat, secondStrike: typing.SupportsFloat) -> None:
        ...
    def secondStrike(self) -> float:
        """
        Returns the second strike.
        """
class SuperSharePayoff(base.StrikedTypePayoff):
    """
    Binary supershare payoff: fixed cash between two strikes.
    """
    def __init__(self, strike: typing.SupportsFloat, secondStrike: typing.SupportsFloat, cashPayoff: typing.SupportsFloat) -> None:
        ...
    def cashPayoff(self) -> float:
        """
        Returns the cash payoff amount.
        """
    def secondStrike(self) -> float:
        """
        Returns the second strike.
        """
class SvenssonFitting(base.FittingMethod):
    """
    Svensson fitting method.
    """
    def __init__(self, weights: Array = ..., optimizationMethod: base.OptimizationMethod = None, l2: Array = ..., minCutoffTime: typing.SupportsFloat = 0.0, maxCutoffTime: typing.SupportsFloat = 1.7976931348623157e+308, constraint: base.Constraint = ...) -> None:
        """
        Constructs a Svensson fitting method.
        """
class SviSmileSection(base.SmileSection):
    """
    Stochastic Volatility Inspired (SVI) smile section.
    
    The SVI total variance formula is:
      w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))
    where k = log(K/F) is the log-moneyness.
    
    Parameters (passed as vector [a, b, sigma, rho, m]):
      a: vertical translation (level)
      b: slope (must be >= 0)
      sigma: ATM curvature (must be > 0)
      rho: rotation (-1 < rho < 1)
      m: horizontal translation
    """
    @typing.overload
    def __init__(self, timeToExpiry: typing.SupportsFloat, forward: typing.SupportsFloat, sviParameters: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs from time to expiry, forward, and SVI parameters [a, b, sigma, rho, m].
        """
    @typing.overload
    def __init__(self, expiryDate: Date, forward: typing.SupportsFloat, sviParameters: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter = ...) -> None:
        """
        Constructs from expiry date, forward, SVI parameters [a, b, sigma, rho, m], and day counter.
        """
class Swap(base.Instrument):
    """
    Interest rate swap base class.
    """
    class engine(base.SwapGenericEngine):
        """
        Pricing engine for swaps.
        """
        def __init__(self) -> None:
            ...
    @typing.overload
    def __init__(self, firstLeg: collections.abc.Sequence[base.CashFlow], secondLeg: collections.abc.Sequence[base.CashFlow]) -> None:
        """
        Constructs swap from two legs. First leg is paid, second is received.
        """
    @typing.overload
    def __init__(self, legs: collections.abc.Sequence[collections.abc.Sequence[base.CashFlow]], payer: collections.abc.Sequence[bool]) -> None:
        """
        Constructs multi-leg swap.
        """
    def endDiscounts(self, j: typing.SupportsInt) -> float:
        """
        Returns the end discount factor for leg j.
        """
    def isExpired(self) -> bool:
        """
        Returns True if the swap has expired.
        """
    def leg(self, j: typing.SupportsInt) -> list[base.CashFlow]:
        """
        Returns leg j.
        """
    def legBPS(self, j: typing.SupportsInt) -> float:
        """
        Returns the BPS of leg j.
        """
    def legNPV(self, j: typing.SupportsInt) -> float:
        """
        Returns the NPV of leg j.
        """
    def legs(self) -> list[list[base.CashFlow]]:
        """
        Returns all legs.
        """
    def maturityDate(self) -> Date:
        """
        Returns the maturity date.
        """
    def npvDateDiscount(self) -> float:
        """
        Returns the discount factor at the NPV date.
        """
    def numberOfLegs(self) -> int:
        """
        Returns the number of legs.
        """
    def payer(self, j: typing.SupportsInt) -> bool:
        """
        Returns True if leg j is paid.
        """
    def startDate(self) -> Date:
        """
        Returns the start date.
        """
    def startDiscounts(self, j: typing.SupportsInt) -> float:
        """
        Returns the start discount factor for leg j.
        """
class SwapArguments(base.PricingEngine.arguments):
    """
    Arguments for swap pricing.
    """
    def __init__(self) -> None:
        ...
    def validate(self) -> None:
        ...
    @property
    def legs(self) -> list[list[base.CashFlow]]:
        ...
    @legs.setter
    def legs(self, arg0: collections.abc.Sequence[collections.abc.Sequence[base.CashFlow]]) -> None:
        ...
    @property
    def payer(self) -> list[float]:
        ...
    @payer.setter
    def payer(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
class SwapIndex(base.InterestRateIndex):
    """
    Swap rate index.
    """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, fixedLegTenor: Period, fixedLegConvention: BusinessDayConvention, fixedLegDayCounter: DayCounter, iborIndex: IborIndex) -> None:
        """
        Constructs a swap index.
        """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, fixedLegTenor: Period, fixedLegConvention: BusinessDayConvention, fixedLegDayCounter: DayCounter, iborIndex: IborIndex, discountingTermStructure: ...) -> None:
        """
        Constructs a swap index with discounting term structure.
        """
    @typing.overload
    def __init__(self, familyName: str, tenor: Period, settlementDays: typing.SupportsInt, currency: Currency, fixingCalendar: Calendar, fixedLegTenor: Period, fixedLegConvention: BusinessDayConvention, fixedLegDayCounter: DayCounter, iborIndex: IborIndex, discountCurve: ...) -> None:
        """
        Constructs a swap index with discounting curve.
        """
    def discountingTermStructure(self) -> ...:
        """
        Returns the discounting term structure handle.
        """
    def exogenousDiscount(self) -> bool:
        """
        Returns true if using exogenous discounting.
        """
    def fixedLegConvention(self) -> BusinessDayConvention:
        """
        Returns the fixed leg business day convention.
        """
    def fixedLegTenor(self) -> Period:
        """
        Returns the fixed leg tenor.
        """
    def forwardingTermStructure(self) -> ...:
        """
        Returns the forwarding term structure handle.
        """
    def iborIndex(self) -> IborIndex:
        """
        Returns the IBOR index.
        """
    def underlyingSwap(self, fixingDate: Date) -> typing.Any:
        """
        Returns the underlying swap for a given fixing date.
        """
class SwapRateHelper(base.RelativeDateRateHelper):
    """
    Rate helper for bootstrapping over swap rates.
    """
    @typing.overload
    def __init__(self, rate: typing.SupportsFloat, tenor: Period, calendar: Calendar, fixedFrequency: Frequency, fixedConvention: BusinessDayConvention, fixedDayCount: DayCounter, iborIndex: IborIndex, spread: QuoteHandle = ..., fwdStart: Period = ..., discountingCurve: YieldTermStructureHandle = ..., settlementDays: typing.Any = None, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., endOfMonth: bool = False) -> None:
        """
        Constructs from rate, tenor, and market conventions.
        """
    @typing.overload
    def __init__(self, rate: QuoteHandle, tenor: Period, calendar: Calendar, fixedFrequency: Frequency, fixedConvention: BusinessDayConvention, fixedDayCount: DayCounter, iborIndex: IborIndex, spread: QuoteHandle = ..., fwdStart: Period = ..., discountingCurve: YieldTermStructureHandle = ..., settlementDays: typing.Any = None, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., endOfMonth: bool = False) -> None:
        """
        Constructs from quote handle, tenor, and market conventions.
        """
    @typing.overload
    def __init__(self, rate: base.Quote, tenor: Period, calendar: Calendar, fixedFrequency: Frequency, fixedConvention: BusinessDayConvention, fixedDayCount: DayCounter, iborIndex: IborIndex, spread: QuoteHandle = ..., fwdStart: Period = ..., discountingCurve: YieldTermStructureHandle = ..., settlementDays: typing.Any = None, pillar: Pillar.Choice = ..., customPillarDate: Date = ..., endOfMonth: bool = False) -> None:
        """
        Constructs from quote, tenor, and market conventions (handle created internally).
        """
    def forwardStart(self) -> Period:
        """
        Returns the forward start period.
        """
    def spread(self) -> float:
        """
        Returns the spread.
        """
    def swap(self) -> ...:
        """
        Returns the underlying swap.
        """
class SwapResults(base.Instrument.results):
    """
    Results from swap pricing.
    """
    def __init__(self) -> None:
        ...
    def reset(self) -> None:
        ...
    @property
    def endDiscounts(self) -> list[float]:
        ...
    @endDiscounts.setter
    def endDiscounts(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def legBPS(self) -> list[float]:
        ...
    @legBPS.setter
    def legBPS(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def legNPV(self) -> list[float]:
        ...
    @legNPV.setter
    def legNPV(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
    @property
    def npvDateDiscount(self) -> float:
        ...
    @npvDateDiscount.setter
    def npvDateDiscount(self, arg0: typing.SupportsFloat) -> None:
        ...
    @property
    def startDiscounts(self) -> list[float]:
        ...
    @startDiscounts.setter
    def startDiscounts(self, arg0: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        ...
class SwapType:
    """
    Swap type: Payer or Receiver.
    
    Members:
    
      Payer
    
      Receiver
    """
    Payer: typing.ClassVar[SwapType]  # value = <SwapType.Payer: 1>
    Receiver: typing.ClassVar[SwapType]  # value = <SwapType.Receiver: -1>
    __members__: typing.ClassVar[dict[str, SwapType]]  # value = {'Payer': <SwapType.Payer: 1>, 'Receiver': <SwapType.Receiver: -1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Swaption(base.Option):
    """
    Option to enter into an interest rate swap.
    """
    class engine(base.SwaptionGenericEngine):
        """
        Base class for swaption pricing engines.
        """
        def __init__(self) -> None:
            ...
    def __init__(self, swap: FixedVsFloatingSwap, exercise: Exercise, delivery: SettlementType = ..., settlementMethod: SettlementMethod = ...) -> None:
        """
        Constructs a swaption.
        """
    def impliedVolatility(self, price: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, guess: typing.SupportsFloat, accuracy: typing.SupportsFloat = 0.0001, maxEvaluations: typing.SupportsInt = 100, minVol: typing.SupportsFloat = 1e-07, maxVol: typing.SupportsFloat = 4.0, type: VolatilityType = ..., displacement: typing.SupportsFloat = 0.0, priceType: SwaptionPriceType = ...) -> float:
        """
        Returns the implied volatility.
        """
    def isExpired(self) -> bool:
        """
        Returns True if the swaption has expired.
        """
    def settlementMethod(self) -> SettlementMethod:
        """
        Returns the settlement method.
        """
    def settlementType(self) -> SettlementType:
        """
        Returns the settlement type.
        """
    def type(self) -> SwapType:
        """
        Returns the underlying swap type.
        """
    def underlying(self) -> FixedVsFloatingSwap:
        """
        Returns the underlying swap.
        """
class SwaptionArguments(FixedVsFloatingSwapArguments, base.Option.arguments):
    """
    Arguments for swaption pricing.
    """
    settlementMethod: SettlementMethod
    settlementType: SettlementType
    swap: FixedVsFloatingSwap
    def __init__(self) -> None:
        ...
    def validate(self) -> None:
        ...
class SwaptionHelper(base.BlackCalibrationHelper):
    """
    Calibration helper for interest-rate swaptions.
    """
    @typing.overload
    def __init__(self, maturity: Period, length: Period, volatility: QuoteHandle, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: YieldTermStructureHandle, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper with period maturity and length.
        """
    @typing.overload
    def __init__(self, maturity: Period, length: Period, volatility: base.Quote, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: base.YieldTermStructure, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper from period maturity and length.
        """
    @typing.overload
    def __init__(self, exerciseDate: Date, length: Period, volatility: QuoteHandle, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: YieldTermStructureHandle, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper with exercise date and swap length.
        """
    @typing.overload
    def __init__(self, exerciseDate: Date, length: Period, volatility: base.Quote, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: base.YieldTermStructure, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper from exercise date and swap length.
        """
    @typing.overload
    def __init__(self, exerciseDate: Date, endDate: Date, volatility: QuoteHandle, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: YieldTermStructureHandle, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper with exercise and end dates.
        """
    @typing.overload
    def __init__(self, exerciseDate: Date, endDate: Date, volatility: base.Quote, index: IborIndex, fixedLegTenor: Period, fixedLegDayCounter: DayCounter, floatingLegDayCounter: DayCounter, termStructure: base.YieldTermStructure, errorType: CalibrationErrorType = ..., strike: typing.SupportsFloat = ..., nominal: typing.SupportsFloat = 1.0, type: VolatilityType = ..., shift: typing.SupportsFloat = 0.0, settlementDays: typing.SupportsInt = ..., averagingMethod: RateAveraging.Type = ...) -> None:
        """
        Constructs swaption helper from exercise and end dates.
        """
    def blackPrice(self, volatility: typing.SupportsFloat) -> float:
        """
        Returns Black price for given volatility.
        """
    def modelValue(self) -> float:
        """
        Returns the model value.
        """
    def swaption(self) -> ...:
        """
        Returns the swaption instrument.
        """
    def underlying(self) -> ...:
        """
        Returns the underlying swap.
        """
class SwaptionPriceType:
    """
    Swaption price type for implied volatility.
    
    Members:
    
      Spot
    
      Forward
    """
    Forward: typing.ClassVar[SwaptionPriceType]  # value = <SwaptionPriceType.Forward: 1>
    Spot: typing.ClassVar[SwaptionPriceType]  # value = <SwaptionPriceType.Spot: 0>
    __members__: typing.ClassVar[dict[str, SwaptionPriceType]]  # value = {'Spot': <SwaptionPriceType.Spot: 0>, 'Forward': <SwaptionPriceType.Forward: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SwaptionVolatilityCube(base.SwaptionVolatilityDiscrete):
    """
    Abstract base for swaption volatility cubes with smile.
    """
    @typing.overload
    def atmStrike(self, optionDate: Date, swapTenor: Period) -> float:
        """
        Returns ATM strike for option date and swap tenor.
        """
    @typing.overload
    def atmStrike(self, optionTenor: Period, swapTenor: Period) -> float:
        """
        Returns ATM strike for option tenor and swap tenor.
        """
    def atmVol(self) -> SwaptionVolatilityStructureHandle:
        """
        Returns the ATM volatility structure handle.
        """
    def shortSwapIndexBase(self) -> SwapIndex:
        """
        Returns the short swap index base.
        """
    def strikeSpreads(self) -> list[float]:
        """
        Returns the strike spreads.
        """
    def swapIndexBase(self) -> SwapIndex:
        """
        Returns the swap index base.
        """
    def vegaWeightedSmileFit(self) -> bool:
        """
        Returns whether smile fit is vega-weighted.
        """
    def volSpreads(self) -> list[list[QuoteHandle]]:
        """
        Returns the volatility spread handles.
        """
class SwaptionVolatilityMatrix(base.SwaptionVolatilityDiscrete):
    """
    Discrete swaption volatility surface backed by a matrix.
    """
    @typing.overload
    def __init__(self, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], swapTenors: collections.abc.Sequence[Period], volatilities: Matrix, dayCounter: DayCounter, flatExtrapolation: bool = False, type: VolatilityType = ..., shifts: Matrix = ...) -> None:
        """
        Constructs from calendar with fixed volatility matrix.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], swapTenors: collections.abc.Sequence[Period], volatilities: Matrix, dayCounter: DayCounter, flatExtrapolation: bool = False, type: VolatilityType = ..., shifts: Matrix = ...) -> None:
        """
        Constructs from reference date with fixed volatility matrix.
        """
    @typing.overload
    def __init__(self, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], swapTenors: collections.abc.Sequence[Period], volatilities: collections.abc.Sequence[collections.abc.Sequence[QuoteHandle]], dayCounter: DayCounter, flatExtrapolation: bool = False, type: VolatilityType = ..., shifts: collections.abc.Sequence[collections.abc.Sequence[typing.SupportsFloat]] = []) -> None:
        """
        Constructs from calendar with quote handle matrix.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionTenors: collections.abc.Sequence[Period], swapTenors: collections.abc.Sequence[Period], volatilities: collections.abc.Sequence[collections.abc.Sequence[QuoteHandle]], dayCounter: DayCounter, flatExtrapolation: bool = False, type: VolatilityType = ..., shifts: collections.abc.Sequence[collections.abc.Sequence[typing.SupportsFloat]] = []) -> None:
        """
        Constructs from reference date with quote handle matrix.
        """
    @typing.overload
    def __init__(self, referenceDate: Date, calendar: Calendar, businessDayConvention: BusinessDayConvention, optionDates: collections.abc.Sequence[Date], swapTenors: collections.abc.Sequence[Period], volatilities: Matrix, dayCounter: DayCounter, flatExtrapolation: bool = False, type: VolatilityType = ..., shifts: Matrix = ...) -> None:
        """
        Constructs from reference date with option dates and matrix.
        """
    @typing.overload
    def locate(self, optionDate: Date, swapTenor: Period) -> tuple[int, int]:
        """
        Returns row/column index pair for given option date and swap tenor.
        """
    @typing.overload
    def locate(self, optionTime: typing.SupportsFloat, swapLength: typing.SupportsFloat) -> tuple[int, int]:
        """
        Returns row/column index pair for given option time and swap length.
        """
class SwaptionVolatilityStructureHandle:
    """
    Handle to SwaptionVolatilityStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: SwaptionVolatilityStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: SwaptionVolatilityStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: SwaptionVolatilityStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.SwaptionVolatilityStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.SwaptionVolatilityStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class Sweden(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Epiphany, January 6th</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Ascension</li>
            <li>Whit(Pentecost) Monday (until 2004)</li>
            <li>May Day, May 1st</li>
            <li>National Day, June 6th</li>
            <li>Midsummer Eve (Friday between June 19-25)</li>
            <li>Christmas Eve, December 24th</li>
            <li>Christmas Day, December 25th</li>
            <li>Boxing Day, December 26th</li>
            <li>New Year's Eve, December 31th</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class Switzerland(Calendar):
    """
    ! Holidays:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Berchtoldstag, January 2nd</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Ascension Day</li>
            <li>Whit Monday</li>
            <li>Labour Day, May 1st</li>
            <li>National Day, August 1st</li>
            <li>Christmas, December 25th</li>
            <li>St. Stephen's Day, December 26th</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class TARGET(Calendar):
    """
    ! Holidays (see http://www.ecb.int):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Good Friday (since 2000)</li>
            <li>Easter Monday (since 2000)</li>
            <li>Labour Day, May 1st (since 2000)</li>
            <li>Christmas, December 25th</li>
            <li>Day of Goodwill, December 26th (since 2000)</li>
            <li>December 31st (1998, 1999, and 2001)</li>
            </ul>
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested
                  against a list of known holidays.
    """
    def __init__(self) -> None:
        ...
class THBCurrency(Currency):
    """
    ! The ISO three-letter code is THB; the numeric code is 764.
            It is divided in 100 stang.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class TNDCurrency(Currency):
    """
    ! Tunisian dinar
    /*! The ISO three-letter code is TND; the numeric code is 788.
         It is divided into 1000 millim.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class TRLCurrency(Currency):
    """
    ! The ISO three-letter code was TRL; the numeric code was 792.
            It was divided in 100 kurus.
    
            Obsoleted by the new Turkish lira since 2005.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class TRYCurrency(Currency):
    """
    ! The ISO three-letter code is TRY; the numeric code is 949.
            It is divided in 100 new kurus.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class TTDCurrency(Currency):
    """
    ! The ISO three-letter code is TTD; the numeric code is 780.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class TWDCurrency(Currency):
    """
    ! The ISO three-letter code is TWD; the numeric code is 901.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class Taiwan(Calendar):
    """
    ! Holidays for the Taiwan stock exchange
            (data from <https://www.twse.com.tw/en/trading/holiday.html>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Peace Memorial Day, February 28</li>
            <li>Labor Day, May 1st</li>
            <li>Double Tenth National Day, October 10th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2002-2024 only:)
            <ul>
            <li>Chinese Lunar New Year</li>
            <li>Tomb Sweeping Day</li>
            <li>Dragon Boat Festival</li>
            <li>Moon Festival</li>
            </ul>
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          TSEC : !< Taiwan stock exchange
        """
        TSEC: typing.ClassVar[Taiwan.Market]  # value = <Market.TSEC: 0>
        __members__: typing.ClassVar[dict[str, Taiwan.Market]]  # value = {'TSEC': <Market.TSEC: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    TSEC: typing.ClassVar[Taiwan.Market]  # value = <Market.TSEC: 0>
    def __init__(self, m: Taiwan.Market = ...) -> None:
        ...
class Thailand(Calendar):
    """
    ! Holidays for the Thailand exchange
            Holidays observed by financial institutions (not to be confused with bank holidays in the United Kingdom) are regulated by the Bank of Thailand.
            If a holiday fall on a weekend the government will announce a replacement day (usually the following Monday).
    
            Sometimes the government add one or two extra holidays in a year.
    
            (data from
             https://www.bot.or.th/en/financial-institutions-holiday.html:
            Fixed holidays
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>Chakri Memorial Day, April 6th</li>
            <li>Songkran holiday, April 13th - 15th</li>
            <li>Labour Day, May 1st</li>
            <li>H.M. the King's Birthday, July 28th (from 2017)</li>
            <li>H.M. the Queen's Birthday, August 12th </li>
            <li>The Passing of H.M. the Late King Bhumibol Adulyadej (Rama IX), October 13th (from 2017) </li>
            <li>H.M. the Late King Bhumibol Adulyadej's Birthday, December 5th</li>
            <li>Constitution Day, December 10th</li>
            <li>New Year's Eve, December 31th</li>
            </ul>
    
            Other holidays for which no rule is given
            (data available for 2000-2024 with some years missing)
            <ul>
            <li>Makha Bucha Day</li>
            <li>Wisakha Bucha Day</li>
            <li>Buddhist Lent Day (until 2006)</li>
            <li>Asarnha Bucha Day (from 2007)</li>
            <li>Chulalongkorn Day</li>
            <li>Other special holidays</li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class Thirty360(DayCounter):
    """
    30/360 day count convention with various market variants (US, European, ISDA, etc.).
    """
    class Convention:
        """
        Members:
        
          USA
        
          BondBasis
        
          European
        
          EurobondBasis
        
          Italian
        
          German
        
          ISMA
        
          ISDA
        
          NASD
        """
        BondBasis: typing.ClassVar[Thirty360.Convention]  # value = <Convention.BondBasis: 1>
        EurobondBasis: typing.ClassVar[Thirty360.Convention]  # value = <Convention.EurobondBasis: 3>
        European: typing.ClassVar[Thirty360.Convention]  # value = <Convention.European: 2>
        German: typing.ClassVar[Thirty360.Convention]  # value = <Convention.German: 5>
        ISDA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.ISDA: 7>
        ISMA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.ISMA: 6>
        Italian: typing.ClassVar[Thirty360.Convention]  # value = <Convention.Italian: 4>
        NASD: typing.ClassVar[Thirty360.Convention]  # value = <Convention.NASD: 8>
        USA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.USA: 0>
        __members__: typing.ClassVar[dict[str, Thirty360.Convention]]  # value = {'USA': <Convention.USA: 0>, 'BondBasis': <Convention.BondBasis: 1>, 'European': <Convention.European: 2>, 'EurobondBasis': <Convention.EurobondBasis: 3>, 'Italian': <Convention.Italian: 4>, 'German': <Convention.German: 5>, 'ISMA': <Convention.ISMA: 6>, 'ISDA': <Convention.ISDA: 7>, 'NASD': <Convention.NASD: 8>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    BondBasis: typing.ClassVar[Thirty360.Convention]  # value = <Convention.BondBasis: 1>
    EurobondBasis: typing.ClassVar[Thirty360.Convention]  # value = <Convention.EurobondBasis: 3>
    European: typing.ClassVar[Thirty360.Convention]  # value = <Convention.European: 2>
    German: typing.ClassVar[Thirty360.Convention]  # value = <Convention.German: 5>
    ISDA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.ISDA: 7>
    ISMA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.ISMA: 6>
    Italian: typing.ClassVar[Thirty360.Convention]  # value = <Convention.Italian: 4>
    NASD: typing.ClassVar[Thirty360.Convention]  # value = <Convention.NASD: 8>
    USA: typing.ClassVar[Thirty360.Convention]  # value = <Convention.USA: 0>
    def __init__(self, arg0: Thirty360.Convention) -> None:
        ...
class Thirty365(DayCounter):
    """
    30/365 day count convention.
    """
    def __init__(self) -> None:
        ...
class TimeGrid:
    """
    Time grid for discretized models.
    """
    def __getitem__(self, i: typing.SupportsInt) -> float:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Default constructor.
        """
    @typing.overload
    def __init__(self, end: typing.SupportsFloat, steps: typing.SupportsInt) -> None:
        """
        Constructs a regularly spaced time grid.
        """
    @typing.overload
    def __init__(self, times: collections.abc.Sequence[typing.SupportsFloat]) -> None:
        """
        Constructs from mandatory time points.
        """
    @typing.overload
    def __init__(self, times: collections.abc.Sequence[typing.SupportsFloat], steps: typing.SupportsInt) -> None:
        """
        Constructs from mandatory time points with minimum steps.
        """
    def __iter__(self) -> collections.abc.Iterator[float]:
        ...
    def __len__(self) -> int:
        ...
    def at(self, i: typing.SupportsInt) -> float:
        """
        Returns the time at index i with bounds checking.
        """
    def back(self) -> float:
        """
        Returns the last time.
        """
    def closestIndex(self, t: typing.SupportsFloat) -> int:
        """
        Returns the index of the time closest to t.
        """
    def closestTime(self, t: typing.SupportsFloat) -> float:
        """
        Returns the time on the grid closest to t.
        """
    def dt(self, i: typing.SupportsInt) -> float:
        """
        Returns the time step dt(i) = t(i+1) - t(i).
        """
    def empty(self) -> bool:
        """
        Returns true if the grid is empty.
        """
    def front(self) -> float:
        """
        Returns the first time (t=0).
        """
    def index(self, t: typing.SupportsFloat) -> int:
        """
        Returns the index i such that grid[i] = t.
        """
    def mandatoryTimes(self) -> list[float]:
        """
        Returns the mandatory time points.
        """
    def size(self) -> int:
        """
        Returns the number of time points.
        """
class TimeUnit:
    """
    Units used to describe time periods.
    
    Members:
    
      Days
    
      Weeks
    
      Months
    
      Years
    
      Hours
    
      Minutes
    
      Seconds
    
      Milliseconds
    
      Microseconds
    """
    Days: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Days: 0>
    Hours: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Hours: 4>
    Microseconds: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Microseconds: 8>
    Milliseconds: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Milliseconds: 7>
    Minutes: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Minutes: 5>
    Months: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Months: 2>
    Seconds: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Seconds: 6>
    Weeks: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Weeks: 1>
    Years: typing.ClassVar[TimeUnit]  # value = <TimeUnit.Years: 3>
    __members__: typing.ClassVar[dict[str, TimeUnit]]  # value = {'Days': <TimeUnit.Days: 0>, 'Weeks': <TimeUnit.Weeks: 1>, 'Months': <TimeUnit.Months: 2>, 'Years': <TimeUnit.Years: 3>, 'Hours': <TimeUnit.Hours: 4>, 'Minutes': <TimeUnit.Minutes: 5>, 'Seconds': <TimeUnit.Seconds: 6>, 'Milliseconds': <TimeUnit.Milliseconds: 7>, 'Microseconds': <TimeUnit.Microseconds: 8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TreeSwaptionEngine(base.PricingEngine):
    """
    Numerical lattice engine for swaptions.
    """
    @typing.overload
    def __init__(self, model: base.ShortRateModel, timeSteps: typing.SupportsInt, termStructure: YieldTermStructureHandle = ...) -> None:
        """
        Constructs tree engine with model and time steps.
        """
    @typing.overload
    def __init__(self, model: base.ShortRateModel, timeGrid: TimeGrid, termStructure: YieldTermStructureHandle = ...) -> None:
        """
        Constructs tree engine with model and time grid.
        """
    @typing.overload
    def __init__(self, model: ShortRateModelHandle, timeSteps: typing.SupportsInt, termStructure: YieldTermStructureHandle = ...) -> None:
        """
        Constructs tree engine with model handle and time steps.
        """
    @typing.overload
    def __init__(self, model: base.ShortRateModel, timeSteps: typing.SupportsInt, termStructure: base.YieldTermStructure) -> None:
        """
        Constructs tree engine with model, time steps, and term structure.
        """
class Turkey(Calendar):
    """
    ! Holidays for the Istanbul Stock Exchange:
            (data from
             <https://borsaistanbul.com/en/sayfa/3631/official-holidays>
    		 and
    		 <https://feiertagskalender.ch/index.php?geo=3539&hl=en>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>National Sovereignty and Children�s Day, April 23rd</li>
            <li>Labour and Solidarity Day, May 1st</li>
            <li>Youth and Sports Day, May 19th</li>
            <li>Democracy and National Unity Day, July 15th</li>
            <li>Victory Day, August 30th</li>
            <li>Republic Day, October 29th</li>
            <li>Local Holidays (Kurban, Ramadan - dates need further validation for >= 2024) </li>
            </ul>
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class TurnbullWakemanAsianEngine(base.PricingEngine):
    """
    Turnbull-Wakeman moment-matching discrete arithmetic Asian engine.
    """
    def __init__(self, process: GeneralizedBlackScholesProcess) -> None:
        """
        Constructs TurnbullWakemanAsianEngine.
        """
class UAHCurrency(Currency):
    """
    ! The ISO three-letter code is UAH; the numeric code is 980.
            It is divided in 100 kopiykas.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class UGXCurrency(Currency):
    """
    ! Ugandan shilling
    /*! The ISO three-letter code is UGX; the numeric code is 800.
        It is the smallest unit.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class UKRPI(ZeroInflationIndex):
    """
    UK Retail Prices Index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs UKRPI without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs UKRPI with a term structure handle.
        """
    @typing.overload
    def __init__(self, zeroInflationTermStructure: ...) -> None:
        """
        Constructs UKRPI with a term structure.
        """
class UKRegion(Region):
    """
    United Kingdom region.
    """
    def __init__(self) -> None:
        ...
class USCPI(ZeroInflationIndex):
    """
    US Consumer Price Index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs USCPI without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs USCPI with a term structure handle.
        """
    @typing.overload
    def __init__(self, zeroInflationTermStructure: ...) -> None:
        """
        Constructs USCPI with a term structure.
        """
class USDCurrency(Currency):
    """
    ! The ISO three-letter code is USD; the numeric code is 840.
            It is divided in 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class USRegion(Region):
    """
    United States region.
    """
    def __init__(self) -> None:
        ...
class UYUCurrency(Currency):
    """
    ! Uruguayan peso
    /*! The ISO three-letter code is UYU; the numeric code is 858.
         A unit of account used in Uruguay.
         \\ingroup currencies
         */
    """
    def __init__(self) -> None:
        ...
class Ukraine(Calendar):
    """
    ! Holidays for the Ukrainian stock exchange
            (data from <http://www.ukrse.kiev.ua/eng/>):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st</li>
            <li>Orthodox Christmas, January 7th</li>
            <li>International Women's Day, March 8th</li>
            <li>Easter Monday</li>
            <li>Holy Trinity Day, 50 days after Easter</li>
            <li>International Workers' Solidarity Days, May 1st and 2nd</li>
            <li>Victory Day, May 9th</li>
            <li>Constitution Day, June 28th</li>
            <li>Independence Day, August 24th</li>
            <li>Defender's Day, October 14th (since 2015)</li>
            </ul>
            Holidays falling on a Saturday or Sunday might be moved to the
            following Monday.
    
            \\ingroup calendars
    """
    class Market:
        """
        
        
        Members:
        
          USE : !< Ukrainian stock exchange
        """
        USE: typing.ClassVar[Ukraine.Market]  # value = <Market.USE: 0>
        __members__: typing.ClassVar[dict[str, Ukraine.Market]]  # value = {'USE': <Market.USE: 0>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    USE: typing.ClassVar[Ukraine.Market]  # value = <Market.USE: 0>
    def __init__(self, m: Ukraine.Market = ...) -> None:
        ...
class UnitedKingdom(Calendar):
    """
    ! Repeating Public holidays (data from https://www.gov.uk/bank-holidays):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Early May Bank Holiday, first Monday of May</li>
            <li>Spring Bank Holiday, last Monday of May</li>
            <li>Summer Bank Holiday, last Monday of August</li>
            <li>Christmas Day, December 25th (possibly moved to Monday or
                Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            </ul>
    
            Holidays for the stock exchange:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Early May Bank Holiday, first Monday of May</li>
            <li>Spring Bank Holiday, last Monday of May</li>
            <li>Summer Bank Holiday, last Monday of August</li>
            <li>Christmas Day, December 25th (possibly moved to Monday or
                Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            </ul>
    
            Holidays for the metals exchange:
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday)</li>
            <li>Good Friday</li>
            <li>Easter Monday</li>
            <li>Early May Bank Holiday, first Monday of May</li>
            <li>Spring Bank Holiday, last Monday of May</li>
            <li>Summer Bank Holiday, last Monday of August</li>
            <li>Christmas Day, December 25th (possibly moved to Monday or
                Tuesday)</li>
            <li>Boxing Day, December 26th (possibly moved to Monday or
                Tuesday)</li>
            </ul>
    
            Note that there are some one-off holidays not listed above.
            See the implementation for the complete list.
    
            \\ingroup calendars
    
            	odo add LIFFE
    
            	est the correctness of the returned results is tested
                  against a list of known holidays.
    """
    class Market:
        """
        ! UK calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          Exchange : !< London stock-exchange calendar
        
          Metals : |< London metals-exchange calendar
        """
        Exchange: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Exchange: 1>
        Metals: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Metals: 2>
        Settlement: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, UnitedKingdom.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'Exchange': <Market.Exchange: 1>, 'Metals': <Market.Metals: 2>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    Exchange: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Exchange: 1>
    Metals: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Metals: 2>
    Settlement: typing.ClassVar[UnitedKingdom.Market]  # value = <Market.Settlement: 0>
    def __init__(self, market: UnitedKingdom.Market = ...) -> None:
        ...
class UnitedStates(Calendar):
    """
    ! Public holidays (see https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday if
                actually on Sunday, or to Friday if on Saturday)</li>
            <li>Martin Luther King's birthday, third Monday in January (since
                1983)</li>
            <li>Presidents' Day (a.k.a. Washington's birthday),
                third Monday in February</li>
            <li>Memorial Day, last Monday in May</li>
            <li>Juneteenth, June 19th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Independence Day, July 4th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Labor Day, first Monday in September</li>
            <li>Columbus Day, second Monday in October</li>
            <li>Veterans' Day, November 11th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Thanksgiving Day, fourth Thursday in November</li>
            <li>Christmas, December 25th (moved to Monday if Sunday or Friday
                if Saturday)</li>
            </ul>
    
            Note that since 2015 Independence Day only impacts Libor if it
            falls on a  weekday (see <https://www.theice.com/iba/libor>,
            <https://www.theice.com/marketdata/reports/170> and
            <https://www.theice.com/publicdocs/LIBOR_Holiday_Calendar_2015.pdf>
            for the fixing and value date calendars).
    
            Holidays for the stock exchange (data from http://www.nyse.com):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday if
                actually on Sunday)</li>
            <li>Martin Luther King's birthday, third Monday in January (since
                1998)</li>
            <li>Presidents' Day (a.k.a. Washington's birthday),
                third Monday in February</li>
            <li>Good Friday</li>
            <li>Memorial Day, last Monday in May</li>
            <li>Independence Day, July 4th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Labor Day, first Monday in September</li>
            <li>Thanksgiving Day, fourth Thursday in November</li>
            <li>Presidential election day, first Tuesday in November of election
                years (until 1980)</li>
            <li>Christmas, December 25th (moved to Monday if Sunday or Friday
                if Saturday)</li>
            <li>Special historic closings (see
                http://www.nyse.com/pdfs/closings.pdf)</li>
            </ul>
    
            Holidays for the government bond market (data from
            http://www.bondmarkets.com):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday if
                actually on Sunday)</li>
            <li>Martin Luther King's birthday, third Monday in January (since
                1983)</li>
            <li>Presidents' Day (a.k.a. Washington's birthday),
                third Monday in February</li>
            <li>Good Friday</li>
            <li>Memorial Day, last Monday in May</li>
            <li>Independence Day, July 4th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Labor Day, first Monday in September</li>
            <li>Columbus Day, second Monday in October</li>
            <li>Veterans' Day, November 11th (moved to Monday if Sunday or
                Friday if Saturday)</li>
            <li>Thanksgiving Day, fourth Thursday in November</li>
            <li>Christmas, December 25th (moved to Monday if Sunday or Friday
                if Saturday)</li>
            </ul>
    
            Holidays for the North American Energy Reliability Council
            (data from http://www.nerc.com/~oc/offpeaks.html):
            <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday if
                actually on Sunday)</li>
            <li>Memorial Day, last Monday in May</li>
            <li>Independence Day, July 4th (moved to Monday if Sunday)</li>
            <li>Labor Day, first Monday in September</li>
            <li>Thanksgiving Day, fourth Thursday in November</li>
            <li>Christmas, December 25th (moved to Monday if Sunday)</li>
            </ul>
    
            Holidays for the Federal Reserve Bankwire System
            (data from https://www.federalreserve.gov/aboutthefed/k8.htm
            and https://www.frbservices.org/about/holiday-schedules):
             <ul>
            <li>Saturdays</li>
            <li>Sundays</li>
            <li>New Year's Day, January 1st (possibly moved to Monday if
                actually on Sunday)</li>
            <li>Martin Luther King's birthday, third Monday in January (since
                1983)</li>
            <li>Presidents' Day (a.k.a. Washington's birthday),
                third Monday in February</li>
            <li>Memorial Day, last Monday in May</li>
            <li>Juneteenth, June 19th (moved to Monday if Sunday)</li>
            <li>Independence Day, July 4th (moved to Monday if Sunday)</li>
            <li>Labor Day, first Monday in September</li>
            <li>Columbus Day, second Monday in October</li>
            <li>Veterans' Day, November 11th (moved to Monday if Sunday)</li>
            <li>Thanksgiving Day, fourth Thursday in November</li>
            <li>Christmas, December 25th (moved to Monday if Sunday)</li>
            </ul>
    
            \\ingroup calendars
    
            	est the correctness of the returned results is tested
                  against a list of known holidays.
    """
    class Market:
        """
        ! US calendars
        
        Members:
        
          Settlement : !< generic settlement calendar
        
          NYSE : !< New York stock exchange calendar
        
          GovernmentBond : !< government-bond calendar
        
          NERC : !< off-peak days for NERC
        
          LiborImpact : !< Libor impact calendar
        
          FederalReserve : !< Federal Reserve Bankwire System
        
          SOFR : !< SOFR fixing calendar
        """
        FederalReserve: typing.ClassVar[UnitedStates.Market]  # value = <Market.FederalReserve: 5>
        GovernmentBond: typing.ClassVar[UnitedStates.Market]  # value = <Market.GovernmentBond: 2>
        LiborImpact: typing.ClassVar[UnitedStates.Market]  # value = <Market.LiborImpact: 4>
        NERC: typing.ClassVar[UnitedStates.Market]  # value = <Market.NERC: 3>
        NYSE: typing.ClassVar[UnitedStates.Market]  # value = <Market.NYSE: 1>
        SOFR: typing.ClassVar[UnitedStates.Market]  # value = <Market.SOFR: 6>
        Settlement: typing.ClassVar[UnitedStates.Market]  # value = <Market.Settlement: 0>
        __members__: typing.ClassVar[dict[str, UnitedStates.Market]]  # value = {'Settlement': <Market.Settlement: 0>, 'NYSE': <Market.NYSE: 1>, 'GovernmentBond': <Market.GovernmentBond: 2>, 'NERC': <Market.NERC: 3>, 'LiborImpact': <Market.LiborImpact: 4>, 'FederalReserve': <Market.FederalReserve: 5>, 'SOFR': <Market.SOFR: 6>}
        def __and__(self, other: typing.Any) -> typing.Any:
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __ge__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __gt__(self, other: typing.Any) -> bool:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: typing.SupportsInt) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __invert__(self) -> typing.Any:
            ...
        def __le__(self, other: typing.Any) -> bool:
            ...
        def __lt__(self, other: typing.Any) -> bool:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __or__(self, other: typing.Any) -> typing.Any:
            ...
        def __rand__(self, other: typing.Any) -> typing.Any:
            ...
        def __repr__(self) -> str:
            ...
        def __ror__(self, other: typing.Any) -> typing.Any:
            ...
        def __rxor__(self, other: typing.Any) -> typing.Any:
            ...
        def __setstate__(self, state: typing.SupportsInt) -> None:
            ...
        def __str__(self) -> str:
            ...
        def __xor__(self, other: typing.Any) -> typing.Any:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    FederalReserve: typing.ClassVar[UnitedStates.Market]  # value = <Market.FederalReserve: 5>
    GovernmentBond: typing.ClassVar[UnitedStates.Market]  # value = <Market.GovernmentBond: 2>
    LiborImpact: typing.ClassVar[UnitedStates.Market]  # value = <Market.LiborImpact: 4>
    NERC: typing.ClassVar[UnitedStates.Market]  # value = <Market.NERC: 3>
    NYSE: typing.ClassVar[UnitedStates.Market]  # value = <Market.NYSE: 1>
    SOFR: typing.ClassVar[UnitedStates.Market]  # value = <Market.SOFR: 6>
    Settlement: typing.ClassVar[UnitedStates.Market]  # value = <Market.Settlement: 0>
    def __init__(self, market: UnitedStates.Market = ...) -> None:
        ...
class UpRounding(Rounding):
    """
    Up-rounding.
    """
    def __init__(self, precision: typing.SupportsInt, digit: typing.SupportsInt = 5) -> None:
        ...
class UpfrontCdsHelper(base.DefaultProbabilityHelper):
    """
    Upfront-quoted CDS bootstrap helper.
    """
    @typing.overload
    def __init__(self, upfront: typing.SupportsFloat, runningSpread: typing.SupportsFloat, tenor: Period, settlementDays: typing.SupportsInt, calendar: Calendar, frequency: Frequency, paymentConvention: BusinessDayConvention, rule: DateGeneration.Rule, dayCounter: DayCounter, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, upfrontSettlementDays: typing.SupportsInt = 3, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, startDate: Date = ..., lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, model: CdsPricingModel = ...) -> None:
        """
        Constructs from upfront and running spread.
        """
    @typing.overload
    def __init__(self, upfront: QuoteHandle, runningSpread: typing.SupportsFloat, tenor: Period, settlementDays: typing.SupportsInt, calendar: Calendar, frequency: Frequency, paymentConvention: BusinessDayConvention, rule: DateGeneration.Rule, dayCounter: DayCounter, recoveryRate: typing.SupportsFloat, discountCurve: YieldTermStructureHandle, upfrontSettlementDays: typing.SupportsInt = 3, settlesAccrual: bool = True, paysAtDefaultTime: bool = True, startDate: Date = ..., lastPeriodDayCounter: typing.Any = None, rebatesAccrual: bool = True, model: CdsPricingModel = ...) -> None:
        """
        Constructs from upfront quote and running spread.
        """
class UsdLiborSwapIsdaFixAm(SwapIndex):
    """
    USD LIBOR swap rate (ISDA fix AM).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class UsdLiborSwapIsdaFixPm(SwapIndex):
    """
    USD LIBOR swap rate (ISDA fix PM).
    """
    @typing.overload
    def __init__(self, tenor: Period) -> None:
        """
        Constructs with given tenor.
        """
    @typing.overload
    def __init__(self, tenor: Period, h: ...) -> None:
        """
        Constructs with forwarding term structure handle.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwarding: ..., discounting: ...) -> None:
        """
        Constructs with forwarding and discounting term structure handles.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ...) -> None:
        """
        Constructs with forwarding term structure.
        """
    @typing.overload
    def __init__(self, tenor: Period, forwardingTermStructure: ..., discountingTermStructure: ...) -> None:
        """
        Constructs with forwarding and discounting term structures.
        """
class VEBCurrency(Currency):
    """
    ! The ISO three-letter code is VEB; the numeric code is 862.
            It is divided in 100 centimos.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class VNDCurrency(Currency):
    """
    ! The ISO three-letter code is VND; the numeric code is 704.
            It was divided in 100 xu.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class VanillaOption(base.OneAssetOption):
    """
    Plain vanilla option on a single asset.
    """
    def __init__(self, payoff: base.StrikedTypePayoff, exercise: Exercise) -> None:
        ...
class VanillaSwap(FixedVsFloatingSwap):
    """
    Plain vanilla swap: fixed vs IBOR floating leg.
    """
    def __init__(self, type: SwapType, nominal: typing.SupportsFloat, fixedSchedule: Schedule, fixedRate: typing.SupportsFloat, fixedDayCount: DayCounter, floatSchedule: Schedule, iborIndex: IborIndex, spread: typing.SupportsFloat, floatingDayCount: DayCounter, paymentConvention: pyquantlib._pyquantlib.BusinessDayConvention | None = None, useIndexedCoupons: bool | None = None) -> None:
        """
        Constructs a vanilla swap.
        """
class Vasicek(base.OneFactorAffineModel):
    """
    Vasicek short-rate model: dr = a(b - r)dt + sigma*dW.
    """
    def __init__(self, r0: typing.SupportsFloat = 0.05, a: typing.SupportsFloat = 0.1, b: typing.SupportsFloat = 0.05, sigma: typing.SupportsFloat = 0.01, lambda: typing.SupportsFloat = 0.0) -> None:
        """
        Constructs Vasicek model with initial rate, mean reversion, long-term rate, volatility, and risk premium.
        """
    def a(self) -> float:
        """
        Returns mean reversion speed.
        """
    def b(self) -> float:
        """
        Returns long-term mean rate.
        """
    def discountBondOption(self, type: OptionType, strike: typing.SupportsFloat, maturity: typing.SupportsFloat, bondMaturity: typing.SupportsFloat) -> float:
        """
        Returns discount bond option price.
        """
    def r0(self) -> float:
        """
        Returns initial short rate.
        """
    def sigma(self) -> float:
        """
        Returns volatility.
        """
    @property
    def lambda_(self) -> float:
        """
        Returns risk premium.
        """
class VolatilityType:
    """
    Volatility type for option pricing.
    
    Members:
    
      ShiftedLognormal : Shifted lognormal (Black) volatility.
    
      Normal : Normal (Bachelier) volatility.
    """
    Normal: typing.ClassVar[VolatilityType]  # value = <VolatilityType.Normal: 1>
    ShiftedLognormal: typing.ClassVar[VolatilityType]  # value = <VolatilityType.ShiftedLognormal: 0>
    __members__: typing.ClassVar[dict[str, VolatilityType]]  # value = {'ShiftedLognormal': <VolatilityType.ShiftedLognormal: 0>, 'Normal': <VolatilityType.Normal: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Weekday:
    """
    Days of the week enumeration.
    
    Members:
    
      Sunday
    
      Monday
    
      Tuesday
    
      Wednesday
    
      Thursday
    
      Friday
    
      Saturday
    
      Sun
    
      Mon
    
      Tue
    
      Wed
    
      Thu
    
      Fri
    
      Sat
    """
    Fri: typing.ClassVar[Weekday]  # value = <Weekday.Friday: 6>
    Friday: typing.ClassVar[Weekday]  # value = <Weekday.Friday: 6>
    Mon: typing.ClassVar[Weekday]  # value = <Weekday.Monday: 2>
    Monday: typing.ClassVar[Weekday]  # value = <Weekday.Monday: 2>
    Sat: typing.ClassVar[Weekday]  # value = <Weekday.Saturday: 7>
    Saturday: typing.ClassVar[Weekday]  # value = <Weekday.Saturday: 7>
    Sun: typing.ClassVar[Weekday]  # value = <Weekday.Sunday: 1>
    Sunday: typing.ClassVar[Weekday]  # value = <Weekday.Sunday: 1>
    Thu: typing.ClassVar[Weekday]  # value = <Weekday.Thursday: 5>
    Thursday: typing.ClassVar[Weekday]  # value = <Weekday.Thursday: 5>
    Tue: typing.ClassVar[Weekday]  # value = <Weekday.Tuesday: 3>
    Tuesday: typing.ClassVar[Weekday]  # value = <Weekday.Tuesday: 3>
    Wed: typing.ClassVar[Weekday]  # value = <Weekday.Wednesday: 4>
    Wednesday: typing.ClassVar[Weekday]  # value = <Weekday.Wednesday: 4>
    __members__: typing.ClassVar[dict[str, Weekday]]  # value = {'Sunday': <Weekday.Sunday: 1>, 'Monday': <Weekday.Monday: 2>, 'Tuesday': <Weekday.Tuesday: 3>, 'Wednesday': <Weekday.Wednesday: 4>, 'Thursday': <Weekday.Thursday: 5>, 'Friday': <Weekday.Friday: 6>, 'Saturday': <Weekday.Saturday: 7>, 'Sun': <Weekday.Sunday: 1>, 'Mon': <Weekday.Monday: 2>, 'Tue': <Weekday.Tuesday: 3>, 'Wed': <Weekday.Wednesday: 4>, 'Thu': <Weekday.Thursday: 5>, 'Fri': <Weekday.Friday: 6>, 'Sat': <Weekday.Saturday: 7>}
    def __and__(self, other: typing.Any) -> typing.Any:
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __ge__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __gt__(self, other: typing.Any) -> bool:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __invert__(self) -> typing.Any:
        ...
    def __le__(self, other: typing.Any) -> bool:
        ...
    def __lt__(self, other: typing.Any) -> bool:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __or__(self, other: typing.Any) -> typing.Any:
        ...
    def __rand__(self, other: typing.Any) -> typing.Any:
        ...
    def __repr__(self) -> str:
        ...
    def __ror__(self, other: typing.Any) -> typing.Any:
        ...
    def __rxor__(self, other: typing.Any) -> typing.Any:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __xor__(self, other: typing.Any) -> typing.Any:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class WeekendsOnly(Calendar):
    """
    ! This calendar has no bank holidays except for weekends
            (Saturdays and Sundays) as required by ISDA for calculating
            conventional CDS spreads.
    
            \\ingroup calendars
    """
    def __init__(self) -> None:
        ...
class XOFCurrency(Currency):
    """
     West African CFA franc
    /*! The ISO three-letter code is XOF; the numeric code is 952.
         It is divided into 100 centime.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class XRPCurrency(Currency):
    """
    ! https://ripple.com/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class YYEUHICP(YoYInflationIndex):
    """
    Year-on-year EU HICP.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs YYEUHICP without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs YYEUHICP with a term structure handle.
        """
    @typing.overload
    def __init__(self, yoyInflationTermStructure: ...) -> None:
        """
        Constructs YYEUHICP with a term structure.
        """
class YYEUHICPXT(YoYInflationIndex):
    """
    Year-on-year EU HICP Excluding Tobacco.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs YYEUHICPXT without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs YYEUHICPXT with a term structure handle.
        """
    @typing.overload
    def __init__(self, yoyInflationTermStructure: ...) -> None:
        """
        Constructs YYEUHICPXT with a term structure.
        """
class YYUKRPI(YoYInflationIndex):
    """
    Year-on-year UK Retail Prices Index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs YYUKRPI without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs YYUKRPI with a term structure handle.
        """
    @typing.overload
    def __init__(self, yoyInflationTermStructure: ...) -> None:
        """
        Constructs YYUKRPI with a term structure.
        """
class YYUSCPI(YoYInflationIndex):
    """
    Year-on-year US Consumer Price Index.
    """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs YYUSCPI without a term structure.
        """
    @typing.overload
    def __init__(self, h: ...) -> None:
        """
        Constructs YYUSCPI with a term structure handle.
        """
    @typing.overload
    def __init__(self, yoyInflationTermStructure: ...) -> None:
        """
        Constructs YYUSCPI with a term structure.
        """
class YieldTermStructureHandle:
    """
    Handle to YieldTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: YieldTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: YieldTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: YieldTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.YieldTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.YieldTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class YoYInflationIndex(base.InflationIndex):
    """
    Year-on-year inflation index.
    """
    @typing.overload
    def __init__(self, underlyingIndex: ZeroInflationIndex) -> None:
        """
        Constructs a year-on-year index as a ratio of a zero index.
        """
    @typing.overload
    def __init__(self, underlyingIndex: ZeroInflationIndex, h: ...) -> None:
        """
        Constructs a year-on-year index with term structure handle.
        """
    @typing.overload
    def __init__(self, underlyingIndex: ZeroInflationIndex, yoyInflationTermStructure: ...) -> None:
        """
        Constructs a year-on-year index with term structure.
        """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency) -> None:
        """
        Constructs a quoted year-on-year index without a term structure.
        """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency, h: ...) -> None:
        """
        Constructs a quoted year-on-year index with term structure handle.
        """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency, yoyInflationTermStructure: ...) -> None:
        """
        Constructs a quoted year-on-year index with term structure.
        """
    def clone(self, h: ...) -> YoYInflationIndex:
        """
        Returns a copy linked to a different term structure.
        """
    def interpolated(self) -> bool:
        """
        Returns true if the index interpolates between fixings.
        """
    def lastFixingDate(self) -> Date:
        """
        Returns the last available fixing date.
        """
    def ratio(self) -> bool:
        """
        Returns true if index is defined as a ratio of zero index fixings.
        """
    def underlyingIndex(self) -> ZeroInflationIndex:
        """
        Returns the underlying zero inflation index (if ratio-based).
        """
    def yoyInflationTermStructure(self) -> ...:
        """
        Returns the YoY inflation term structure handle.
        """
class YoYInflationTermStructureHandle:
    """
    Handle to YoYInflationTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: YoYInflationTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: YoYInflationTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: YoYInflationTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.YoYInflationTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.YoYInflationTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class ZARCurrency(Currency):
    """
    ! The ISO three-letter code is ZAR; the numeric code is 710.
            It is divided into 100 cents.
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ZARegion(Region):
    """
    South Africa region.
    """
    def __init__(self) -> None:
        ...
class ZECCurrency(Currency):
    """
    ! https://z.cash/
    
            \\ingroup currencies
    """
    def __init__(self) -> None:
        ...
class ZMWCurrency(Currency):
    """
    ! Zambian kwacha
    /*! The ISO three-letter code is ZMW; the numeric code is 967.
        It is divided into 100 ngwee.
         \\ingroup currencies
        */
    """
    def __init__(self) -> None:
        ...
class ZeroCouponBond(Bond):
    """
    Zero coupon bond.
    """
    def __init__(self, settlementDays: typing.SupportsInt, calendar: Calendar, faceAmount: typing.SupportsFloat, maturityDate: Date, paymentConvention: BusinessDayConvention = ..., redemption: typing.SupportsFloat = 100.0, issueDate: Date = ...) -> None:
        """
        Constructs a zero coupon bond.
        """
class ZeroCouponSwap(Swap):
    """
    Zero-coupon interest rate swap.
    """
    @typing.overload
    def __init__(self, type: SwapType, baseNominal: typing.SupportsFloat, startDate: Date, maturityDate: Date, fixedPayment: typing.SupportsFloat, iborIndex: IborIndex, paymentCalendar: Calendar, paymentConvention: BusinessDayConvention = ..., paymentDelay: typing.SupportsInt = 0) -> None:
        """
        Constructs from fixed payment amount.
        """
    @typing.overload
    def __init__(self, type: SwapType, baseNominal: typing.SupportsFloat, startDate: Date, maturityDate: Date, fixedRate: typing.SupportsFloat, fixedDayCounter: DayCounter, iborIndex: IborIndex, paymentCalendar: Calendar, paymentConvention: BusinessDayConvention = ..., paymentDelay: typing.SupportsInt = 0) -> None:
        """
        Constructs from fixed rate.
        """
    def baseNominal(self) -> float:
        """
        Base notional amount.
        """
    def fairFixedPayment(self) -> float:
        """
        Fair fixed payment amount.
        """
    def fairFixedRate(self, dayCounter: DayCounter) -> float:
        """
        Fair fixed rate for a given day counter.
        """
    def fixedLeg(self) -> list[base.CashFlow]:
        """
        Fixed leg.
        """
    def fixedLegNPV(self) -> float:
        """
        NPV of the fixed leg.
        """
    def fixedPayment(self) -> float:
        """
        Fixed payment amount.
        """
    def floatingLeg(self) -> list[base.CashFlow]:
        """
        Floating leg.
        """
    def floatingLegNPV(self) -> float:
        """
        NPV of the floating leg.
        """
    def iborIndex(self) -> IborIndex:
        """
        Ibor index.
        """
    def maturityDate(self) -> Date:
        """
        Maturity date.
        """
    def startDate(self) -> Date:
        """
        Start date.
        """
    def type(self) -> SwapType:
        """
        Swap type (payer or receiver).
        """
class ZeroCurve(base.YieldTermStructure):
    """
    Yield curve based on zero rates with linear interpolation.
    """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], yields: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from dates, yields, and day counter.
        """
    @typing.overload
    def __init__(self, dates: collections.abc.Sequence[Date], yields: collections.abc.Sequence[typing.SupportsFloat], dayCounter: DayCounter, calendar: Calendar, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from dates, yields, day counter, and calendar.
        """
    def data(self) -> list[float]:
        """
        Returns the zero rates.
        """
    def dates(self) -> list[Date]:
        """
        Returns the curve dates.
        """
    def nodes(self) -> list[tuple[Date, float]]:
        """
        Returns the (date, rate) pairs.
        """
    def times(self) -> list[float]:
        """
        Returns the curve times.
        """
    def zeroRates(self) -> list[float]:
        """
        Returns the zero rates.
        """
class ZeroInflationIndex(base.InflationIndex):
    """
    Zero-coupon inflation index.
    """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency) -> None:
        """
        Constructs a zero inflation index without a term structure.
        """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency, h: ...) -> None:
        """
        Constructs a zero inflation index with term structure handle.
        """
    @typing.overload
    def __init__(self, familyName: str, region: Region, revised: bool, frequency: Frequency, availabilityLag: Period, currency: Currency, zeroInflationTermStructure: ...) -> None:
        """
        Constructs a zero inflation index with term structure.
        """
    def clone(self, h: ...) -> ZeroInflationIndex:
        """
        Returns a copy linked to a different term structure.
        """
    def lastFixingDate(self) -> Date:
        """
        Returns the last available fixing date.
        """
    def zeroInflationTermStructure(self) -> ...:
        """
        Returns the zero inflation term structure handle.
        """
class ZeroInflationTermStructureHandle:
    """
    Handle to ZeroInflationTermStructure.
    """
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """
        Checks if the handle is non-empty.
        """
    def __eq__(self, arg0: ZeroInflationTermStructureHandle) -> bool:
        ...
    @typing.overload
    def __init__(self) -> None:
        """
        Creates an empty handle.
        """
    @typing.overload
    def __init__(self, ptr: typing.Any, registerAsObserver: bool = True) -> None:
        """
        Creates a handle linked to the given object.
        """
    def __lt__(self, arg0: ZeroInflationTermStructureHandle) -> bool:
        ...
    def __ne__(self, arg0: ZeroInflationTermStructureHandle) -> bool:
        ...
    def asObservable(self) -> Observable:
        """
        Converts to Observable for observer registration.
        """
    def currentLink(self) -> base.ZeroInflationTermStructure:
        """
        Returns the shared_ptr to the current object link.
        """
    def empty(self) -> bool:
        """
        Returns true if the handle is empty.
        """
    def get(self) -> base.ZeroInflationTermStructure:
        """
        Returns the underlying shared_ptr. Raises error if empty.
        """
class ZeroSpreadedTermStructure(base.YieldTermStructure):
    """
    Yield curve with an additive spread on zero rates.
    """
    @typing.overload
    def __init__(self, curveHandle: YieldTermStructureHandle, spreadHandle: QuoteHandle, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from yield curve and spread handles.
        """
    @typing.overload
    def __init__(self, curve: base.YieldTermStructure, spread: base.Quote, compounding: Compounding = ..., frequency: Frequency = ...) -> None:
        """
        Constructs from yield curve and spread (handles created internally).
        """
def Abs(array: Array) -> Array:
    """
    Returns element-wise absolute values.
    """
def BinomialVanillaEngine(process: GeneralizedBlackScholesProcess, treeType: str, timeSteps: typing.SupportsInt) -> base.PricingEngine:
    """
    Binomial tree pricing engine for vanilla options.
    
    Parameters:
      process: Black-Scholes process
      treeType: Tree type - one of:
        'jr' or 'jarrowrudd': Jarrow-Rudd
        'crr' or 'coxrossrubinstein': Cox-Ross-Rubinstein
        'eqp' or 'additiveeqp': Additive equal probabilities
        'trigeorgis': Trigeorgis
        'tian': Tian
        'lr' or 'leisenreimer': Leisen-Reimer
        'joshi' or 'joshi4': Joshi
      timeSteps: Number of time steps (minimum 2)
    """
def DotProduct(a1: Array, a2: Array) -> float:
    """
    Returns the dot product of two arrays.
    """
def Exp(array: Array) -> Array:
    """
    Returns element-wise exponentials.
    """
def Log(array: Array) -> Array:
    """
    Returns element-wise natural logarithms.
    """
def MCAmericanEngine(process: GeneralizedBlackScholesProcess, rngType: str = 'pseudorandom', timeSteps: typing.Any = None, timeStepsPerYear: typing.Any = None, antitheticVariate: bool = False, controlVariate: bool = False, requiredSamples: typing.Any = None, requiredTolerance: typing.Any = None, maxSamples: typing.Any = None, seed: typing.SupportsInt = 0, polynomialOrder: typing.SupportsInt = 2, polynomialType: PolynomialType = ..., calibrationSamples: typing.SupportsInt = 2048) -> base.PricingEngine:
    """
    Monte Carlo American option pricing engine (Longstaff-Schwartz).
    
    Parameters:
      process: Black-Scholes process
      rngType: 'pseudorandom' or 'lowdiscrepancy'
      timeSteps: Number of time steps
      timeStepsPerYear: Time steps per year (alternative to timeSteps)
      antitheticVariate: Use antithetic variates
      controlVariate: Use control variate (European option)
      requiredSamples: Number of samples
      requiredTolerance: Target tolerance (alternative to requiredSamples)
      maxSamples: Maximum samples
      seed: Random seed (0 for random)
      polynomialOrder: Order of regression polynomial
      polynomialType: Polynomial basis type (Monomial, Laguerre, etc.)
      calibrationSamples: Samples for regression calibration
    """
def MCDiscreteArithmeticAPEngine(process: GeneralizedBlackScholesProcess, rngType: str = 'pseudorandom', brownianBridge: bool = True, antitheticVariate: bool = False, controlVariate: bool = False, requiredSamples: typing.Any = None, requiredTolerance: typing.Any = None, maxSamples: typing.Any = None, seed: typing.SupportsInt = 0) -> base.PricingEngine:
    """
    Monte Carlo discrete arithmetic average price Asian engine.
    """
def MCEuropeanEngine(process: GeneralizedBlackScholesProcess, rngType: str = 'pseudorandom', timeSteps: typing.Any = None, timeStepsPerYear: typing.Any = None, brownianBridge: bool = False, antitheticVariate: bool = False, requiredSamples: typing.Any = None, requiredTolerance: typing.Any = None, maxSamples: typing.Any = None, seed: typing.SupportsInt = 0) -> base.PricingEngine:
    """
    Monte Carlo European option pricing engine.
    
    Parameters:
      process: Black-Scholes process
      rngType: 'pseudorandom' or 'lowdiscrepancy'
      timeSteps: Number of time steps
      timeStepsPerYear: Time steps per year (alternative to timeSteps)
      brownianBridge: Use Brownian bridge
      antitheticVariate: Use antithetic variates
      requiredSamples: Number of samples
      requiredTolerance: Target tolerance (alternative to requiredSamples)
      maxSamples: Maximum samples
      seed: Random seed (0 for random)
    """
def Pow(array: Array, exponent: typing.SupportsFloat) -> Array:
    """
    Returns element-wise power.
    """
def Sqrt(array: Array) -> Array:
    """
    Returns element-wise square roots.
    """
def bachelierBlackFormula(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0) -> float:
    """
    Bachelier (normal) formula. stdDev = absoluteVol * sqrt(T).
    """
def bachelierBlackFormulaImpliedVol(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, tte: typing.SupportsFloat, bachelierPrice: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0) -> float:
    """
    Bachelier implied volatility (exact, Jaeckel 2017).
    """
def bachelierBlackFormulaStdDevDerivative(strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0) -> float:
    """
    Bachelier formula derivative w.r.t. stdDev.
    """
def blackFormula(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Black 1976 formula. stdDev = volatility * sqrt(T).
    """
def blackFormulaAssetItmProbability(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Asset measure probability N(d1).
    """
def blackFormulaCashItmProbability(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Probability of finishing in the money N(d2).
    """
def blackFormulaForwardDerivative(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Black formula derivative w.r.t. forward.
    """
def blackFormulaImpliedStdDev(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, blackPrice: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0, guess: typing.SupportsFloat = ..., accuracy: typing.SupportsFloat = 1e-06, maxIterations: typing.SupportsInt = 100) -> float:
    """
    Black 1976 implied standard deviation (volatility * sqrt(T)).
    """
def blackFormulaImpliedStdDevApproximation(optionType: OptionType, strike: typing.SupportsFloat, forward: typing.SupportsFloat, blackPrice: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Approximated Black implied stdDev (Corrado-Miller).
    """
def blackFormulaStdDevDerivative(strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Black formula derivative w.r.t. stdDev. Vega = this * sqrt(T).
    """
def blackFormulaVolDerivative(strike: typing.SupportsFloat, forward: typing.SupportsFloat, stdDev: typing.SupportsFloat, expiry: typing.SupportsFloat, discount: typing.SupportsFloat = 1.0, displacement: typing.SupportsFloat = 0.0) -> float:
    """
    Black formula derivative w.r.t. implied vol (vega).
    """
def cdsMaturity(tradeDate: Date, tenor: Period, rule: DateGeneration.Rule) -> Date:
    """
    CDS maturity date from trade date and tenor.
    """
def checkSviParameters(a: typing.SupportsFloat, b: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, m: typing.SupportsFloat, tte: typing.SupportsFloat) -> None:
    """
    Validates SVI parameters for no-arbitrage conditions.
    
    Checks:
      - b >= 0
      - |rho| < 1
      - sigma > 0
      - a + b * sigma * sqrt(1 - rho^2) >= 0
      - b * (1 + |rho|) <= 4
    """
def close(m1: Money, m2: Money, n: typing.SupportsInt = 42) -> bool:
    """
    Returns true if the two amounts are close.
    """
def close_enough(m1: Money, m2: Money, n: typing.SupportsInt = 42) -> bool:
    """
    Returns true if the two amounts are close enough.
    """
def days(period: Period) -> float:
    """
    Convert a Period to days.
    """
def daysBetween(d1: Date, d2: Date) -> float:
    """
    Difference in days (including fraction) between dates.
    """
def inflationPeriod(date: Date, frequency: Frequency) -> tuple[Date, Date]:
    """
    Returns the start and end dates of the inflation period.
    """
def months(period: Period) -> float:
    """
    Convert a Period to months.
    """
def outerProduct(a1: Array, a2: Array) -> Matrix:
    """
    Returns the outer product of two arrays.
    """
def sabrVolatility(strike: typing.SupportsFloat, forward: typing.SupportsFloat, expiryTime: typing.SupportsFloat, alpha: typing.SupportsFloat, beta: typing.SupportsFloat, nu: typing.SupportsFloat, rho: typing.SupportsFloat, volatilityType: VolatilityType = ...) -> float:
    """
    Computes SABR implied volatility (with parameter validation).
    """
def setCouponPricer(leg: collections.abc.Sequence[base.CashFlow], pricer: base.FloatingRateCouponPricer) -> None:
    """
    Sets the coupon pricer for all floating-rate coupons in the leg.
    """
def shiftedSabrVolatility(strike: typing.SupportsFloat, forward: typing.SupportsFloat, expiryTime: typing.SupportsFloat, alpha: typing.SupportsFloat, beta: typing.SupportsFloat, nu: typing.SupportsFloat, rho: typing.SupportsFloat, shift: typing.SupportsFloat, volatilityType: VolatilityType = ...) -> float:
    """
    Computes shifted SABR implied volatility.
    """
def sviTotalVariance(a: typing.SupportsFloat, b: typing.SupportsFloat, sigma: typing.SupportsFloat, rho: typing.SupportsFloat, m: typing.SupportsFloat, k: typing.SupportsFloat) -> float:
    """
    Computes SVI total variance: a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2)).
    
    Arguments:
      a: vertical translation
      b: slope
      sigma: ATM curvature
      rho: rotation
      m: horizontal translation
      k: log-moneyness (log(K/F))
    """
def transpose(matrix: Matrix) -> Matrix:
    """
    Returns the transpose of a matrix.
    """
def validateSabrParameters(alpha: typing.SupportsFloat, beta: typing.SupportsFloat, nu: typing.SupportsFloat, rho: typing.SupportsFloat) -> None:
    """
    Validates SABR parameters (raises on invalid).
    """
def weeks(period: Period) -> float:
    """
    Convert a Period to weeks.
    """
def yearFractionToDate(dayCounter: DayCounter, referenceDate: Date, t: typing.SupportsFloat) -> Date:
    ...
def years(period: Period) -> float:
    """
    Convert a Period to years.
    """
Akima: CubicDerivativeApprox  # value = <CubicDerivativeApprox.Akima: 6>
Annual: Frequency  # value = <Frequency.Annual: 1>
Apr: Month  # value = <Month.April: 4>
April: Month  # value = <Month.April: 4>
Aug: Month  # value = <Month.August: 8>
August: Month  # value = <Month.August: 8>
BOOST_VERSION: int = 108800
Bimonthly: Frequency  # value = <Frequency.Bimonthly: 6>
Biweekly: Frequency  # value = <Frequency.Biweekly: 26>
Call: OptionType  # value = <OptionType.Call: 1>
Chebyshev: PolynomialType  # value = <PolynomialType.Chebyshev: 5>
Chebyshev2nd: PolynomialType  # value = <PolynomialType.Chebyshev2nd: 6>
Compounded: Compounding  # value = <Compounding.Compounded: 1>
CompoundedThenSimple: Compounding  # value = <Compounding.CompoundedThenSimple: 4>
Continuous: Compounding  # value = <Compounding.Continuous: 2>
CraigSneyd: FdmSchemeType  # value = <FdmSchemeType.CraigSneyd: 2>
CrankNicolson: FdmSchemeType  # value = <FdmSchemeType.CrankNicolson: 8>
Daily: Frequency  # value = <Frequency.Daily: 365>
Days: TimeUnit  # value = <TimeUnit.Days: 0>
Dec: Month  # value = <Month.December: 12>
December: Month  # value = <Month.December: 12>
Douglas: FdmSchemeType  # value = <FdmSchemeType.Douglas: 1>
EPSILON: float = 2.220446049250313e-16
Escrowed: CashDividendModel  # value = <CashDividendModel.Escrowed: 1>
EveryFourthMonth: Frequency  # value = <Frequency.EveryFourthMonth: 3>
EveryFourthWeek: Frequency  # value = <Frequency.EveryFourthWeek: 13>
ExplicitEuler: FdmSchemeType  # value = <FdmSchemeType.ExplicitEuler: 5>
Feb: Month  # value = <Month.February: 2>
February: Month  # value = <Month.February: 2>
FirstDerivative: CubicBoundaryCondition  # value = <CubicBoundaryCondition.FirstDerivative: 1>
Following: BusinessDayConvention  # value = <BusinessDayConvention.Following: 0>
FourthOrder: CubicDerivativeApprox  # value = <CubicDerivativeApprox.FourthOrder: 3>
Fri: Weekday  # value = <Weekday.Friday: 6>
Friday: Weekday  # value = <Weekday.Friday: 6>
FritschButland: CubicDerivativeApprox  # value = <CubicDerivativeApprox.FritschButland: 5>
HalfMonthModifiedFollowing: BusinessDayConvention  # value = <BusinessDayConvention.HalfMonthModifiedFollowing: 5>
Harmonic: CubicDerivativeApprox  # value = <CubicDerivativeApprox.Harmonic: 8>
Hermite: PolynomialType  # value = <PolynomialType.Hermite: 2>
Hours: TimeUnit  # value = <TimeUnit.Hours: 4>
Hundsdorfer: FdmSchemeType  # value = <FdmSchemeType.Hundsdorfer: 0>
Hyperbolic: PolynomialType  # value = <PolynomialType.Hyperbolic: 3>
ImplicitEuler: FdmSchemeType  # value = <FdmSchemeType.ImplicitEuler: 4>
Jan: Month  # value = <Month.January: 1>
January: Month  # value = <Month.January: 1>
JoinBusinessDays: JointCalendarRule  # value = <JointCalendarRule.JoinBusinessDays: 1>
JoinHolidays: JointCalendarRule  # value = <JointCalendarRule.JoinHolidays: 0>
Jul: Month  # value = <Month.July: 7>
July: Month  # value = <Month.July: 7>
Jun: Month  # value = <Month.June: 6>
June: Month  # value = <Month.June: 6>
Kruger: CubicDerivativeApprox  # value = <CubicDerivativeApprox.Kruger: 7>
Lagrange: CubicBoundaryCondition  # value = <CubicBoundaryCondition.Lagrange: 4>
Laguerre: PolynomialType  # value = <PolynomialType.Laguerre: 1>
Legendre: PolynomialType  # value = <PolynomialType.Legendre: 4>
MAX_INTEGER: int = 2147483647
MAX_REAL: float = 1.7976931348623157e+308
MIN_INTEGER: int = -2147483648
MIN_POSITIVE_REAL: float = 2.2250738585072014e-308
MIN_REAL: float = -1.7976931348623157e+308
Mar: Month  # value = <Month.March: 3>
March: Month  # value = <Month.March: 3>
May: Month  # value = <Month.May: 5>
MethodOfLines: FdmSchemeType  # value = <FdmSchemeType.MethodOfLines: 6>
Microseconds: TimeUnit  # value = <TimeUnit.Microseconds: 8>
Milliseconds: TimeUnit  # value = <TimeUnit.Milliseconds: 7>
Minutes: TimeUnit  # value = <TimeUnit.Minutes: 5>
ModifiedCraigSneyd: FdmSchemeType  # value = <FdmSchemeType.ModifiedCraigSneyd: 3>
ModifiedFollowing: BusinessDayConvention  # value = <BusinessDayConvention.ModifiedFollowing: 1>
ModifiedPreceding: BusinessDayConvention  # value = <BusinessDayConvention.ModifiedPreceding: 3>
Mon: Weekday  # value = <Weekday.Monday: 2>
Monday: Weekday  # value = <Weekday.Monday: 2>
Monomial: PolynomialType  # value = <PolynomialType.Monomial: 0>
Monthly: Frequency  # value = <Frequency.Monthly: 12>
Months: TimeUnit  # value = <TimeUnit.Months: 2>
Nearest: BusinessDayConvention  # value = <BusinessDayConvention.Nearest: 6>
NoFrequency: Frequency  # value = <Frequency.NoFrequency: -1>
NotAKnot: CubicBoundaryCondition  # value = <CubicBoundaryCondition.NotAKnot: 0>
Nov: Month  # value = <Month.November: 11>
November: Month  # value = <Month.November: 11>
Oct: Month  # value = <Month.October: 10>
October: Month  # value = <Month.October: 10>
Once: Frequency  # value = <Frequency.Once: 0>
OtherFrequency: Frequency  # value = <Frequency.OtherFrequency: 999>
Parabolic: CubicDerivativeApprox  # value = <CubicDerivativeApprox.Parabolic: 4>
Periodic: CubicBoundaryCondition  # value = <CubicBoundaryCondition.Periodic: 3>
Preceding: BusinessDayConvention  # value = <BusinessDayConvention.Preceding: 2>
Put: OptionType  # value = <OptionType.Put: -1>
QL_VERSION: str = '1.40'
QL_VERSION_HEX: int = 20971760
Quarterly: Frequency  # value = <Frequency.Quarterly: 4>
Sat: Weekday  # value = <Weekday.Saturday: 7>
Saturday: Weekday  # value = <Weekday.Saturday: 7>
SecondDerivative: CubicBoundaryCondition  # value = <CubicBoundaryCondition.SecondDerivative: 2>
Seconds: TimeUnit  # value = <TimeUnit.Seconds: 6>
Semiannual: Frequency  # value = <Frequency.Semiannual: 2>
Sep: Month  # value = <Month.September: 9>
September: Month  # value = <Month.September: 9>
Simple: Compounding  # value = <Compounding.Simple: 0>
SimpleThenCompounded: Compounding  # value = <Compounding.SimpleThenCompounded: 3>
Spline: CubicDerivativeApprox  # value = <CubicDerivativeApprox.Spline: 0>
SplineOM1: CubicDerivativeApprox  # value = <CubicDerivativeApprox.SplineOM1: 1>
SplineOM2: CubicDerivativeApprox  # value = <CubicDerivativeApprox.SplineOM2: 2>
Spot: CashDividendModel  # value = <CashDividendModel.Spot: 0>
Sun: Weekday  # value = <Weekday.Sunday: 1>
Sunday: Weekday  # value = <Weekday.Sunday: 1>
Thu: Weekday  # value = <Weekday.Thursday: 5>
Thursday: Weekday  # value = <Weekday.Thursday: 5>
TrBDF2: FdmSchemeType  # value = <FdmSchemeType.TrBDF2: 7>
Tue: Weekday  # value = <Weekday.Tuesday: 3>
Tuesday: Weekday  # value = <Weekday.Tuesday: 3>
Unadjusted: BusinessDayConvention  # value = <BusinessDayConvention.Unadjusted: 4>
Wed: Weekday  # value = <Weekday.Wednesday: 4>
Wednesday: Weekday  # value = <Weekday.Wednesday: 4>
Weekly: Frequency  # value = <Frequency.Weekly: 52>
Weeks: TimeUnit  # value = <TimeUnit.Weeks: 1>
Years: TimeUnit  # value = <TimeUnit.Years: 3>
__version__: str = '0.1.0'
BlackScholesMertonProcess = GeneralizedBlackScholesProcess
PiecewiseFlatForward = PiecewiseBackwardFlatForward
PiecewiseFlatHazardRate = PiecewiseBackwardFlatHazard
