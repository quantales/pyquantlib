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
#include <ql/experimental/finitedifferences/fdornsteinuhlenbeckvanillaengine.hpp>
#include <ql/processes/ornsteinuhlenbeckprocess.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdornsteinuhlenbeckvanillaengine(py::module_& m) {
    py::class_<FdOrnsteinUhlenbeckVanillaEngine,
               ext::shared_ptr<FdOrnsteinUhlenbeckVanillaEngine>,
               PricingEngine>(
        m, "FdOrnsteinUhlenbeckVanillaEngine",
        "Finite-differences Ornstein-Uhlenbeck vanilla option engine.")
        .def(py::init<ext::shared_ptr<OrnsteinUhlenbeckProcess>,
                      const ext::shared_ptr<YieldTermStructure>&,
                      Size, Size, Size, Real,
                      const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("riskFreeRate"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("epsilon") = 0.0001,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD OU engine.")
        .def(py::init<ext::shared_ptr<OrnsteinUhlenbeckProcess>,
                      const ext::shared_ptr<YieldTermStructure>&,
                      DividendSchedule,
                      Size, Size, Size, Real,
                      const FdmSchemeDesc&>(),
            py::arg("process"),
            py::arg("riskFreeRate"),
            py::arg("dividends"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("epsilon") = 0.0001,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs FD OU engine with dividends.");
}
