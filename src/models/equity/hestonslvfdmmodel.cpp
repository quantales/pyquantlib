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
#include <ql/models/equity/hestonslvfdmmodel.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::hestonslvfdmmodel(py::module_& m) {
    // HestonSLVFokkerPlanckFdmParams struct
    py::class_<HestonSLVFokkerPlanckFdmParams>(m, "HestonSLVFokkerPlanckFdmParams",
        "Parameters for Heston SLV Fokker-Planck FDM calibration.")
        .def(py::init([](Size xGrid, Size vGrid,
                         Size tMaxStepsPerYear, Size tMinStepsPerYear,
                         Real tStepNumberDecay,
                         Size nRannacherTimeSteps,
                         Size predictionCorrectionSteps,
                         Real x0Density, Real localVolEpsProb,
                         Size maxIntegrationIterations,
                         Real vLowerEps, Real vUpperEps, Real vMin,
                         Real v0Density, Real vLowerBoundDensity,
                         Real vUpperBoundDensity,
                         Real leverageFctPropEps,
                         FdmHestonGreensFct::Algorithm greensAlgorithm,
                         FdmSquareRootFwdOp::TransformationType trafoType,
                         const FdmSchemeDesc& schemeDesc) {
                return HestonSLVFokkerPlanckFdmParams{
                    xGrid, vGrid,
                    tMaxStepsPerYear, tMinStepsPerYear,
                    tStepNumberDecay, nRannacherTimeSteps,
                    predictionCorrectionSteps,
                    x0Density, localVolEpsProb, maxIntegrationIterations,
                    vLowerEps, vUpperEps, vMin,
                    v0Density, vLowerBoundDensity, vUpperBoundDensity,
                    leverageFctPropEps,
                    greensAlgorithm, trafoType, schemeDesc};
             }),
            py::arg("xGrid") = 301,
            py::arg("vGrid") = 601,
            py::arg("tMaxStepsPerYear") = 2000,
            py::arg("tMinStepsPerYear") = 30,
            py::arg("tStepNumberDecay") = 2.0,
            py::arg("nRannacherTimeSteps") = 2,
            py::arg("predictionCorrectionSteps") = 2,
            py::arg("x0Density") = 0.1,
            py::arg("localVolEpsProb") = 1e-4,
            py::arg("maxIntegrationIterations") = 10000,
            py::arg("vLowerEps") = 1e-6,
            py::arg("vUpperEps") = 1e-6,
            py::arg("vMin") = 1e-6,
            py::arg("v0Density") = 1.0,
            py::arg("vLowerBoundDensity") = 10.0,
            py::arg("vUpperBoundDensity") = 10.0,
            py::arg("leverageFctPropEps") = 1e-5,
            py::arg("greensAlgorithm") = FdmHestonGreensFct::Gaussian,
            py::arg("trafoType") = FdmSquareRootFwdOp::Log,
            py::arg("schemeDesc") = FdmSchemeDesc::ModifiedCraigSneyd(),
            "Constructs with keyword arguments.")
        .def_readwrite("xGrid", &HestonSLVFokkerPlanckFdmParams::xGrid)
        .def_readwrite("vGrid", &HestonSLVFokkerPlanckFdmParams::vGrid)
        .def_readwrite("tMaxStepsPerYear",
            &HestonSLVFokkerPlanckFdmParams::tMaxStepsPerYear)
        .def_readwrite("tMinStepsPerYear",
            &HestonSLVFokkerPlanckFdmParams::tMinStepsPerYear)
        .def_readwrite("tStepNumberDecay",
            &HestonSLVFokkerPlanckFdmParams::tStepNumberDecay)
        .def_readwrite("nRannacherTimeSteps",
            &HestonSLVFokkerPlanckFdmParams::nRannacherTimeSteps)
        .def_property("predictionCorrectionSteps",
            [](const HestonSLVFokkerPlanckFdmParams& p) {
                return p.predictionCorretionSteps;
            },
            [](HestonSLVFokkerPlanckFdmParams& p, Size v) {
                p.predictionCorretionSteps = v;
            })
        .def_readwrite("x0Density",
            &HestonSLVFokkerPlanckFdmParams::x0Density)
        .def_readwrite("localVolEpsProb",
            &HestonSLVFokkerPlanckFdmParams::localVolEpsProb)
        .def_readwrite("maxIntegrationIterations",
            &HestonSLVFokkerPlanckFdmParams::maxIntegrationIterations)
        .def_readwrite("vLowerEps",
            &HestonSLVFokkerPlanckFdmParams::vLowerEps)
        .def_readwrite("vUpperEps",
            &HestonSLVFokkerPlanckFdmParams::vUpperEps)
        .def_readwrite("vMin",
            &HestonSLVFokkerPlanckFdmParams::vMin)
        .def_readwrite("v0Density",
            &HestonSLVFokkerPlanckFdmParams::v0Density)
        .def_readwrite("vLowerBoundDensity",
            &HestonSLVFokkerPlanckFdmParams::vLowerBoundDensity)
        .def_readwrite("vUpperBoundDensity",
            &HestonSLVFokkerPlanckFdmParams::vUpperBoundDensity)
        .def_readwrite("leverageFctPropEps",
            &HestonSLVFokkerPlanckFdmParams::leverageFctPropEps)
        .def_readwrite("greensAlgorithm",
            &HestonSLVFokkerPlanckFdmParams::greensAlgorithm)
        .def_readwrite("trafoType",
            &HestonSLVFokkerPlanckFdmParams::trafoType)
        .def_readonly("schemeDesc",
            &HestonSLVFokkerPlanckFdmParams::schemeDesc);

    // HestonSLVFDMModel
    py::class_<HestonSLVFDMModel, LazyObject,
               ext::shared_ptr<HestonSLVFDMModel>>(
        m, "HestonSLVFDMModel",
        "Heston stochastic local volatility model calibrated via FDM.")
        .def(py::init<Handle<LocalVolTermStructure>,
                       Handle<HestonModel>,
                       const Date&,
                       HestonSLVFokkerPlanckFdmParams,
                       bool, std::vector<Date>, Real>(),
            py::arg("localVol"),
            py::arg("hestonModel"),
            py::arg("endDate"),
            py::arg("params"),
            py::arg("logging") = false,
            py::arg("mandatoryDates") = std::vector<Date>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<LocalVolTermStructure>& localVol,
                         const ext::shared_ptr<HestonModel>& hestonModel,
                         const Date& endDate,
                         HestonSLVFokkerPlanckFdmParams params,
                         bool logging,
                         std::vector<Date> mandatoryDates,
                         Real mixingFactor) {
                return ext::make_shared<HestonSLVFDMModel>(
                    Handle<LocalVolTermStructure>(localVol),
                    Handle<HestonModel>(hestonModel),
                    endDate, std::move(params), logging,
                    std::move(mandatoryDates), mixingFactor);
             }),
            py::arg("localVol"),
            py::arg("hestonModel"),
            py::arg("endDate"),
            py::arg("params"),
            py::arg("logging") = false,
            py::arg("mandatoryDates") = std::vector<Date>(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from objects (handles created internally).")
        .def("hestonProcess", &HestonSLVFDMModel::hestonProcess,
            "Returns the Heston process.")
        .def("localVol", &HestonSLVFDMModel::localVol,
            "Returns the local volatility surface.")
        .def("leverageFunction", &HestonSLVFDMModel::leverageFunction,
            "Returns the calibrated leverage function.");
}
