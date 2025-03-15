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

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/equityfx/localvolsurface.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::localvolsurface(py::module_& m) {
    py::class_<LocalVolSurface, LocalVolTermStructure,
               ext::shared_ptr<LocalVolSurface>>(
        m, "LocalVolSurface",
        "Local volatility surface derived from a Black volatility surface.")
        // With quote handle for underlying
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<Quote>&>(),
            py::arg("blackVolTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            "Constructs from Black vol surface and quote handle for underlying.")
        // With fixed underlying value
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      Real>(),
            py::arg("blackVolTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            "Constructs from Black vol surface and fixed underlying value.");
}
