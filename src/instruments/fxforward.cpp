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
#include <ql/instruments/fxforward.hpp>
#include <ql/currency.hpp>
#include <ql/time/calendar.hpp>
#include <ql/time/calendars/nullcalendar.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::fxforward(py::module_& m) {
    py::class_<FxForward, Instrument, ext::shared_ptr<FxForward>>(
        m, "FxForward",
        "FX forward: exchange of two currency nominals at a future date.")
        // Nominal-based constructor
        .def(py::init<Real, const Currency&, Real, const Currency&,
                      const Date&, bool, Natural, const Calendar&>(),
            py::arg("sourceNominal"),
            py::arg("sourceCurrency"),
            py::arg("targetNominal"),
            py::arg("targetCurrency"),
            py::arg("maturityDate"),
            py::arg("paySourceCurrency"),
            py::arg("settlementDays") = 2,
            py::arg("paymentCalendar") = NullCalendar(),
            "Constructs from source and target nominals.")
        // Rate-based constructor
        .def(py::init<Real, const Currency&, const Currency&, Real,
                      const Date&, bool, Natural, const Calendar&>(),
            py::arg("sourceNominal"),
            py::arg("sourceCurrency"),
            py::arg("targetCurrency"),
            py::arg("forwardRate"),
            py::arg("maturityDate"),
            py::arg("paySourceCurrency"),
            py::arg("settlementDays") = 2,
            py::arg("paymentCalendar") = NullCalendar(),
            "Constructs from a source nominal and a forward rate (target/source).")
        // Inspectors
        .def("sourceNominal", &FxForward::sourceNominal,
            "Returns the source-currency nominal.")
        .def("sourceCurrency", &FxForward::sourceCurrency,
            "Returns the source currency.")
        .def("targetNominal", &FxForward::targetNominal,
            "Returns the target-currency nominal.")
        .def("targetCurrency", &FxForward::targetCurrency,
            "Returns the target currency.")
        .def("maturityDate", &FxForward::maturityDate,
            "Returns the maturity (settlement) date of the contract.")
        .def("paySourceCurrency", &FxForward::paySourceCurrency,
            "Returns True if paying the source currency.")
        .def("forwardRate", &FxForward::forwardRate,
            "Returns the contracted forward rate (target per unit of source).")
        .def("settlementDays", &FxForward::settlementDays,
            "Returns the number of settlement days (0=O/N, 1=T/N, 2=Spot).")
        .def("settlementCalendar", &FxForward::settlementCalendar,
            "Returns the settlement calendar.")
        .def("settlementDate", &FxForward::settlementDate,
            "Returns the settlement date (evaluation date + settlementDays).")
        // Engine-computed results
        .def("fairForwardRate", &FxForward::fairForwardRate,
            "Returns the market-implied fair forward rate (target/source).")
        .def("npvSourceCurrency", &FxForward::npvSourceCurrency,
            "Returns the NPV expressed in source-currency terms.")
        .def("npvTargetCurrency", &FxForward::npvTargetCurrency,
            "Returns the NPV expressed in target-currency terms.");
}
