# Changelog

All notable changes to PyQuantLib will be documented in this file.

```{seealso}
{doc}`building` for build requirements and setup instructions.
```

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sphinx documentation with Read the Docs support
- Examples directory with Jupyter notebooks
- API reference documentation

## [0.1.0] - 2025-XX-XX

Initial alpha release.

### Added

#### Core Infrastructure
- pybind11-based bindings with scikit-build-core
- Cross-platform support (Windows, macOS, Linux)
- Type stub files (`.pyi`) for IDE support
- Observer/Observable pattern bindings

#### Time Module
- `Date`, `Period`, `TimeUnit`, `Weekday`, `Month`
- `Calendar` with implementations (TARGET, UnitedStates, UnitedKingdom, etc.)
- `DayCounter` with implementations (Actual365Fixed, Actual360, etc.)
- `Schedule` and `MakeSchedule` for date generation
- `TimeGrid` for discretization

#### Core Module
- `Settings` singleton for global evaluation date
- `InterestRate` with compounding conversions
- `Rounding` implementations
- Mathematical constants

#### Math Module
- `Array` and `Matrix` with NumPy interoperability
- Optimization: `EndCriteria`, `Constraint`, `LevenbergMarquardt`
- `Problem` and `CostFunction` for custom optimization

#### Market Data
- `SimpleQuote`, `DerivedQuote`, `CompositeQuote`
- `QuoteHandle` and `RelinkableQuoteHandle`

#### Currencies
- Major currency definitions (USD, EUR, GBP, JPY, etc.)
- `Money` and `ExchangeRate`

#### Cash Flows
- `CashFlow` and `Coupon` base classes
- `FixedRateCoupon` and `FixedRateLeg`

#### Term Structures
- Yield: `YieldTermStructure`, `FlatForward`, `ZeroCurve`
- Black vol: `BlackVolTermStructure`, `BlackConstantVol`, `BlackVarianceSurface`
- Local vol: `LocalVolTermStructure`, `LocalConstantVol`, `LocalVolSurface`, `FixedLocalVolSurface`
- All handle types (relinkable and non-relinkable)

#### Processes
- `StochasticProcess`, `StochasticProcess1D`
- `GeneralizedBlackScholesProcess`, `BlackScholesProcess`, `BlackScholesMertonProcess`
- `HestonProcess`

#### Models
- `HestonModel`

#### Instruments
- `Instrument` base class
- `VanillaOption`, `EuropeanOption`, `BasketOption`
- Payoffs: `PlainVanillaPayoff`, basket payoffs
- Exercise types: `EuropeanExercise`, `AmericanExercise`, `BermudanExercise`

#### Pricing Engines
- `AnalyticEuropeanEngine` (Black-Scholes)
- `MCEuropeanEngine` (Monte Carlo)
- `AnalyticHestonEngine`
- Basket engines: `MCEuropeanBasketEngine`, `KirkEngine`, `StulzEngine`
- `Fd2dBlackScholesVanillaEngine`

#### Methods
- Finite difference infrastructure

### Notes
- Requires QuantLib 1.40+ built as static library with `std::shared_ptr`
- API is subject to change during alpha period

[Unreleased]: https://github.com/quantales/pyquantlib/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/quantales/pyquantlib/releases/tag/v0.1.0
