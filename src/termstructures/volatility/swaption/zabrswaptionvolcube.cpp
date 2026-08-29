/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/volatility/swaption/zabrswaptionvolatilitycube.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/math/optimization/endcriteria.hpp>
#include <ql/math/optimization/method.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::zabrswaptionvolcube(py::module_& m) {
    py::class_<ZabrSwaptionVolatilityCube, SwaptionVolatilityCube,
               ext::shared_ptr<ZabrSwaptionVolatilityCube>>(
        m, "ZabrSwaptionVolatilityCube",
        "ZABR-parameterized swaption volatility cube (alpha, beta, nu, rho, gamma).")
        .def(py::init([](const Handle<SwaptionVolatilityStructure>& atmVolStructure,
                         const std::vector<Period>& optionTenors,
                         const std::vector<Period>& swapTenors,
                         const std::vector<Spread>& strikeSpreads,
                         const std::vector<std::vector<Handle<Quote>>>& volSpreads,
                         const ext::shared_ptr<SwapIndex>& swapIndexBase,
                         const ext::shared_ptr<SwapIndex>& shortSwapIndexBase,
                         bool vegaWeightedSmileFit,
                         const std::vector<std::vector<Handle<Quote>>>& parametersGuess,
                         const std::vector<bool>& isParameterFixed,
                         bool isAtmCalibrated,
                         const ext::shared_ptr<EndCriteria>& endCriteria,
                         const py::object& maxErrorTolerance,
                         const ext::shared_ptr<OptimizationMethod>& optMethod,
                         const py::object& errorAccept,
                         bool useMaxError,
                         Size maxGuesses,
                         bool backwardFlat,
                         Real cutoffStrike) {
            Real maxErr = maxErrorTolerance.is_none()
                ? Null<Real>() : maxErrorTolerance.cast<Real>();
            Real errAcc = errorAccept.is_none()
                ? Null<Real>() : errorAccept.cast<Real>();
            return ext::make_shared<ZabrSwaptionVolatilityCube>(
                atmVolStructure, optionTenors, swapTenors,
                strikeSpreads, volSpreads,
                swapIndexBase, shortSwapIndexBase,
                vegaWeightedSmileFit,
                parametersGuess, isParameterFixed, isAtmCalibrated,
                endCriteria, maxErr, optMethod, errAcc,
                useMaxError, maxGuesses, backwardFlat, cutoffStrike);
        }),
            py::arg("atmVolStructure"),
            py::arg("optionTenors"), py::arg("swapTenors"),
            py::arg("strikeSpreads"), py::arg("volSpreads"),
            py::arg("swapIndexBase"), py::arg("shortSwapIndexBase"),
            py::arg("vegaWeightedSmileFit"),
            py::arg("parametersGuess"), py::arg("isParameterFixed"),
            py::arg("isAtmCalibrated"),
            py::arg("endCriteria") = ext::shared_ptr<EndCriteria>(),
            py::arg("maxErrorTolerance") = py::none(),
            py::arg("optMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("errorAccept") = py::none(),
            py::arg("useMaxError") = false,
            py::arg("maxGuesses") = 50,
            py::arg("backwardFlat") = false,
            py::arg("cutoffStrike") = 0.0001,
            "Constructs ZABR swaption volatility cube.")
        .def("sparseSabrParameters", &ZabrSwaptionVolatilityCube::sparseSabrParameters,
            "Returns sparse ZABR parameters matrix (alpha, beta, nu, rho, gamma per point).")
        .def("denseSabrParameters", &ZabrSwaptionVolatilityCube::denseSabrParameters,
            "Returns dense ZABR parameters matrix (alpha, beta, nu, rho, gamma per point).")
        .def("marketVolCube",
            py::overload_cast<>(&ZabrSwaptionVolatilityCube::marketVolCube, py::const_),
            "Returns the market volatility cube.")
        .def("volCubeAtmCalibrated", &ZabrSwaptionVolatilityCube::volCubeAtmCalibrated,
            "Returns the ATM-calibrated volatility cube.")
        .def("recalibration",
            py::overload_cast<Real, const Period&>(
                &ZabrSwaptionVolatilityCube::recalibration),
            py::arg("beta"), py::arg("swapTenor"),
            "Recalibrates with fixed beta for a given swap tenor.")
        .def("recalibration",
            py::overload_cast<const std::vector<Real>&, const Period&>(
                &ZabrSwaptionVolatilityCube::recalibration),
            py::arg("beta"), py::arg("swapTenor"),
            "Recalibrates with beta vector for a given swap tenor.")
        .def("updateAfterRecalibration",
            &ZabrSwaptionVolatilityCube::updateAfterRecalibration,
            "Updates internal state after recalibration.");
}
