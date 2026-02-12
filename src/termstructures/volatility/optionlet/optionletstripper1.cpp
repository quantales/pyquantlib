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
#include <ql/termstructures/volatility/optionlet/optionletstripper1.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::optionletstripper1(py::module_& m) {
    py::class_<OptionletStripper1,
               ext::shared_ptr<OptionletStripper1>, OptionletStripper>(
        m, "OptionletStripper1",
        "Strips optionlet volatilities from a cap/floor term volatility surface.")
        // Constructor with py::none() sentinels for Null<Rate>() and ext::nullopt
        .def(py::init([](const ext::shared_ptr<CapFloorTermVolSurface>& surface,
                         const ext::shared_ptr<IborIndex>& index,
                         const py::object& switchStrike,
                         Real accuracy, Natural maxIter,
                         const Handle<YieldTermStructure>& discount,
                         VolatilityType type, Real displacement,
                         bool dontThrow,
                         const py::object& optionletFrequency) {
            Rate ss = switchStrike.is_none() ? Null<Rate>()
                                             : switchStrike.cast<Rate>();
            ext::optional<Period> freq = optionletFrequency.is_none()
                ? ext::nullopt
                : ext::optional<Period>(optionletFrequency.cast<Period>());
            return ext::make_shared<OptionletStripper1>(
                surface, index, ss, accuracy, maxIter,
                discount, type, displacement, dontThrow, freq);
        }),
            py::arg("termVolSurface"),
            py::arg("index"),
            py::arg("switchStrike") = py::none(),
            py::arg("accuracy") = 1.0e-6,
            py::arg("maxIter") = 100,
            py::arg("discount") = Handle<YieldTermStructure>(),
            py::arg("type") = ShiftedLognormal,
            py::arg("displacement") = 0.0,
            py::arg("dontThrow") = false,
            py::arg("optionletFrequency") = py::none(),
            "Constructs an optionlet stripper.")
        // Hidden handle: accept shared_ptr<YieldTermStructure> for discount
        .def(py::init([](const ext::shared_ptr<CapFloorTermVolSurface>& surface,
                         const ext::shared_ptr<IborIndex>& index,
                         const py::object& switchStrike,
                         Real accuracy, Natural maxIter,
                         const ext::shared_ptr<YieldTermStructure>& discount,
                         VolatilityType type, Real displacement,
                         bool dontThrow,
                         const py::object& optionletFrequency) {
            Rate ss = switchStrike.is_none() ? Null<Rate>()
                                             : switchStrike.cast<Rate>();
            ext::optional<Period> freq = optionletFrequency.is_none()
                ? ext::nullopt
                : ext::optional<Period>(optionletFrequency.cast<Period>());
            return ext::make_shared<OptionletStripper1>(
                surface, index, ss, accuracy, maxIter,
                Handle<YieldTermStructure>(discount),
                type, displacement, dontThrow, freq);
        }),
            py::arg("termVolSurface"),
            py::arg("index"),
            py::arg("switchStrike") = py::none(),
            py::arg("accuracy") = 1.0e-6,
            py::arg("maxIter") = 100,
            py::arg("discount"),
            py::arg("type") = ShiftedLognormal,
            py::arg("displacement") = 0.0,
            py::arg("dontThrow") = false,
            py::arg("optionletFrequency") = py::none(),
            "Constructs an optionlet stripper (handle created internally).")
        .def("capFloorPrices", &OptionletStripper1::capFloorPrices,
            py::return_value_policy::reference_internal,
            "Returns the cap/floor prices matrix.")
        .def("capletVols", &OptionletStripper1::capletVols,
            py::return_value_policy::reference_internal,
            "Returns the caplet volatilities matrix.")
        .def("capFloorVolatilities", &OptionletStripper1::capFloorVolatilities,
            py::return_value_policy::reference_internal,
            "Returns the cap/floor volatilities matrix.")
        .def("optionletPrices", &OptionletStripper1::optionletPrices,
            py::return_value_policy::reference_internal,
            "Returns the optionlet prices matrix.")
        .def("switchStrike", &OptionletStripper1::switchStrike,
            "Returns the switch strike.");
}
