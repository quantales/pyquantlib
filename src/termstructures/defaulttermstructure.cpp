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
#include "pyquantlib/binding_manager.h"
#include "pyquantlib/trampolines.h"
#include <ql/termstructures/defaulttermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::defaultprobabilitytermstructure(py::module_& m) {
    py::class_<DefaultProbabilityTermStructure,
               PyDefaultProbabilityTermStructure, TermStructure,
               ext::shared_ptr<DefaultProbabilityTermStructure>>(
        m, "DefaultProbabilityTermStructure",
        "Default probability term structure.")
        .def(py::init_alias<>())
        .def("survivalProbability",
            static_cast<Probability (DefaultProbabilityTermStructure::*)(
                const Date&, bool) const>(
                &DefaultProbabilityTermStructure::survivalProbability),
            py::arg("date"), py::arg("extrapolate") = false,
            "Survival probability to a given date.")
        .def("defaultProbability",
            static_cast<Probability (DefaultProbabilityTermStructure::*)(
                const Date&, bool) const>(
                &DefaultProbabilityTermStructure::defaultProbability),
            py::arg("date"), py::arg("extrapolate") = false,
            "Default probability to a given date.")
        .def("defaultProbabilityBetween",
            static_cast<Probability (DefaultProbabilityTermStructure::*)(
                const Date&, const Date&, bool) const>(
                &DefaultProbabilityTermStructure::defaultProbability),
            py::arg("date1"), py::arg("date2"),
            py::arg("extrapolate") = false,
            "Default probability between two dates.")
        .def("defaultDensity",
            static_cast<Real (DefaultProbabilityTermStructure::*)(
                const Date&, bool) const>(
                &DefaultProbabilityTermStructure::defaultDensity),
            py::arg("date"), py::arg("extrapolate") = false,
            "Default density at a given date.")
        .def("hazardRate",
            static_cast<Rate (DefaultProbabilityTermStructure::*)(
                const Date&, bool) const>(
                &DefaultProbabilityTermStructure::hazardRate),
            py::arg("date"), py::arg("extrapolate") = false,
            "Hazard rate at a given date.");
}

void ql_termstructures::defaultprobabilitytermstructurehandle(py::module_& m) {
    bindHandle<DefaultProbabilityTermStructure>(
        m, "DefaultProbabilityTermStructureHandle",
        "Handle to DefaultProbabilityTermStructure.");
    bindRelinkableHandle<DefaultProbabilityTermStructure>(
        m, "RelinkableDefaultProbabilityTermStructureHandle",
        "Relinkable handle to DefaultProbabilityTermStructure.");
}
