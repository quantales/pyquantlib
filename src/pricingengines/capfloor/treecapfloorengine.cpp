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
#include <ql/pricingengines/capfloor/treecapfloorengine.hpp>
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::treecapfloorengine(py::module_& m) {
    py::class_<TreeCapFloorEngine,
               ext::shared_ptr<TreeCapFloorEngine>,
               PricingEngine>(
        m, "TreeCapFloorEngine",
        "Lattice cap/floor engine for short-rate models.")
        // Constructor with time steps
        .def(py::init<const ext::shared_ptr<ShortRateModel>&, Size,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs tree cap/floor engine with time steps.")
        // Constructor with time grid
        .def(py::init<const ext::shared_ptr<ShortRateModel>&, const TimeGrid&,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("timeGrid"),
            py::arg("termStructure") = Handle<YieldTermStructure>(),
            "Constructs tree cap/floor engine with time grid.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<ShortRateModel>& model,
                         Size timeSteps,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<TreeCapFloorEngine>(
                model, timeSteps,
                ts ? Handle<YieldTermStructure>(ts)
                   : Handle<YieldTermStructure>());
        }),
            py::arg("model"),
            py::arg("timeSteps"),
            py::arg("termStructure"),
            "Constructs tree cap/floor engine (handle created internally).");
}
