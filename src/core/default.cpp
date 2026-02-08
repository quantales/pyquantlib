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
#include <ql/default.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::protectionside(py::module_& m) {
    py::enum_<Protection::Side>(m, "ProtectionSide",
        "Protection buyer or seller.")
        .value("Buyer", Protection::Buyer, "Protection buyer.")
        .value("Seller", Protection::Seller, "Protection seller.");
}
