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
#include <ql/pricingengines/vanilla/fdhestonhullwhitevanillaengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/processes/hullwhiteprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdhestonhullwhitevanillaengine(py::module_& m) {
    py::class_<FdHestonHullWhiteVanillaEngine,
               ext::shared_ptr<FdHestonHullWhiteVanillaEngine>,
               PricingEngine>(
        m, "FdHestonHullWhiteVanillaEngine",
        "Finite-differences Heston + Hull-White vanilla option engine.")
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      ext::shared_ptr<HullWhiteProcess>,
                      Real, Size, Size, Size, Size, Size, bool,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("hwProcess"),
            py::arg("corrEquityShortRate"),
            py::arg("tGrid") = 50,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 40,
            py::arg("rGrid") = 20,
            py::arg("dampingSteps") = 0,
            py::arg("controlVariate") = true,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD Heston-HW engine.")
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      ext::shared_ptr<HullWhiteProcess>,
                      DividendSchedule,
                      Real, Size, Size, Size, Size, Size, bool,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("hwProcess"),
            py::arg("dividends"),
            py::arg("corrEquityShortRate"),
            py::arg("tGrid") = 50,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 40,
            py::arg("rGrid") = 20,
            py::arg("dampingSteps") = 0,
            py::arg("controlVariate") = true,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs FD Heston-HW engine with dividends.");
}
