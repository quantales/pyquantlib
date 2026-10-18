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
#include <ql/indexes/ibor/bbsw.hpp>

using namespace QuantLib;

void ql_indexes::bbsw(py::module_& m) {
    bindTenorIborIndex<Bbsw>(m, "Bbsw",
        "Australian Bank Bill Swap Rate (BBSW) fixed by AFMA.");

    bindFixedTenorIndex<Bbsw1M, Bbsw>(m, "Bbsw1M",
        "1-month BBSW index.");

    bindFixedTenorIndex<Bbsw2M, Bbsw>(m, "Bbsw2M",
        "2-month BBSW index.");

    bindFixedTenorIndex<Bbsw3M, Bbsw>(m, "Bbsw3M",
        "3-month BBSW index.");

    bindFixedTenorIndex<Bbsw4M, Bbsw>(m, "Bbsw4M",
        "4-month BBSW index.");

    bindFixedTenorIndex<Bbsw5M, Bbsw>(m, "Bbsw5M",
        "5-month BBSW index.");

    bindFixedTenorIndex<Bbsw6M, Bbsw>(m, "Bbsw6M",
        "6-month BBSW index.");
}
