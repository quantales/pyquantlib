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
#include <ql/models/equity/hestonslvmcmodel.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::hestonslvmcmodel(py::module_& m) {
    py::class_<HestonSLVMCModel, LazyObject,
               ext::shared_ptr<HestonSLVMCModel>>(
        m, "HestonSLVMCModel",
        "Heston stochastic local volatility model calibrated via Monte Carlo.")
        .def(py::init<Handle<LocalVolTermStructure>,
                       Handle<HestonModel>,
                       ext::shared_ptr<BrownianGeneratorFactory>,
                       const Date&, Size, Size, Size,
                       const std::vector<Date>&, Real>(),
            py::arg("localVol"),
            py::arg("hestonModel"),
            py::arg("brownianGeneratorFactory"),
            py::arg("endDate"),
            py::arg("timeStepsPerYear") = 365,
            py::arg("nBins") = 201,
            py::arg("calibrationPaths") = (1 << 15),
            py::arg("mandatoryDates") = std::vector<Date>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<LocalVolTermStructure>& localVol,
                         const ext::shared_ptr<HestonModel>& hestonModel,
                         const ext::shared_ptr<BrownianGeneratorFactory>& bgf,
                         const Date& endDate,
                         Size timeStepsPerYear, Size nBins,
                         Size calibrationPaths,
                         const std::vector<Date>& mandatoryDates,
                         Real mixingFactor) {
                return ext::make_shared<HestonSLVMCModel>(
                    Handle<LocalVolTermStructure>(localVol),
                    Handle<HestonModel>(hestonModel),
                    bgf, endDate, timeStepsPerYear, nBins,
                    calibrationPaths, mandatoryDates, mixingFactor);
             }),
            py::arg("localVol"),
            py::arg("hestonModel"),
            py::arg("brownianGeneratorFactory"),
            py::arg("endDate"),
            py::arg("timeStepsPerYear") = 365,
            py::arg("nBins") = 201,
            py::arg("calibrationPaths") = (1 << 15),
            py::arg("mandatoryDates") = std::vector<Date>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from objects (handles created internally).")
        .def("hestonProcess", &HestonSLVMCModel::hestonProcess,
            "Returns the Heston process.")
        .def("localVol", &HestonSLVMCModel::localVol,
            "Returns the local volatility surface.")
        .def("leverageFunction", &HestonSLVMCModel::leverageFunction,
            "Returns the calibrated leverage function.");
}
