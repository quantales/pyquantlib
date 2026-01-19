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
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(indexes_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");

    manager.addFunction(ql_indexes::interestrateindex, b, "InterestRateIndex ABC");
    manager.addFunction(ql_indexes::iborindex, m, "IborIndex - IBOR index base class");
    manager.addFunction(ql_indexes::euribor, m, "Euribor - Euribor indexes");
}
