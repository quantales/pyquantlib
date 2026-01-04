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
#include "pyquantlib/trampolines.h"
#include <ql/instruments/multiassetoption.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::multiassetoption(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    auto pyMultiAssetOption = py::class_<MultiAssetOption, PyMultiAssetOption,
        ext::shared_ptr<MultiAssetOption>, Option>(
        base, "MultiAssetOption", "Base class for options on multiple assets.")
        .def(py::init<ext::shared_ptr<Payoff>, ext::shared_ptr<Exercise>>(),
            py::arg("payoff"), py::arg("exercise"),
            "Constructs with payoff and exercise.")
        .def("isExpired", &MultiAssetOption::isExpired,
            "Returns whether the option has expired.")
        .def("delta", &MultiAssetOption::delta,
            "Returns delta.")
        .def("gamma", &MultiAssetOption::gamma,
            "Returns gamma.")
        .def("theta", &MultiAssetOption::theta,
            "Returns theta.")
        .def("vega", &MultiAssetOption::vega,
            "Returns vega.")
        .def("rho", &MultiAssetOption::rho,
            "Returns rho.")
        .def("dividendRho", &MultiAssetOption::dividendRho,
            "Returns dividend rho.");

    py::class_<MultiAssetOption::results, Instrument::results, Greeks,
        ext::shared_ptr<MultiAssetOption::results>>(
        pyMultiAssetOption, "results", "Results from multi-asset option calculation.")
        .def(py::init<>())
        .def("reset", &MultiAssetOption::results::reset,
            "Resets all results.");
}
