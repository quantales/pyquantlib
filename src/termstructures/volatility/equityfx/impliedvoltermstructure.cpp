/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/equityfx/impliedvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::impliedvoltermstructure(py::module_& m) {
    py::class_<ImpliedVolTermStructure, BlackVarianceTermStructure,
               ext::shared_ptr<ImpliedVolTermStructure>>(
        m, "ImpliedVolTermStructure",
        "Black volatility term structure implied at a future reference date.")
        .def(py::init<Handle<BlackVolTermStructure>, const Date&>(),
            py::arg("originalTS"), py::arg("referenceDate"),
            "Constructs from the original structure handle and the new reference date.")
        .def(py::init([](const ext::shared_ptr<BlackVolTermStructure>& originalTS,
                         const Date& referenceDate) {
            return ext::make_shared<ImpliedVolTermStructure>(
                Handle<BlackVolTermStructure>(originalTS), referenceDate);
        }),
            py::arg("originalTS"), py::arg("referenceDate"),
            "Constructs from the original structure (handle created internally).")
        .def("dayCounter", &ImpliedVolTermStructure::dayCounter,
            "Returns the day counter.")
        .def("maxDate", &ImpliedVolTermStructure::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &ImpliedVolTermStructure::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &ImpliedVolTermStructure::maxStrike,
            "Returns the maximum strike.");
}
