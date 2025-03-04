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

#pragma once

#include <pybind11/pybind11.h>
#include "pyquantlib/binding_manager.h"

// Support for boost::shared_ptr when QuantLib uses it
// QuantLib defines QL_USE_STD_SHARED_PTR when using std::shared_ptr
#if !defined(QL_USE_STD_SHARED_PTR)
PYBIND11_DECLARE_HOLDER_TYPE(T, boost::shared_ptr<T>, true);
#endif

namespace py = pybind11;

// -----------------------------------------------------------------------------
// Module bindings declarations
// -----------------------------------------------------------------------------

DECLARE_MODULE_BINDINGS(submodules_bindings);
DECLARE_MODULE_BINDINGS(patterns_bindings);
DECLARE_MODULE_BINDINGS(utilities_bindings);
DECLARE_MODULE_BINDINGS(time_bindings);
DECLARE_MODULE_BINDINGS(core_bindings);
DECLARE_MODULE_BINDINGS(math_bindings);
DECLARE_MODULE_BINDINGS(quotes_bindings);
DECLARE_MODULE_BINDINGS(currencies_bindings);

// -----------------------------------------------------------------------------
// Individual binding declarations
// -----------------------------------------------------------------------------

namespace ql_patterns {
    void observable(py::module_&);
    void observer(py::module_&);
    void lazyobject(py::module_&);
}

namespace ql_utilities {
    void observablevalue(py::module_&);
    void null(py::module_&);
}

namespace ql_time {
    void weekday(py::module_&);
    void date(py::module_&);
    void datevector(py::module_&);
    void timeunit(py::module_&);
    void frequency(py::module_&);
    void period(py::module_&);
    void businessdayconvention(py::module_&);
    void calendar(py::module_&);
    void calendars(py::module_&);
    void calendarvector(py::module_&);
    void daycounter(py::module_&);
    void daycounters(py::module_&);
    void dategenerationrule(py::module_&);
    void schedule(py::module_&);
}

namespace ql_core {
    void constants(py::module_&);
    void quote(py::module_&);
    void quotehandle(py::module_&);
    void relinkablequotehandle(py::module_&);
    void settings(py::module_&);
    void compounding(py::module_&);
    void interestrate(py::module_&);
    void cashflow(py::module_&);
    void index(py::module_&);
    void currency(py::module_&);
    void money(py::module_&);
    void exchangerate(py::module_&);
    void termstructure(py::module_&);
    void exercise(py::module_&);
    void pricingengine(py::module_&);
    void instrument(py::module_&);
    void option(py::module_&);
    void timegrid(py::module_&);
    void payoff(py::module_&);
    void stochasticprocess(py::module_&);
}

namespace ql_math {
    void array(py::module_&);
    void matrix(py::module_&);
    void rounding(py::module_&);
    void constraint(py::module_&);
    void constraints(py::module_&);
    void costfunction(py::module_&);
    void optimizationmethod(py::module_&);
    void endcriteria(py::module_&);
    void problem(py::module_&);
    void levenbergmarquardt(py::module_&);
}

namespace ql_quotes {
    void simplequote(py::module_&);
    void derivedquote(py::module_&);
    void compositequote(py::module_&);
}

namespace ql_currencies {
    void all_currencies(py::module_&);
    void exchangeratemanager(py::module_&);
}
