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
#include <ql/pricingengines/capfloor/gaussian1dcapfloorengine.hpp>
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::gaussian1dcapfloorengine(py::module_& m) {
    py::class_<Gaussian1dCapFloorEngine,
               ext::shared_ptr<Gaussian1dCapFloorEngine>,
               PricingEngine>(
        m, "Gaussian1dCapFloorEngine",
        "Gaussian 1-D cap/floor pricing engine.")
        .def(py::init<const ext::shared_ptr<Gaussian1dModel>&,
                      int, Real, bool, bool,
                      Handle<YieldTermStructure>>(),
            py::arg("model"),
            py::arg("integrationPoints") = 64,
            py::arg("stddevs") = 7.0,
            py::arg("extrapolatePayoff") = true,
            py::arg("flatPayoffExtrapolation") = false,
            py::arg("discountCurve") = Handle<YieldTermStructure>(),
            "Constructs Gaussian 1-D cap/floor engine.");
}
