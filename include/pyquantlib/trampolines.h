/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#pragma once

#include <ql/patterns/observable.hpp>
#include <ql/patterns/lazyobject.hpp>
#include <ql/quote.hpp>
#include <ql/cashflow.hpp>
#include <ql/cashflows/coupon.hpp>
#include <ql/index.hpp>
#include <ql/indexes/interestrateindex.hpp>
#include <ql/termstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/voltermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <ql/exercise.hpp>
#include <ql/pricingengine.hpp>
#include <ql/pricingengines/genericmodelengine.hpp>
#include <ql/instrument.hpp>
#include <ql/option.hpp>
#include <ql/payoff.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/instruments/oneassetoption.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/stochasticprocess.hpp>
#include <ql/models/model.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/math/optimization/costfunction.hpp>
#include <ql/math/optimization/method.hpp>
#include <ql/math/optimization/problem.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

// NOTE: PYBIND11_OVERRIDE_PURE macros use a trailing comma after the function name
// (e.g., `value,` instead of `value`). This is intentional — it prevents C++20
// warnings about variadic macros when there are no function arguments.

// -----------------------------------------------------------------------------
// Observer Trampoline
// -----------------------------------------------------------------------------
class PyObserver : public QuantLib::Observer {
public:
    using QuantLib::Observer::Observer;

    PyObserver() : Observer() {}

    void update() override {
        PYBIND11_OVERRIDE_PURE(
            void,
            QuantLib::Observer,
            update,
        );
    }
};

// -----------------------------------------------------------------------------
// Observable Trampoline
// -----------------------------------------------------------------------------
class PyObservable : public QuantLib::Observable {
public:
    using QuantLib::Observable::Observable;

    PyObservable() : Observable() {}
};

// -----------------------------------------------------------------------------
// LazyObject Trampoline
// -----------------------------------------------------------------------------
class PyLazyObject : public QuantLib::LazyObject {
public:
    using QuantLib::LazyObject::LazyObject;

    PyLazyObject() : LazyObject() {}

    void performCalculations() const override {
        PYBIND11_OVERRIDE_PURE(
            void,
            QuantLib::LazyObject,
            performCalculations,
        );
    }
};

// -----------------------------------------------------------------------------
// Quote Trampoline
// -----------------------------------------------------------------------------
class PyQuote : public QuantLib::Quote {
public:
    using QuantLib::Quote::Quote;

    QuantLib::Real value() const override {
        PYBIND11_OVERRIDE_PURE(
            QuantLib::Real,
            QuantLib::Quote,
            value,
        );
    }

    bool isValid() const override {
        PYBIND11_OVERRIDE_PURE(
            bool,
            QuantLib::Quote,
            isValid,
        );
    }
};

// -----------------------------------------------------------------------------
// Event Trampoline
// -----------------------------------------------------------------------------
class PyEvent : public QuantLib::Event {
public:
    using QuantLib::Event::Event;

    PyEvent() : Event() {}

    QuantLib::Date date() const override {
        PYBIND11_OVERRIDE_PURE(
            QuantLib::Date,
            QuantLib::Event,
            date,
        );
    }
};

// -----------------------------------------------------------------------------
// CashFlow Trampoline
// -----------------------------------------------------------------------------
class PyCashFlow : public QuantLib::CashFlow {
public:
    using QuantLib::CashFlow::CashFlow;

    PyCashFlow() : CashFlow() {}

    QuantLib::Real amount() const override {
        PYBIND11_OVERRIDE_PURE(
            QuantLib::Real,
            QuantLib::CashFlow,
            amount,
        );
    }

    QuantLib::Date date() const override {
        PYBIND11_OVERRIDE_PURE(
            QuantLib::Date,
            QuantLib::CashFlow,
            date,
        );
    }
};

// -----------------------------------------------------------------------------
// Coupon Trampoline
// -----------------------------------------------------------------------------
class PyCoupon : public QuantLib::Coupon {
public:
    using QuantLib::Coupon::Coupon;

    PyCoupon() : Coupon(QuantLib::Date(), 0.0, QuantLib::Date(), QuantLib::Date()) {}

    QuantLib::Date date() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::Coupon, date,);
    }

    QuantLib::Real amount() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::Coupon, amount,);
    }

    QuantLib::Rate nominal() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Rate, QuantLib::Coupon, nominal,);
    }

    QuantLib::DayCounter dayCounter() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::DayCounter, QuantLib::Coupon, dayCounter,);
    }

    QuantLib::Rate rate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Rate, QuantLib::Coupon, rate,);
    }

    QuantLib::Real accruedAmount(const QuantLib::Date& d) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::Coupon, accruedAmount, d);
    }
};

// -----------------------------------------------------------------------------
// Index Trampoline
// -----------------------------------------------------------------------------
class PyIndex : public QuantLib::Index {
public:
    using QuantLib::Index::Index;

    PyIndex() : Index() {}

    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, QuantLib::Index, name,);
    }

    QuantLib::Calendar fixingCalendar() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Calendar, QuantLib::Index, fixingCalendar,);
    }

    bool isValidFixingDate(const QuantLib::Date& fixingDate) const override {
        PYBIND11_OVERRIDE_PURE(bool, QuantLib::Index, isValidFixingDate, fixingDate);
    }

    QuantLib::Real fixing(const QuantLib::Date& fixingDate,
                          bool forecastTodaysFixing = false) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::Index, fixing,
                               fixingDate, forecastTodaysFixing);
    }

    void update() override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::Index, update,);
    }
};

// -----------------------------------------------------------------------------
// InterestRateIndex Trampoline
// -----------------------------------------------------------------------------
class PyInterestRateIndex : public QuantLib::InterestRateIndex {
public:
    using QuantLib::InterestRateIndex::InterestRateIndex;

    std::string name() const override {
        PYBIND11_OVERRIDE(std::string, QuantLib::InterestRateIndex, name,);
    }

    QuantLib::Calendar fixingCalendar() const override {
        PYBIND11_OVERRIDE(QuantLib::Calendar, QuantLib::InterestRateIndex, fixingCalendar,);
    }

    bool isValidFixingDate(const QuantLib::Date& fixingDate) const override {
        PYBIND11_OVERRIDE(bool, QuantLib::InterestRateIndex, isValidFixingDate, fixingDate);
    }

    QuantLib::Real fixing(const QuantLib::Date& fixingDate,
                          bool forecastTodaysFixing = false) const override {
        PYBIND11_OVERRIDE(QuantLib::Real, QuantLib::InterestRateIndex, fixing,
                          fixingDate, forecastTodaysFixing);
    }

    QuantLib::Date fixingDate(const QuantLib::Date& valueDate) const override {
        PYBIND11_OVERRIDE(QuantLib::Date, QuantLib::InterestRateIndex, fixingDate, valueDate);
    }

    QuantLib::Date valueDate(const QuantLib::Date& fixingDate) const override {
        PYBIND11_OVERRIDE(QuantLib::Date, QuantLib::InterestRateIndex, valueDate, fixingDate);
    }

    QuantLib::Date maturityDate(const QuantLib::Date& valueDate) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::InterestRateIndex, maturityDate, valueDate);
    }

    QuantLib::Rate forecastFixing(const QuantLib::Date& fixingDate) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Rate, QuantLib::InterestRateIndex, forecastFixing, fixingDate);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::InterestRateIndex, update,);
    }
};

// -----------------------------------------------------------------------------
// TermStructure Trampoline
// -----------------------------------------------------------------------------
class PyTermStructure : public QuantLib::TermStructure {
public:
    using QuantLib::TermStructure::TermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::TermStructure, maxDate,);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::TermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// YieldTermStructure Trampoline
// -----------------------------------------------------------------------------
class PyYieldTermStructure : public QuantLib::YieldTermStructure {
public:
    using QuantLib::YieldTermStructure::YieldTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::YieldTermStructure, maxDate,);
    }

    QuantLib::DiscountFactor discountImpl(QuantLib::Time t) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::DiscountFactor, QuantLib::YieldTermStructure,
                               discountImpl, t);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::YieldTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// VolatilityTermStructure Trampoline
// -----------------------------------------------------------------------------
class PyVolatilityTermStructure : public QuantLib::VolatilityTermStructure {
public:
    using QuantLib::VolatilityTermStructure::VolatilityTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::VolatilityTermStructure, maxDate,);
    }

    QuantLib::Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::VolatilityTermStructure, minStrike,);
    }

    QuantLib::Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::VolatilityTermStructure, maxStrike,);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::VolatilityTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// BlackVolTermStructure Trampoline
// -----------------------------------------------------------------------------
class PyBlackVolTermStructure : public QuantLib::BlackVolTermStructure {
public:
    using QuantLib::BlackVolTermStructure::BlackVolTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::BlackVolTermStructure, maxDate,);
    }

    QuantLib::Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVolTermStructure, minStrike,);
    }

    QuantLib::Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVolTermStructure, maxStrike,);
    }

    QuantLib::Volatility blackVolImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Volatility, QuantLib::BlackVolTermStructure,
                               blackVolImpl, t, strike);
    }

    QuantLib::Real blackVarianceImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVolTermStructure,
                               blackVarianceImpl, t, strike);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::BlackVolTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// BlackVolatilityTermStructure Trampoline (volatility-based adapter)
// -----------------------------------------------------------------------------
class PyBlackVolatilityTermStructure : public QuantLib::BlackVolatilityTermStructure {
public:
    using QuantLib::BlackVolatilityTermStructure::BlackVolatilityTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::BlackVolatilityTermStructure, maxDate,);
    }

    QuantLib::Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVolatilityTermStructure, minStrike,);
    }

    QuantLib::Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVolatilityTermStructure, maxStrike,);
    }

    QuantLib::Volatility blackVolImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Volatility, QuantLib::BlackVolatilityTermStructure,
                               blackVolImpl, t, strike);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::BlackVolatilityTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// BlackVarianceTermStructure Trampoline (variance-based adapter)
// -----------------------------------------------------------------------------
class PyBlackVarianceTermStructure : public QuantLib::BlackVarianceTermStructure {
public:
    using QuantLib::BlackVarianceTermStructure::BlackVarianceTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::BlackVarianceTermStructure, maxDate,);
    }

    QuantLib::Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVarianceTermStructure, minStrike,);
    }

    QuantLib::Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVarianceTermStructure, maxStrike,);
    }

    QuantLib::Real blackVarianceImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::BlackVarianceTermStructure,
                               blackVarianceImpl, t, strike);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::BlackVarianceTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// LocalVolTermStructure Trampoline
// -----------------------------------------------------------------------------
class PyLocalVolTermStructure : public QuantLib::LocalVolTermStructure {
public:
    using QuantLib::LocalVolTermStructure::LocalVolTermStructure;

    QuantLib::Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Date, QuantLib::LocalVolTermStructure, maxDate,);
    }

    QuantLib::Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::LocalVolTermStructure, minStrike,);
    }

    QuantLib::Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::LocalVolTermStructure, maxStrike,);
    }

    QuantLib::Volatility localVolImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Volatility, QuantLib::LocalVolTermStructure,
                               localVolImpl, t, strike);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::LocalVolTermStructure, update,);
    }
};

// -----------------------------------------------------------------------------
// Exercise Trampoline
// -----------------------------------------------------------------------------
class PyExercise : public QuantLib::Exercise {
public:
    using QuantLib::Exercise::Exercise;
};

// -----------------------------------------------------------------------------
// PricingEngine Trampolines
// -----------------------------------------------------------------------------
class PyPricingEngineArguments : public QuantLib::PricingEngine::arguments {
public:
    using QuantLib::PricingEngine::arguments::arguments;

    void validate() const override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::PricingEngine::arguments, validate,);
    }
};

class PyPricingEngineResults : public QuantLib::PricingEngine::results {
public:
    using QuantLib::PricingEngine::results::results;

    void reset() override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::PricingEngine::results, reset,);
    }
};

class PyPricingEngine : public QuantLib::PricingEngine {
public:
    using QuantLib::PricingEngine::PricingEngine;

    PyPricingEngine() : PricingEngine() {}

    QuantLib::PricingEngine::arguments* getArguments() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::PricingEngine::arguments*,
                               QuantLib::PricingEngine, getArguments,);
    }

    const QuantLib::PricingEngine::results* getResults() const override {
        PYBIND11_OVERRIDE_PURE(const QuantLib::PricingEngine::results*,
                               QuantLib::PricingEngine, getResults,);
    }

    void reset() override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::PricingEngine, reset,);
    }

    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::PricingEngine, calculate,);
    }
};

// -----------------------------------------------------------------------------
// Instrument Trampoline
// -----------------------------------------------------------------------------
class PyInstrument : public QuantLib::Instrument {
public:
    using QuantLib::Instrument::Instrument;

    PyInstrument() : Instrument() {}

    bool isExpired() const override {
        PYBIND11_OVERRIDE_PURE(bool, QuantLib::Instrument, isExpired,);
    }

    void performCalculations() const override {
        PYBIND11_OVERRIDE(void, QuantLib::Instrument, performCalculations,);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::Instrument, update,);
    }
};

// -----------------------------------------------------------------------------
// Option Trampoline
// -----------------------------------------------------------------------------
class PyOption : public QuantLib::Option {
public:
    using QuantLib::Option::Option;

    bool isExpired() const override {
        PYBIND11_OVERRIDE_PURE(bool, QuantLib::Option, isExpired,);
    }

    void performCalculations() const override {
        PYBIND11_OVERRIDE(void, QuantLib::Option, performCalculations,);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::Option, update,);
    }
};

// -----------------------------------------------------------------------------
// Payoff Trampoline
// -----------------------------------------------------------------------------
class PyPayoff : public QuantLib::Payoff {
public:
    using QuantLib::Payoff::Payoff;

    PyPayoff() : Payoff() {}

    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, QuantLib::Payoff, name,);
    }

    std::string description() const override {
        PYBIND11_OVERRIDE_PURE(std::string, QuantLib::Payoff, description,);
    }

    QuantLib::Real operator()(QuantLib::Real price) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::Payoff, operator(), price);
    }
};

// -----------------------------------------------------------------------------
// StochasticProcess Trampoline
// -----------------------------------------------------------------------------
class PyStochasticProcess : public QuantLib::StochasticProcess {
public:
    using QuantLib::StochasticProcess::StochasticProcess;

    PyStochasticProcess() : StochasticProcess() {}

    QuantLib::Size size() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Size, QuantLib::StochasticProcess, size,);
    }

    QuantLib::Size factors() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Size, QuantLib::StochasticProcess, factors,);
    }

    QuantLib::Array initialValues() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Array, QuantLib::StochasticProcess, initialValues,);
    }

    QuantLib::Array drift(QuantLib::Time t, const QuantLib::Array& x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Array, QuantLib::StochasticProcess, drift, t, x);
    }

    QuantLib::Matrix diffusion(QuantLib::Time t, const QuantLib::Array& x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Matrix, QuantLib::StochasticProcess, diffusion, t, x);
    }

    QuantLib::Array evolve(QuantLib::Time t0, const QuantLib::Array& x0,
                           QuantLib::Time dt, const QuantLib::Array& dw) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Array, QuantLib::StochasticProcess, evolve, t0, x0, dt, dw);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::StochasticProcess, update,);
    }
};

// -----------------------------------------------------------------------------
// StochasticProcess1D::discretization Trampoline
// -----------------------------------------------------------------------------
class PyDiscretization : public QuantLib::StochasticProcess1D::discretization {
public:
    using QuantLib::StochasticProcess1D::discretization::discretization;

    QuantLib::Real drift(const QuantLib::StochasticProcess1D& process,
                         QuantLib::Time t0, QuantLib::Real x0, QuantLib::Time dt) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D::discretization,
                               drift, process, t0, x0, dt);
    }

    QuantLib::Real diffusion(const QuantLib::StochasticProcess1D& process,
                             QuantLib::Time t0, QuantLib::Real x0, QuantLib::Time dt) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D::discretization,
                               diffusion, process, t0, x0, dt);
    }

    QuantLib::Real variance(const QuantLib::StochasticProcess1D& process,
                            QuantLib::Time t0, QuantLib::Real x0, QuantLib::Time dt) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D::discretization,
                               variance, process, t0, x0, dt);
    }
};

// -----------------------------------------------------------------------------
// StochasticProcess1D Trampoline
// -----------------------------------------------------------------------------
class PyStochasticProcess1D : public QuantLib::StochasticProcess1D {
public:
    using QuantLib::StochasticProcess1D::StochasticProcess1D;

    PyStochasticProcess1D() : StochasticProcess1D() {}

    QuantLib::Real x0() const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D, x0,);
    }

    QuantLib::Real drift(QuantLib::Time t, QuantLib::Real x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D, drift, t, x);
    }

    QuantLib::Real diffusion(QuantLib::Time t, QuantLib::Real x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D, diffusion, t, x);
    }

    QuantLib::Real evolve(QuantLib::Time t0, QuantLib::Real x0,
                          QuantLib::Time dt, QuantLib::Real dw) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StochasticProcess1D, evolve, t0, x0, dt, dw);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::StochasticProcess1D, update,);
    }
};

// -----------------------------------------------------------------------------
// CostFunction Trampoline
// -----------------------------------------------------------------------------
class PyCostFunction : public QuantLib::CostFunction {
public:
    using QuantLib::CostFunction::CostFunction;

    QuantLib::Real value(const QuantLib::Array& x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::CostFunction, value, x);
    }

    QuantLib::Array values(const QuantLib::Array& x) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Array, QuantLib::CostFunction, values, x);
    }
};

// -----------------------------------------------------------------------------
// OptimizationMethod Trampoline
// -----------------------------------------------------------------------------
class PyOptimizationMethod : public QuantLib::OptimizationMethod {
public:
    using QuantLib::OptimizationMethod::OptimizationMethod;

    QuantLib::EndCriteria::Type minimize(QuantLib::Problem& p,
                                         const QuantLib::EndCriteria& endCriteria) override {
        PYBIND11_OVERRIDE_PURE(QuantLib::EndCriteria::Type, QuantLib::OptimizationMethod,
                               minimize, p, endCriteria);
    }
};

// -----------------------------------------------------------------------------
// StrikedTypePayoff Trampoline
// -----------------------------------------------------------------------------
class PyStrikedTypePayoff : public QuantLib::StrikedTypePayoff {
public:
    // Expose protected constructor for Python subclassing
    PyStrikedTypePayoff(QuantLib::Option::Type type, QuantLib::Real strike)
        : QuantLib::StrikedTypePayoff(type, strike) {}

    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, QuantLib::StrikedTypePayoff, name,);
    }

    std::string description() const override {
        PYBIND11_OVERRIDE(std::string, QuantLib::StrikedTypePayoff, description,);
    }

    QuantLib::Real operator()(QuantLib::Real price) const override {
        PYBIND11_OVERRIDE_PURE(QuantLib::Real, QuantLib::StrikedTypePayoff, operator(), price);
    }
};

// -----------------------------------------------------------------------------
// OneAssetOption Trampoline
// -----------------------------------------------------------------------------
class PyOneAssetOption : public QuantLib::OneAssetOption {
public:
    using QuantLib::OneAssetOption::OneAssetOption;

    bool isExpired() const override {
        PYBIND11_OVERRIDE_PURE(bool, QuantLib::OneAssetOption, isExpired,);
    }

    void performCalculations() const override {
        PYBIND11_OVERRIDE(void, QuantLib::OneAssetOption, performCalculations,);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::OneAssetOption, update,);
    }
};

// -----------------------------------------------------------------------------
// OneAssetOption Engine Trampolines
// -----------------------------------------------------------------------------
using OneAssetGenericEngine = QuantLib::GenericEngine<QuantLib::OneAssetOption::arguments,
                                                       QuantLib::OneAssetOption::results>;

class PyOneAssetGenericEngine : public OneAssetGenericEngine {
public:
    using OneAssetGenericEngine::OneAssetGenericEngine;

    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, OneAssetGenericEngine, calculate,);
    }
};

class PyOneAssetOptionEngine : public QuantLib::OneAssetOption::engine {
public:
    using QuantLib::OneAssetOption::engine::engine;

    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, QuantLib::OneAssetOption::engine, calculate,);
    }
};

// -----------------------------------------------------------------------------
// GenericHestonModelEngine Trampoline
// -----------------------------------------------------------------------------
using GenericHestonModelEngine = QuantLib::GenericModelEngine<QuantLib::HestonModel,
                                                               QuantLib::VanillaOption::arguments,
                                                               QuantLib::VanillaOption::results>;

class PyGenericHestonModelEngine : public GenericHestonModelEngine {
public:
    using GenericHestonModelEngine::GenericHestonModelEngine;

    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, GenericHestonModelEngine, calculate,);
    }
};

// -----------------------------------------------------------------------------
// CalibratedModel Trampoline
// -----------------------------------------------------------------------------
class PyCalibratedModel : public QuantLib::CalibratedModel {
public:
    // Expose protected constructor for Python subclassing
    PyCalibratedModel(QuantLib::Size nArguments)
        : QuantLib::CalibratedModel(nArguments) {}

    void calibrate(
        const std::vector<QuantLib::ext::shared_ptr<QuantLib::CalibrationHelper>>& instruments,
        QuantLib::OptimizationMethod& method,
        const QuantLib::EndCriteria& endCriteria,
        const QuantLib::Constraint& constraint,
        const std::vector<QuantLib::Real>& weights,
        const std::vector<bool>& fixParameters) override {
        PYBIND11_OVERRIDE(void, QuantLib::CalibratedModel, calibrate,
                         instruments, method, endCriteria, constraint,
                         weights, fixParameters);
    }

    void setParams(const QuantLib::Array& params) override {
        PYBIND11_OVERRIDE(void, QuantLib::CalibratedModel, setParams, params);
    }

    void update() override {
        PYBIND11_OVERRIDE(void, QuantLib::CalibratedModel, update,);
    }
};
