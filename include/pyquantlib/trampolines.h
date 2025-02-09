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
#include <ql/index.hpp>
#include <ql/termstructure.hpp>
#include <ql/exercise.hpp>
#include <ql/pricingengine.hpp>
#include <ql/instrument.hpp>
#include <ql/option.hpp>
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
