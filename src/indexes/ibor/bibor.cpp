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
#include <ql/indexes/ibor/bibor.hpp>

using namespace QuantLib;

void ql_indexes::bibor(py::module_& m) {
    bindTenorIborIndex<Bibor>(m, "Bibor",
        "Bangkok Interbank Offered Rate (BIBOR) fixed by the Bank of Thailand.");

    bindFixedTenorIndex<BiborSW, Bibor>(m, "BiborSW",
        "1-week BIBOR index.");

    bindFixedTenorIndex<Bibor1M, Bibor>(m, "Bibor1M",
        "1-month BIBOR index.");

    bindFixedTenorIndex<Bibor2M, Bibor>(m, "Bibor2M",
        "2-month BIBOR index.");

    bindFixedTenorIndex<Bibor3M, Bibor>(m, "Bibor3M",
        "3-month BIBOR index.");

    bindFixedTenorIndex<Bibor6M, Bibor>(m, "Bibor6M",
        "6-month BIBOR index.");

    bindFixedTenorIndex<Bibor1Y, Bibor>(m, "Bibor1Y",
        "1-year BIBOR index.");
}
