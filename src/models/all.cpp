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

DECLARE_MODULE_BINDINGS(models_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_models::model, m,
        "CalibratedModel - base class for calibrated models");
    manager.addFunction(ql_models::parameter, m,
        "Parameter - model parameter with constraints");
    manager.addFunction(ql_models::calibrationhelper, m,
        "CalibrationHelper - base class for calibration helpers");
    manager.addFunction(ql_models::hestonmodel, m,
        "HestonModel - Heston stochastic volatility model");
    manager.addFunction(ql_models::hestonmodelhandle, m,
        "HestonModelHandle - handle to Heston model");
    manager.addFunction(ql_models::piecewisetimedependenthestonmodel, m,
        "PiecewiseTimeDependentHestonModel - time-dependent Heston model");
}
