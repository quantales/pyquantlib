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
#include <ql/experimental/coupons/swapspreadindex.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::swapspreadindex(py::module_& m) {
    py::class_<SwapSpreadIndex, InterestRateIndex,
               ext::shared_ptr<SwapSpreadIndex>>(
        m, "SwapSpreadIndex",
        "Index for the spread between two swap rates.")
        .def(py::init<const std::string&,
                      const ext::shared_ptr<SwapIndex>&,
                      ext::shared_ptr<SwapIndex>,
                      Real, Real>(),
            py::arg("familyName"),
            py::arg("swapIndex1"),
            py::arg("swapIndex2"),
            py::arg("gearing1") = 1.0,
            py::arg("gearing2") = -1.0,
            "Constructs a swap spread index.")
        .def("swapIndex1", &SwapSpreadIndex::swapIndex1,
            "Returns the first swap index.")
        .def("swapIndex2", &SwapSpreadIndex::swapIndex2,
            "Returns the second swap index.")
        .def("gearing1", &SwapSpreadIndex::gearing1,
            "Returns the gearing for the first index.")
        .def("gearing2", &SwapSpreadIndex::gearing2,
            "Returns the gearing for the second index.");
}
