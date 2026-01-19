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
#include <ql/pricingengines/vanilla/qdfpamericanengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::qdfpamericanengine(py::module_& m) {
    // Iteration scheme base class
    py::class_<QdFpIterationScheme, ext::shared_ptr<QdFpIterationScheme>>(
        m, "QdFpIterationScheme",
        "Base class for QD+ fixed-point iteration schemes.");

    // Concrete scheme classes (needed for proper polymorphic handling)
    py::class_<QdFpLegendreScheme, QdFpIterationScheme,
               ext::shared_ptr<QdFpLegendreScheme>>(
        m, "QdFpLegendreScheme",
        "Gauss-Legendre (l,m,n)-p iteration scheme.")
        .def(py::init<Size, Size, Size, Size>(),
            py::arg("l"), py::arg("m"), py::arg("n"), py::arg("p"),
            "Constructs with integration order l, iteration steps m, "
            "Chebyshev nodes n, and final integration order p.");

    py::class_<QdFpLegendreTanhSinhScheme, QdFpLegendreScheme,
               ext::shared_ptr<QdFpLegendreTanhSinhScheme>>(
        m, "QdFpLegendreTanhSinhScheme",
        "Legendre-Tanh-Sinh (l,m,n)-eps iteration scheme.")
        .def(py::init<Size, Size, Size, Real>(),
            py::arg("l"), py::arg("m"), py::arg("n"), py::arg("eps"),
            "Constructs with integration order l, iteration steps m, "
            "Chebyshev nodes n, and tanh-sinh precision eps.");

    py::class_<QdFpTanhSinhIterationScheme, QdFpIterationScheme,
               ext::shared_ptr<QdFpTanhSinhIterationScheme>>(
        m, "QdFpTanhSinhIterationScheme",
        "Tanh-sinh (m,n)-eps iteration scheme.")
        .def(py::init<Size, Size, Real>(),
            py::arg("m"), py::arg("n"), py::arg("eps"),
            "Constructs with iteration steps m, Chebyshev nodes n, "
            "and tanh-sinh precision eps.");

    // Fixed point equation enum
    py::enum_<QdFpAmericanEngine::FixedPointEquation>(m, "QdFpFixedPointEquation",
        "Fixed point equation type for QD+ American engine.")
        .value("FP_A", QdFpAmericanEngine::FixedPointEquation::FP_A)
        .value("FP_B", QdFpAmericanEngine::FixedPointEquation::FP_B)
        .value("Auto", QdFpAmericanEngine::FixedPointEquation::Auto);

    // Main engine class
    py::class_<QdFpAmericanEngine, PricingEngine, ext::shared_ptr<QdFpAmericanEngine>>(
        m, "QdFpAmericanEngine",
        "High performance American option engine based on QD+ fixed-point iteration.")
        // Simple constructor with just process (uses default accurate scheme)
        .def(py::init([](ext::shared_ptr<GeneralizedBlackScholesProcess> process) {
            return ext::make_shared<QdFpAmericanEngine>(process);
        }),
            py::arg("process"),
            "Constructs with process using default accurate scheme.")
        // Full constructor
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<QdFpIterationScheme>,
                      QdFpAmericanEngine::FixedPointEquation>(),
            py::arg("process"),
            py::arg("iterationScheme"),
            py::arg("fpEquation") = QdFpAmericanEngine::FixedPointEquation::Auto,
            "Constructs with process, iteration scheme, and fixed-point equation type.")
        .def_static("fastScheme", &QdFpAmericanEngine::fastScheme,
            "Returns the fast iteration scheme.")
        .def_static("accurateScheme", &QdFpAmericanEngine::accurateScheme,
            "Returns the accurate iteration scheme (default).")
        .def_static("highPrecisionScheme", &QdFpAmericanEngine::highPrecisionScheme,
            "Returns the high precision iteration scheme.");
}
