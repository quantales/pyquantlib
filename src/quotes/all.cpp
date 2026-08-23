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
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(quotes_bindings) {
    ADD_MAIN_BINDING(ql_quotes::simplequote, "SimpleQuote");
    ADD_MAIN_BINDING(ql_quotes::derivedquote, "DerivedQuote");
    ADD_MAIN_BINDING(ql_quotes::compositequote, "CompositeQuote");
    ADD_MAIN_BINDING(ql_quotes::multicompositequote, "MultiCompositeQuote");
    ADD_MAIN_BINDING(ql_quotes::deltavolquote, "DeltaVolQuote");
}
