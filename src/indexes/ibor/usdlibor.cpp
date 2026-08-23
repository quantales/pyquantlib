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
#include <ql/indexes/ibor/usdlibor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::usdlibor(py::module_& m) {
    py::class_<USDLibor, Libor, ext::shared_ptr<USDLibor>>(
        m, "USDLibor",
        "ICE USD LIBOR index.")
        .def(py::init([](const Period& tenor) {
            return ext::make_shared<USDLibor>(tenor);
        }),
             py::arg("tenor"),
             "Constructs a USD LIBOR index with the given tenor.")
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
             py::arg("tenor"),
             py::arg("h"),
             "Constructs a USD LIBOR index with a forwarding term structure handle.")
        .def(py::init([](const Period& tenor,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<USDLibor>(tenor,
                                              Handle<YieldTermStructure>(ts));
        }),
             py::arg("tenor"),
             py::arg("forwardingTermStructure"),
             "Constructs a USD LIBOR index (handle created internally).");

    py::class_<DailyTenorUSDLibor, DailyTenorLibor,
               ext::shared_ptr<DailyTenorUSDLibor>>(
        m, "DailyTenorUSDLibor",
        "Base class for the one-day-deposit ICE USD LIBOR indexes.")
        .def(py::init([](Natural settlementDays) {
            return ext::make_shared<DailyTenorUSDLibor>(settlementDays);
        }),
             py::arg("settlementDays"),
             "Constructs a daily-tenor USD LIBOR index.")
        .def(py::init<Natural, const Handle<YieldTermStructure>&>(),
             py::arg("settlementDays"),
             py::arg("h"),
             "Constructs a daily-tenor USD LIBOR index with a forwarding handle.")
        .def(py::init([](Natural settlementDays,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<DailyTenorUSDLibor>(
                settlementDays, Handle<YieldTermStructure>(ts));
        }),
             py::arg("settlementDays"),
             py::arg("forwardingTermStructure"),
             "Constructs a daily-tenor USD LIBOR index (handle created internally).");

    py::class_<USDLiborON, DailyTenorUSDLibor, ext::shared_ptr<USDLiborON>>(
        m, "USDLiborON",
        "Overnight ICE USD LIBOR index.")
        .def(py::init([]() { return ext::make_shared<USDLiborON>(); }),
             "Constructs an overnight USD LIBOR index.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
             py::arg("h"),
             "Constructs an overnight USD LIBOR index with a forwarding handle.")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<USDLiborON>(Handle<YieldTermStructure>(ts));
        }),
             py::arg("forwardingTermStructure"),
             "Constructs an overnight USD LIBOR index (handle created internally).");
}
