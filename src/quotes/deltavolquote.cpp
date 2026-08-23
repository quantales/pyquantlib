/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/quotes/deltavolquote.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_quotes::deltavolquote(py::module_& m) {
    auto cls = py::class_<DeltaVolQuote, Quote, ext::shared_ptr<DeltaVolQuote>>(
        m, "DeltaVolQuote",
        "Quote of an FX volatility against a delta (or ATM) convention.");

    py::enum_<DeltaVolQuote::DeltaType>(cls, "DeltaType", "FX delta convention.")
        .value("Spot", DeltaVolQuote::Spot)
        .value("Fwd", DeltaVolQuote::Fwd)
        .value("PaSpot", DeltaVolQuote::PaSpot)
        .value("PaFwd", DeltaVolQuote::PaFwd)
        .export_values();

    py::enum_<DeltaVolQuote::AtmType>(cls, "AtmType", "FX at-the-money convention.")
        .value("AtmNull", DeltaVolQuote::AtmNull)
        .value("AtmSpot", DeltaVolQuote::AtmSpot)
        .value("AtmFwd", DeltaVolQuote::AtmFwd)
        .value("AtmDeltaNeutral", DeltaVolQuote::AtmDeltaNeutral)
        .value("AtmVegaMax", DeltaVolQuote::AtmVegaMax)
        .value("AtmGammaMax", DeltaVolQuote::AtmGammaMax)
        .value("AtmPutCall50", DeltaVolQuote::AtmPutCall50)
        .export_values();

    cls
        // Delta quote (explicit handle)
        .def(py::init<Real, Handle<Quote>, Time, DeltaVolQuote::DeltaType>(),
            py::arg("delta"), py::arg("vol"), py::arg("maturity"), py::arg("deltaType"),
            "Constructs a delta-vs-vol quote.")
        // Delta quote (hidden handle)
        .def(py::init([](Real delta, const ext::shared_ptr<Quote>& vol, Time maturity,
                         DeltaVolQuote::DeltaType deltaType) {
            return ext::make_shared<DeltaVolQuote>(delta, Handle<Quote>(vol), maturity, deltaType);
        }),
            py::arg("delta"), py::arg("vol"), py::arg("maturity"), py::arg("deltaType"),
            "Constructs a delta-vs-vol quote (handle created internally).")
        // ATM quote (explicit handle)
        .def(py::init<Handle<Quote>, DeltaVolQuote::DeltaType, Time, DeltaVolQuote::AtmType>(),
            py::arg("vol"), py::arg("deltaType"), py::arg("maturity"), py::arg("atmType"),
            "Constructs an ATM vol quote.")
        // ATM quote (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& vol, DeltaVolQuote::DeltaType deltaType,
                         Time maturity, DeltaVolQuote::AtmType atmType) {
            return ext::make_shared<DeltaVolQuote>(Handle<Quote>(vol), deltaType, maturity, atmType);
        }),
            py::arg("vol"), py::arg("deltaType"), py::arg("maturity"), py::arg("atmType"),
            "Constructs an ATM vol quote (handle created internally).")
        // Inspectors
        .def("delta", &DeltaVolQuote::delta, "Returns the delta.")
        .def("maturity", &DeltaVolQuote::maturity, "Returns the maturity (year fraction).")
        .def("atmType", &DeltaVolQuote::atmType, "Returns the ATM convention.")
        .def("deltaType", &DeltaVolQuote::deltaType, "Returns the delta convention.");
}
