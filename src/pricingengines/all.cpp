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
    ADD_MAIN_BINDING(ql_pricingengines::midpointcdsengine,
        "MidPointCdsEngine - mid-point CDS engine");
    ADD_MAIN_BINDING(ql_pricingengines::isdacdsengine,
        "IsdaCdsEngine - ISDA-compliant CDS engine");

    // Inflation engines
    ADD_MAIN_BINDING(ql_pricingengines::inflationcapfloorengines,
        "YoYInflation Black/UnitDisplaced/Bachelier CapFloorEngine");

    ADD_MAIN_BINDING(ql_pricingengines::replicatingvarianceswapengine,
        "ReplicatingVarianceSwapEngine - variance swap replicating portfolio");
    ADD_MAIN_BINDING(ql_pricingengines::binomialconvertibleengine,
        "BinomialConvertibleEngine - binomial tree convertible bond pricing");

    // Lookback engines
    ADD_MAIN_BINDING(ql_pricingengines::analyticcontinuousfloatinglookbackengine,
        "AnalyticContinuousFloatingLookbackEngine - floating-strike lookback");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcontinuousfixedlookbackengine,
        "AnalyticContinuousFixedLookbackEngine - fixed-strike lookback");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcontinuouspartialfloatinglookbackengine,
        "AnalyticContinuousPartialFloatingLookbackEngine - partial floating lookback");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcontinuouspartialfixedlookbackengine,
        "AnalyticContinuousPartialFixedLookbackEngine - partial fixed lookback");

    // Cliquet, compound, chooser engines
    ADD_MAIN_BINDING(ql_pricingengines::analyticcliquetengine,
        "AnalyticCliquetEngine - cliquet option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcompoundoptionengine,
        "AnalyticCompoundOptionEngine - compound option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticsimplechooserengine,
        "AnalyticSimpleChooserEngine - simple chooser option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticcomplexchooserengine,
        "AnalyticComplexChooserEngine - complex chooser option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticeuropeanmargrabeengine,
        "AnalyticEuropeanMargrabeEngine - European exchange option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticamericanmargrabeengine,
        "AnalyticAmericanMargrabeEngine - American exchange option pricing");

    // Forward engines
    ADD_MAIN_BINDING(ql_pricingengines::forwardengine,
        "ForwardEuropeanEngine, ForwardPerformanceEuropeanEngine");

    // Quanto engines
    ADD_MAIN_BINDING(ql_pricingengines::quantoengine,
        "QuantoVanillaEngine, QuantoForwardVanillaEngine - quanto option pricing");

    // Calculators
    ADD_MAIN_BINDING(ql_pricingengines::blackcalculator,
        "BlackCalculator - Black 1976 pricing and Greeks calculator");
    ADD_MAIN_BINDING(ql_pricingengines::bacheliercalculator,
        "BachelierCalculator - Bachelier (normal-vol) pricing and Greeks calculator");

    // FD vanilla engines
    ADD_MAIN_BINDING(ql_pricingengines::fdhestonvanillaengine,
        "FdHestonVanillaEngine + MakeFdHestonVanillaEngine - FD Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdbatesvanillaengine,
        "FdBatesVanillaEngine - FD Bates (Heston + jumps) pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdsabrvanillaengine,
        "FdSabrVanillaEngine - FD SABR pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdcevvanillaengine,
        "FdCEVVanillaEngine - FD CEV pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdblackscholesshoutengine,
        "FdBlackScholesShoutEngine - FD Black-Scholes shout option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdhestonhullwhitevanillaengine,
        "FdHestonHullWhiteVanillaEngine - FD Heston + Hull-White pricing");
    ADD_MAIN_BINDING(ql_pricingengines::fdornsteinuhlenbeckvanillaengine,
        "FdOrnsteinUhlenbeckVanillaEngine - FD Ornstein-Uhlenbeck pricing");

    // Heston engine ecosystem
    ADD_MAIN_BINDING(ql_pricingengines::coshestonengine,
        "COSHestonEngine - Fourier-cosine series Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::exponentialfittinghestonengine,
        "ExponentialFittingHestonEngine - exponential fitting Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticptdhestonengine,
        "AnalyticPTDHestonEngine - piecewise time-dependent Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticpdfhestonengine,
        "AnalyticPDFHestonEngine - PDF-based Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analytichestonhullwhiteengine,
        "AnalyticHestonHullWhiteEngine - Heston + Hull-White stochastic rates");
    ADD_MAIN_BINDING(ql_pricingengines::analytich1hwengine,
        "AnalyticH1HWEngine - H1-HW approximation with equity-rate correlation");
    ADD_MAIN_BINDING(ql_pricingengines::hestonexpansionengine,
        "HestonExpansionEngine - analytic expansion Heston pricing");

    // American, digital, dividend engines
    ADD_MAIN_BINDING(ql_pricingengines::juquadraticengine,
        "JuQuadraticApproximationEngine - Ju quadratic American approximation");
    ADD_MAIN_BINDING(ql_pricingengines::qdplusamericanengine,
        "QdPlusAmericanEngine - QD+ American option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticdigitalamericanengine,
        "AnalyticDigitalAmericanEngine - analytic digital American pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mcdigitalengine,
        "MCDigitalEngine - Monte Carlo digital option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticdividendeuropeanengine,
        "AnalyticDividendEuropeanEngine - European with discrete dividends");
    ADD_MAIN_BINDING(ql_pricingengines::analyticbsmhullwhiteengine,
        "AnalyticBSMHullWhiteEngine - BSM + Hull-White stochastic rates");

    // Cap/floor engines
    ADD_MAIN_BINDING(ql_pricingengines::analyticcapfloorengine,
        "AnalyticCapFloorEngine - analytic cap/floor for affine models");
    ADD_MAIN_BINDING(ql_pricingengines::treecapfloorengine,
        "TreeCapFloorEngine - lattice cap/floor engine");
    ADD_MAIN_BINDING(ql_pricingengines::gaussian1dcapfloorengine,
        "Gaussian1dCapFloorEngine - Gaussian 1-D cap/floor engine");

    // Gaussian1D swaption engines
    ADD_MAIN_BINDING(ql_pricingengines::gaussian1dswaptionengine,
        "Gaussian1dSwaptionEngine - Gaussian 1-D swaption engine");
    ADD_MAIN_BINDING(ql_pricingengines::gaussian1djamshidianswaptionengine,
        "Gaussian1dJamshidianSwaptionEngine - Gaussian 1-D Jamshidian swaption engine");
    ADD_MAIN_BINDING(ql_pricingengines::gaussian1dnonstandardswaptionengine,
        "Gaussian1dNonstandardSwaptionEngine - Gaussian 1-D nonstandard swaption engine");
    ADD_MAIN_BINDING(ql_pricingengines::gaussian1dfloatfloatswaptionengine,
        "Gaussian1dFloatFloatSwaptionEngine - Gaussian 1-D float-float swaption engine");

    // Exotic option engines
    ADD_MAIN_BINDING(ql_pricingengines::analyticholderextensibleoptionengine,
        "AnalyticHolderExtensibleOptionEngine - holder-extensible option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analyticwriterextensibleoptionengine,
        "AnalyticWriterExtensibleOptionEngine - writer-extensible option pricing");
    ADD_MAIN_BINDING(ql_pricingengines::analytictwoassetcorrelationengine,
        "AnalyticTwoAssetCorrelationEngine - two-asset correlation option pricing");

    ADD_MAIN_BINDING(ql_pricingengines::analyticgjrgarchengine,
        "AnalyticGJRGARCHEngine - analytic GJR-GARCH option pricing");

    // MC engines
    ADD_MAIN_BINDING(ql_pricingengines::mcforwardeuropeanbsengine,
        "MCForwardEuropeanBSEngine - MC forward-start BS pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mcforwardeuropeanhestonengine,
        "MCForwardEuropeanHestonEngine - MC forward-start Heston pricing");
    ADD_MAIN_BINDING(ql_pricingengines::mceuropeanhestonengine,
        "MCEuropeanHestonEngine - MC European Heston pricing");
}
