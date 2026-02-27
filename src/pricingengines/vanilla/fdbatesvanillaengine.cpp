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
#include <ql/pricingengines/vanilla/fdbatesvanillaengine.hpp>
#include <ql/models/equity/batesmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdbatesvanillaengine(py::module_& m) {
    py::class_<FdBatesVanillaEngine,
               ext::shared_ptr<FdBatesVanillaEngine>,
               PricingEngine>(
        m, "FdBatesVanillaEngine",
        "Partial integro finite-differences Bates vanilla option engine.")
        // Basic constructor
        .def(py::init<const ext::shared_ptr<BatesModel>&,
                      Size, Size, Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD Bates engine.")
        // With dividends
        .def(py::init<const ext::shared_ptr<BatesModel>&,
                      DividendSchedule,
                      Size, Size, Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("dividends"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD Bates engine with dividends.");
}
