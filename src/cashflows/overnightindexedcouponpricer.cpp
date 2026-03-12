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
#include <ql/cashflows/overnightindexedcouponpricer.hpp>
#include <ql/cashflows/blackovernightindexedcouponpricer.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::overnightindexedcouponpricer(py::module_& m) {
    py::class_<CompoundingOvernightIndexedCouponPricer,
               FloatingRateCouponPricer,
               ext::shared_ptr<CompoundingOvernightIndexedCouponPricer>>(
        m, "CompoundingOvernightIndexedCouponPricer",
        "Pricer for compounded overnight indexed coupons.")
        .def(py::init<>(),
            "Constructs a compounding overnight pricer.")
        .def("swapletRate", &CompoundingOvernightIndexedCouponPricer::swapletRate,
            "Returns the compounded swaplet rate.");

    py::class_<ArithmeticAveragedOvernightIndexedCouponPricer,
               FloatingRateCouponPricer,
               ext::shared_ptr<ArithmeticAveragedOvernightIndexedCouponPricer>>(
        m, "ArithmeticAveragedOvernightIndexedCouponPricer",
        "Pricer for arithmetically averaged overnight indexed coupons.")
        .def(py::init<Real, Real, bool>(),
            py::arg("meanReversion") = 0.03,
            py::arg("volatility") = 0.00,
            py::arg("byApprox") = false,
            "Constructs with convexity adjustment parameters.")
        .def(py::init<bool>(),
            py::arg("byApprox"),
            "Constructs with approximation flag (no convexity adjustment).")
        .def("swapletRate",
            &ArithmeticAveragedOvernightIndexedCouponPricer::swapletRate,
            "Returns the averaged swaplet rate.");

    py::class_<BlackCompoundingOvernightIndexedCouponPricer,
               CompoundingOvernightIndexedCouponPricer,
               ext::shared_ptr<BlackCompoundingOvernightIndexedCouponPricer>>(
        m, "BlackCompoundingOvernightIndexedCouponPricer",
        "Black pricer for capped/floored compounded overnight coupons.")
        .def(py::init<>(),
            "Constructs without optionlet volatility.")
        .def(py::init<Handle<OptionletVolatilityStructure>, bool>(),
            py::arg("v"),
            py::arg("effectiveVolatilityInput") = false,
            "Constructs with optionlet volatility and effective vol flag.");

    py::class_<BlackAveragingOvernightIndexedCouponPricer,
               ArithmeticAveragedOvernightIndexedCouponPricer,
               ext::shared_ptr<BlackAveragingOvernightIndexedCouponPricer>>(
        m, "BlackAveragingOvernightIndexedCouponPricer",
        "Black pricer for capped/floored averaged overnight coupons.")
        .def(py::init<>(),
            "Constructs without optionlet volatility.")
        .def(py::init<Handle<OptionletVolatilityStructure>, bool>(),
            py::arg("v"),
            py::arg("effectiveVolatilityInput") = false,
            "Constructs with optionlet volatility and effective vol flag.");
}
