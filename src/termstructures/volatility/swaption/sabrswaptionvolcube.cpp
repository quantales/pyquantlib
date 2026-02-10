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
#include <ql/termstructures/volatility/swaption/sabrswaptionvolatilitycube.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/math/optimization/endcriteria.hpp>
#include <ql/math/optimization/method.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::sabrswaptionvolcube(py::module_& m) {
    py::class_<SabrSwaptionVolatilityCube, SwaptionVolatilityCube,
               ext::shared_ptr<SabrSwaptionVolatilityCube>>(
        m, "SabrSwaptionVolatilityCube",
        "SABR-parameterized swaption volatility cube.")
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
            return ext::make_shared<SabrSwaptionVolatilityCube>(
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
            "Constructs SABR swaption volatility cube.")
        .def("sparseSabrParameters", &SabrSwaptionVolatilityCube::sparseSabrParameters,
            "Returns sparse SABR parameters matrix.")
        .def("denseSabrParameters", &SabrSwaptionVolatilityCube::denseSabrParameters,
            "Returns dense SABR parameters matrix.")
        .def("marketVolCube",
            py::overload_cast<>(&SabrSwaptionVolatilityCube::marketVolCube, py::const_),
            "Returns the market volatility cube.")
        .def("volCubeAtmCalibrated", &SabrSwaptionVolatilityCube::volCubeAtmCalibrated,
            "Returns the ATM-calibrated volatility cube.")
        .def("recalibration",
            py::overload_cast<Real, const Period&>(
                &SabrSwaptionVolatilityCube::recalibration),
            py::arg("beta"), py::arg("swapTenor"),
            "Recalibrates with fixed beta for a given swap tenor.")
        .def("recalibration",
            py::overload_cast<const std::vector<Real>&, const Period&>(
                &SabrSwaptionVolatilityCube::recalibration),
            py::arg("beta"), py::arg("swapTenor"),
            "Recalibrates with beta vector for a given swap tenor.")
        .def("updateAfterRecalibration",
            &SabrSwaptionVolatilityCube::updateAfterRecalibration,
            "Updates internal state after recalibration.");
}
