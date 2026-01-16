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
    auto m = manager.module();

    manager.addFunction(ql_processes::eulerdiscretization, m,
        "EulerDiscretization - Euler scheme for SDE discretization");
    manager.addFunction(ql_processes::blackscholesprocess, m,
        "BlackScholesProcess - geometric Brownian motion processes");
    manager.addFunction(ql_processes::hestonprocess, m,
        "HestonProcess - stochastic volatility process");
    manager.addFunction(ql_processes::stochasticprocessarray, m,
        "StochasticProcessArray - array of correlated 1D processes");
}
