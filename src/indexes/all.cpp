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
    ADD_BASE_BINDING(manager, ql_indexes::interestrateindex, "InterestRateIndex ABC");
    ADD_MAIN_BINDING(manager, ql_indexes::iborindex, "IborIndex - IBOR index base class");
    ADD_MAIN_BINDING(manager, ql_indexes::euribor, "Euribor - Euribor indexes");
}
