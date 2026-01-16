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

DECLARE_MODULE_BINDINGS(cashflows_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");

    // Abstract base classes
    manager.addFunction(ql_cashflows::coupon, b, "Coupon ABC");

    // Concrete implementations
    manager.addFunction(ql_cashflows::simplecashflow, m, "SimpleCashFlow");
    manager.addFunction(ql_cashflows::fixedratecoupon, m, "FixedRateCoupon");
}
