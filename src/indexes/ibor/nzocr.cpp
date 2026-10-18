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
#include <ql/indexes/ibor/nzocr.hpp>

using namespace QuantLib;

void ql_indexes::nzocr(py::module_& m) {
    bindOvernightIndex<Nzocr>(m, "Nzocr",
        "New Zealand Official Cash Rate (OCR) index.");
}
