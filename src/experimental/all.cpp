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

DECLARE_MODULE_BINDINGS(experimental_bindings) {
    // Volatility
    ADD_MAIN_BINDING(ql_experimental::svismilesection,
        "SviSmileSection (Stochastic Volatility Inspired)");

    // Credit
    ADD_MAIN_BINDING(ql_experimental::cdsoption,
        "CdsOption - option on credit default swap");
    ADD_MAIN_BINDING(ql_experimental::blackcdsoptionengine,
        "BlackCdsOptionEngine - Black-formula CDS option engine");
}
