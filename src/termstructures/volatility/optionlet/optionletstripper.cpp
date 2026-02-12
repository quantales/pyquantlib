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
#include <ql/termstructures/volatility/optionlet/optionletstripper.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::optionletstripper(py::module_& m) {
    py::class_<OptionletStripper,
               ext::shared_ptr<OptionletStripper>, StrippedOptionletBase>(
        m, "OptionletStripper",
        "Abstract base class for optionlet strippers.")
        // No constructor (protected in QuantLib)
        .def("optionletFixingTenors", &OptionletStripper::optionletFixingTenors,
            py::return_value_policy::reference_internal,
            "Returns optionlet fixing tenors.")
        .def("optionletPaymentDates", &OptionletStripper::optionletPaymentDates,
            py::return_value_policy::reference_internal,
            "Returns optionlet payment dates.")
        .def("optionletAccrualPeriods", &OptionletStripper::optionletAccrualPeriods,
            py::return_value_policy::reference_internal,
            "Returns optionlet accrual periods.")
        .def("termVolSurface", &OptionletStripper::termVolSurface,
            "Returns the cap/floor term volatility surface.")
        .def("iborIndex", &OptionletStripper::iborIndex,
            "Returns the IBOR index.")
        .def("optionletFrequency", &OptionletStripper::optionletFrequency,
            "Returns the optionlet frequency.");
}
