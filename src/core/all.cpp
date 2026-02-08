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


DECLARE_MODULE_BINDINGS(core_bindings) {
    ADD_MAIN_BINDING(ql_core::constants, "Mathematical and financial constants");
    ADD_BASE_BINDING(ql_core::quote, "Quote ABC - market data interface");
    ADD_MAIN_BINDING(ql_core::quotehandle, "Handle<Quote> - smart pointer to quotes");
    ADD_MAIN_BINDING(ql_core::relinkablequotehandle, "RelinkableHandle<Quote> - relinkable quote pointer");
    ADD_MAIN_BINDING(ql_core::settings, "Global settings and evaluation date");
    ADD_MAIN_BINDING(ql_core::compounding, "Compounding conventions enum");
    ADD_MAIN_BINDING(ql_core::interestrate, "Interest rate with compounding algebra");
    ADD_BASE_BINDING(ql_core::cashflow, "Event and CashFlow ABCs");
    ADD_BASE_BINDING(ql_core::index, "Index ABC - market index interface");
    ADD_MAIN_BINDING(ql_core::currency, "Currency specification");
    ADD_MAIN_BINDING(ql_core::money, "Monetary amount with currency");
    ADD_MAIN_BINDING(ql_core::exchangerate, "Exchange rate between currencies");
    ADD_BASE_BINDING(ql_core::termstructure, "TermStructure ABC");
    ADD_MAIN_BINDING(ql_core::exercise, "Option exercise styles");
    ADD_BASE_BINDING(ql_core::pricingengine, "PricingEngine ABC");
    ADD_BASE_BINDING(ql_core::instrument, "Instrument ABC");
    ADD_MAIN_BINDING(ql_core::option, "Option ABC and Greeks");
    ADD_MAIN_BINDING(ql_core::timegrid, "Time grid for discretized models");
    ADD_MAIN_BINDING(ql_core::payoff, "Payoff ABC");
    ADD_MAIN_BINDING(ql_core::stochasticprocess, "StochasticProcess ABCs");
    ADD_MAIN_BINDING(ql_core::protectionside,
        "Protection::Side - Buyer/Seller enum");
    ADD_MAIN_BINDING(ql_core::cdspricingmodel,
        "CreditDefaultSwap::PricingModel enum");
}
