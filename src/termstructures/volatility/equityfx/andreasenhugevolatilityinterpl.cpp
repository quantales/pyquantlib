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
#include <ql/termstructures/volatility/equityfx/andreasenhugevolatilityinterpl.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::andreasenhugevolatilityinterpl(py::module_& m) {
    using AH = AndreasenHugeVolatilityInterpl;

    py::enum_<AH::InterpolationType>(m, "AndreasenHugeInterpolationType",
        "Interpolation type for Andreasen-Huge calibration.")
        .value("PiecewiseConstant", AH::PiecewiseConstant)
        .value("Linear", AH::Linear)
        .value("CubicSpline", AH::CubicSpline);

    py::enum_<AH::CalibrationType>(m, "AndreasenHugeCalibrationType",
        "Calibration type for Andreasen-Huge volatility interpolation.")
        .value("Call", AH::Call)
        .value("Put", AH::Put)
        .value("CallPut", AH::CallPut);

    py::class_<AH, ext::shared_ptr<AH>>(
        m, "AndreasenHugeVolatilityInterpl",
        "Andreasen-Huge local volatility calibration and interpolation. "
        "Calibrates a local vol surface to a sparse grid of vanilla options.")
        .def(py::init([](const AH::CalibrationSet& calibrationSet,
                         const Handle<Quote>& spot,
                         const Handle<YieldTermStructure>& rTS,
                         const Handle<YieldTermStructure>& qTS,
                         AH::InterpolationType interpolationType,
                         AH::CalibrationType calibrationType,
                         Size nGridPoints,
                         const py::object& minStrike,
                         const py::object& maxStrike,
                         const ext::shared_ptr<OptimizationMethod>& optimizationMethod,
                         const EndCriteria& endCriteria) {
                Real minS = minStrike.is_none() ? Null<Real>() : minStrike.cast<Real>();
                Real maxS = maxStrike.is_none() ? Null<Real>() : maxStrike.cast<Real>();
                auto opt = optimizationMethod ? optimizationMethod
                           : ext::make_shared<LevenbergMarquardt>();
                return ext::make_shared<AH>(
                    calibrationSet, spot, rTS, qTS,
                    interpolationType, calibrationType,
                    nGridPoints, minS, maxS, opt, endCriteria);
            }),
            py::arg("calibrationSet"),
            py::arg("spot"),
            py::arg("rTS"),
            py::arg("qTS"),
            py::arg("interpolationType") = AH::CubicSpline,
            py::arg("calibrationType") = AH::Call,
            py::arg("nGridPoints") = 500,
            py::arg("minStrike") = py::none(),
            py::arg("maxStrike") = py::none(),
            py::arg("optimizationMethod") = ext::shared_ptr<OptimizationMethod>(),
            py::arg("endCriteria") = EndCriteria(500, 100, 1e-12, 1e-10, 1e-10),
            "Constructs from a calibration set of (VanillaOption, Quote) pairs.")
        .def("maxDate", &AH::maxDate)
        .def("minStrike", &AH::minStrike)
        .def("maxStrike", &AH::maxStrike)
        .def("fwd", &AH::fwd, py::arg("t"),
            "Returns the forward price at time t.")
        .def("riskFreeRate", &AH::riskFreeRate,
            py::return_value_policy::reference_internal)
        .def("calibrationError", &AH::calibrationError,
            "Returns (min, max, avg) calibration error in volatility units.")
        .def("optionPrice", &AH::optionPrice,
            py::arg("t"), py::arg("strike"), py::arg("optionType"),
            "Returns the calibrated option price.")
        .def("localVol", &AH::localVol,
            py::arg("t"), py::arg("strike"),
            "Returns the calibrated local volatility.");
}
