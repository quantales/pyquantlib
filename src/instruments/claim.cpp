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
#include "pyquantlib/trampolines.h"
#include <ql/instruments/claim.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::claim(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // --- Claim ABC ---
    py::classh<Claim, PyClaim,
               Observable, Observer>(
        base, "Claim",
        "Abstract base class for default-event claims.")
        .def(py::init_alias<>())
        .def("amount", &Claim::amount,
            py::arg("defaultDate"), py::arg("notional"),
            py::arg("recoveryRate"),
            "Returns the claim amount given default date, notional, and recovery rate.");

    // --- FaceValueClaim ---
    py::classh<FaceValueClaim, Claim>(
        m, "FaceValueClaim",
        "Claim on a notional.")
        .def(py::init<>(),
            "Constructs a face value claim.");

    // --- FaceValueAccrualClaim ---
    py::classh<FaceValueAccrualClaim, Claim>(
        m, "FaceValueAccrualClaim",
        "Claim on the notional of a reference security, including accrual.")
        .def(py::init<const ext::shared_ptr<Bond>&>(),
            py::arg("referenceSecurity"),
            "Constructs from a reference bond.");
}
