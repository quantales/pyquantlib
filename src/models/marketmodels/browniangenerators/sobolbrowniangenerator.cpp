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
#include <ql/models/marketmodels/browniangenerators/sobolbrowniangenerator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::sobolbrowniangenerator(py::module_& m) {
    py::enum_<SobolBrownianGeneratorBase::Ordering>(m, "Ordering",
        "Ordering schemes for Sobol Brownian generators.")
        .value("Factors", SobolBrownianGeneratorBase::Factors,
            "Best-quality variates for the first factor.")
        .value("Steps", SobolBrownianGeneratorBase::Steps,
            "Best-quality variates for the largest steps.")
        .value("Diagonal", SobolBrownianGeneratorBase::Diagonal,
            "Diagonal schema balancing factors and steps.")
        .export_values();
}
