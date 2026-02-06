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
DECLARE_MODULE_BINDINGS(math_bindings);
DECLARE_MODULE_BINDINGS(core_bindings);
DECLARE_MODULE_BINDINGS(quotes_bindings);
DECLARE_MODULE_BINDINGS(currencies_bindings);
DECLARE_MODULE_BINDINGS(cashflows_bindings);
DECLARE_MODULE_BINDINGS(indexes_bindings);
DECLARE_MODULE_BINDINGS(termstructures_bindings);
DECLARE_MODULE_BINDINGS(processes_bindings);
DECLARE_MODULE_BINDINGS(models_bindings);
DECLARE_MODULE_BINDINGS(instruments_bindings);
DECLARE_MODULE_BINDINGS(pricingengines_bindings);
DECLARE_MODULE_BINDINGS(methods_bindings);
DECLARE_MODULE_BINDINGS(experimental_bindings);

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
    void extrapolation(py::module_&);
    void interpolation(py::module_&);
    void linearinterpolation(py::module_&);
    void loglinearinterpolation(py::module_&);
    void backwardflatinterpolation(py::module_&);
    void cubicinterpolation(py::module_&);
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

namespace ql_quotes {
    void simplequote(py::module_&);
    void derivedquote(py::module_&);
    void compositequote(py::module_&);
}

namespace ql_currencies {
    void all_currencies(py::module_&);
    void exchangeratemanager(py::module_&);
}

namespace ql_cashflows {
    void coupon(py::module_&);
    void simplecashflow(py::module_&);
    void fixedratecoupon(py::module_&);
    void couponpricer_base(py::module_&);
    void couponpricer(py::module_&);
    void floatingratecoupon(py::module_&);
    void iborcoupon(py::module_&);
    void overnightindexedcoupon(py::module_&);
}

namespace ql_indexes {
    void interestrateindex(py::module_&);
    void iborindex(py::module_&);
    void euribor(py::module_&);
}

namespace ql_termstructures {
    void yieldtermstructure(py::module_&);
    void yieldtermstructurehandle(py::module_&);
    void relinkableyieldtermstructurehandle(py::module_&);
    void flatforward(py::module_&);
    void volatilitytype(py::module_&);
    void voltermstructure(py::module_&);
    void blackvoltermstructure(py::module_&);
    void blackvoltermstructurehandle(py::module_&);
    void relinkableblackvoltermstructurehandle(py::module_&);
    void blackconstantvol(py::module_&);
    void blackvariancesurface(py::module_&);
    void localvoltermstructure(py::module_&);
    void localvoltermstructurehandle(py::module_&);
    void relinkablelocalvoltermstructurehandle(py::module_&);
    void localconstantvol(py::module_&);
    void localvolsurface(py::module_&);
    void fixedlocalvolsurface(py::module_&);
    void noexceptlocalvolsurface(py::module_&);
    void smilesection(py::module_&);
}

namespace ql_processes {
    void eulerdiscretization(py::module_&);
    void blackscholesprocess(py::module_&);
    void hestonprocess(py::module_&);
    void stochasticprocessarray(py::module_&);
    void batesprocess(py::module_&);
}

namespace ql_models {
    void model(py::module_&);
    void parameter(py::module_&);
    void calibrationhelper(py::module_&);
    void hestonmodel(py::module_&);
    void hestonmodelhandle(py::module_&);
    void piecewisetimedependenthestonmodel(py::module_&);
    void onefactormodel(py::module_&);
    void twofactormodel(py::module_&);
    void vasicek(py::module_&);
    void hullwhite(py::module_&);
    void blackkarasinski(py::module_&);
    void g2(py::module_&);
    void batesmodel(py::module_&);
    void swaptionhelper(py::module_&);
}

namespace ql_instruments {
    void swap(py::module_&);
    void fixedvsfloatingswap(py::module_&);
    void vanillaswap(py::module_&);
    void swaption(py::module_&);
    void strikedtypepayoff(py::module_&);
    void payoffs(py::module_&);
    void oneassetoption(py::module_&);
    void vanillaoption(py::module_&);
    void multiassetoption(py::module_&);
    void basketoption(py::module_&);
}

namespace ql_pricingengines {
    void blackformula(py::module_&);
    void genericmodelengine(py::module_&);
    void analyticeuropeanengine(py::module_&);
    void analytichestonengine(py::module_&);
    void mceuropeanengine(py::module_&);
    void spreadblackscholesvanillaengine(py::module_&);
    void kirkengine(py::module_&);
    void bjerksundstenslandspreadengine(py::module_&);
    void operatorsplittingspreadengine(py::module_&);
    void denglizhoubasketengine(py::module_&);
    void stulzengine(py::module_&);
    void fd2dblackscholesvanillaengine(py::module_&);
    void mceuropeanbasketengine(py::module_&);
    void baroneadesiwhaleyengine(py::module_&);
    void bjerksundstenslandengine(py::module_&);
    void fdblackscholesvanillaengine(py::module_&);
    void binomialengine(py::module_&);
    void mcamericanengine(py::module_&);
    void integralengine(py::module_&);
    void qdfpamericanengine(py::module_&);
    void analyticeuropeanvasicekengine(py::module_&);
    void batesengine(py::module_&);
    void discountingswapengine(py::module_&);
    void treeswaptionengine(py::module_&);
    void jamshidianswaptionengine(py::module_&);
    void g2swaptionengine(py::module_&);
    void fdhullwhiteswaptionengine(py::module_&);
    void fdg2swaptionengine(py::module_&);
}

namespace ql_methods {
    void fdmbackwardsolver(py::module_&);
}

namespace ql_experimental {
    void svismilesection(py::module_&);
}
