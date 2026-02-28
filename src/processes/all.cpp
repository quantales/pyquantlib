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

DECLARE_MODULE_BINDINGS(processes_bindings) {
    ADD_MAIN_BINDING(ql_processes::eulerdiscretization,
        "EulerDiscretization - Euler scheme for SDE discretization");
    ADD_MAIN_BINDING(ql_processes::blackscholesprocess,
        "BlackScholesProcess - geometric Brownian motion processes");
    ADD_MAIN_BINDING(ql_processes::hestonprocess,
        "HestonProcess - stochastic volatility process");
    ADD_MAIN_BINDING(ql_processes::stochasticprocessarray,
        "StochasticProcessArray - array of correlated 1D processes");
    ADD_MAIN_BINDING(ql_processes::batesprocess,
        "BatesProcess - Heston process with jumps");
    ADD_MAIN_BINDING(ql_processes::gjrgarchprocess,
        "GJRGARCHProcess - GJR-GARCH(1,1) stochastic process");
    ADD_MAIN_BINDING(ql_processes::ornsteinuhlenbeckprocess,
        "OrnsteinUhlenbeckProcess - mean-reverting OU process");
    ADD_BASE_BINDING(ql_processes::forwardmeasureprocess,
        "ForwardMeasureProcess - forward-measure stochastic process ABCs");
    ADD_MAIN_BINDING(ql_processes::hullwhiteprocess,
        "HullWhiteProcess - Hull-White short-rate processes");
    ADD_MAIN_BINDING(ql_processes::hestonslvprocess,
        "HestonSLVProcess - Heston stochastic local volatility process");
}
