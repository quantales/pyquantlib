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
#include <ql/instruments/makeyoyinflationcapfloor.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::makeyoyinflationcapfloor(py::module_& m) {
    py::class_<MakeYoYInflationCapFloor>(
        m, "MakeYoYInflationCapFloor",
        "Builder for YoY inflation caps and floors.")
        .def(py::init<YoYInflationCapFloor::Type,
                       ext::shared_ptr<YoYInflationIndex>,
                       const Size&,
                       Calendar,
                       const Period&,
                       CPI::InterpolationType>(),
            py::arg("type"),
            py::arg("index"),
            py::arg("length"),
            py::arg("calendar"),
            py::arg("observationLag"),
            py::arg("interpolation"),
            "Constructs a MakeYoYInflationCapFloor builder.")
        .def("withNominal",
            [](MakeYoYInflationCapFloor& self, Real n)
                -> MakeYoYInflationCapFloor& {
                return self.withNominal(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withEffectiveDate",
            [](MakeYoYInflationCapFloor& self, const Date& d)
                -> MakeYoYInflationCapFloor& {
                return self.withEffectiveDate(d);
            },
            py::return_value_policy::reference_internal,
            py::arg("effectiveDate"))
        .def("withPaymentDayCounter",
            [](MakeYoYInflationCapFloor& self, const DayCounter& dc)
                -> MakeYoYInflationCapFloor& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal,
            py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](MakeYoYInflationCapFloor& self, BusinessDayConvention bdc)
                -> MakeYoYInflationCapFloor& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal,
            py::arg("convention"))
        .def("withFixingDays",
            [](MakeYoYInflationCapFloor& self, Natural days)
                -> MakeYoYInflationCapFloor& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal,
            py::arg("fixingDays"))
        .def("withPricingEngine",
            [](MakeYoYInflationCapFloor& self,
               const ext::shared_ptr<PricingEngine>& engine)
                -> MakeYoYInflationCapFloor& {
                return self.withPricingEngine(engine);
            },
            py::return_value_policy::reference_internal, py::arg("engine"))
        .def("asOptionlet",
            [](MakeYoYInflationCapFloor& self, bool b)
                -> MakeYoYInflationCapFloor& {
                return self.asOptionlet(b);
            },
            py::return_value_policy::reference_internal,
            py::arg("flag") = true)
        .def("withStrike",
            [](MakeYoYInflationCapFloor& self, Rate strike)
                -> MakeYoYInflationCapFloor& {
                return self.withStrike(strike);
            },
            py::return_value_policy::reference_internal, py::arg("strike"))
        .def("withAtmStrike",
            [](MakeYoYInflationCapFloor& self,
               const Handle<YieldTermStructure>& yts)
                -> MakeYoYInflationCapFloor& {
                return self.withAtmStrike(yts);
            },
            py::return_value_policy::reference_internal,
            py::arg("nominalTermStructure"))
        .def("withForwardStart",
            [](MakeYoYInflationCapFloor& self, Period fwd)
                -> MakeYoYInflationCapFloor& {
                return self.withForwardStart(std::move(fwd));
            },
            py::return_value_policy::reference_internal,
            py::arg("forwardStart"))
        // Named conversion method
        .def("capFloor",
            [](const MakeYoYInflationCapFloor& self) {
                return static_cast<ext::shared_ptr<YoYInflationCapFloor>>(
                    self);
            },
            "Builds and returns the YoY inflation cap/floor.");
}
