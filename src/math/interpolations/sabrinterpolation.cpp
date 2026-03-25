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
#include <ql/math/interpolations/sabrinterpolation.hpp>
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

    // Extended data holder that also stores forward on the heap.
    // SABRInterpolation stores const Real& forward, so forward needs
    // a stable address that survives the move into shared_ptr's deleter.
    struct SABRDataHolder {
        std::vector<Real> x, y;
        ext::shared_ptr<Real> forward;

        template <typename T>
        void operator()(T* p) const { delete p; }
    };

}  // namespace

void ql_math::sabrinterpolation(py::module_& m) {
    py::class_<SABRInterpolation, Interpolation,
               ext::shared_ptr<SABRInterpolation>>(
        m, "SABRInterpolation",
        "SABR smile interpolation between discrete volatility points.")
        .def(py::init([](std::vector<Real> strikes,
                        std::vector<Real> vols,
                        Real t,
                        Real forward,
                        Real alpha, Real beta, Real nu, Real rho,
                        bool alphaIsFixed, bool betaIsFixed,
                        bool nuIsFixed, bool rhoIsFixed,
                        bool vegaWeighted,
                        const ext::shared_ptr<EndCriteria>& endCriteria,
                        const ext::shared_ptr<OptimizationMethod>& optMethod,
                        Real errorAccept,
                        bool useMaxError,
                        Size maxGuesses,
                        Real shift) {

            QL_REQUIRE(strikes.size() == vols.size(),
                       "strikes and vols must have the same size");
            QL_REQUIRE(strikes.size() >= 2,
                       "at least 2 points required");

            SABRDataHolder holder{
                std::move(strikes), std::move(vols),
                ext::make_shared<Real>(forward)};

            auto* ptr = new SABRInterpolation(
                holder.x.begin(), holder.x.end(), holder.y.begin(),
                t, *holder.forward,
                alpha, beta, nu, rho,
                alphaIsFixed, betaIsFixed, nuIsFixed, rhoIsFixed,
                vegaWeighted, endCriteria, optMethod,
                errorAccept, useMaxError, maxGuesses,
                shift);

            return ext::shared_ptr<SABRInterpolation>(ptr, std::move(holder));
        }),
        py::arg("strikes"), py::arg("vols"),
        py::arg("expiry"), py::arg("forward"),
        py::arg("alpha"), py::arg("beta"), py::arg("nu"), py::arg("rho"),
        py::arg("alphaIsFixed"), py::arg("betaIsFixed"),
        py::arg("nuIsFixed"), py::arg("rhoIsFixed"),
        py::arg("vegaWeighted") = true,
        py::arg("endCriteria") = ext::shared_ptr<EndCriteria>(),
        py::arg("optMethod") = ext::shared_ptr<OptimizationMethod>(),
        py::arg("errorAccept") = 0.0020,
        py::arg("useMaxError") = false,
        py::arg("maxGuesses") = Size(50),
        py::arg("shift") = 0.0,
        "Constructs SABR interpolation from strikes and volatilities.")
        .def("expiry", &SABRInterpolation::expiry, "Returns the expiry.")
        .def("forward", &SABRInterpolation::forward, "Returns the forward.")
        .def("alpha", &SABRInterpolation::alpha, "Returns calibrated alpha.")
        .def("beta", &SABRInterpolation::beta, "Returns calibrated beta.")
        .def("nu", &SABRInterpolation::nu, "Returns calibrated nu.")
        .def("rho", &SABRInterpolation::rho, "Returns calibrated rho.")
        .def("rmsError", &SABRInterpolation::rmsError, "Returns RMS calibration error.")
        .def("maxError", &SABRInterpolation::maxError, "Returns max calibration error.")
        .def("endCriteria", &SABRInterpolation::endCriteria, "Returns the end criteria type.")
        .def("interpolationWeights", &SABRInterpolation::interpolationWeights,
            py::return_value_policy::reference_internal,
            "Returns the interpolation weights.");
}
