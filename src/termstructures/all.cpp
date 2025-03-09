/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(termstructures_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");

    // Abstract base classes
    manager.addFunction(ql_termstructures::yieldtermstructure, b,
        "YieldTermStructure ABC");

    // Handle types
    manager.addFunction(ql_termstructures::yieldtermstructurehandle, m,
        "Handle<YieldTermStructure>");
    manager.addFunction(ql_termstructures::relinkableyieldtermstructurehandle, m,
        "RelinkableHandle<YieldTermStructure>");

    // Concrete implementations
    manager.addFunction(ql_termstructures::flatforward, m,
        "FlatForward yield curve");
}
