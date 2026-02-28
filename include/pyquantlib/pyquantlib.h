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

// PyQuantLib requires QuantLib built with std::shared_ptr.
// See CONTRIBUTING.md § "QuantLib Build Requirements" for details.
#if !defined(QL_USE_STD_SHARED_PTR)
static_assert(false,
    "PyQuantLib requires QuantLib built with std::shared_ptr. "
    "Rebuild QuantLib with -DQL_USE_STD_SHARED_PTR=ON. "
    "See CONTRIBUTING.md for details.");
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
    void normaldistribution(py::module_&);
    void bivariatenormaldistribution(py::module_&);
    void solvers1d(py::module_&);
    void statistics(py::module_&);
    void incrementalstatistics(py::module_&);
    void sequencestatistics(py::module_&);
    void mt19937uniformrng(py::module_&);
    void sobolrsg(py::module_&);
    void haltonrsg(py::module_&);
    void burley2020sobolrsg(py::module_&);
    void boxmullergaussianrng(py::module_&);
    void inversecumulativerng(py::module_&);
    void randomsequencegenerator(py::module_&);
    void inversecumulativersg(py::module_&);
    void sobolbrownianbridgersg(py::module_&);
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
    void protectionside(py::module_&);
    void cdspricingmodel(py::module_&);
    void forward(py::module_&);
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
    void rateaveraging(py::module_&);
    void iborcoupon(py::module_&);
    void overnightindexedcoupon(py::module_&);
    void duration(py::module_&);
    void cmscoupon(py::module_&);
    void cmscouponpricer(py::module_&);
    void lineartsrpricer(py::module_&);
    void inflationcoupon(py::module_&);
    void zeroinflationcashflow(py::module_&);
    void yoyinflationcoupon(py::module_&);
    void capflooredinflationcoupon(py::module_&);
    void inflationcouponpricer(py::module_&);
    void dividend(py::module_&);
}

namespace ql_indexes {
    void interestrateindex(py::module_&);
    void iborindex(py::module_&);
    void euribor(py::module_&);
    void sofr(py::module_&);
    void eonia(py::module_&);
    void estr(py::module_&);
    void sonia(py::module_&);
    void swapindex(py::module_&);
    void swapindexes(py::module_&);
    void region(py::module_&);
    void inflationindex(py::module_&);
    void cpi(py::module_&);
    void zeroinflationindex(py::module_&);
    void yoyinflationindex(py::module_&);
    void ukrpi(py::module_&);
    void euhicp(py::module_&);
    void uscpi(py::module_&);
    void aucpi(py::module_&);
    void frhicp(py::module_&);
    void zacpi(py::module_&);
    void equityindex(py::module_&);
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
    void sabrsmilesection(py::module_&);
    void sabrinterpolatedsmilesection(py::module_&);
    void pillar(py::module_&);
    void ratehelper(py::module_&);
    void ratehelpers(py::module_&);
    void oisratehelper(py::module_&);
    void piecewiseyieldcurve(py::module_&);
    void zerocurve(py::module_&);
    void discountcurve(py::module_&);
    void forwardcurve(py::module_&);
    void zerospreadedtermstructure(py::module_&);
    void bondhelpers(py::module_&);
    void fittingmethod(py::module_&);
    void fittedbonddiscountcurve(py::module_&);
    void nonlinearfittingmethods(py::module_&);
    void defaultprobabilitytermstructure(py::module_&);
    void defaultprobabilitytermstructurehandle(py::module_&);
    void flathazardrate(py::module_&);
    void defaultprobabilityhelper(py::module_&);
    void defaultprobabilityhelpers(py::module_&);
    void piecewisedefaultcurve(py::module_&);
    void swaptionvolstructure(py::module_&);
    void swaptionvolstructurehandle(py::module_&);
    void relinkableswaptionvolstructurehandle(py::module_&);
    void constantswaptionvolatility(py::module_&);
    void swaptionvoldiscrete(py::module_&);
    void swaptionvolmatrix(py::module_&);
    void swaptionvolcube(py::module_&);
    void sabrswaptionvolcube(py::module_&);
    void capfloortermvolatilitystructure(py::module_&);
    void capfloortermvolsurface(py::module_&);
    void optionletvolatilitystructure(py::module_&);
    void optionletvolatilitystructurehandle(py::module_&);
    void relinkableoptionletvolatilitystructurehandle(py::module_&);
    void constantoptionletvolatility(py::module_&);
    void strippedoptionletbase(py::module_&);
    void optionletstripper(py::module_&);
    void optionletstripper1(py::module_&);
    void strippedoptionletadapter(py::module_&);
    void inflationtermstructure(py::module_&);
    void zeroinflationtermstructurehandle(py::module_&);
    void yoyinflationtermstructurehandle(py::module_&);
    void seasonality(py::module_&);
    void inflationhelper(py::module_&);
    void inflationhelpers(py::module_&);
    void interpolatedzeroinflationcurve(py::module_&);
    void interpolatedyoyinflationcurve(py::module_&);
    void piecewisezeroinflationcurve(py::module_&);
    void piecewiseyoyinflationcurve(py::module_&);
    void yoyinflationoptionletvolatilitystructure(py::module_&);
}

namespace ql_processes {
    void eulerdiscretization(py::module_&);
    void blackscholesprocess(py::module_&);
    void hestonprocess(py::module_&);
    void stochasticprocessarray(py::module_&);
    void batesprocess(py::module_&);
    void gjrgarchprocess(py::module_&);
    void ornsteinuhlenbeckprocess(py::module_&);
    void forwardmeasureprocess(py::module_&);
    void hullwhiteprocess(py::module_&);
    void hestonslvprocess(py::module_&);
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
    void caphelper(py::module_&);
    void hestonmodelhelper(py::module_&);
    void coxingersollross(py::module_&);
    void extendedcoxingersollross(py::module_&);
    void gaussian1dmodel(py::module_&);
    void gsr(py::module_&);
    void markovfunctional(py::module_&);
    void gjrgarchmodel(py::module_&);
    void browniangenerator(py::module_&);
    void sobolbrowniangenerator(py::module_&);
    void mtbrowniangenerator(py::module_&);
    void hestonslvmcmodel(py::module_&);
    void hestonslvfdmmodel(py::module_&);
}

namespace ql_instruments {
    void bond(py::module_&);
    void fixedratebond(py::module_&);
    void zerocouponbond(py::module_&);
    void floatingratebond(py::module_&);
    void amortizingfixedratebond(py::module_&);
    void amortizingfloatingratebond(py::module_&);
    void cmsratebond(py::module_&);
    void amortizingcmsratebond(py::module_&);
    void cpibond(py::module_&);
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
    void overnightindexedswap(py::module_&);
    void makeois(py::module_&);
    void capfloor(py::module_&);
    void makecapfloor(py::module_&);
    void makevanillaswap(py::module_&);
    void makeswaption(py::module_&);
    void zerocouponswap(py::module_&);
    void compositeinstrument(py::module_&);
    void forwardrateagreement(py::module_&);
    void barriertype(py::module_&);
    void barrieroption(py::module_&);
    void doublebarriertype(py::module_&);
    void doublebarrieroption(py::module_&);
    void averagetype(py::module_&);
    void asianoption(py::module_&);
    void assetswap(py::module_&);
    void claim(py::module_&);
    void creditdefaultswap(py::module_&);
    void zerocouponinflationswap(py::module_&);
    void yearonyearinflationswap(py::module_&);
    void inflationcapfloor(py::module_&);
    void makeyoyinflationcapfloor(py::module_&);

    void bondforward(py::module_&);
    void varianceswap(py::module_&);
    void nonstandardswap(py::module_&);
    void nonstandardswaption(py::module_&);
    void floatfloatswap(py::module_&);
    void floatfloatswaption(py::module_&);
    void equitytotalreturnswap(py::module_&);
    void callability(py::module_&);
    void convertiblebonds(py::module_&);
    void lookbackoption(py::module_&);
    void cliquetoption(py::module_&);
    void compoundoption(py::module_&);
    void simplechooseroption(py::module_&);
    void complexchooseroption(py::module_&);
    void quantovanillaoption(py::module_&);
    void margrabeoption(py::module_&);
    void forwardvanillaoption(py::module_&);
    void quantoforwardvanillaoption(py::module_&);
    void holderextensibleoption(py::module_&);
    void writerextensibleoption(py::module_&);
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
    void discountingbondengine(py::module_&);
    void discountingswapengine(py::module_&);
    void treeswaptionengine(py::module_&);
    void jamshidianswaptionengine(py::module_&);
    void g2swaptionengine(py::module_&);
    void fdhullwhiteswaptionengine(py::module_&);
    void fdg2swaptionengine(py::module_&);
    void blackcapfloorengine(py::module_&);
    void bacheliercapfloorengine(py::module_&);
    void blackswaptionengine(py::module_&);
    void bondfunctions(py::module_&);
    void analyticbarrierengine(py::module_&);
    void analyticdoublebarrierengine(py::module_&);
    void fdblackscholesbarrierengine(py::module_&);
    void analyticcontinuousgeometricasianengine(py::module_&);
    void analyticdiscretegeometricasianengine(py::module_&);
    void mcdiscretearithmeticapengine(py::module_&);
    void turnbullwakemanasianengine(py::module_&);
    void midpointcdsengine(py::module_&);
    void isdacdsengine(py::module_&);
    void inflationcapfloorengines(py::module_&);

    void replicatingvarianceswapengine(py::module_&);
    void binomialconvertibleengine(py::module_&);
    void analyticcontinuousfloatinglookbackengine(py::module_&);
    void analyticcontinuousfixedlookbackengine(py::module_&);
    void analyticcontinuouspartialfloatinglookbackengine(py::module_&);
    void analyticcontinuouspartialfixedlookbackengine(py::module_&);
    void analyticcliquetengine(py::module_&);
    void analyticcompoundoptionengine(py::module_&);
    void analyticsimplechooserengine(py::module_&);
    void analyticcomplexchooserengine(py::module_&);
    void analyticeuropeanmargrabeengine(py::module_&);
    void analyticamericanmargrabeengine(py::module_&);
    void forwardengine(py::module_&);
    void quantoengine(py::module_&);
    void blackcalculator(py::module_&);
    void bacheliercalculator(py::module_&);
    void fdhestonvanillaengine(py::module_&);
    void fdbatesvanillaengine(py::module_&);
    void fdsabrvanillaengine(py::module_&);
    void fdcevvanillaengine(py::module_&);
    void fdblackscholesshoutengine(py::module_&);
    void fdhestonhullwhitevanillaengine(py::module_&);
    void fdornsteinuhlenbeckvanillaengine(py::module_&);
    void coshestonengine(py::module_&);
    void exponentialfittinghestonengine(py::module_&);
    void analyticptdhestonengine(py::module_&);
    void analyticpdfhestonengine(py::module_&);
    void analytichestonhullwhiteengine(py::module_&);
    void analytich1hwengine(py::module_&);
    void hestonexpansionengine(py::module_&);
    void juquadraticengine(py::module_&);
    void qdplusamericanengine(py::module_&);
    void analyticdigitalamericanengine(py::module_&);
    void mcdigitalengine(py::module_&);
    void analyticdividendeuropeanengine(py::module_&);
    void analyticbsmhullwhiteengine(py::module_&);
    void analyticcapfloorengine(py::module_&);
    void treecapfloorengine(py::module_&);
    void gaussian1dcapfloorengine(py::module_&);
    void gaussian1dswaptionengine(py::module_&);
    void gaussian1djamshidianswaptionengine(py::module_&);
    void gaussian1dnonstandardswaptionengine(py::module_&);
    void gaussian1dfloatfloatswaptionengine(py::module_&);
    void analyticholderextensibleoptionengine(py::module_&);
    void analyticwriterextensibleoptionengine(py::module_&);
    void analytictwoassetcorrelationengine(py::module_&);
    void analyticgjrgarchengine(py::module_&);
    void mcforwardeuropeanbsengine(py::module_&);
    void mcforwardeuropeanhestonengine(py::module_&);
    void mceuropeanhestonengine(py::module_&);
}

namespace ql_methods {
    void fdmbackwardsolver(py::module_&);
    void fdmhestongreensfct(py::module_&);
    void fdmsquarerootfwdop(py::module_&);
    void lsmbasissystem(py::module_&);
    void sample(py::module_&);
    void path(py::module_&);
    void multipath(py::module_&);
    void brownianbridge(py::module_&);
    void pathgenerator(py::module_&);
    void multipathgenerator(py::module_&);
}

namespace ql_experimental {
    void svismilesection(py::module_&);
    void cdsoption(py::module_&);
    void blackcdsoptionengine(py::module_&);
    void callablebond(py::module_&);
    void callablebondvolstructure(py::module_&);
    void callablebondconstantvol(py::module_&);
    void treecallablebondengine(py::module_&);
    void blackcallablebondengine(py::module_&);
    void twoassetcorrelationoption(py::module_&);
    void variancegammaprocess(py::module_&);
    void variancegammamodel(py::module_&);
    void analyticvariancegammaengine(py::module_&);
    void fftvariancegammaengine(py::module_&);
}
