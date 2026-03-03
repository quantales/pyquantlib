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
#include <ql/cashflows/replication.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::replication(py::module_& m) {
    py::enum_<Replication::Type>(m, "ReplicationType",
        "Digital option replication strategy.")
        .value("Sub", Replication::Sub,
            "Sub-replication (lower bound).")
        .value("Central", Replication::Central,
            "Central replication.")
        .value("Super", Replication::Super,
            "Super-replication (upper bound).");

    py::class_<DigitalReplication, ext::shared_ptr<DigitalReplication>>(
        m, "DigitalReplication",
        "Digital option replication configuration.")
        .def(py::init<Replication::Type, Real>(),
            py::arg("replicationType") = Replication::Central,
            py::arg("gap") = 1e-4,
            "Constructs with replication type and gap.")
        .def("replicationType", &DigitalReplication::replicationType,
            "Returns the replication type.")
        .def("gap", &DigitalReplication::gap,
            "Returns the gap size.");
}
