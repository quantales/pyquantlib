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
#include "pyquantlib/binding_manager.h"


DECLARE_MODULE_BINDINGS(time_bindings) {
    auto m = manager.module();
    
    // Basic time types
    manager.addFunction(ql_time::weekday, m, "Weekday enum (Monday, Tuesday, etc.)");
    manager.addFunction(ql_time::date, m, "Date class");
    manager.addFunction(ql_time::timeunit, m, "TimeUnit enum (Days, Weeks, Months, Years)");
    manager.addFunction(ql_time::frequency, m, "Frequency enum (Annual, Semiannual, Quarterly, etc.)");
    manager.addFunction(ql_time::period, m, "Time period with length and units");
    
    // Business day conventions
    manager.addFunction(ql_time::businessdayconvention, m, "Business day conventions");
    
    // Calendar
    manager.addFunction(ql_time::calendar, m, "Calendar base class");
    manager.addFunction(ql_time::calendars, m, "Specific calendar implementations (US, UK, etc.)");
    manager.addFunction(ql_time::calendarvector, m, "A vector of Calendar objects, exposed as a Python list");
    
    // Day counters
    manager.addFunction(ql_time::daycounter, m, "Day count convention base class");
    manager.addFunction(ql_time::daycounters, m, "Day count implementations (Actual360, 30/360, etc.)");
    
    // Schedule
    manager.addFunction(ql_time::dategenerationrule, m, "Date generation rules enum");
    manager.addFunction(ql_time::schedule, m, "Schedule class");
}
