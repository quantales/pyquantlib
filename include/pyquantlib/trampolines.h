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
#include <ql/exercise.hpp>
#include <ql/pricingengine.hpp>
#include <ql/instrument.hpp>
#include <ql/option.hpp>
#include <ql/payoff.hpp>
#include <ql/stochasticprocess.hpp>
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
