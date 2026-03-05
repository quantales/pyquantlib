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
#include <ql/indexes/bmaindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::bmaindex(py::module_& m) {
    py::class_<BMAIndex, InterestRateIndex,
               ext::shared_ptr<BMAIndex>>(
        m, "BMAIndex",
        "Bond Market Association index (tax-exempt reference rate).")
        // No-arg constructor (empty handle)
        .def(py::init<>(),
            "Constructs a BMA index without a forwarding curve.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>>(),
            py::arg("h"),
            "Constructs a BMA index from yield curve handle.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<BMAIndex>(
                Handle<YieldTermStructure>(curve));
        }),
            py::arg("curve"),
            "Constructs from yield curve (handle created internally).")
        .def("isValidFixingDate", &BMAIndex::isValidFixingDate,
            py::arg("fixingDate"),
            "Returns true if the date is a valid BMA fixing date.")
        .def("forwardingTermStructure", &BMAIndex::forwardingTermStructure,
            "Returns the forwarding term structure handle.")
        .def("fixingSchedule",
            &BMAIndex::fixingSchedule,
            py::arg("start"), py::arg("end"),
            "Returns the fixing schedule between two dates.");
}
