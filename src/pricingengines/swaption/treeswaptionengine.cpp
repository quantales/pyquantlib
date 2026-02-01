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
#include <ql/pricingengines/swaption/treeswaptionengine.hpp>
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::treeswaptionengine(py::module_& m) {
    py::class_<TreeSwaptionEngine, PricingEngine, ext::shared_ptr<TreeSwaptionEngine>>(
        m, "TreeSwaptionEngine",
        "Numerical lattice engine for swaptions.")
        // Constructor with shared_ptr model and time steps
        .def(py::init<const ext::shared_ptr<ShortRateModel>&, Size,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs tree engine with model and time steps.")
        // Constructor with shared_ptr model and time grid
        .def(py::init<const ext::shared_ptr<ShortRateModel>&, const TimeGrid&,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeGrid"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs tree engine with model and time grid.")
        // Constructor with handle model and time steps
        .def(py::init<const Handle<ShortRateModel>&, Size,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs tree engine with model handle and time steps.")
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                        Size timeSteps,
                        const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<TreeSwaptionEngine>(
                model, timeSteps,
                ts ? Handle<YieldTermStructure>(ts) : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure"),
            "Constructs tree engine with model, time steps, and term structure.");
}
