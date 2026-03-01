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
#include <ql/methods/finitedifferences/meshers/fdmhestonvariancemesher.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhestonvariancemesher(py::module_& m) {
    py::class_<FdmHestonVarianceMesher, Fdm1dMesher,
               ext::shared_ptr<FdmHestonVarianceMesher>>(
        m, "FdmHestonVarianceMesher",
        "One-dimensional variance mesher for the Heston model.")
        .def(py::init<Size,
                      const ext::shared_ptr<HestonProcess>&,
                      Time, Size, Real, Real>(),
            py::arg("size"),
            py::arg("process"),
            py::arg("maturity"),
            py::arg("tAvgSteps") = 10,
            py::arg("epsilon") = 0.0001,
            py::arg("mixingFactor") = 1.0,
            "Constructs a Heston variance mesher.")
        .def("volaEstimate", &FdmHestonVarianceMesher::volaEstimate,
            "Returns the volatility estimate.");

    py::class_<FdmHestonLocalVolatilityVarianceMesher, Fdm1dMesher,
               ext::shared_ptr<FdmHestonLocalVolatilityVarianceMesher>>(
        m, "FdmHestonLocalVolatilityVarianceMesher",
        "Variance mesher for the Heston model with local volatility.")
        .def(py::init<Size,
                      const ext::shared_ptr<HestonProcess>&,
                      const ext::shared_ptr<LocalVolTermStructure>&,
                      Time, Size, Real, Real>(),
            py::arg("size"),
            py::arg("process"),
            py::arg("leverageFct"),
            py::arg("maturity"),
            py::arg("tAvgSteps") = 10,
            py::arg("epsilon") = 0.0001,
            py::arg("mixingFactor") = 1.0,
            "Constructs a Heston local vol variance mesher.")
        .def("volaEstimate",
            &FdmHestonLocalVolatilityVarianceMesher::volaEstimate,
            "Returns the volatility estimate.");
}
