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
#include <ql/instruments/makeswaption.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::makeswaption(py::module_& m) {
    py::class_<MakeSwaption>(m, "MakeSwaption",
        "Helper class for constructing standard market swaptions.")
        // Constructor: tenor-based with py::none() sentinel for Null<Rate>()
        .def(py::init([](const ext::shared_ptr<SwapIndex>& swapIndex,
                         const Period& optionTenor,
                         const py::object& strike) {
            Rate s = strike.is_none() ? Null<Rate>() : strike.cast<Rate>();
            return MakeSwaption(swapIndex, optionTenor, s);
        }),
            py::arg("swapIndex"),
            py::arg("optionTenor"),
            py::arg("strike") = py::none(),
            "Constructs a swaption builder from option tenor.")
        // Constructor: fixing-date-based
        .def(py::init([](const ext::shared_ptr<SwapIndex>& swapIndex,
                         const Date& fixingDate,
                         const py::object& strike) {
            Rate s = strike.is_none() ? Null<Rate>() : strike.cast<Rate>();
            return MakeSwaption(swapIndex, fixingDate, s);
        }),
            py::arg("swapIndex"),
            py::arg("fixingDate"),
            py::arg("strike") = py::none(),
            "Constructs a swaption builder from fixing date.")
        // Builder methods
        .def("withNominal", &MakeSwaption::withNominal,
            py::arg("nominal"),
            py::return_value_policy::reference_internal,
            "Sets the nominal amount.")
        .def("withSettlementType", &MakeSwaption::withSettlementType,
            py::arg("type"),
            py::return_value_policy::reference_internal,
            "Sets the settlement type.")
        .def("withSettlementMethod", &MakeSwaption::withSettlementMethod,
            py::arg("method"),
            py::return_value_policy::reference_internal,
            "Sets the settlement method.")
        .def("withOptionConvention", &MakeSwaption::withOptionConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the option convention.")
        .def("withExerciseDate", &MakeSwaption::withExerciseDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the exercise date.")
        .def("withUnderlyingType", &MakeSwaption::withUnderlyingType,
            py::arg("type"),
            py::return_value_policy::reference_internal,
            "Sets the underlying swap type.")
        .def("withIndexedCoupons", &MakeSwaption::withIndexedCoupons,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Uses indexed coupons for the underlying swap.")
        .def("withAtParCoupons", &MakeSwaption::withAtParCoupons,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Uses at-par coupons for the underlying swap.")
        .def("withPricingEngine", &MakeSwaption::withPricingEngine,
            py::arg("engine"),
            py::return_value_policy::reference_internal,
            "Sets the pricing engine.")
        // Conversion to Swaption
        .def("swaption", [](const MakeSwaption& self) {
            return ext::shared_ptr<Swaption>(self);
        }, "Builds and returns the Swaption.");
}
