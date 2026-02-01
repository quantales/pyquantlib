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
#include <ql/models/shortrate/twofactormodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::twofactormodel(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // TwoFactorModel ABC
    py::class_<TwoFactorModel, ShortRateModel, ext::shared_ptr<TwoFactorModel>>(
        base, "TwoFactorModel",
        "Abstract base class for two-factor short-rate models.");
}
