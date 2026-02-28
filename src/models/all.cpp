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

DECLARE_MODULE_BINDINGS(models_bindings) {
    ADD_MAIN_BINDING(ql_models::model,
        "CalibratedModel - base class for calibrated models");
    ADD_MAIN_BINDING(ql_models::parameter,
        "Parameter - model parameter with constraints");
    ADD_MAIN_BINDING(ql_models::calibrationhelper,
        "CalibrationHelper - base class for calibration helpers");
    ADD_MAIN_BINDING(ql_models::hestonmodel,
        "HestonModel - Heston stochastic volatility model");
    ADD_MAIN_BINDING(ql_models::hestonmodelhandle,
        "HestonModelHandle - handle to Heston model");
    ADD_MAIN_BINDING(ql_models::piecewisetimedependenthestonmodel,
        "PiecewiseTimeDependentHestonModel - time-dependent Heston model");
    ADD_MAIN_BINDING(ql_models::onefactormodel,
        "OneFactorModel - single-factor short-rate model base classes");
    ADD_MAIN_BINDING(ql_models::twofactormodel,
        "TwoFactorModel - two-factor short-rate model base class");
    ADD_MAIN_BINDING(ql_models::vasicek,
        "Vasicek - Vasicek short-rate model");
    ADD_MAIN_BINDING(ql_models::hullwhite,
        "HullWhite - Hull-White extended Vasicek model");
    ADD_MAIN_BINDING(ql_models::blackkarasinski,
        "BlackKarasinski - Black-Karasinski short-rate model");
    ADD_MAIN_BINDING(ql_models::g2,
        "G2 - Two-additive-factor Gaussian model G2++");
    ADD_MAIN_BINDING(ql_models::batesmodel,
        "BatesModel - Heston model with jumps");
    ADD_MAIN_BINDING(ql_models::swaptionhelper,
        "SwaptionHelper - calibration helper for swaptions");
    ADD_MAIN_BINDING(ql_models::caphelper,
        "CapHelper - calibration helper for ATM caps");
    ADD_MAIN_BINDING(ql_models::hestonmodelhelper,
        "HestonModelHelper - calibration helper for Heston model");
    ADD_MAIN_BINDING(ql_models::coxingersollross,
        "CoxIngersollRoss - CIR short-rate model");
    ADD_MAIN_BINDING(ql_models::extendedcoxingersollross,
        "ExtendedCoxIngersollRoss - extended CIR fitted to term structure");
    ADD_MAIN_BINDING(ql_models::gaussian1dmodel,
        "Gaussian1dModel - abstract Gaussian 1-D short-rate model");
    ADD_MAIN_BINDING(ql_models::gsr,
        "Gsr - Gaussian short-rate model in forward measure");
    ADD_MAIN_BINDING(ql_models::markovfunctional,
        "MarkovFunctional - Markov Functional 1-factor model");
    ADD_MAIN_BINDING(ql_models::gjrgarchmodel,
        "GJRGARCHModel - GJR-GARCH(1,1) calibrated model");
    // Brownian generators (ABCs + Sobol registered in math/all.cpp)
    ADD_MAIN_BINDING(ql_models::mtbrowniangenerator,
        "MTBrownianGenerator - Mersenne-Twister Brownian generator");
}
