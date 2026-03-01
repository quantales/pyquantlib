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
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopiterator.hpp>
#include <ql/instruments/basketoption.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdminnervaluecalculator(py::module_& m) {
    // ABC on base submodule
    auto base = py::module_::import("pyquantlib.base");
    py::class_<FdmInnerValueCalculator,
               ext::shared_ptr<FdmInnerValueCalculator>>(
        base, "FdmInnerValueCalculator",
        "Abstract base for inner value calculations on FDM grids.")
        .def("innerValue", &FdmInnerValueCalculator::innerValue,
            py::arg("iter"), py::arg("t"),
            "Returns inner value at grid point.")
        .def("avgInnerValue", &FdmInnerValueCalculator::avgInnerValue,
            py::arg("iter"), py::arg("t"),
            "Returns cell-averaged inner value at grid point.");

    // FdmCellAveragingInnerValue
    py::class_<FdmCellAveragingInnerValue,
               ext::shared_ptr<FdmCellAveragingInnerValue>,
               FdmInnerValueCalculator>(
        m, "FdmCellAveragingInnerValue",
        "Cell-averaging inner value calculator for FDM grids.")
        .def(py::init([](const ext::shared_ptr<Payoff>& payoff,
                         const ext::shared_ptr<FdmMesher>& mesher,
                         Size direction,
                         const py::object& gridMapping) {
            if (gridMapping.is_none())
                return ext::make_shared<FdmCellAveragingInnerValue>(
                    payoff, mesher, direction);
            return ext::make_shared<FdmCellAveragingInnerValue>(
                payoff, mesher, direction,
                gridMapping.cast<std::function<Real(Real)>>());
        }),
            py::arg("payoff"), py::arg("mesher"),
            py::arg("direction"),
            py::arg("gridMapping") = py::none(),
            "Constructs with payoff, mesher, direction, and optional grid mapping.");

    // FdmLogInnerValue
    py::class_<FdmLogInnerValue,
               ext::shared_ptr<FdmLogInnerValue>,
               FdmCellAveragingInnerValue>(
        m, "FdmLogInnerValue",
        "Log-space inner value calculator for equity options.")
        .def(py::init<const ext::shared_ptr<Payoff>&,
                      const ext::shared_ptr<FdmMesher>&,
                      Size>(),
            py::arg("payoff"), py::arg("mesher"), py::arg("direction"),
            "Constructs with payoff, mesher, and direction.");

    // FdmLogBasketInnerValue
    py::class_<FdmLogBasketInnerValue,
               ext::shared_ptr<FdmLogBasketInnerValue>,
               FdmInnerValueCalculator>(
        m, "FdmLogBasketInnerValue",
        "Log-space inner value calculator for basket options.")
        .def(py::init<ext::shared_ptr<BasketPayoff>,
                      ext::shared_ptr<FdmMesher>>(),
            py::arg("payoff"), py::arg("mesher"),
            "Constructs with basket payoff and mesher.");

    // FdmZeroInnerValue
    py::class_<FdmZeroInnerValue,
               ext::shared_ptr<FdmZeroInnerValue>,
               FdmInnerValueCalculator>(
        m, "FdmZeroInnerValue",
        "Zero inner value calculator (always returns 0).")
        .def(py::init<>());
}
