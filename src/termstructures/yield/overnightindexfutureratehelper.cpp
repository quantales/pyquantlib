/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/yield/overnightindexfutureratehelper.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/quote.hpp>
#include <ql/quotes/simplequote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::overnightindexfutureratehelper(py::module_& m) {
    py::class_<OvernightIndexFutureRateHelper, RateHelper,
               ext::shared_ptr<OvernightIndexFutureRateHelper>>(
        m, "OvernightIndexFutureRateHelper",
        "Rate helper for bootstrapping over overnight compounding futures.")
        .def(py::init<const Handle<Quote>&, const Date&, const Date&,
                      const ext::shared_ptr<OvernightIndex>&,
                      const Handle<Quote>&, RateAveraging::Type,
                      Pillar::Choice, const Date&>(),
             py::arg("price"),
             py::arg("valueDate"),
             py::arg("maturityDate"),
             py::arg("overnightIndex"),
             py::arg("convexityAdjustment") = Handle<Quote>(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             "Constructs from a futures price quote handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<Quote>& price,
                         const Date& valueDate, const Date& maturityDate,
                         const ext::shared_ptr<OvernightIndex>& index,
                         const ext::shared_ptr<Quote>& convexityAdjustment,
                         RateAveraging::Type averagingMethod,
                         Pillar::Choice pillar, const Date& customPillarDate) {
            return ext::make_shared<OvernightIndexFutureRateHelper>(
                Handle<Quote>(price), valueDate, maturityDate, index,
                convexityAdjustment ? Handle<Quote>(convexityAdjustment)
                                    : Handle<Quote>(),
                averagingMethod, pillar, customPillarDate);
        }),
             py::arg("price"),
             py::arg("valueDate"),
             py::arg("maturityDate"),
             py::arg("overnightIndex"),
             py::arg("convexityAdjustment") = ext::shared_ptr<Quote>(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             "Constructs from a futures price quote (handle created internally).")
        // Plain price
        .def(py::init([](Real price, const Date& valueDate,
                         const Date& maturityDate,
                         const ext::shared_ptr<OvernightIndex>& index,
                         Real convexityAdjustment,
                         RateAveraging::Type averagingMethod,
                         Pillar::Choice pillar, const Date& customPillarDate) {
            return ext::make_shared<OvernightIndexFutureRateHelper>(
                Handle<Quote>(ext::make_shared<SimpleQuote>(price)), valueDate,
                maturityDate, index,
                Handle<Quote>(ext::make_shared<SimpleQuote>(convexityAdjustment)),
                averagingMethod, pillar, customPillarDate);
        }),
             py::arg("price"),
             py::arg("valueDate"),
             py::arg("maturityDate"),
             py::arg("overnightIndex"),
             py::arg("convexityAdjustment") = 0.0,
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             "Constructs from a plain futures price.")
        .def("convexityAdjustment",
             &OvernightIndexFutureRateHelper::convexityAdjustment,
             "Returns the convexity adjustment.");

    py::class_<SofrFutureRateHelper, OvernightIndexFutureRateHelper,
               ext::shared_ptr<SofrFutureRateHelper>>(
        m, "SofrFutureRateHelper",
        "Rate helper for bootstrapping over CME SOFR futures.")
        .def(py::init([](Real price, Month referenceMonth, Year referenceYear,
                         Frequency referenceFreq, Real convexityAdjustment,
                         Pillar::Choice pillar, const Date& customPillarDate) {
            return ext::make_shared<SofrFutureRateHelper>(
                price, referenceMonth, referenceYear, referenceFreq,
                convexityAdjustment, pillar, customPillarDate);
        }),
             py::arg("price"),
             py::arg("referenceMonth"),
             py::arg("referenceYear"),
             py::arg("referenceFreq"),
             py::arg("convexityAdjustment") = 0.0,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             "Constructs from a plain SOFR futures price.")
        .def(py::init([](const Handle<Quote>& price, Month referenceMonth,
                         Year referenceYear, Frequency referenceFreq,
                         const Handle<Quote>& convexityAdjustment,
                         Pillar::Choice pillar, const Date& customPillarDate) {
            return ext::make_shared<SofrFutureRateHelper>(
                price, referenceMonth, referenceYear, referenceFreq,
                convexityAdjustment, pillar, customPillarDate);
        }),
             py::arg("price"),
             py::arg("referenceMonth"),
             py::arg("referenceYear"),
             py::arg("referenceFreq"),
             py::arg("convexityAdjustment") = Handle<Quote>(),
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             "Constructs from a SOFR futures price quote handle.");
}
