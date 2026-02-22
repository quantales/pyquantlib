/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/experimental/callablebonds/treecallablebondengine.hpp>
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::treecallablebondengine(py::module_& m) {
    // TreeCallableFixedRateBondEngine
    py::class_<TreeCallableFixedRateBondEngine, PricingEngine,
               ext::shared_ptr<TreeCallableFixedRateBondEngine>>(
        m, "TreeCallableFixedRateBondEngine",
        "Numerical lattice engine for callable fixed rate bonds.")
        // Constructor: model + time steps
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         Size timeSteps) {
            return ext::make_shared<TreeCallableFixedRateBondEngine>(model, timeSteps);
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            "Constructs tree engine with model and time steps.")
        // Constructor: model + time steps + term structure handle
        .def(py::init<const ext::shared_ptr<ShortRateModel>&, Size,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure"),
            "Constructs tree engine with model, time steps, and term structure.")
        // Constructor: model + time grid
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         const TimeGrid& timeGrid) {
            return ext::make_shared<TreeCallableFixedRateBondEngine>(model, timeGrid);
        }),
            py::arg("model"),
            py::arg("timeGrid"),
            "Constructs tree engine with model and time grid.")
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         Size timeSteps,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<TreeCallableFixedRateBondEngine>(
                model, timeSteps,
                ts ? Handle<YieldTermStructure>(ts) : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure"),
            "Constructs tree engine (handle created internally).");

    // TreeCallableZeroCouponBondEngine
    py::class_<TreeCallableZeroCouponBondEngine, TreeCallableFixedRateBondEngine,
               ext::shared_ptr<TreeCallableZeroCouponBondEngine>>(
        m, "TreeCallableZeroCouponBondEngine",
        "Numerical lattice engine for callable zero coupon bonds.")
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         Size timeSteps) {
            return ext::make_shared<TreeCallableZeroCouponBondEngine>(model, timeSteps);
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            "Constructs tree engine with model and time steps.")
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         Size timeSteps,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<TreeCallableZeroCouponBondEngine>(
                model, timeSteps,
                ts ? Handle<YieldTermStructure>(ts) : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure"),
            "Constructs tree engine (handle created internally).");
}
