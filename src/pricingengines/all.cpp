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

DECLARE_MODULE_BINDINGS(pricingengines_bindings) {
    ADD_MAIN_BINDING(ql_pricingengines::blackformula,
        "Black formula functions for option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::genericmodelengine,
        "GenericModelEngine - Generic option engine based on a model");
    ADD_MAIN_BINDING(ql_pricingengines::analyticeuropeanengine,
        "AnalyticEuropeanEngine - Black-Scholes European option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analytichestonengine,
        "AnalyticHestonEngine - Heston stochastic volatility pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mceuropeanengine,
        "MCEuropeanEngine - Monte Carlo European option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::spreadblackscholesvanillaengine,
        "SpreadBlackScholesVanillaEngine - spread option pricing base class");
    ADD_MAIN_BINDING(ql_pricingengines::kirkengine,
        "KirkEngine - Kirk spread option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::bjerksundstenslandspreadengine,
        "BjerksundStenslandSpreadEngine - Bjerksund-Stensland spread option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::operatorsplittingspreadengine,
        "OperatorSplittingSpreadEngine - Operator splitting spread option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::denglizhoubasketengine,
        "DengLiZhouBasketEngine - Deng-Li-Zhou N-dim basket option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::stulzengine,
        "StulzEngine - Stulz 2D min/max basket option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fd2dblackscholesvanillaengine,
        "Fd2dBlackScholesVanillaEngine - 2D FD basket option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mceuropeanbasketengine,
        "MCEuropeanBasketEngine - Monte Carlo European basket option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::baroneadesiwhaleyengine,
        "BaroneAdesiWhaleyApproximationEngine - Barone-Adesi-Whaley American approximation");
    ADD_MAIN_BINDING(ql_pricingengines::bjerksundstenslandengine,
        "BjerksundStenslandApproximationEngine - Bjerksund-Stensland American approximation");
    ADD_MAIN_BINDING(ql_pricingengines::fdblackscholesvanillaengine,
        "FdBlackScholesVanillaEngine - 1D finite-difference vanilla option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::binomialengine,
        "BinomialVanillaEngine - binomial tree vanilla option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mcamericanengine,
        "MCAmericanEngine - Monte Carlo American option pricing (Longstaff-Schwartz)");
    ADD_MAIN_BINDING(ql_pricingengines::integralengine,
        "IntegralEngine - European option pricing using integral approach");
    ADD_MAIN_BINDING(ql_pricingengines::qdfpamericanengine,
        "QdFpAmericanEngine - QD+ fixed-point American option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticeuropeanvasicekengine,
        "AnalyticBlackVasicekEngine - European option with stochastic Vasicek rates");
    ADD_MAIN_BINDING(ql_pricingengines::batesengine,
        "BatesEngine - Analytic Bates model pricing");
    ADD_MAIN_BINDING(ql_pricingengines::discountingbondengine,
        "DiscountingBondEngine - Discounting engine for bonds");
    ADD_MAIN_BINDING(ql_pricingengines::discountingswapengine,
        "DiscountingSwapEngine - Discounting engine for swaps");
    ADD_MAIN_BINDING(ql_pricingengines::treeswaptionengine,
        "TreeSwaptionEngine - Lattice engine for swaptions");
    ADD_MAIN_BINDING(ql_pricingengines::jamshidianswaptionengine,
        "JamshidianSwaptionEngine - Analytic swaption engine using bond option decomposition");
    ADD_MAIN_BINDING(ql_pricingengines::g2swaptionengine,
        "G2SwaptionEngine - Swaption engine for G2++ two-factor model");
    ADD_MAIN_BINDING(ql_pricingengines::fdhullwhiteswaptionengine,
        "FdHullWhiteSwaptionEngine - FD swaption engine for Hull-White model");
    ADD_MAIN_BINDING(ql_pricingengines::fdg2swaptionengine,
        "FdG2SwaptionEngine - FD swaption engine for G2++ two-factor model");
    ADD_MAIN_BINDING(ql_pricingengines::blackcapfloorengine,
        "BlackCapFloorEngine - Black-formula cap/floor engine");
    ADD_MAIN_BINDING(ql_pricingengines::bacheliercapfloorengine,
        "BachelierCapFloorEngine - Bachelier (normal) cap/floor engine");
    ADD_MAIN_BINDING(ql_pricingengines::analyticbarrierengine,
        "AnalyticBarrierEngine - Analytic barrier option engine");
    ADD_MAIN_BINDING(ql_pricingengines::analyticdoublebarrierengine,
        "AnalyticDoubleBarrierEngine - Analytic double barrier option engine");
    ADD_MAIN_BINDING(ql_pricingengines::fdblackscholesbarrierengine,
        "FdBlackScholesBarrierEngine - FD barrier option engine");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcontinuousgeometricasianengine,
        "AnalyticContinuousGeometricAveragePriceAsianEngine - Continuous geometric Asian");
    ADD_MAIN_BINDING(ql_pricingengines::analyticdiscretegeometricasianengine,
        "AnalyticDiscreteGeometricAveragePriceAsianEngine - Discrete geometric Asian");
    ADD_MAIN_BINDING(ql_pricingengines::mcdiscretearithmeticapengine,
        "MCDiscreteArithmeticAPEngine - MC discrete arithmetic Asian");
    ADD_MAIN_BINDING(ql_pricingengines::turnbullwakemanasianengine,
        "TurnbullWakemanAsianEngine - Turnbull-Wakeman Asian approximation");
    ADD_MAIN_BINDING(ql_pricingengines::blackswaptionengine,
        "BlackSwaptionEngine, BachelierSwaptionEngine - swaption engines");
    ADD_MAIN_BINDING(ql_pricingengines::bondfunctions,
        "BondFunctions - static bond analytics");
}
