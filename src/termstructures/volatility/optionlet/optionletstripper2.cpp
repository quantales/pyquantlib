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
#include <ql/termstructures/volatility/optionlet/optionletstripper2.hpp>
#include <ql/termstructures/volatility/optionlet/optionletstripper1.hpp>
#include <ql/termstructures/volatility/capfloor/capfloortermvolcurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::optionletstripper2(py::module_& m) {
    py::class_<OptionletStripper2,
               ext::shared_ptr<OptionletStripper2>, OptionletStripper>(
        m, "OptionletStripper2",
        "Adjusts stripped optionlet volatilities to match at-the-money cap/floor "
        "term volatilities.")
        .def(py::init([](const ext::shared_ptr<OptionletStripper1>& stripper,
                         const ext::shared_ptr<CapFloorTermVolCurve>& atmCurve) {
            return ext::make_shared<OptionletStripper2>(
                stripper, Handle<CapFloorTermVolCurve>(atmCurve));
        }),
            py::arg("optionletStripper1"),
            py::arg("atmCapFloorTermVolCurve"),
            "Constructs from a stripper and an ATM cap/floor term volatility curve "
            "(handle created internally).")
        .def("atmCapFloorStrikes", &OptionletStripper2::atmCapFloorStrikes,
            "Returns the at-the-money cap/floor strikes.")
        .def("atmCapFloorPrices", &OptionletStripper2::atmCapFloorPrices,
            "Returns the at-the-money cap/floor prices.")
        .def("spreadsVol", &OptionletStripper2::spreadsVol,
            "Returns the volatility spreads applied to match the ATM curve.");
}
