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
    ADD_MAIN_BINDING(manager, ql_processes::eulerdiscretization,
        "EulerDiscretization - Euler scheme for SDE discretization");
    ADD_MAIN_BINDING(manager, ql_processes::blackscholesprocess,
        "BlackScholesProcess - geometric Brownian motion processes");
    ADD_MAIN_BINDING(manager, ql_processes::hestonprocess,
        "HestonProcess - stochastic volatility process");
    ADD_MAIN_BINDING(manager, ql_processes::stochasticprocessarray,
        "StochasticProcessArray - array of correlated 1D processes");
    ADD_MAIN_BINDING(manager, ql_processes::batesprocess,
        "BatesProcess - Heston process with jumps");
}
