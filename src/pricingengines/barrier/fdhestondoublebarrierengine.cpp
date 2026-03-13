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
#include <ql/pricingengines/barrier/fdhestondoublebarrierengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdhestondoublebarrierengine(py::module_& m) {
    py::class_<FdHestonDoubleBarrierEngine, PricingEngine,
               ext::shared_ptr<FdHestonDoubleBarrierEngine>>(
        m, "FdHestonDoubleBarrierEngine",
        "Finite-difference Heston double barrier option engine.")
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      Size, Size, Size, Size,
                      const FdmSchemeDesc&>(),
            py::arg("model"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("vGrid") = 50,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs engine.");
}
