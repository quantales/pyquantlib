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

#pragma once

#include <ql/time/date.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>

namespace pybind11 {
namespace detail {

/**
 * Custom type caster for QuantLib::Date.
 *
 * Enables automatic conversion between Python datetime.date/datetime
 * and QuantLib::Date.
 */
template <>
struct type_caster<QuantLib::Date> {
public:
    PYBIND11_TYPE_CASTER(QuantLib::Date, _("QuantLib::Date"));

    // Python -> C++
    bool load(py::handle src, bool) {
        py::object datetime = py::module_::import("datetime");
        if (py::isinstance(src, datetime.attr("date")) ||
            py::isinstance(src, datetime.attr("datetime"))) {
            auto dt = py::reinterpret_borrow<py::object>(src);
            int day = dt.attr("day").cast<int>();
            int month = dt.attr("month").cast<int>();
            int year = dt.attr("year").cast<int>();
            value = QuantLib::Date(day, static_cast<QuantLib::Month>(month), year);
            return true;
        }

        throw py::type_error(
            "Cannot convert object to QuantLib::Date. "
            "Expected datetime.date or datetime.datetime.");
    }

    // C++ -> Python
    static handle cast(const QuantLib::Date& d, return_value_policy, handle) {
        py::module_ datetime = py::module_::import("datetime");
        return datetime.attr("date")(d.year(), d.month(), d.dayOfMonth())
            .release();
    }
};

}  // namespace detail
}  // namespace pybind11
