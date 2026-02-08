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
#include <ql/instruments/makecapfloor.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::makecapfloor(py::module_& m) {
    py::class_<MakeCapFloor>(m, "MakeCapFloor",
        "Helper class for constructing standard market caps and floors.")
        // Constructor with py::none() sentinel for Null<Rate>()
        .def(py::init([](CapFloor::Type type,
                         const Period& tenor,
                         const ext::shared_ptr<IborIndex>& index,
                         const py::object& strike,
                         const Period& forwardStart) {
            Rate s = strike.is_none() ? Null<Rate>() : strike.cast<Rate>();
            return MakeCapFloor(type, tenor, index, s, forwardStart);
        }),
            py::arg("type"),
            py::arg("tenor"),
            py::arg("index"),
            py::arg("strike") = py::none(),
            py::arg("forwardStart") = Period(0, Days),
            "Constructs a cap/floor builder.")
        // Builder methods
        .def("withNominal", &MakeCapFloor::withNominal,
            py::arg("nominal"),
            py::return_value_policy::reference_internal,
            "Sets the nominal amount.")
        .def("withEffectiveDate", &MakeCapFloor::withEffectiveDate,
            py::arg("effectiveDate"),
            py::arg("firstCapletExcluded"),
            py::return_value_policy::reference_internal,
            "Sets the effective date.")
        .def("withTenor", &MakeCapFloor::withTenor,
            py::arg("tenor"),
            py::return_value_policy::reference_internal,
            "Sets the coupon tenor.")
        .def("withCalendar", &MakeCapFloor::withCalendar,
            py::arg("calendar"),
            py::return_value_policy::reference_internal,
            "Sets the calendar.")
        .def("withConvention", &MakeCapFloor::withConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the business day convention.")
        .def("withTerminationDateConvention",
            &MakeCapFloor::withTerminationDateConvention,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets the termination date convention.")
        .def("withRule", &MakeCapFloor::withRule,
            py::arg("rule"),
            py::return_value_policy::reference_internal,
            "Sets the date generation rule.")
        .def("withEndOfMonth", &MakeCapFloor::withEndOfMonth,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Sets the end-of-month flag.")
        .def("withFirstDate", &MakeCapFloor::withFirstDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the first date.")
        .def("withNextToLastDate", &MakeCapFloor::withNextToLastDate,
            py::arg("date"),
            py::return_value_policy::reference_internal,
            "Sets the next-to-last date.")
        .def("withDayCount", &MakeCapFloor::withDayCount,
            py::arg("dayCount"),
            py::return_value_policy::reference_internal,
            "Sets the day count convention.")
        .def("asOptionlet", &MakeCapFloor::asOptionlet,
            py::arg("flag") = true,
            py::return_value_policy::reference_internal,
            "Gets only the last coupon.")
        .def("withPricingEngine", &MakeCapFloor::withPricingEngine,
            py::arg("engine"),
            py::return_value_policy::reference_internal,
            "Sets the pricing engine.")
        // Conversion to CapFloor
        .def("capFloor", [](const MakeCapFloor& self) {
            return ext::shared_ptr<CapFloor>(self);
        }, "Builds and returns the CapFloor.");
}
