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


DECLARE_MODULE_BINDINGS(math_bindings) {
    auto m = manager.module();
    auto b = manager.getSubmodule("base");
    
    manager.addFunction(ql_math::array, m, "Mathematical array for vector operations");
    manager.addFunction(ql_math::matrix, m, "Mathematical matrix for linear algebra");
    manager.addFunction(ql_math::rounding, m, "Rounding conventions");
    manager.addFunction(ql_math::constraint, b, "Constraint ABC");
    manager.addFunction(ql_math::constraints, m, "Concrete constraint implementations");
    manager.addFunction(ql_math::costfunction, b, "CostFunction ABC");
}
