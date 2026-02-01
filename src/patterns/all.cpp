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


DECLARE_MODULE_BINDINGS(patterns_bindings) {
    ADD_BASE_BINDING(manager, ql_patterns::observer, "Observer ABC");
    ADD_MAIN_BINDING(manager, ql_patterns::observable, "Observable");
    ADD_BASE_BINDING(manager, ql_patterns::lazyobject, "LazyObject ABC");
}
