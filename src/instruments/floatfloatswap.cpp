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
#include <ql/instruments/floatfloatswap.hpp>
#include <ql/indexes/interestrateindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::floatfloatswap(py::module_& m) {
    py::class_<FloatFloatSwap, Swap, ext::shared_ptr<FloatFloatSwap>>(
        m, "FloatFloatSwap",
        "Swap exchanging two floating legs with caps and floors.")
        // Scalar constructor
        .def(py::init([](Swap::Type type,
                         Real nominal1, Real nominal2,
                         Schedule schedule1,
                         ext::shared_ptr<InterestRateIndex> index1,
                         DayCounter dayCount1,
                         Schedule schedule2,
                         ext::shared_ptr<InterestRateIndex> index2,
                         DayCounter dayCount2,
                         bool intermediateCapitalExchange,
                         bool finalCapitalExchange,
                         Real gearing1, Real spread1,
                         const py::object& cappedRate1,
                         const py::object& flooredRate1,
                         Real gearing2, Real spread2,
                         const py::object& cappedRate2,
                         const py::object& flooredRate2,
                         const py::object& paymentConvention1,
                         const py::object& paymentConvention2) {
            Real cap1 = cappedRate1.is_none() ? Null<Real>() : cappedRate1.cast<Real>();
            Real floor1 = flooredRate1.is_none() ? Null<Real>() : flooredRate1.cast<Real>();
            Real cap2 = cappedRate2.is_none() ? Null<Real>() : cappedRate2.cast<Real>();
            Real floor2 = flooredRate2.is_none() ? Null<Real>() : flooredRate2.cast<Real>();
            ext::optional<BusinessDayConvention> pc1 = ext::nullopt;
            ext::optional<BusinessDayConvention> pc2 = ext::nullopt;
            if (!paymentConvention1.is_none())
                pc1 = paymentConvention1.cast<BusinessDayConvention>();
            if (!paymentConvention2.is_none())
                pc2 = paymentConvention2.cast<BusinessDayConvention>();
            return ext::make_shared<FloatFloatSwap>(
                type, nominal1, nominal2,
                std::move(schedule1), std::move(index1), std::move(dayCount1),
                std::move(schedule2), std::move(index2), std::move(dayCount2),
                intermediateCapitalExchange, finalCapitalExchange,
                gearing1, spread1, cap1, floor1,
                gearing2, spread2, cap2, floor2,
                pc1, pc2);
        }),
            py::arg("type"),
            py::arg("nominal1"),
            py::arg("nominal2"),
            py::arg("schedule1"),
            py::arg("index1"),
            py::arg("dayCount1"),
            py::arg("schedule2"),
            py::arg("index2"),
            py::arg("dayCount2"),
            py::arg("intermediateCapitalExchange") = false,
            py::arg("finalCapitalExchange") = false,
            py::arg("gearing1") = 1.0,
            py::arg("spread1") = 0.0,
            py::arg("cappedRate1") = py::none(),
            py::arg("flooredRate1") = py::none(),
            py::arg("gearing2") = 1.0,
            py::arg("spread2") = 0.0,
            py::arg("cappedRate2") = py::none(),
            py::arg("flooredRate2") = py::none(),
            py::arg("paymentConvention1") = py::none(),
            py::arg("paymentConvention2") = py::none(),
            "Constructs with scalar parameters.")
        // Vector constructor
        .def(py::init([](Swap::Type type,
                         std::vector<Real> nominal1,
                         std::vector<Real> nominal2,
                         Schedule schedule1,
                         ext::shared_ptr<InterestRateIndex> index1,
                         DayCounter dayCount1,
                         Schedule schedule2,
                         ext::shared_ptr<InterestRateIndex> index2,
                         DayCounter dayCount2,
                         bool intermediateCapitalExchange,
                         bool finalCapitalExchange,
                         std::vector<Real> gearing1,
                         std::vector<Real> spread1,
                         std::vector<Real> cappedRate1,
                         std::vector<Real> flooredRate1,
                         std::vector<Real> gearing2,
                         std::vector<Real> spread2,
                         std::vector<Real> cappedRate2,
                         std::vector<Real> flooredRate2,
                         const py::object& paymentConvention1,
                         const py::object& paymentConvention2) {
            ext::optional<BusinessDayConvention> pc1 = ext::nullopt;
            ext::optional<BusinessDayConvention> pc2 = ext::nullopt;
            if (!paymentConvention1.is_none())
                pc1 = paymentConvention1.cast<BusinessDayConvention>();
            if (!paymentConvention2.is_none())
                pc2 = paymentConvention2.cast<BusinessDayConvention>();
            return ext::make_shared<FloatFloatSwap>(
                type, std::move(nominal1), std::move(nominal2),
                std::move(schedule1), std::move(index1), std::move(dayCount1),
                std::move(schedule2), std::move(index2), std::move(dayCount2),
                intermediateCapitalExchange, finalCapitalExchange,
                std::move(gearing1), std::move(spread1),
                std::move(cappedRate1), std::move(flooredRate1),
                std::move(gearing2), std::move(spread2),
                std::move(cappedRate2), std::move(flooredRate2),
                pc1, pc2);
        }),
            py::arg("type"),
            py::arg("nominal1"),
            py::arg("nominal2"),
            py::arg("schedule1"),
            py::arg("index1"),
            py::arg("dayCount1"),
            py::arg("schedule2"),
            py::arg("index2"),
            py::arg("dayCount2"),
            py::arg("intermediateCapitalExchange") = false,
            py::arg("finalCapitalExchange") = false,
            py::arg("gearing1") = std::vector<Real>(),
            py::arg("spread1") = std::vector<Real>(),
            py::arg("cappedRate1") = std::vector<Real>(),
            py::arg("flooredRate1") = std::vector<Real>(),
            py::arg("gearing2") = std::vector<Real>(),
            py::arg("spread2") = std::vector<Real>(),
            py::arg("cappedRate2") = std::vector<Real>(),
            py::arg("flooredRate2") = std::vector<Real>(),
            py::arg("paymentConvention1") = py::none(),
            py::arg("paymentConvention2") = py::none(),
            "Constructs with vector parameters.")
        // Inspectors
        .def("type", &FloatFloatSwap::type,
            "Returns the swap type.")
        .def("nominal1", &FloatFloatSwap::nominal1,
            py::return_value_policy::reference_internal,
            "Returns leg 1 nominals.")
        .def("nominal2", &FloatFloatSwap::nominal2,
            py::return_value_policy::reference_internal,
            "Returns leg 2 nominals.")
        .def("schedule1", &FloatFloatSwap::schedule1,
            py::return_value_policy::reference_internal,
            "Returns leg 1 schedule.")
        .def("schedule2", &FloatFloatSwap::schedule2,
            py::return_value_policy::reference_internal,
            "Returns leg 2 schedule.")
        .def("index1", &FloatFloatSwap::index1,
            py::return_value_policy::reference_internal,
            "Returns leg 1 index.")
        .def("index2", &FloatFloatSwap::index2,
            py::return_value_policy::reference_internal,
            "Returns leg 2 index.")
        .def("spread1", &FloatFloatSwap::spread1,
            "Returns leg 1 spreads.")
        .def("spread2", &FloatFloatSwap::spread2,
            "Returns leg 2 spreads.")
        .def("gearing1", &FloatFloatSwap::gearing1,
            "Returns leg 1 gearings.")
        .def("gearing2", &FloatFloatSwap::gearing2,
            "Returns leg 2 gearings.")
        .def("cappedRate1", &FloatFloatSwap::cappedRate1,
            "Returns leg 1 caps.")
        .def("flooredRate1", &FloatFloatSwap::flooredRate1,
            "Returns leg 1 floors.")
        .def("cappedRate2", &FloatFloatSwap::cappedRate2,
            "Returns leg 2 caps.")
        .def("flooredRate2", &FloatFloatSwap::flooredRate2,
            "Returns leg 2 floors.")
        .def("dayCount1", &FloatFloatSwap::dayCount1,
            py::return_value_policy::reference_internal,
            "Returns leg 1 day counter.")
        .def("dayCount2", &FloatFloatSwap::dayCount2,
            py::return_value_policy::reference_internal,
            "Returns leg 2 day counter.")
        .def("paymentConvention1", &FloatFloatSwap::paymentConvention1,
            "Returns leg 1 payment convention.")
        .def("paymentConvention2", &FloatFloatSwap::paymentConvention2,
            "Returns leg 2 payment convention.")
        .def("leg1", &FloatFloatSwap::leg1,
            py::return_value_policy::reference_internal,
            "Returns leg 1 cash flows.")
        .def("leg2", &FloatFloatSwap::leg2,
            py::return_value_policy::reference_internal,
            "Returns leg 2 cash flows.");
}
