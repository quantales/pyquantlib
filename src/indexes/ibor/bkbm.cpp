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
#include <ql/indexes/ibor/bkbm.hpp>

using namespace QuantLib;

void ql_indexes::bkbm(py::module_& m) {
    bindTenorIborIndex<Bkbm>(m, "Bkbm",
        "New Zealand Bank Bill Benchmark rate (BKBM).");

    bindFixedTenorIndex<Bkbm1M, Bkbm>(m, "Bkbm1M",
        "1-month BKBM index.");

    bindFixedTenorIndex<Bkbm2M, Bkbm>(m, "Bkbm2M",
        "2-month BKBM index.");

    bindFixedTenorIndex<Bkbm3M, Bkbm>(m, "Bkbm3M",
        "3-month BKBM index.");

    bindFixedTenorIndex<Bkbm4M, Bkbm>(m, "Bkbm4M",
        "4-month BKBM index.");

    bindFixedTenorIndex<Bkbm5M, Bkbm>(m, "Bkbm5M",
        "5-month BKBM index.");

    bindFixedTenorIndex<Bkbm6M, Bkbm>(m, "Bkbm6M",
        "6-month BKBM index.");
}
