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
#include <ql/models/shortrate/onefactormodels/markovfunctional.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/termstructures/volatility/optionlet/optionletvolatilitystructure.hpp>
#include <ql/indexes/swapindex.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::markovfunctional(py::module_& m) {
    // ModelSettings::Adjustments enum
    py::enum_<MarkovFunctional::ModelSettings::Adjustments>(
        m, "MarkovFunctionalAdjustments",
        "Adjustment flags for MarkovFunctional model.")
        .value("AdjustNone", MarkovFunctional::ModelSettings::AdjustNone)
        .value("AdjustDigitals", MarkovFunctional::ModelSettings::AdjustDigitals)
        .value("AdjustYts", MarkovFunctional::ModelSettings::AdjustYts)
        .value("ExtrapolatePayoffFlat", MarkovFunctional::ModelSettings::ExtrapolatePayoffFlat)
        .value("NoPayoffExtrapolation", MarkovFunctional::ModelSettings::NoPayoffExtrapolation)
        .value("KahaleSmile", MarkovFunctional::ModelSettings::KahaleSmile)
        .value("SmileExponentialExtrapolation", MarkovFunctional::ModelSettings::SmileExponentialExtrapolation)
        .value("KahaleInterpolation", MarkovFunctional::ModelSettings::KahaleInterpolation)
        .value("SmileDeleteArbitragePoints", MarkovFunctional::ModelSettings::SmileDeleteArbitragePoints)
        .value("SabrSmile", MarkovFunctional::ModelSettings::SabrSmile)
        .value("CustomSmile", MarkovFunctional::ModelSettings::CustomSmile)
        .export_values();

    // ModelSettings struct
    py::class_<MarkovFunctional::ModelSettings>(
        m, "MarkovFunctionalModelSettings",
        "Configuration settings for MarkovFunctional model.")
        .def(py::init<>(),
            "Constructs default settings (KahaleSmile + SmileExponentialExtrapolation).")
        .def(py::init<Size, Real, Size, Real, Real, Real, Real, int,
                      std::vector<Real>>(),
            py::arg("yGridPoints"),
            py::arg("yStdDevs"),
            py::arg("gaussHermitePoints"),
            py::arg("digitalGap"),
            py::arg("marketRateAccuracy"),
            py::arg("lowerRateBound"),
            py::arg("upperRateBound"),
            py::arg("adjustments"),
            py::arg("smileMoneyCheckpoints") = std::vector<Real>(),
            "Constructs with full parameters.")
        // Builder methods (return reference for chaining)
        .def("withYGridPoints", &MarkovFunctional::ModelSettings::withYGridPoints,
            py::arg("n"), py::return_value_policy::reference_internal,
            "Sets grid points for state process discretization.")
        .def("withYStdDevs", &MarkovFunctional::ModelSettings::withYStdDevs,
            py::arg("s"), py::return_value_policy::reference_internal,
            "Sets standard deviations for state grid coverage.")
        .def("withGaussHermitePoints", &MarkovFunctional::ModelSettings::withGaussHermitePoints,
            py::arg("n"), py::return_value_policy::reference_internal,
            "Sets Gauss-Hermite integration points.")
        .def("withDigitalGap", &MarkovFunctional::ModelSettings::withDigitalGap,
            py::arg("d"), py::return_value_policy::reference_internal,
            "Sets digital gap for smile calibration.")
        .def("withMarketRateAccuracy", &MarkovFunctional::ModelSettings::withMarketRateAccuracy,
            py::arg("a"), py::return_value_policy::reference_internal,
            "Sets market rate inversion accuracy.")
        .def("withUpperRateBound", &MarkovFunctional::ModelSettings::withUpperRateBound,
            py::arg("u"), py::return_value_policy::reference_internal,
            "Sets upper rate bound.")
        .def("withLowerRateBound", &MarkovFunctional::ModelSettings::withLowerRateBound,
            py::arg("l"), py::return_value_policy::reference_internal,
            "Sets lower rate bound.")
        .def("withAdjustments", &MarkovFunctional::ModelSettings::withAdjustments,
            py::arg("a"), py::return_value_policy::reference_internal,
            "Sets adjustment flags.")
        .def("addAdjustment", &MarkovFunctional::ModelSettings::addAdjustment,
            py::arg("a"), py::return_value_policy::reference_internal,
            "Adds an adjustment flag.")
        .def("removeAdjustment", &MarkovFunctional::ModelSettings::removeAdjustment,
            py::arg("a"), py::return_value_policy::reference_internal,
            "Removes an adjustment flag.")
        .def("withSmileMoneynessCheckpoints",
            &MarkovFunctional::ModelSettings::withSmileMoneynessCheckpoints,
            py::arg("m"), py::return_value_policy::reference_internal,
            "Sets smile moneyness checkpoints.")
        // Public data members
        .def_readwrite("yGridPoints", &MarkovFunctional::ModelSettings::yGridPoints_)
        .def_readwrite("yStdDevs", &MarkovFunctional::ModelSettings::yStdDevs_)
        .def_readwrite("gaussHermitePoints", &MarkovFunctional::ModelSettings::gaussHermitePoints_)
        .def_readwrite("digitalGap", &MarkovFunctional::ModelSettings::digitalGap_)
        .def_readwrite("marketRateAccuracy", &MarkovFunctional::ModelSettings::marketRateAccuracy_)
        .def_readwrite("lowerRateBound", &MarkovFunctional::ModelSettings::lowerRateBound_)
        .def_readwrite("upperRateBound", &MarkovFunctional::ModelSettings::upperRateBound_)
        .def_readwrite("adjustments", &MarkovFunctional::ModelSettings::adjustments_);

    // ModelOutputs struct (read-only diagnostics)
    py::class_<MarkovFunctional::ModelOutputs>(
        m, "MarkovFunctionalModelOutputs",
        "Diagnostic output from MarkovFunctional calibration.")
        .def_readonly("dirty", &MarkovFunctional::ModelOutputs::dirty_)
        .def_readonly("settings", &MarkovFunctional::ModelOutputs::settings_)
        .def_readonly("expiries", &MarkovFunctional::ModelOutputs::expiries_)
        .def_readonly("tenors", &MarkovFunctional::ModelOutputs::tenors_)
        .def_readonly("atm", &MarkovFunctional::ModelOutputs::atm_)
        .def_readonly("annuity", &MarkovFunctional::ModelOutputs::annuity_)
        .def_readonly("adjustmentFactors",
            &MarkovFunctional::ModelOutputs::adjustmentFactors_)
        .def_readonly("digitalsAdjustmentFactors",
            &MarkovFunctional::ModelOutputs::digitalsAdjustmentFactors_)
        .def_readonly("messages", &MarkovFunctional::ModelOutputs::messages_)
        .def_readonly("smileStrikes", &MarkovFunctional::ModelOutputs::smileStrikes_)
        .def_readonly("marketRawCallPremium",
            &MarkovFunctional::ModelOutputs::marketRawCallPremium_)
        .def_readonly("marketRawPutPremium",
            &MarkovFunctional::ModelOutputs::marketRawPutPremium_)
        .def_readonly("marketCallPremium",
            &MarkovFunctional::ModelOutputs::marketCallPremium_)
        .def_readonly("marketPutPremium",
            &MarkovFunctional::ModelOutputs::marketPutPremium_)
        .def_readonly("modelCallPremium",
            &MarkovFunctional::ModelOutputs::modelCallPremium_)
        .def_readonly("modelPutPremium",
            &MarkovFunctional::ModelOutputs::modelPutPremium_)
        .def_readonly("marketVega", &MarkovFunctional::ModelOutputs::marketVega_)
        .def_readonly("marketZerorate",
            &MarkovFunctional::ModelOutputs::marketZerorate_)
        .def_readonly("modelZerorate",
            &MarkovFunctional::ModelOutputs::modelZerorate_);

    // MarkovFunctional model
    py::class_<MarkovFunctional, Gaussian1dModel, CalibratedModel,
               ext::shared_ptr<MarkovFunctional>>(
        m, "MarkovFunctional",
        "Markov Functional 1-factor model.")
        // Swaption smile calibrated constructor
        .def(py::init<const Handle<YieldTermStructure>&,
                      Real, std::vector<Date>, std::vector<Real>,
                      const Handle<SwaptionVolatilityStructure>&,
                      const std::vector<Date>&,
                      const std::vector<Period>&,
                      const ext::shared_ptr<SwapIndex>&,
                      MarkovFunctional::ModelSettings>(),
            py::arg("termStructure"),
            py::arg("reversion"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("swaptionVol"),
            py::arg("swaptionExpiries"),
            py::arg("swaptionTenors"),
            py::arg("swapIndexBase"),
            py::arg("modelSettings") = MarkovFunctional::ModelSettings(),
            "Constructs swaption smile calibrated model.")
        // Caplet smile calibrated constructor
        .def(py::init<const Handle<YieldTermStructure>&,
                      Real, std::vector<Date>, std::vector<Real>,
                      const Handle<OptionletVolatilityStructure>&,
                      const std::vector<Date>&,
                      ext::shared_ptr<IborIndex>,
                      MarkovFunctional::ModelSettings>(),
            py::arg("termStructure"),
            py::arg("reversion"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("capletVol"),
            py::arg("capletExpiries"),
            py::arg("iborIndex"),
            py::arg("modelSettings") = MarkovFunctional::ModelSettings(),
            "Constructs caplet smile calibrated model.")
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                         Real reversion,
                         std::vector<Date> volstepdates,
                         std::vector<Real> volatilities,
                         const Handle<SwaptionVolatilityStructure>& swaptionVol,
                         const std::vector<Date>& swaptionExpiries,
                         const std::vector<Period>& swaptionTenors,
                         const ext::shared_ptr<SwapIndex>& swapIndexBase,
                         MarkovFunctional::ModelSettings modelSettings) {
            return ext::make_shared<MarkovFunctional>(
                Handle<YieldTermStructure>(ts),
                reversion, std::move(volstepdates), std::move(volatilities),
                swaptionVol, swaptionExpiries, swaptionTenors,
                swapIndexBase, std::move(modelSettings));
        }),
            py::arg("termStructure"),
            py::arg("reversion"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("swaptionVol"),
            py::arg("swaptionExpiries"),
            py::arg("swaptionTenors"),
            py::arg("swapIndexBase"),
            py::arg("modelSettings") = MarkovFunctional::ModelSettings(),
            "Constructs swaption calibrated model (handle created internally).")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                         Real reversion,
                         std::vector<Date> volstepdates,
                         std::vector<Real> volatilities,
                         const Handle<OptionletVolatilityStructure>& capletVol,
                         const std::vector<Date>& capletExpiries,
                         ext::shared_ptr<IborIndex> iborIndex,
                         MarkovFunctional::ModelSettings modelSettings) {
            return ext::make_shared<MarkovFunctional>(
                Handle<YieldTermStructure>(ts),
                reversion, std::move(volstepdates), std::move(volatilities),
                capletVol, capletExpiries, std::move(iborIndex),
                std::move(modelSettings));
        }),
            py::arg("termStructure"),
            py::arg("reversion"),
            py::arg("volstepdates"),
            py::arg("volatilities"),
            py::arg("capletVol"),
            py::arg("capletExpiries"),
            py::arg("iborIndex"),
            py::arg("modelSettings") = MarkovFunctional::ModelSettings(),
            "Constructs caplet calibrated model (handle created internally).")
        // Methods
        .def("modelSettings", &MarkovFunctional::modelSettings,
            py::return_value_policy::reference_internal,
            "Returns the model settings.")
        .def("modelOutputs", &MarkovFunctional::modelOutputs,
            py::return_value_policy::reference_internal,
            "Returns diagnostic model outputs.")
        .def("numeraireDate", &MarkovFunctional::numeraireDate,
            "Returns the numeraire date.")
        .def("numeraireTime", &MarkovFunctional::numeraireTime,
            "Returns the numeraire time.")
        .def("volatility", &MarkovFunctional::volatility,
            "Returns the volatility parameters.");
}
