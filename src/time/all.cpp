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
#include "pyquantlib/binding_manager.h"


DECLARE_MODULE_BINDINGS(time_bindings) {
    // Basic time types
    ADD_MAIN_BINDING(manager, ql_time::weekday, "Weekday enum (Monday, Tuesday, etc.)");
    ADD_MAIN_BINDING(manager, ql_time::date, "Date class");
    ADD_MAIN_BINDING(manager, ql_time::timeunit, "TimeUnit enum (Days, Weeks, Months, Years)");
    ADD_MAIN_BINDING(manager, ql_time::frequency, "Frequency enum (Annual, Semiannual, Quarterly, etc.)");
    ADD_MAIN_BINDING(manager, ql_time::period, "Time period with length and units");

    // Business day conventions
    ADD_MAIN_BINDING(manager, ql_time::businessdayconvention, "Business day conventions");

    // Calendar
    ADD_MAIN_BINDING(manager, ql_time::calendar, "Calendar base class");
    ADD_MAIN_BINDING(manager, ql_time::calendars, "Specific calendar implementations (US, UK, etc.)");
    ADD_MAIN_BINDING(manager, ql_time::calendarvector, "A vector of Calendar objects, exposed as a Python list");

    // Day counters
    ADD_MAIN_BINDING(manager, ql_time::daycounter, "Day count convention base class");
    ADD_MAIN_BINDING(manager, ql_time::daycounters, "Day count implementations (Actual360, 30/360, etc.)");

    // Schedule
    ADD_MAIN_BINDING(manager, ql_time::dategenerationrule, "Date generation rules enum");
    ADD_MAIN_BINDING(manager, ql_time::schedule, "Schedule class");
}
