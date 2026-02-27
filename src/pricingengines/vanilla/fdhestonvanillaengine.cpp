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
#include <ql/pricingengines/vanilla/fdhestonvanillaengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdhestonvanillaengine(py::module_& m) {
    py::class_<FdHestonVanillaEngine,
               ext::shared_ptr<FdHestonVanillaEngine>,
               PricingEngine>(
        m, "FdHestonVanillaEngine",
        "Finite-differences Heston vanilla option engine.")
        // Basic constructor
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      Size, Size, Size, Size,
                      const FdmSchemeDesc&,
                      ext::shared_ptr<LocalVolTermStructure>,
                      Real>(),
            py::arg("model"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("leverageFct") = ext::shared_ptr<LocalVolTermStructure>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs FD Heston engine.")
        // With dividends
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      DividendSchedule,
                      Size, Size, Size, Size,
                      const FdmSchemeDesc&,
                      ext::shared_ptr<LocalVolTermStructure>,
                      Real>(),
            py::arg("model"),
            py::arg("dividends"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("leverageFct") = ext::shared_ptr<LocalVolTermStructure>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs FD Heston engine with dividends.")
        .def("enableMultipleStrikesCaching",
            &FdHestonVanillaEngine::enableMultipleStrikesCaching,
            py::arg("strikes"),
            "Enables caching for multiple strikes.");

    // MakeFdHestonVanillaEngine builder
    py::class_<MakeFdHestonVanillaEngine>(
        m, "MakeFdHestonVanillaEngine",
        "Builder for FdHestonVanillaEngine.")
        .def(py::init<ext::shared_ptr<HestonModel>>(),
            py::arg("hestonModel"),
            "Constructs the builder.")
        .def("withTGrid", &MakeFdHestonVanillaEngine::withTGrid,
            py::arg("tGrid"),
            py::return_value_policy::reference_internal)
        .def("withXGrid", &MakeFdHestonVanillaEngine::withXGrid,
            py::arg("xGrid"),
            py::return_value_policy::reference_internal)
        .def("withVGrid", &MakeFdHestonVanillaEngine::withVGrid,
            py::arg("vGrid"),
            py::return_value_policy::reference_internal)
        .def("withDampingSteps", &MakeFdHestonVanillaEngine::withDampingSteps,
            py::arg("dampingSteps"),
            py::return_value_policy::reference_internal)
        .def("withFdmSchemeDesc", &MakeFdHestonVanillaEngine::withFdmSchemeDesc,
            py::arg("schemeDesc"),
            py::return_value_policy::reference_internal)
        .def("withCashDividends", &MakeFdHestonVanillaEngine::withCashDividends,
            py::arg("dividendDates"),
            py::arg("dividendAmounts"),
            py::return_value_policy::reference_internal)
        .def("engine",
            [](const MakeFdHestonVanillaEngine& builder) {
                return static_cast<ext::shared_ptr<PricingEngine>>(builder);
            },
            "Returns the pricing engine.");
}
