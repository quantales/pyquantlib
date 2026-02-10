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
#include <ql/cashflows/couponpricer.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::couponpricer_base(py::module_& m) {
    py::class_<FloatingRateCouponPricer, ext::shared_ptr<FloatingRateCouponPricer>,
               Observer, Observable>(m, "FloatingRateCouponPricer",
        "Abstract base class for floating-rate coupon pricers.");
}

void ql_cashflows::couponpricer(py::module_& m) {
    py::class_<BlackIborCouponPricer, FloatingRateCouponPricer,
               ext::shared_ptr<BlackIborCouponPricer>>(m, "BlackIborCouponPricer",
        "Black-formula pricer for capped/floored Ibor coupons.")
        .def(py::init<>(),
             "Constructs with no optionlet volatility.")
        .def(py::init<const Handle<OptionletVolatilityStructure>&>(),
             py::arg("volatility"),
             "Constructs with optionlet volatility.");

    m.def("setCouponPricer",
        [](const Leg& leg, const ext::shared_ptr<FloatingRateCouponPricer>& pricer) {
            setCouponPricer(leg, pricer);
        },
        py::arg("leg"), py::arg("pricer"),
        "Sets the coupon pricer for all floating-rate coupons in the leg.");
}

void ql_cashflows::cmscouponpricer(py::module_& m) {
    // MeanRevertingPricer ABC
    py::class_<MeanRevertingPricer, ext::shared_ptr<MeanRevertingPricer>>(m, "MeanRevertingPricer",
        "ABC for mean-reverting coupon pricers.")
        .def("meanReversion", &MeanRevertingPricer::meanReversion,
            "Returns the mean reversion value.")
        .def("setMeanReversion", &MeanRevertingPricer::setMeanReversion,
            py::arg("meanReversion"),
            "Sets the mean reversion handle.");

    // CmsCouponPricer ABC
    py::class_<CmsCouponPricer, FloatingRateCouponPricer,
               ext::shared_ptr<CmsCouponPricer>>(m, "CmsCouponPricer",
        "ABC for CMS coupon pricers.")
        .def("swaptionVolatility", &CmsCouponPricer::swaptionVolatility,
            "Returns the swaption volatility handle.")
        .def("setSwaptionVolatility",
            [](CmsCouponPricer& self, const py::object& vol) {
                if (vol.is_none())
                    self.setSwaptionVolatility();
                else
                    self.setSwaptionVolatility(
                        vol.cast<Handle<SwaptionVolatilityStructure>>());
            },
            py::arg("volatility") = py::none(),
            "Sets the swaption volatility handle.");
}
