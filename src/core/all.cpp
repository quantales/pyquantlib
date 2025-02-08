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
    manager.addFunction(ql_core::settings, m, "Global settings and evaluation date");
    manager.addFunction(ql_core::compounding, m, "Compounding conventions enum");
    manager.addFunction(ql_core::interestrate, m, "Interest rate with compounding algebra");
    manager.addFunction(ql_core::cashflow, b, "Event and CashFlow ABCs");
    manager.addFunction(ql_core::index, b, "Index ABC - market index interface");
    manager.addFunction(ql_core::currency, m, "Currency specification");
    manager.addFunction(ql_core::money, m, "Monetary amount with currency");
    manager.addFunction(ql_core::exchangerate, m, "Exchange rate between currencies");
    manager.addFunction(ql_core::termstructure, b, "TermStructure ABC");
}
