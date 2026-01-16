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
#include <ql/time/businessdayconvention.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::businessdayconvention(py::module_& m)
{
    py::enum_<QuantLib::BusinessDayConvention>(m, "BusinessDayConvention",
        "Conventions for adjusting dates that fall on non-business days.")
        .value("Following", QuantLib::Following,
            "Choose the first business day after the given holiday.")
        .value("ModifiedFollowing", QuantLib::ModifiedFollowing,
            "Choose the first business day after the holiday unless it belongs "
            "to a different month, in which case choose the first before.")
        .value("Preceding", QuantLib::Preceding,
            "Choose the first business day before the given holiday.")
        .value("ModifiedPreceding", QuantLib::ModifiedPreceding,
            "Choose the first business day before the holiday unless it belongs "
            "to a different month, in which case choose the first after.")
        .value("Unadjusted", QuantLib::Unadjusted,
            "Do not adjust.")
        .value("HalfMonthModifiedFollowing", QuantLib::HalfMonthModifiedFollowing,
            "Choose the first business day after the holiday unless that day "
            "crosses mid-month (15th) or end of month, then choose before.")
        .value("Nearest", QuantLib::Nearest,
            "Choose the nearest business day. If equidistant, default to following.")
        .export_values();
}