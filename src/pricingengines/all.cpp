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

DECLARE_MODULE_BINDINGS(pricingengines_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_pricingengines::genericmodelengine, m,
        "GenericModelEngine - Generic option engine based on a model");
    manager.addFunction(ql_pricingengines::analyticeuropeanengine, m,
        "AnalyticEuropeanEngine - Black-Scholes European option pricing");
    manager.addFunction(ql_pricingengines::analytichestonengine, m,
        "AnalyticHestonEngine - Heston stochastic volatility pricing");
    manager.addFunction(ql_pricingengines::mceuropeanengine, m,
        "MCEuropeanEngine - Monte Carlo European option pricing");
    manager.addFunction(ql_pricingengines::spreadblackscholesvanillaengine, m,
        "SpreadBlackScholesVanillaEngine - spread option pricing base class");
    manager.addFunction(ql_pricingengines::kirkengine, m,
        "KirkEngine - Kirk spread option pricing");
    manager.addFunction(ql_pricingengines::bjerksundstenslandspreadengine, m,
        "BjerksundStenslandSpreadEngine - Bjerksund-Stensland spread option pricing");
    manager.addFunction(ql_pricingengines::operatorsplittingspreadengine, m,
        "OperatorSplittingSpreadEngine - Operator splitting spread option pricing");
    manager.addFunction(ql_pricingengines::denglizhoubasketengine, m,
        "DengLiZhouBasketEngine - Deng-Li-Zhou N-dim basket option pricing");
    manager.addFunction(ql_pricingengines::stulzengine, m,
        "StulzEngine - Stulz 2D min/max basket option pricing");
    manager.addFunction(ql_pricingengines::mceuropeanbasketengine, m,
        "MCEuropeanBasketEngine - Monte Carlo European basket option pricing");
}
