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

DECLARE_MODULE_BINDINGS(quotes_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_quotes::simplequote, m, "SimpleQuote");
    manager.addFunction(ql_quotes::derivedquote, m, "DerivedQuote");
    manager.addFunction(ql_quotes::compositequote, m, "CompositeQuote");
}
