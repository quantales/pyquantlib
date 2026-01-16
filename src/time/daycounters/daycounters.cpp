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
#include <ql/time/daycounters/all.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::daycounters(py::module_& m)
{
    py::class_<Actual360, DayCounter, ext::shared_ptr<Actual360>>(m, "Actual360",
        "Actual/360 day count convention, also known as 'Act/360' or 'A/360'.")
        .def(py::init<>())
        ;

    py::class_<Actual364, DayCounter, ext::shared_ptr<Actual364>>(m, "Actual364",
        "Actual/364 day count convention.")
        .def(py::init<>())
        ;

    auto pyClassActual365Fixed =
        py::class_<Actual365Fixed, DayCounter, ext::shared_ptr<Actual365Fixed>>(m, "Actual365Fixed",
            "Actual/365 (Fixed) day count convention, also known as 'Act/365 (Fixed)' or 'A/365F'.");

    py::enum_<Actual365Fixed::Convention>(pyClassActual365Fixed, "Convention", py::arithmetic())
        .value("Standard", Actual365Fixed::Standard)
        .value("Canadian", Actual365Fixed::Canadian)
        .value("NoLeap", Actual365Fixed::NoLeap)
        .export_values();

    pyClassActual365Fixed
        .def(py::init<Actual365Fixed::Convention>(),
            py::arg("c") = Actual365Fixed::Standard)
        ;

    py::class_<Actual36525, DayCounter, ext::shared_ptr<Actual36525>>(m, "Actual36525",
        "Actual/365.25 day count convention.")
        .def(py::init<>())
        ;

    py::class_<Actual366, DayCounter, ext::shared_ptr<Actual366>>(m, "Actual366",
        "Actual/366 day count convention.")
        .def(py::init<>())
        ;


    auto pyClassActualActual =
        py::class_<ActualActual, DayCounter, ext::shared_ptr<ActualActual>>(m, "ActualActual",
            "Actual/Actual day count convention with ISDA, ISMA (Bond), and AFB (Euro) variants.");

    py::enum_<ActualActual::Convention>(pyClassActualActual, "Convention", py::arithmetic())
        .value("ISMA", ActualActual::ISMA)
        .value("Bond", ActualActual::Bond)
        .value("ISDA", ActualActual::ISDA)
        .value("Historical", ActualActual::Historical)
        .value("Actual365", ActualActual::Actual365)
        .value("AFB", ActualActual::AFB)
        .value("Euro", ActualActual::Euro)
        .export_values();

    pyClassActualActual
        .def(py::init<ActualActual::Convention>(),
            py::arg("c") = ActualActual::ISDA)
        ;

    py::class_<Business252, DayCounter, ext::shared_ptr<Business252>>(m, "Business252",
        "Business/252 day count convention.")
        .def(py::init<Calendar>(),
            py::arg("c") = Brazil())
        ;

    py::class_<OneDayCounter, DayCounter, ext::shared_ptr<OneDayCounter>>(m, "OneDayCounter",
        "1/1 day count convention.")
        .def(py::init<>())
        ;

    py::class_<SimpleDayCounter, DayCounter, ext::shared_ptr<SimpleDayCounter>>(m, "SimpleDayCounter",
        "Simple day counter returning whole-month distances as simple fractions "
        "(1 year = 1.0, 6 months = 0.5, etc.). Use with NullCalendar.")
        .def(py::init<>())
        ;

    auto pyClassThirty360 =
        py::class_<Thirty360, DayCounter, ext::shared_ptr<Thirty360>>(m, "Thirty360",
            "30/360 day count convention with various market variants (US, European, ISDA, etc.).");

    py::enum_<Thirty360::Convention>(pyClassThirty360, "Convention", py::arithmetic())
        .value("USA", Thirty360::USA)
        .value("BondBasis", Thirty360::BondBasis)
        .value("European", Thirty360::European)
        .value("EurobondBasis", Thirty360::EurobondBasis)
        .value("Italian", Thirty360::Italian)
        .value("German", Thirty360::German)
        .value("ISMA", Thirty360::ISMA)
        .value("ISDA", Thirty360::ISDA)
        .value("NASD", Thirty360::NASD)
        .export_values();

    pyClassThirty360
        .def(py::init<Thirty360::Convention>())
        ;

    py::class_<Thirty365, DayCounter, ext::shared_ptr<Thirty365>>(m, "Thirty365",
        "30/365 day count convention.")
        .def(py::init<>())
        ;

    m.def("yearFractionToDate", yearFractionToDate,
        py::arg("dayCounter"), py::arg("referenceDate"), py::arg("t"));
}