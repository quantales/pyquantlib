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
#include <ql/interestrate.hpp>
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <boost/functional/hash.hpp>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::interestrate(py::module_& m) {
    py::class_<InterestRate>(m, "InterestRate",
        "Interest rate with compounding algebra.")
        .def(py::init<>(),
            "Default constructor returning a null interest rate.")
        .def(py::init<Rate, DayCounter, Compounding, Frequency>(),
            py::arg("rate"), py::arg("dayCounter"), py::arg("compounding"), py::arg("frequency"),
            "Construct an interest rate with the given parameters.")
        .def("rate", &InterestRate::rate,
            "Returns the rate value.")
        .def("dayCounter", &InterestRate::dayCounter,
            "Returns the day counter.")
        .def("compounding", &InterestRate::compounding,
            "Returns the compounding convention.")
        .def("frequency", &InterestRate::frequency,
            "Returns the compounding frequency.")
        .def("discountFactor",
            py::overload_cast<Time>(&InterestRate::discountFactor, py::const_),
            py::arg("time"),
            "Discount factor for a given time period.")
        .def("discountFactor",
            py::overload_cast<const Date&, const Date&, const Date&, const Date&>(
                &InterestRate::discountFactor, py::const_),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("refStart") = Date(), py::arg("refEnd") = Date(),
            "Discount factor between two dates.")
        .def("compoundFactor",
            py::overload_cast<Time>(&InterestRate::compoundFactor, py::const_),
            py::arg("time"),
            "Compound factor for a given time period.")
        .def("compoundFactor",
            py::overload_cast<const Date&, const Date&, const Date&, const Date&>(
                &InterestRate::compoundFactor, py::const_),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("refStart") = Date(), py::arg("refEnd") = Date(),
            "Compound factor between two dates.")
        .def_static("impliedRate",
            py::overload_cast<Real, const DayCounter&, Compounding, Frequency, Time>(
                &InterestRate::impliedRate),
            py::arg("compound"), py::arg("dayCounter"), py::arg("compounding"),
            py::arg("frequency"), py::arg("time"),
            "Implied rate from a compound factor over a time period.")
        .def_static("impliedRate",
            py::overload_cast<Real, const DayCounter&, Compounding, Frequency,
                const Date&, const Date&, const Date&, const Date&>(
                &InterestRate::impliedRate),
            py::arg("compound"), py::arg("dayCounter"), py::arg("compounding"),
            py::arg("frequency"), py::arg("startDate"), py::arg("endDate"),
            py::arg("refStart") = Date(), py::arg("refEnd") = Date(),
            "Implied rate from a compound factor between two dates.")
        .def("equivalentRate",
            py::overload_cast<Compounding, Frequency, Time>(
                &InterestRate::equivalentRate, py::const_),
            py::arg("compounding"), py::arg("frequency"), py::arg("time"),
            "Equivalent rate with different compounding over a time period.")
        .def("equivalentRate",
            py::overload_cast<const DayCounter&, Compounding, Frequency,
                Date, Date, const Date&, const Date&>(
                &InterestRate::equivalentRate, py::const_),
            py::arg("dayCounter"), py::arg("compounding"), py::arg("frequency"),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("refStart") = Date(), py::arg("refEnd") = Date(),
            "Equivalent rate with different compounding between two dates.")
        .def("isNull", [](const InterestRate& ir) {
                return ir.rate() == Null<Rate>();
            },
            "Returns true if the rate is null (uninitialized).")
        .def("__str__", [](const InterestRate& ir) {
                std::ostringstream oss;
                oss << ir;
                return oss.str();
            })
        .def("__repr__", [](const InterestRate& ir) {
                std::ostringstream oss;
                oss << "<InterestRate: " << ir << ">";
                return oss.str();
            })
        .def("__float__", [](const InterestRate& ir) {
                return static_cast<double>(ir.rate());
            })
        .def("__eq__", [](const InterestRate& lhs, const InterestRate& rhs) {
                return lhs.rate() == rhs.rate() &&
                       lhs.dayCounter().name() == rhs.dayCounter().name() &&
                       lhs.compounding() == rhs.compounding() &&
                       lhs.frequency() == rhs.frequency();
            }, py::is_operator())
        .def("__ne__", [](const InterestRate& lhs, const InterestRate& rhs) {
                return lhs.rate() != rhs.rate() ||
                       lhs.dayCounter().name() != rhs.dayCounter().name() ||
                       lhs.compounding() != rhs.compounding() ||
                       lhs.frequency() != rhs.frequency();
            }, py::is_operator())
        .def("__hash__", [](const InterestRate& ir) {
                size_t seed = 0;
                boost::hash_combine(seed, ir.rate());
                boost::hash_combine(seed, ir.dayCounter().name());
                boost::hash_combine(seed, static_cast<int>(ir.compounding()));
                boost::hash_combine(seed, static_cast<int>(ir.frequency()));
                return seed;
            });
}
