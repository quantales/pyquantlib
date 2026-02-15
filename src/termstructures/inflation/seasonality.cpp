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
#include <ql/termstructures/inflation/seasonality.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::seasonality(py::module_& m) {
    // Seasonality ABC (base submodule)
    auto base = py::module_::import("pyquantlib.base");

    py::class_<Seasonality, PySeasonality, ext::shared_ptr<Seasonality>>(
        base, "Seasonality",
        "Abstract base class for inflation seasonality corrections.")
        .def(py::init_alias<>())
        .def("correctZeroRate", &Seasonality::correctZeroRate,
            py::arg("date"), py::arg("rate"),
            py::arg("inflationTermStructure"),
            "Returns the seasonality-corrected zero rate.")
        .def("correctYoYRate", &Seasonality::correctYoYRate,
            py::arg("date"), py::arg("rate"),
            py::arg("inflationTermStructure"),
            "Returns the seasonality-corrected year-on-year rate.")
        .def("isConsistent", &Seasonality::isConsistent,
            py::arg("inflationTermStructure"),
            "Returns true if the seasonality is consistent with the term structure.");

    // MultiplicativePriceSeasonality (main module)
    py::class_<MultiplicativePriceSeasonality, Seasonality,
               ext::shared_ptr<MultiplicativePriceSeasonality>>(
        m, "MultiplicativePriceSeasonality",
        "Multiplicative price seasonality correction.")
        .def(py::init<>(),
            "Constructs a default (empty) seasonality.")
        .def(py::init<const Date&, Frequency, const std::vector<Rate>&>(),
            py::arg("seasonalityBaseDate"),
            py::arg("frequency"),
            py::arg("seasonalityFactors"),
            "Constructs from base date, frequency, and factors.")
        .def("set", &MultiplicativePriceSeasonality::set,
            py::arg("seasonalityBaseDate"),
            py::arg("frequency"),
            py::arg("seasonalityFactors"),
            "Sets the seasonality parameters.")
        .def("seasonalityBaseDate",
            &MultiplicativePriceSeasonality::seasonalityBaseDate,
            "Returns the seasonality base date.")
        .def("frequency", &MultiplicativePriceSeasonality::frequency,
            "Returns the seasonality frequency.")
        .def("seasonalityFactors",
            &MultiplicativePriceSeasonality::seasonalityFactors,
            "Returns the seasonality factors.")
        .def("seasonalityFactor",
            &MultiplicativePriceSeasonality::seasonalityFactor,
            py::arg("date"),
            "Returns the seasonality factor for the given date.");

    // KerkhofSeasonality
    py::class_<KerkhofSeasonality, MultiplicativePriceSeasonality,
               ext::shared_ptr<KerkhofSeasonality>>(
        m, "KerkhofSeasonality",
        "Kerkhof seasonality correction (monthly frequency).")
        .def(py::init<const Date&, const std::vector<Rate>&>(),
            py::arg("seasonalityBaseDate"),
            py::arg("seasonalityFactors"),
            "Constructs from base date and monthly factors.");
}
