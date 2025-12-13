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
#include <pybind11/pybind11.h>

namespace py = pybind11;

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
            update
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
            performCalculations
        );
    }
};
