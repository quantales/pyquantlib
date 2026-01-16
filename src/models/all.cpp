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
