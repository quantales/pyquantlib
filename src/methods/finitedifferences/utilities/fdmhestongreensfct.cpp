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
#include <ql/methods/finitedifferences/utilities/fdmhestongreensfct.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhestongreensfct(py::module_& m) {
    py::enum_<FdmHestonGreensFct::Algorithm>(m, "FdmHestonGreensFctAlgorithm",
        "Algorithm for Heston Fokker-Planck Green's function.")
        .value("ZeroCorrelation", FdmHestonGreensFct::ZeroCorrelation)
        .value("Gaussian", FdmHestonGreensFct::Gaussian)
        .value("SemiAnalytical", FdmHestonGreensFct::SemiAnalytical);
}
