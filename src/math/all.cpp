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


DECLARE_MODULE_BINDINGS(math_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");
    
    manager.addFunction(ql_math::array, m, "Mathematical array for vector operations");
    manager.addFunction(ql_math::matrix, m, "Mathematical matrix for linear algebra");
    manager.addFunction(ql_math::rounding, m, "Rounding conventions");
    manager.addFunction(ql_math::constraint, b, "Constraint ABC");
    manager.addFunction(ql_math::constraints, m, "Concrete constraint implementations");
    manager.addFunction(ql_math::costfunction, b, "CostFunction ABC");
    manager.addFunction(ql_math::optimizationmethod, b, "OptimizationMethod ABC");
    manager.addFunction(ql_math::endcriteria, m, "End criteria for optimization");
    manager.addFunction(ql_math::problem, m, "Optimization problem");
    manager.addFunction(ql_math::levenbergmarquardt, m, "Levenberg-Marquardt optimizer");
    manager.addFunction(ql_math::extrapolation, b, "Extrapolator base class");
}
