# Changelog

All notable changes to PyQuantLib will be documented in this file.

```{seealso}
{doc}`building` for build requirements and setup instructions.
```

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Cash Flows
- `CmsCoupon`, `CmsLeg` for Constant Maturity Swap coupons
- `MeanRevertingPricer` ABC, `CmsCouponPricer` ABC (in `pyquantlib.base`)
- `LinearTsrPricer` with `LinearTsrPricerSettings` and `LinearTsrPricerStrategy`

#### Indexes
- Concrete swap index subclasses: `EuriborSwapIsdaFixA`, `EuriborSwapIsdaFixB`, `EuriborSwapIfrFix`, `EurLiborSwapIsdaFixA`, `EurLiborSwapIsdaFixB`, `EurLiborSwapIfrFix`, `UsdLiborSwapIsdaFixAm`, `UsdLiborSwapIsdaFixPm`, `JpyLiborSwapIsdaFixAm`, `JpyLiborSwapIsdaFixPm`, `GbpLiborSwapIsdaFix`, `ChfLiborSwapIsdaFix`

#### Term Structures
- **Fitted bond discount curves**: `FittedBondDiscountCurve`, `FittingMethod` ABC
- **Fitting methods**: `NelsonSiegelFitting`, `SvenssonFitting`, `ExponentialSplinesFitting`, `CubicBSplinesFitting`, `SimplePolynomialFitting`, `SpreadFittingMethod`
- **Swaption volatility**: `SwaptionVolatilityStructure` ABC, `ConstantSwaptionVolatility`, `SwaptionVolatilityDiscrete`, `SwaptionVolatilityMatrix`, `SwaptionVolatilityCube`, `SabrSwaptionVolatilityCube`, handles
- **Optionlet volatility**: `OptionletVolatilityStructure` ABC, `ConstantOptionletVolatility`, handles
- **Cap/floor term volatility**: `CapFloorTermVolatilityStructure` ABC, `CapFloorTermVolSurface`
- **Optionlet stripping**: `StrippedOptionletBase` ABC, `OptionletStripper` ABC, `OptionletStripper1`, `StrippedOptionletAdapter`

### Fixed
- Handle constructors now use `shared_ptr_from_python` for safe `shared_ptr` extraction from `py::classh` types with diamond/virtual inheritance
- Compile-time check enforcing `QL_USE_STD_SHARED_PTR`; building against QuantLib with `boost::shared_ptr` caused heap corruption at runtime

## [0.1.0] - 2026-02-08

Initial release targeting QuantLib 1.40.

### Added

#### Core Infrastructure
- pybind11-based bindings with scikit-build-core
- Cross-platform support (Windows, macOS, Linux)
- Type stub files (`.pyi`) for IDE support
- CI with GitHub Actions and cibuildwheel
- Sphinx documentation with API reference

#### Patterns and Utilities
- `Observable`, `Observer`, `LazyObject` base classes
- `ObservableValue`, `Null` sentinels

#### Time Module
- `Date`, `Period`, `TimeUnit`, `Weekday`, `Month`, `Frequency`
- `Calendar` with implementations (TARGET, UnitedStates, UnitedKingdom, etc.)
- `DayCounter` with implementations (Actual365Fixed, Actual360, Thirty360, etc.)
- `BusinessDayConvention` enum
- `DateGeneration::Rule` enum
- `Schedule` and `MakeSchedule` for date generation

#### Core Module
- `Settings` singleton for global evaluation date
- `InterestRate` with compounding conversions
- `Compounding` enum
- Mathematical and financial constants
- `TimeGrid` for discretization
- `Quote` ABC, `QuoteHandle`, `RelinkableQuoteHandle`
- `CashFlow` and `Event` ABCs
- `Index` ABC
- `Currency`, `Money`, `ExchangeRate`
- `TermStructure` ABC
- `Exercise` styles (European, American, Bermudan)
- `PricingEngine` ABC, `Instrument` ABC
- `Option` ABC with Greeks results
- `Payoff` ABC
- `StochasticProcess`, `StochasticProcess1D` ABCs
- `Protection::Side` (Buyer, Seller) enum
- `CreditDefaultSwap::PricingModel` (Midpoint, ISDA) enum

#### Math Module
- `Array` and `Matrix` with NumPy interoperability
- `Rounding` implementations
- Optimization: `EndCriteria`, `Constraint`, `LevenbergMarquardt`, `Problem`, `CostFunction`
- Interpolation: `LinearInterpolation`, `LogLinearInterpolation`, `BackwardFlatInterpolation`, `CubicInterpolation`
- Distributions: `NormalDistribution`, `CumulativeNormalDistribution`, `InverseCumulativeNormal`, `BivariateCumulativeNormalDistribution`
- 1-D root-finding solvers: `Brent`, `Bisection`, `Secant`, `Ridder`, `FalsePosition`, `Newton`, `NewtonSafe`

#### Market Data
- `SimpleQuote`, `DerivedQuote`, `CompositeQuote`

#### Currencies
- Major currency definitions (USD, EUR, GBP, JPY, CHF, AUD, CAD, etc.)
- `ExchangeRateManager`

#### Cash Flows
- `CashFlow`, `Coupon`, `FloatingRateCoupon` base classes
- `SimpleCashFlow`, `Redemption`, `AmortizingPayment`
- `FixedRateCoupon`, `FixedRateLeg`
- `FloatingRateCouponPricer` ABC, `BlackIborCouponPricer`
- `IborCoupon`, `IborLeg`
- `OvernightIndexedCoupon`, `OvernightLeg`
- `RateAveraging` enum (Simple, Compound)
- `Duration::Type` enum (Simple, Macaulay, Modified)
- `setCouponPricer` utility

#### Indexes
- `InterestRateIndex` base class
- `IborIndex` with Euribor family (1W through 1Y)
- Overnight indices: `Sofr`, `Eonia`, `Estr`, `Sonia`
- `SwapIndex`, `EuriborSwapIsdaFixA`

#### Term Structures
- **Yield curves**: `YieldTermStructure`, `FlatForward`
- **Interpolated yield curves**: `ZeroCurve`, `DiscountCurve`, `ForwardCurve`
- **Bootstrapped yield curves**: `PiecewiseCubicDiscount`, `PiecewiseLinearDiscount`, `PiecewiseLogLinearDiscount`, `PiecewiseLinearZero`, `PiecewiseCubicZero`, `PiecewiseLinearForward`, `PiecewiseFlatForward` (alias for `PiecewiseBackwardFlatForward`)
- **Rate helpers**: `DepositRateHelper`, `FraRateHelper`, `SwapRateHelper`, `OISRateHelper`
- **Pillar** date choices for bootstrap
- `ZeroSpreadedTermStructure`
- **Black vol**: `BlackVolTermStructure`, `BlackConstantVol`, `BlackVarianceSurface`
- **Local vol**: `LocalVolTermStructure`, `LocalConstantVol`, `LocalVolSurface`, `FixedLocalVolSurface`, `NoExceptLocalVolSurface`
- **Smile sections**: `SmileSection` ABC, `SabrSmileSection`, `SabrInterpolatedSmileSection`
- `VolatilityType` enum (ShiftedLognormal, Normal)
- **Credit**: `DefaultProbabilityTermStructure`, `FlatHazardRate`
- **Credit helpers**: `SpreadCdsHelper`, `UpfrontCdsHelper`
- **Bootstrapped default curves**: `PiecewiseLogLinearSurvival`, `PiecewiseFlatHazardRate`, `PiecewiseBackwardFlatHazard`
- All handle types (relinkable and non-relinkable)

#### Processes
- `GeneralizedBlackScholesProcess`, `BlackScholesProcess`, `BlackScholesMertonProcess`
- `HestonProcess`, `BatesProcess`
- `StochasticProcessArray`
- `EulerDiscretization`

#### Models
- `CalibratedModel` ABC, `AffineModel` ABC
- `HestonModel`, `HestonModelHandle`, `PiecewiseTimeDependentHestonModel`
- `BatesModel`
- Short-rate models: `Vasicek`, `HullWhite`, `BlackKarasinski`
- Two-factor models: `G2`
- `SwaptionHelper` for model calibration

#### Instruments
- **Bonds**: `Bond`, `FixedRateBond`, `ZeroCouponBond`, `FloatingRateBond`
- **Swaps**: `Swap`, `FixedVsFloatingSwap`, `VanillaSwap`, `OvernightIndexedSwap`, `ZeroCouponSwap`
- **Swap builders**: `MakeVanillaSwap`, `MakeOIS`
- **Options**: `VanillaOption`, `EuropeanOption`, `BasketOption`
- **Barrier options**: `BarrierOption`, `DoubleBarrierOption` with type enums
- **Asian options**: `AsianOption` with `AverageType` enum
- **Swaptions**: `Swaption`, `MakeSwaption`
- **Cap/Floor**: `CapFloor`, `MakeCapFloor`
- **Credit**: `CreditDefaultSwap`, `cdsMaturity` helper
- `ForwardRateAgreement`
- `AssetSwap`
- `CompositeInstrument`
- Payoffs: `PlainVanillaPayoff`, `CashOrNothingPayoff`, `AssetOrNothingPayoff`, basket payoffs

#### Pricing Engines
- **European**: `AnalyticEuropeanEngine`, `MCEuropeanEngine`, `IntegralEngine`
- **American**: `BaroneAdesiWhaleyApproximationEngine`, `BjerksundStenslandApproximationEngine`, `FdBlackScholesVanillaEngine`, `BinomialVanillaEngine`, `MCAmericanEngine`, `QdFpAmericanEngine`
- **Heston/Bates**: `AnalyticHestonEngine`, `BatesEngine`
- **Stochastic rates**: `AnalyticBlackVasicekEngine`
- **Spread**: `KirkEngine`, `BjerksundStenslandSpreadEngine`, `OperatorSplittingSpreadEngine`
- **Basket**: `MCEuropeanBasketEngine`, `DengLiZhouBasketEngine`, `StulzEngine`, `Fd2dBlackScholesVanillaEngine`
- **Barrier**: `AnalyticBarrierEngine`, `AnalyticDoubleBarrierEngine`, `FdBlackScholesBarrierEngine`
- **Asian**: `AnalyticContinuousGeometricAveragePriceAsianEngine`, `AnalyticDiscreteGeometricAveragePriceAsianEngine`, `MCDiscreteArithmeticAPEngine`, `TurnbullWakemanAsianEngine`
- **Swaption**: `TreeSwaptionEngine`, `JamshidianSwaptionEngine`, `G2SwaptionEngine`, `FdHullWhiteSwaptionEngine`, `FdG2SwaptionEngine`, `BlackSwaptionEngine`, `BachelierSwaptionEngine`
- **Cap/Floor**: `BlackCapFloorEngine`, `BachelierCapFloorEngine`
- **Bond**: `DiscountingBondEngine`, `BondFunctions` (static analytics)
- **Swap**: `DiscountingSwapEngine`
- **Credit**: `MidPointCdsEngine`, `IsdaCdsEngine`
- **Utility**: `blackFormula`, `blackFormulaImpliedStdDev`, `GenericModelEngine`

#### Methods
- Finite difference infrastructure (`FdmBackwardSolver`)

#### Experimental
- `SviSmileSection` (SVI volatility smile parameterization)

#### Python Extensions
- `ModifiedKirkEngine` (pure Python spread option engine)
- `SviSmileSection` (pure Python SVI implementation)

### Notes
- Requires QuantLib 1.40+ built as static library with `std::shared_ptr`
- API is subject to change during beta period
- `QdFpAmericanEngine` has a known issue on Windows (access violation during `calculate()`)

[Unreleased]: https://github.com/quantales/pyquantlib/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/quantales/pyquantlib/releases/tag/v0.1.0
