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

DECLARE_MODULE_BINDINGS(methods_bindings) {
    // finitedifferences/solvers
    ADD_MAIN_BINDING(ql_methods::fdmbackwardsolver,
        "FdmSchemeDesc and FdmSchemeType from fdmbackwardsolver.hpp");
    // Monte Carlo
    ADD_MAIN_BINDING(ql_methods::lsmbasissystem,
        "LsmBasisSystem - polynomial type enum for LSM basis systems");
    ADD_MAIN_BINDING(ql_methods::sample,
        "Sample - weighted sample types for MC simulation");
}
