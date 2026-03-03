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
#include <ql/math/integrals/gaussianquadratures.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::gaussianquadratures(py::module_& m) {
    // GaussianQuadrature base class (not directly constructible)
    auto base = py::module_::import("pyquantlib.base");

    py::class_<GaussianQuadrature, ext::shared_ptr<GaussianQuadrature>>(
        base, "GaussianQuadrature",
        "Base class for Gaussian quadrature integration.")
        .def("__call__", [](const GaussianQuadrature& self,
                            const std::function<Real(Real)>& f) {
            return self(f);
        },
        py::arg("f"),
        "Evaluates the quadrature integral of f.")
        .def("order", &GaussianQuadrature::order,
            "Returns the quadrature order.")
        .def("weights", &GaussianQuadrature::weights,
            py::return_value_policy::reference_internal,
            "Returns the quadrature weights.")
        .def("x", &GaussianQuadrature::x,
            py::return_value_policy::reference_internal,
            "Returns the quadrature abscissas.");

    // Concrete Gaussian quadrature classes
    py::class_<GaussLaguerreIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussLaguerreIntegration>>(
        m, "GaussLaguerreIntegration",
        "Gauss-Laguerre integration over [0, inf) with weight x^s * exp(-x).")
        .def(py::init<Size, Real>(),
            py::arg("n"), py::arg("s") = 0.0,
            "Constructs with n quadrature points and parameter s.");

    py::class_<GaussHermiteIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussHermiteIntegration>>(
        m, "GaussHermiteIntegration",
        "Gauss-Hermite integration over (-inf, inf) with weight |x|^(2*mu) * exp(-x^2).")
        .def(py::init<Size, Real>(),
            py::arg("n"), py::arg("mu") = 0.0,
            "Constructs with n quadrature points and parameter mu.");

    py::class_<GaussJacobiIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussJacobiIntegration>>(
        m, "GaussJacobiIntegration",
        "Gauss-Jacobi integration over [-1, 1] with weight (1-x)^alpha * (1+x)^beta.")
        .def(py::init<Size, Real, Real>(),
            py::arg("n"), py::arg("alpha"), py::arg("beta"),
            "Constructs with n quadrature points and parameters alpha, beta.");

    py::class_<GaussHyperbolicIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussHyperbolicIntegration>>(
        m, "GaussHyperbolicIntegration",
        "Gauss-Hyperbolic integration over (-inf, inf) with weight 1/cosh(x).")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussLegendreIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussLegendreIntegration>>(
        m, "GaussLegendreIntegration",
        "Gauss-Legendre integration over [-1, 1] with unit weight.")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussChebyshevIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussChebyshevIntegration>>(
        m, "GaussChebyshevIntegration",
        "Gauss-Chebyshev integration over [-1, 1] with weight (1-x^2)^(-1/2).")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussChebyshev2ndIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussChebyshev2ndIntegration>>(
        m, "GaussChebyshev2ndIntegration",
        "Gauss-Chebyshev 2nd kind integration over [-1, 1] with weight (1-x^2)^(1/2).")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussGegenbauerIntegration, GaussianQuadrature,
               ext::shared_ptr<GaussGegenbauerIntegration>>(
        m, "GaussGegenbauerIntegration",
        "Gauss-Gegenbauer integration over [-1, 1] with weight (1-x^2)^(lambda-1/2).")
        .def(py::init<Size, Real>(),
            py::arg("n"), py::arg("lambda_"),
            "Constructs with n quadrature points and parameter lambda.");

    // TabulatedGaussLegendre (precomputed, orders 6/7/12/20 only)
    py::class_<TabulatedGaussLegendre, ext::shared_ptr<TabulatedGaussLegendre>>(
        m, "TabulatedGaussLegendre",
        "Tabulated Gauss-Legendre quadrature (precomputed for orders 6, 7, 12, 20).")
        .def(py::init<Size>(),
            py::arg("n") = 20,
            "Constructs with the given order (6, 7, 12, or 20).")
        .def("__call__", [](const TabulatedGaussLegendre& self,
                            const std::function<Real(Real)>& f) {
            return self(f);
        },
        py::arg("f"),
        "Evaluates the quadrature integral of f.")
        .def("order",
            static_cast<Size (TabulatedGaussLegendre::*)() const>(&TabulatedGaussLegendre::order),
            "Returns the quadrature order.");

    // GaussianQuadratureIntegrator typedefs (these ARE Integrators)
    py::class_<GaussLegendreIntegrator, Integrator,
               ext::shared_ptr<GaussLegendreIntegrator>>(
        m, "GaussLegendreIntegrator",
        "Integrator using Gauss-Legendre quadrature.")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussChebyshevIntegrator, Integrator,
               ext::shared_ptr<GaussChebyshevIntegrator>>(
        m, "GaussChebyshevIntegrator",
        "Integrator using Gauss-Chebyshev quadrature.")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");

    py::class_<GaussChebyshev2ndIntegrator, Integrator,
               ext::shared_ptr<GaussChebyshev2ndIntegrator>>(
        m, "GaussChebyshev2ndIntegrator",
        "Integrator using Gauss-Chebyshev 2nd kind quadrature.")
        .def(py::init<Size>(),
            py::arg("n"),
            "Constructs with n quadrature points.");
}
