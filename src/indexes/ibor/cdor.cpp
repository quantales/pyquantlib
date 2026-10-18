/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/index_helper.h"
#include <ql/indexes/ibor/cdor.hpp>

using namespace QuantLib;

void ql_indexes::cdor(py::module_& m) {
    bindTenorIborIndex<Cdor>(m, "Cdor",
        "Canadian Dollar Offered Rate (CDOR).");
}
