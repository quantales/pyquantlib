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

// Support for boost::shared_ptr when QuantLib uses it (e.g., macOS Homebrew)
// QuantLib defines QL_USE_STD_SHARED_PTR when using std::shared_ptr
// When not defined, QuantLib uses boost::shared_ptr
#if !defined(QL_USE_STD_SHARED_PTR)
PYBIND11_DECLARE_HOLDER_TYPE(T, boost::shared_ptr<T>, true);
#endif

namespace py = pybind11;

// Submodules
DECLARE_MODULE_BINDINGS(submodules_bindings);

// Aggregated modules
DECLARE_MODULE_BINDINGS(patterns_bindings);
DECLARE_MODULE_BINDINGS(utilities_bindings);
DECLARE_MODULE_BINDINGS(time_bindings);
DECLARE_MODULE_BINDINGS(core_bindings);
DECLARE_MODULE_BINDINGS(math_bindings);
DECLARE_MODULE_BINDINGS(quotes_bindings);
DECLARE_MODULE_BINDINGS(cashflows_bindings);
DECLARE_MODULE_BINDINGS(currencies_bindings);
DECLARE_MODULE_BINDINGS(indexes_bindings);
DECLARE_MODULE_BINDINGS(termstructures_bindings);
DECLARE_MODULE_BINDINGS(instruments_bindings);
DECLARE_MODULE_BINDINGS(processes_bindings);
DECLARE_MODULE_BINDINGS(models_bindings);
DECLARE_MODULE_BINDINGS(pricingengines_bindings);


// Individual declarations 

namespace ql_patterns {
    void observable(py::module_&);
    void observer(py::module_&);
    void lazyobject(py::module_&);
}

namespace ql_utilities {
    void observablevalue(py::module_& m);
    void null(py::module_& m);
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
    void stochasticprocess(py::module_&);
    void timegrid(py::module_&);
    void payoff(py::module_&);
}

namespace ql_math {
    void array(py::module_& m);
    void matrix(py::module_& m);
    void rounding(py::module_& m);
    void constraint(py::module_& m);      // ABC only
    void constraints(py::module_& m);     // Concrete implementations
    void endcriteria(py::module_& m);
    void optimizationmethod(py::module_& m);
    void problem(py::module_& m);
    void costfunction(py::module_& m);
    void levenbergmarquardt(py::module_& m);
}

namespace ql_quotes {
    void simplequote(py::module_& m);
    void simplequotehandle(py::module_& m);
    void derivedquote(py::module_& m);
    void compositequote(py::module_& m);
}

namespace ql_cashflows {
    void coupon(py::module_& m);
    void simplecashflow(py::module_& m);
    void fixedratecoupon(py::module_& m);
}

namespace ql_currencies {
    void all_currencies(py::module_& m);
    void exchangeratemanager(py::module_& m);
}

namespace ql_indexes {
    void interestrateindex(py::module_& m);
}

namespace ql_termstructures {
    // Abstract base classes
    void yieldtermstructure(py::module_& m);
    void voltermstructure(py::module_& m);
    void blackvoltermstructure(py::module_& m);
    void localvoltermstructure(py::module_& m);
    
    // Handle types
    void yieldtermstructurehandle(py::module_& m);
    void blackvoltermstructurehandle(py::module_& m);
    void localvoltermstructurehandle(py::module_& m);

    // Relinkable handles
    void relinkableyieldtermstructurehandle(py::module_& m);
    void relinkableblackvoltermstructurehandle(py::module_& m);
    
    // Concrete implementations
    void flatforward(py::module_& m);
    void blackconstantvol(py::module_& m);
    void localconstantvol(py::module_& m);
    void localvolsurface(py::module_& m);
    void fixedlocalvolsurface(py::module_& m);
    void noexceptlocalvolsurface(py::module_& m);
    void blackvariancesurface(py::module_& m);
}

namespace ql_instruments {
    void strikedtypepayoff(py::module_& m);
    void payoffs(py::module_& m);
    void oneassetoption(py::module_& m);
    void vanillaoption(py::module_& m);
}

namespace ql_processes {
    void eulerdiscretization(py::module_& m);
    void blackscholesprocess(py::module_& m);
    void hestonprocess(py::module_& m);
}

namespace ql_models {
    // Abstract base classes
    void calibrationhelper(py::module_& m);
    void model(py::module_& m);
    
    // Concrete implementations
    void parameter(py::module_& m);
    void hestonmodel(py::module_& m);
    void hestonmodelhandle(py::module_& m);
    void piecewisetimedependenthestonmodel(py::module_& m);
}

namespace ql_pricingengines {
    void genericmodelengine(py::module_& m);
    void analyticeuropeanengine(py::module_& m);
    void analytichestonengine(py::module_& m);
    void mceuropeanengine(py::module_& m);
}
