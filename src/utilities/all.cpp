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

DECLARE_MODULE_BINDINGS(utilities_bindings) {
    auto m = manager.module();  
    manager.addFunction(ql_utilities::observablevalue, m, "ObservableValue - observable wrapper for values");
    manager.addFunction(ql_utilities::null, m, "Null - QuantLib Null utilities");
}
