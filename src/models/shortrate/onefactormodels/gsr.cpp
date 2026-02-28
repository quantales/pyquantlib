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
#include <ql/models/shortrate/onefactormodels/gsr.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/models/calibrationhelper.hpp>
#include <ql/math/optimization/method.hpp>
#include <ql/math/optimization/endcriteria.hpp>
#include <ql/math/optimization/constraint.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::gsr(py::module_& m) {
    py::class_<Gsr, Gaussian1dModel, CalibratedModel,
               ext::shared_ptr<Gsr>>(
        m, "Gsr",
        "Gaussian short-rate model (GSR) in forward measure.")
        // Constructor 1: constant mean reversion, static data
        .def(py::init<const Handle<YieldTermStructure>&,
                      std::vector<Date>, const std::vector<Real>&,
                      Real, Real>(),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversion"),
            py::arg("T") = 60.0,
            "Constructs GSR with constant mean reversion.")
        // Constructor 2: piecewise mean reversion, static data
        .def(py::init<const Handle<YieldTermStructure>&,
                      std::vector<Date>, const std::vector<Real>&,
                      const std::vector<Real>&, Real>(),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversions"),
            py::arg("T") = 60.0,
            "Constructs GSR with piecewise mean reversion.")
        // Constructor 3: constant mean reversion, floating data
        .def(py::init<const Handle<YieldTermStructure>&,
                      std::vector<Date>, std::vector<Handle<Quote>>,
                      const Handle<Quote>&, Real>(),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversion"),
            py::arg("T") = 60.0,
            "Constructs GSR with constant mean reversion (floating data).")
        // Constructor 4: piecewise mean reversion, floating data
        .def(py::init<const Handle<YieldTermStructure>&,
                      std::vector<Date>, std::vector<Handle<Quote>>,
                      std::vector<Handle<Quote>>, Real>(),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversions"),
            py::arg("T") = 60.0,
            "Constructs GSR with piecewise mean reversion (floating data).")
        // Hidden handle constructors (static data only)
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                         std::vector<Date> volstepdates,
                         const std::vector<Real>& volatilities,
                         Real reversion, Real T) {
            return ext::make_shared<Gsr>(
                Handle<YieldTermStructure>(ts),
                std::move(volstepdates), volatilities, reversion, T);
        }),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversion"),
            py::arg("T") = 60.0,
            "Constructs GSR with constant mean reversion (handle created internally).")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                         std::vector<Date> volstepdates,
                         const std::vector<Real>& volatilities,
                         const std::vector<Real>& reversions, Real T) {
            return ext::make_shared<Gsr>(
                Handle<YieldTermStructure>(ts),
                std::move(volstepdates), volatilities, reversions, T);
        }),
            py::arg("termStructure"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("reversions"),
            py::arg("T") = 60.0,
            "Constructs GSR with piecewise mean reversion (handle created internally).")
        // Methods
        .def("numeraireTime",
            py::overload_cast<>(&Gsr::numeraireTime, py::const_),
            "Returns the forward measure time.")
        .def("setNumeraireTime",
            py::overload_cast<Real>(&Gsr::numeraireTime),
            py::arg("T"),
            "Sets the forward measure time.")
        .def("reversion", &Gsr::reversion,
            "Returns the mean reversion parameters.")
        .def("volatility", &Gsr::volatility,
            "Returns the volatility parameters.")
        // Calibration constraint helpers
        .def("FixedReversions", &Gsr::FixedReversions,
            "Returns fix-parameter mask with all reversions fixed.")
        .def("FixedVolatilities", &Gsr::FixedVolatilities,
            "Returns fix-parameter mask with all volatilities fixed.")
        .def("MoveVolatility", &Gsr::MoveVolatility,
            py::arg("i"),
            "Returns fix-parameter mask with only volatility i free.")
        .def("MoveReversion", &Gsr::MoveReversion,
            py::arg("i"),
            "Returns fix-parameter mask with only reversion i free.")
        // Iterative calibration
        .def("calibrateVolatilitiesIterative",
            &Gsr::calibrateVolatilitiesIterative,
            py::arg("helpers"),
            py::arg("method"),
            py::arg("endCriteria"),
            py::arg("constraint") = Constraint(),
            py::arg("weights") = std::vector<Real>(),
            "Calibrates volatilities one by one to helpers.")
        .def("calibrateReversionsIterative",
            &Gsr::calibrateReversionsIterative,
            py::arg("helpers"),
            py::arg("method"),
            py::arg("endCriteria"),
            py::arg("constraint") = Constraint(),
            py::arg("weights") = std::vector<Real>(),
            "Calibrates reversions one by one to helpers.");
}
