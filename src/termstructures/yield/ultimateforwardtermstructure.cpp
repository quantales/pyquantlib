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
#include <ql/termstructures/yield/ultimateforwardtermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::ultimateforwardtermstructure(py::module_& m) {
    py::class_<UltimateForwardTermStructure, YieldTermStructure,
               ext::shared_ptr<UltimateForwardTermStructure>>(
        m, "UltimateForwardTermStructure",
        "UFR extrapolation (Smith-Wilson) for regulatory term structures.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>,
                      Handle<Quote>,
                      Handle<Quote>,
                      const Period&, Real>(),
            py::arg("curveHandle"),
            py::arg("lastLiquidForwardRate"),
            py::arg("ultimateForwardRate"),
            py::arg("firstSmoothingPoint"),
            py::arg("alpha"),
            "Constructs from handles.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve,
                         const ext::shared_ptr<Quote>& llfr,
                         const ext::shared_ptr<Quote>& ufr,
                         const Period& fsp, Real alpha) {
            return ext::make_shared<UltimateForwardTermStructure>(
                Handle<YieldTermStructure>(curve),
                Handle<Quote>(llfr),
                Handle<Quote>(ufr),
                fsp, alpha);
        }),
            py::arg("curve"),
            py::arg("lastLiquidForwardRate"),
            py::arg("ultimateForwardRate"),
            py::arg("firstSmoothingPoint"),
            py::arg("alpha"),
            "Constructs from shared_ptrs (handles created internally).");
}
