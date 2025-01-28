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


DECLARE_MODULE_BINDINGS(core_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");
    
    manager.addFunction(ql_core::constants, m, "Mathematical and financial constants");
    manager.addFunction(ql_core::quote, b, "Quote ABC - market data interface");
    manager.addFunction(ql_core::quotehandle, m, "Handle<Quote> - smart pointer to quotes");
    manager.addFunction(ql_core::relinkablequotehandle, m, "RelinkableHandle<Quote> - relinkable quote pointer");
}
