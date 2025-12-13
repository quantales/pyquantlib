/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/time/period.hpp>
#include <ql/utilities/dataparsers.hpp>
#include <boost/functional/hash.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::period(py::module_& m) {
    py::class_<Period>(m, "Period", "Time period represented by length and units.")
        // Constructors
        .def(py::init<>())
        .def(py::init<Integer, TimeUnit>(), py::arg("length"), py::arg("units"))
        .def(py::init<Frequency>(), py::arg("frequency"))

        // String-based constructor to convert ISO 8601-style strings into Period objects
        .def(py::init([](const std::string& s) {
            try {
                return PeriodParser::parse(s);
            } catch (const std::exception& e) {
                throw py::value_error("Invalid period string '" + s + "': " + e.what());
            }
        }), "Create Period from a string like '3M', '2Y', etc.")

        // Member functions
        .def("length", &Period::length)
        .def("units", &Period::units)
        .def("frequency", &Period::frequency)
        .def("normalize", &Period::normalize)
        .def("normalized", &Period::normalized)

        // In-place operators
        .def("__iadd__", &Period::operator+=)
        .def("__isub__", &Period::operator-=)
        .def("__imul__", &Period::operator*=)
        .def("__itruediv__", &Period::operator/=)

        // Rich comparisons
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(py::self <= py::self)
        .def(py::self > py::self)
        .def(py::self >= py::self)

        // Arithmetic operators
        .def("__neg__", [](const Period& p) { return -p; })
        .def("__add__", [](const Period& a, const Period& b) { return a + b; })
        .def("__sub__", [](const Period& a, const Period& b) { return a - b; })
        .def("__mul__", [](const Period& a, Integer n) { return a * n; }, py::is_operator())
        .def("__rmul__", [](const Period& a, Integer n) { return n * a; }, py::is_operator())
        .def("__truediv__", [](const Period& a, Integer n) { return a / n; }, py::is_operator())

        // __str__ and __repr__
        .def("__str__", [](const Period& p) {
            std::ostringstream oss;
            oss << p;
            return oss.str();
        })
        .def("__repr__", [](const Period& p) {
            std::ostringstream oss;
            oss << "<Period: " << p << ">";
            return oss.str();
        })

        .def("__hash__", [](const Period& p) {
            size_t seed = 0;
            Period per = p.normalized();
            boost::hash_combine(seed, per.length());
            boost::hash_combine(seed, per.units());
            return seed;
        })
        ;

    // Free functions (global)
    m.def("years", &years, py::arg("period"), "Convert a Period to years.");
    m.def("months", &months, py::arg("period"), "Convert a Period to months.");
    m.def("weeks", &weeks, py::arg("period"), "Convert a Period to weeks.");
    m.def("days", &days, py::arg("period"), "Convert a Period to days.");
}
