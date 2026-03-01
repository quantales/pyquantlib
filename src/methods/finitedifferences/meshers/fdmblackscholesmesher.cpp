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
#include <ql/methods/finitedifferences/meshers/fdmblackscholesmesher.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmblackscholesmesher(py::module_& m) {
    py::class_<FdmBlackScholesMesher, Fdm1dMesher,
               ext::shared_ptr<FdmBlackScholesMesher>>(
        m, "FdmBlackScholesMesher",
        "One-dimensional mesher for the Black-Scholes process (in ln(S)).")
        .def(py::init([](Size size,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Time maturity, Real strike,
                         const py::object& xMinConstraint,
                         const py::object& xMaxConstraint,
                         Real eps, Real scaleFactor,
                         const py::object& cPoint,
                         const DividendSchedule& dividendSchedule,
                         const ext::shared_ptr<FdmQuantoHelper>& fdmQuantoHelper,
                         Real spotAdjustment) {
            Real xMin = xMinConstraint.is_none()
                ? Null<Real>() : xMinConstraint.cast<Real>();
            Real xMax = xMaxConstraint.is_none()
                ? Null<Real>() : xMaxConstraint.cast<Real>();
            const Real nr = Null<Real>();
            std::pair<Real, Real> cp(nr, nr);
            if (!cPoint.is_none())
                cp = cPoint.cast<std::pair<Real, Real>>();
            return ext::make_shared<FdmBlackScholesMesher>(
                size, process, maturity, strike,
                xMin, xMax, eps, scaleFactor, cp,
                dividendSchedule, fdmQuantoHelper, spotAdjustment);
        }),
            py::arg("size"),
            py::arg("process"),
            py::arg("maturity"),
            py::arg("strike"),
            py::arg("xMinConstraint") = py::none(),
            py::arg("xMaxConstraint") = py::none(),
            py::arg("eps") = 0.0001,
            py::arg("scaleFactor") = 1.5,
            py::arg("cPoint") = py::none(),
            py::arg("dividendSchedule") = DividendSchedule(),
            py::arg("fdmQuantoHelper") = ext::shared_ptr<FdmQuantoHelper>(),
            py::arg("spotAdjustment") = 0.0,
            "Constructs a Black-Scholes mesher.")
        .def_static("processHelper",
            &FdmBlackScholesMesher::processHelper,
            py::arg("s0"), py::arg("rTS"), py::arg("qTS"), py::arg("vol"),
            "Creates a GeneralizedBlackScholesProcess from basic inputs.");
}
