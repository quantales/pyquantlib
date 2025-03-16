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

DECLARE_MODULE_BINDINGS(processes_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_processes::eulerdiscretization, m,
        "EulerDiscretization - Euler scheme for SDE discretization");
    manager.addFunction(ql_processes::blackscholesprocess, m,
        "BlackScholesProcess - geometric Brownian motion processes");
    manager.addFunction(ql_processes::hestonprocess, m,
        "HestonProcess - stochastic volatility process");
}
