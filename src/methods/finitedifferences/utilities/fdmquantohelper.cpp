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
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmquantohelper(py::module_& m) {
    py::class_<FdmQuantoHelper, Observable,
               ext::shared_ptr<FdmQuantoHelper>>(
        m, "FdmQuantoHelper",
        "Helper storing market data for FDM quanto adjustment.")
        .def(py::init<ext::shared_ptr<YieldTermStructure>,
                      ext::shared_ptr<YieldTermStructure>,
                      ext::shared_ptr<BlackVolTermStructure>,
                      Real, Real>(),
            py::arg("rTS"),
            py::arg("fTS"),
            py::arg("fxVolTS"),
            py::arg("equityFxCorrelation"),
            py::arg("exchRateATMlevel"),
            "Constructs from rate curves, FX vol, correlation, and FX rate.")
        .def("quantoAdjustment",
            py::overload_cast<Volatility, Time, Time>(
                &FdmQuantoHelper::quantoAdjustment, py::const_),
            py::arg("equityVol"), py::arg("t1"), py::arg("t2"),
            "Returns the quanto adjustment for scalar equity volatility.")
        .def("quantoAdjustment",
            py::overload_cast<const Array&, Time, Time>(
                &FdmQuantoHelper::quantoAdjustment, py::const_),
            py::arg("equityVol"), py::arg("t1"), py::arg("t2"),
            "Returns the quanto adjustment for an Array of equity volatilities.")
        .def_readonly("rTS", &FdmQuantoHelper::rTS_)
        .def_readonly("fTS", &FdmQuantoHelper::fTS_)
        .def_readonly("fxVolTS", &FdmQuantoHelper::fxVolTS_)
        .def_readonly("equityFxCorrelation",
            &FdmQuantoHelper::equityFxCorrelation_)
        .def_readonly("exchRateATMlevel",
            &FdmQuantoHelper::exchRateATMlevel_);
}
