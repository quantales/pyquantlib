# Changelog

All notable changes to PyQuantLib will be documented in this file.

```{seealso}
{doc}`building` for build requirements and setup instructions.
```

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### Time
- `Period.__radd__` and `Period.__rsub__` enabling `datetime.date + ql.Period` and `datetime.date - ql.Period` arithmetic (returns `ql.Date`)

#### Math
- `Statistics` (= `RiskStatistics`) with empirical-distribution risk measures, Gaussian-assumption analytics, and percentile/VaR/ES methods
- `IncrementalStatistics` for online (streaming) statistics via boost accumulators
- `SequenceStatistics` for N-dimensional statistics with covariance and correlation matrices

#### Instruments
- `HolderExtensibleOption` extensible option with holder's extension right
- `WriterExtensibleOption` extensible option with writer's extension right
- `QuantoForwardVanillaOption` quanto forward-start vanilla option with `qvega()`, `qrho()`, `qlambda()`
- `AmortizingCmsRateBond` amortizing CMS-rate bond with vector notionals

#### Pricing Engines
- `BlackCalculator` for Black 1976 option pricing with full Greeks (delta, gamma, theta, vega, rho, etc.)
- `BachelierCalculator` for normal-volatility option pricing with full Greeks
- `FdHestonVanillaEngine` + `MakeFdHestonVanillaEngine` builder for finite-differences Heston pricing
- `FdBatesVanillaEngine` for finite-differences Bates (Heston + jumps) pricing
- `FdSabrVanillaEngine` for finite-differences SABR pricing
- `FdCEVVanillaEngine` for finite-differences CEV pricing
- `FdBlackScholesShoutEngine` for finite-differences shout option pricing
- `COSHestonEngine` for Fourier-cosine series Heston pricing with cumulant accessors
- `ExponentialFittingHestonEngine` for exponentially-fitted Gauss-Laguerre Heston pricing
- `AnalyticPTDHestonEngine` for piecewise time-dependent Heston models
- `AnalyticPDFHestonEngine` for PDF-based Heston pricing of arbitrary European payoffs
- `AnalyticHestonHullWhiteEngine` for Heston + Hull-White stochastic rates
- `AnalyticH1HWEngine` for H1-HW approximation with equity-rate correlation
- `HestonExpansionEngine` with LPP2, LPP3, and Forde expansion formulas
- `JuQuadraticApproximationEngine` for Ju quadratic approximation of American options
- `QdPlusAmericanEngine` with configurable solver types (Brent, Newton, Ridder, Halley, SuperHalley)
- `AnalyticDigitalAmericanEngine` for analytic digital American option pricing (knock-in)
- `AnalyticDigitalAmericanKOEngine` for analytic digital American option pricing (knock-out)
- `MCDigitalEngine` factory function for Monte Carlo digital option pricing (pseudo-random and low-discrepancy)
- `AnalyticDividendEuropeanEngine` for European options with discrete dividends
- `AnalyticBSMHullWhiteEngine` for BSM + Hull-White stochastic interest rates
- `Gaussian1dSwaptionEngine` for Gaussian 1-D model swaption pricing (European/Bermudan)
- `Gaussian1dJamshidianSwaptionEngine` for Jamshidian decomposition swaption pricing
- `Gaussian1dNonstandardSwaptionEngine` for nonstandard swaption pricing with OAS support
- `Gaussian1dFloatFloatSwaptionEngine` for float-float swaption pricing with OAS support
- `Gaussian1dCapFloorEngine` for Gaussian 1-D model cap/floor pricing
- `AnalyticCapFloorEngine` for analytic cap/floor pricing with affine short-rate models
- `TreeCapFloorEngine` for lattice-based cap/floor pricing with short-rate models
- `AnalyticHolderExtensibleOptionEngine` for holder extensible option pricing
- `AnalyticWriterExtensibleOptionEngine` for writer extensible option pricing
- `AnalyticGJRGARCHEngine` for GJR-GARCH(1,1) option pricing
- `MCForwardEuropeanBSEngine` Monte Carlo forward-start option engine (BS)
- `MCForwardEuropeanHestonEngine` Monte Carlo forward-start option engine (Heston)
- `QuantoForwardVanillaEngine` quanto forward-start vanilla option engine
- `FdHestonHullWhiteVanillaEngine` finite-differences Heston + Hull-White stochastic rates engine
- `FdOrnsteinUhlenbeckVanillaEngine` finite-differences Ornstein-Uhlenbeck vanilla engine
- `MCEuropeanHestonEngine` Monte Carlo European Heston engine (pseudo-random and low-discrepancy)

#### Processes
- `OrnsteinUhlenbeckProcess` mean-reverting OU process
- `HullWhiteProcess` Hull-White short-rate process
- `ForwardMeasureProcess` and `ForwardMeasureProcess1D` ABCs for forward-measure processes (in `pyquantlib.base`)
- `HullWhiteForwardProcess` Hull-White process under the T-forward measure
- `GJRGARCHProcess` GJR-GARCH(1,1) stochastic process with discretization schemes

#### Models
- `Gaussian1dModel` ABC for Gaussian 1-D short-rate models (in `pyquantlib.base`)
- `Gsr` Gaussian short-rate model with piecewise volatility and reversion, plus calibration methods
- `MarkovFunctional` Markov-functional model with `ModelSettings` builder and `ModelOutputs` diagnostics
- `Gaussian1dModelHandle` and `RelinkableGaussian1dModelHandle` for Gaussian1dModel references
- `CoxIngersollRoss` (CIR) short-rate model with Feller constraint support
- `ExtendedCoxIngersollRoss` extended CIR model fitted to the initial term structure
- `CapHelper` calibration helper for ATM caps (with handle and hidden-handle constructors)
- `HestonModelHelper` calibration helper for the Heston model (Real and Handle spot variants)
- `GJRGARCHModel` GJR-GARCH(1,1) calibrated model

#### Methods
- `LsmBasisSystem` / `PolynomialType` enum for Longstaff-Schwartz Monte Carlo basis systems (moved from MCAmericanEngine to its proper header location)
- `SampleNumber` (`Sample<Real>`) and `SampleRealVector` (`Sample<vector<Real>>`) weighted sample types
- `Path` single-factor price path with time grid, indexing, and value/time accessors
- `MultiPath` correlated multi-asset paths with per-asset indexing
- `SamplePath` (`Sample<Path>`) and `SampleMultiPath` (`Sample<MultiPath>`) weighted path samples
- `BrownianBridge` variance-reduction bridge construction from steps, times, or time grid
- `GaussianPathGenerator` single-factor path generator using pseudo-random Gaussian variates
- `GaussianSobolPathGenerator` single-factor path generator using Sobol low-discrepancy variates
- `GaussianMultiPathGenerator` multi-factor path generator using pseudo-random Gaussian variates
- `GaussianSobolMultiPathGenerator` multi-factor path generator using Sobol low-discrepancy variates
- `BrownianGenerator` ABC and `BrownianGeneratorFactory` ABC for Brownian motion generation (in `pyquantlib.base`)
- `MTBrownianGenerator` and `MTBrownianGeneratorFactory` Mersenne-Twister Brownian generators
- `SobolBrownianGenerator` and `SobolBrownianGeneratorFactory` Sobol-based Brownian generators
- `Burley2020SobolBrownianGenerator` and `Burley2020SobolBrownianGeneratorFactory` scrambled Sobol Brownian generators

#### Random Number Generators
- `MersenneTwisterUniformRng` (MT19937) with seed and vector-seed constructors
- `SobolRsg` low-discrepancy sequence generator with `DirectionIntegers` enum (10 direction integer sets) and `skipTo()`
- `HaltonRsg` Halton low-discrepancy sequence generator
- `Burley2020SobolRsg` scrambled Sobol sequence generator (Burley 2020 hash-based Owen scrambling) with `skipTo()`
- `BoxMullerGaussianRng` Box-Muller Gaussian random number generator
- `GaussianRandomGenerator` inverse cumulative normal Gaussian RNG
- `UniformRandomSequenceGenerator` MT-based uniform random sequence generator
- `GaussianRandomSequenceGenerator` MT-based Gaussian random sequence generator (inverse cumulative)
- `GaussianLowDiscrepancySequenceGenerator` Sobol-based Gaussian low-discrepancy sequence generator
- `SobolBrownianBridgeRsg` Sobol quasi-random with Brownian bridge ordering
- `Burley2020SobolBrownianBridgeRsg` scrambled Sobol with Brownian bridge ordering
- `Ordering` enum (Factors, Steps, Diagonal) for Sobol Brownian generator ordering

#### Experimental
- `TwoAssetCorrelationOption` two-asset correlation option with analytic engine
- `AnalyticTwoAssetCorrelationEngine` for two-asset correlation option pricing
- `VarianceGammaProcess` Variance Gamma stochastic process
- `VarianceGammaModel` Variance Gamma calibrated model
- `VarianceGammaEngine` analytic Variance Gamma option pricing
- `FFTVarianceGammaEngine` FFT-based Variance Gamma option pricing

### Fixed
- Autodoc class population on Read the Docs by installing the built wheel and removing `sys.path` hacks that shadowed the installed package

## [0.4.0] - 2026-02-27

### Added

#### Core
- `Forward` ABC for forward contracts (in `pyquantlib.base`) with inspectors (`settlementDate`, `forwardValue`, `spotValue`, `spotIncome`, `impliedYield`)
- `ForwardTypePayoff` for long/short forward payoffs
- `FloatingTypePayoff` for floating-strike lookback options

#### Indexes
- `EquityIndex` with minimal, full Handle, and hidden-handle constructors

#### Instruments
- `BondForward` forward contract on a bond with `forwardPrice()` and `cleanForwardPrice()`
- `NonstandardSwaption` option to enter into a nonstandard swap
- `FloatFloatSwaption` option to enter into a float-float swap
- `Callability` and `CallabilityType` enum for call/put schedules
- `CallableFixedRateBond` and `CallableZeroCouponBond`
- `EquityTotalReturnSwap` with IborIndex and OvernightIndex variants
- `SoftCallability` with trigger level for soft-call provisions
- `ConvertibleBond` base class with `conversionRatio()` and `callability()`
- `ConvertibleZeroCouponBond`, `ConvertibleFixedCouponBond`, `ConvertibleFloatingRateBond`
- **Lookback options**: `ContinuousFloatingLookbackOption`, `ContinuousFixedLookbackOption`, `ContinuousPartialFloatingLookbackOption`, `ContinuousPartialFixedLookbackOption`
- `CliquetOption` cliquet (ratchet) option with periodic resets
- `CompoundOption` option on an option (mother/daughter)
- `SimpleChooserOption` and `ComplexChooserOption` chooser options
- `MargrabeOption` exchange option with `delta1()`, `delta2()`, `gamma1()`, `gamma2()`
- `ForwardVanillaOption` forward-start vanilla option
- `QuantoVanillaOption` quanto option with `qvega()`, `qrho()`, `qlambda()`

#### Cash Flows
- `Dividend` ABC (in `pyquantlib.base`) for custom dividend implementations
- `FixedDividend` fixed cash dividend
- `FractionalDividend` proportional dividend (rate * nominal)
- `DividendVector` helper to build a sequence of fixed dividends

#### Pricing Engines
- `BinomialConvertibleEngine` Tsiveriotis-Fernandes lattice engine for convertible bonds (7 tree types: jr, crr, eqp, trigeorgis, tian, lr, joshi)
- **Lookback engines**: `AnalyticContinuousFloatingLookbackEngine`, `AnalyticContinuousFixedLookbackEngine`, `AnalyticContinuousPartialFloatingLookbackEngine`, `AnalyticContinuousPartialFixedLookbackEngine`
- `AnalyticCliquetEngine` analytic cliquet option engine
- `AnalyticCompoundOptionEngine` analytic compound option engine
- `AnalyticSimpleChooserEngine` and `AnalyticComplexChooserEngine` chooser option engines
- `AnalyticEuropeanMargrabeEngine` and `AnalyticAmericanMargrabeEngine` exchange option engines
- `ForwardEuropeanEngine` and `ForwardPerformanceEuropeanEngine` forward-start option engines
- `QuantoVanillaEngine` quanto European option engine with hidden handle constructors

#### Experimental
- `CallableBond` ABC (in `pyquantlib.base`) with OAS, effective duration/convexity, implied volatility
- `CallableBondVolatilityStructure` ABC (in `pyquantlib.base`), `CallableBondConstantVolatility`
- `TreeCallableFixedRateBondEngine`, `TreeCallableZeroCouponBondEngine`
- `BlackCallableFixedRateBondEngine`, `BlackCallableZeroCouponBondEngine`

## [0.3.0] - 2026-02-22

### Added

#### Indexes
- `Region` base class with concrete regions (`AustraliaRegion`, `EURegion`, `FranceRegion`, `UKRegion`, `USRegion`, `ZARegion`) and `CustomRegion`
- `InflationIndex` ABC, `ZeroInflationIndex` ABC, `YoYInflationIndex` ABC (in `pyquantlib.base`)
- `CPI` interpolation struct (`AsIndex`, `Flat`, `Linear`)
- Concrete inflation indexes: `USCPI`, `YYUSCPI`, `EUHICP`, `EUHICPXT`, `YYEUHICP`, `YYEUHICPXT`, `UKRPI`, `YYUKRPI`, `AUCPI`, `YYAUCPI`, `FRHICP`, `YYFRHICP`, `ZACPI`, `YYZACPI`

#### Term Structures
- `InflationTermStructure`, `ZeroInflationTermStructure`, `YoYInflationTermStructure` ABCs (in `pyquantlib.base`)
- `ZeroInflationTermStructureHandle`, `RelinkableZeroInflationTermStructureHandle`, `YoYInflationTermStructureHandle`, `RelinkableYoYInflationTermStructureHandle`
- `inflationPeriod` free function
- **Seasonality**: `Seasonality` ABC (in `pyquantlib.base`), `MultiplicativePriceSeasonality`, `KerkhofSeasonality`
- **Inflation bootstrap helpers**: `ZeroInflationHelper`, `YoYInflationHelper` ABCs (in `pyquantlib.base`), `ZeroCouponInflationSwapHelper`, `YearOnYearInflationSwapHelper`
- **Interpolated inflation curves**: `ZeroInflationCurve`, `YoYInflationCurve` (Linear interpolation)
- **Piecewise inflation curves**: `PiecewiseZeroInflationCurve`, `PiecewiseYoYInflationCurve` (Linear interpolation)
- `setSeasonality()` and `seasonality()` on `InflationTermStructure`
- **YoY inflation optionlet volatility**: `YoYOptionletVolatilitySurface` ABC (in `pyquantlib.base`), `ConstantYoYOptionletVolatility`, `YoYOptionletVolatilitySurfaceHandle`, `RelinkableYoYOptionletVolatilitySurfaceHandle`

#### Cash Flows
- `InflationCoupon` ABC (in `pyquantlib.base`)
- `ZeroInflationCashFlow` for zero-coupon inflation legs
- `YoYInflationCoupon` and `yoyInflationLeg` builder
- `CappedFlooredYoYInflationCoupon` for capped/floored YoY coupons
- `InflationCouponPricer` ABC (in `pyquantlib.base`), `YoYInflationCouponPricer`, `BlackYoYInflationCouponPricer`, `UnitDisplacedBlackYoYInflationCouponPricer`, `BachelierYoYInflationCouponPricer`
- `setCouponPricer` overload for inflation legs

#### Instruments
- `AmortizingFixedRateBond` amortizing fixed-rate bond with `sinkingSchedule` and `sinkingNotionals` helper functions
- `AmortizingFloatingRateBond` amortizing floating-rate bond
- `CmsRateBond` CMS-rate bond linked to a swap index
- `CPIBond` CPI inflation-linked bond
- `ZeroCouponInflationSwap` zero-coupon inflation swap
- `YearOnYearInflationSwap` year-on-year inflation swap
- `YoYInflationCapFloor` with `YoYInflationCap`, `YoYInflationFloor`, `YoYInflationCollar` convenience classes
- `MakeYoYInflationCapFloor` builder (C++ binding and Python kwargs wrapper)
- `VarianceSwap` variance swap instrument
- `NonstandardSwap` swap with period-dependent nominal and strike
- `FloatFloatSwap` swap exchanging two floating legs with caps and floors

#### Pricing Engines
- `YoYInflationBlackCapFloorEngine`, `YoYInflationUnitDisplacedBlackCapFloorEngine`, `YoYInflationBachelierCapFloorEngine` for YoY inflation cap/floor pricing
- `ReplicatingVarianceSwapEngine` variance swap engine using replicating portfolio

#### Experimental
- `CdsOption` option on a credit default swap
- `BlackCdsOptionEngine` Black-formula CDS option engine

## [0.2.0] - 2026-02-15

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

[Unreleased]: https://github.com/quantales/pyquantlib/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/quantales/pyquantlib/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/quantales/pyquantlib/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/quantales/pyquantlib/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/quantales/pyquantlib/releases/tag/v0.1.0
