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
#include <ql/models/shortrate/onefactormodel.hpp>
#include <ql/option.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::onefactormodel(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // OneFactorModel ABC
    py::class_<OneFactorModel, ShortRateModel, ext::shared_ptr<OneFactorModel>>(
        base, "OneFactorModel",
        "Abstract base class for single-factor short-rate models.");

    // OneFactorAffineModel ABC
    py::class_<OneFactorAffineModel, OneFactorModel, AffineModel,
               ext::shared_ptr<OneFactorAffineModel>>(
        base, "OneFactorAffineModel",
        "Abstract base class for single-factor affine short-rate models.")
        .def("discountBond",
            py::overload_cast<Time, Time, Rate>(&OneFactorAffineModel::discountBond, py::const_),
            py::arg("now"), py::arg("maturity"), py::arg("rate"),
            "Returns the discount bond price P(now, maturity, rate).");
}
