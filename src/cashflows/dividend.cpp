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
#include "pyquantlib/trampolines.h"
#include <ql/cashflows/dividend.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::dividend(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // Dividend ABC
    py::class_<Dividend, PyDividend, ext::shared_ptr<Dividend>, CashFlow>(
        base, "Dividend",
        "Abstract base class for dividends.")
        .def(py::init_alias<const Date&>(),
            py::arg("date"),
            "Constructs a dividend with a given date.")
        .def("date", &Dividend::date,
            "Returns the dividend date.");

    // FixedDividend
    py::class_<FixedDividend, Dividend, ext::shared_ptr<FixedDividend>>(
        m, "FixedDividend",
        "Fixed cash dividend.")
        .def(py::init<Real, const Date&>(),
            py::arg("amount"),
            py::arg("date"),
            "Constructs a fixed dividend.")
        .def("amount", py::overload_cast<>(&FixedDividend::amount, py::const_),
            "Returns the dividend amount.");

    // FractionalDividend
    py::class_<FractionalDividend, Dividend, ext::shared_ptr<FractionalDividend>>(
        m, "FractionalDividend",
        "Fractional (proportional) dividend.")
        .def(py::init<Real, const Date&>(),
            py::arg("rate"),
            py::arg("date"),
            "Constructs a fractional dividend (rate only).")
        .def(py::init<Real, Real, const Date&>(),
            py::arg("rate"),
            py::arg("nominal"),
            py::arg("date"),
            "Constructs a fractional dividend with nominal.")
        .def("rate", &FractionalDividend::rate,
            "Returns the dividend rate.")
        .def("nominal", &FractionalDividend::nominal,
            "Returns the nominal value.");

    // DividendVector helper function
    m.def("DividendVector",
        &DividendVector,
        py::arg("dividendDates"),
        py::arg("dividends"),
        "Builds a sequence of fixed dividends from dates and amounts.");
}
