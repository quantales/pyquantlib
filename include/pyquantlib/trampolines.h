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

#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;


// --- Observer Trampoline ---
class PyObserver : public QuantLib::Observer {
public:
    // Provide the dummy constructor for py::init_alias()
    PyObserver() : Observer() {}
public:
    // Inherit constructors from QuantLib::Observer
    using QuantLib::Observer::Observer;

    // Trampoline for the pure virtual function update()
    void update() override {
        PYBIND11_OVERRIDE_PURE(
            void,               // Return type
            QuantLib::Observer, // Parent class
            update              // Name of the function in C++ (and Python)
                                // No arguments for this version of update
        );
    }
};

// A simple trampoline for Observable. Its only purpose is to provide
// a default-constructible type for py::init_alias() to use when
// setting up Python inheritance.
class PyObservable : public Observable {
public:
    // Inherit any non-default constructors from the base class
    using Observable::Observable;

    // Provide the explicit default constructor that py::init_alias() requires.
    PyObservable() : Observable() {}
};

// --- LazyObject Trampoline ---
// Needed to support Python inheritance and py::init_alias()
class PyLazyObject : public LazyObject {
public:
    PyLazyObject() : LazyObject() {}
public:
    using LazyObject::LazyObject; // Inherit constructors
    
    void performCalculations() const override {
        PYBIND11_OVERRIDE_PURE(void, LazyObject, performCalculations, );
    }
}; 

// --- Quote Trampoline ---
class PyQuote : public Quote {
public:
    using Quote::Quote; // Inherit constructors

    Real value() const override {
        PYBIND11_OVERRIDE_PURE(
            Real,      // Return type
            Quote,     // Parent class
            value      // Name of the function in C++
                       // No arguments
        );
    }

    bool isValid() const override {
        PYBIND11_OVERRIDE_PURE(
            bool,      // Return type
            Quote,     // Parent class
            isValid    // Name of the function in C++
                       // No arguments
        );
    }
    // update() from Observable is not pure, so no need to trampoline here
    // unless specifically overriding its behavior in a Python-derived Quote.
};

// --- Event Trampoline ---
class PyEvent : public Event {
public:
    PyEvent() : Event() {}
public:
    using Event::Event; 

    Date date() const override {
        PYBIND11_OVERRIDE_PURE(
            Date,       // Return type
            Event,      // Parent class
            date        // Method name
        );
    }
};

// --- CashFlow Trampoline ---
class PyCashFlow : public CashFlow {
public:
    PyCashFlow() : CashFlow() {} // Dummy constructor for subclassing 
public:
    using CashFlow::CashFlow;
    
    // Override pure virtual methods
    Real amount() const override {
        PYBIND11_OVERRIDE_PURE(
            Real,       // Return type
            CashFlow,   // Parent class
            amount      // Method name
        );
    }

    Date date() const override {
        PYBIND11_OVERRIDE_PURE(
            Date,       // Return type
            CashFlow,   // Parent class
            date        // Method name
        );
    }
};

// --- Coupon Trampoline ---
class PyCoupon : public Coupon {
public:
    PyCoupon() : Coupon(Date(), 0.0, Date(), Date()) {}

public:
    using Coupon::Coupon;

    Date date() const override {
        PYBIND11_OVERRIDE_PURE(Date, Coupon, date, );
    }
    Real amount() const override {
        PYBIND11_OVERRIDE_PURE(Real, Coupon, amount, );
    }
    // Override pure virtual methods from Coupon class
    Rate nominal() const override {
        PYBIND11_OVERRIDE_PURE(Rate, Coupon, nominal, );
    }
    DayCounter dayCounter() const override {
        PYBIND11_OVERRIDE_PURE(DayCounter, Coupon, dayCounter, );
    }
    Date accrualStartDate() const {
        PYBIND11_OVERRIDE_PURE(Date, Coupon, accrualStartDate, );
    }
    Date accrualEndDate() const {
        PYBIND11_OVERRIDE_PURE(Date, Coupon, accrualEndDate, );
    }
    Date referencePeriodStart() const {
        PYBIND11_OVERRIDE_PURE(Date, Coupon, referencePeriodStart, );
    }
    Date referencePeriodEnd() const {
        PYBIND11_OVERRIDE_PURE(Date, Coupon, referencePeriodEnd, );
    }
    Time accrualPeriod() const {
        PYBIND11_OVERRIDE(Time, Coupon, accrualPeriod, ); // Not pure, but overridable
    }
    BigInteger accrualDays() const {
        PYBIND11_OVERRIDE(BigInteger, Coupon, accrualDays, ); // Not pure, but overridable
    }
    Rate rate() const override {
        PYBIND11_OVERRIDE_PURE(Rate, Coupon, rate, );
    }
    Real accruedAmount(const Date&) const override {
        PYBIND11_OVERRIDE_PURE(Real, Coupon, accruedAmount, );
    }
};

// --- Index Trampoline ---
class PyIndex : public Index {
public:
    using Index::Index;

    PyIndex() : Index() {}

    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, Index, name, );
    }

    Calendar fixingCalendar() const override {
        PYBIND11_OVERRIDE_PURE(Calendar, Index, fixingCalendar, );
    }

    bool isValidFixingDate(const Date& fixingDate) const override {
        PYBIND11_OVERRIDE_PURE(bool, Index, isValidFixingDate, fixingDate);
    }

    Real fixing(const Date& fixingDate, bool forecastTodaysFixing = false) const override {
        PYBIND11_OVERRIDE_PURE(Real, Index, fixing, fixingDate, forecastTodaysFixing);
    }

    // From Observer class 
    void update() override {
        PYBIND11_OVERRIDE_PURE(void, Index, update, );
    }
};

// --- PyInterestRateIndex Trampoline ---
class PyInterestRateIndex : public InterestRateIndex
{
public:
    using InterestRateIndex::InterestRateIndex;

    std::string name() const override
    {
        PYBIND11_OVERRIDE(
            std::string, // return type
            QuantLib::InterestRateIndex, // parent class
            name // function name (c++)
        );
    }
    Calendar fixingCalendar() const override
    {
        PYBIND11_OVERRIDE_NAME(
            Calendar, // return type
            QuantLib::InterestRateIndex, // parent class
            "fixingCalendar", // function name (python)
            fixingCalendar // function name (c++)
        );
    }
    bool isValidFixingDate(const Date & fixingDate) const override
    {
        PYBIND11_OVERRIDE_NAME(
            bool, // return type
            QuantLib::InterestRateIndex, // parent class
            "isValidFixingDate", // function name (python)
            isValidFixingDate, // function name (c++)
            fixingDate // params
        );
    }
    Rate fixing(const Date & fixingDate, bool forecastTodaysFixing = false) const override
    {
        PYBIND11_OVERRIDE(
            Rate, // return type
            QuantLib::InterestRateIndex, // parent class
            fixing, // function name (c++)
            fixingDate, forecastTodaysFixing // params
        );
    }
    Date fixingDate(const Date & valueDate) const override
    {
        PYBIND11_OVERRIDE_NAME(
            Date, // return type
            QuantLib::InterestRateIndex, // parent class
            "fixingDate", // function name (python)
            fixingDate, // function name (c++)
            valueDate // params
        );
    }
    Date valueDate(const Date & fixingDate) const override
    {
        PYBIND11_OVERRIDE_NAME(
            Date, // return type
            QuantLib::InterestRateIndex, // parent class
            "valueDate", // function name (python)
            valueDate, // function name (c++)
            fixingDate // params
        );
    }
    Date maturityDate(const Date & valueDate) const override
    {
        PYBIND11_OVERRIDE_PURE_NAME(
            Date, // return type
            QuantLib::InterestRateIndex, // parent class
            "maturityDate", // function name (python)
            maturityDate, // function name (c++)
            valueDate // params
        );
    }
    Rate forecastFixing(const Date & fixingDate) const override
    {
        PYBIND11_OVERRIDE_PURE_NAME(
            Rate, // return type
            QuantLib::InterestRateIndex, // parent class
            "forecastFixing", // function name (python)
            forecastFixing, // function name (c++)
            fixingDate // params
        );
    }
};

// --- TermStructure Trampoline ---
class PyTermStructure : public TermStructure {
public:
    // Inherit constructors from the base class.
    using TermStructure::TermStructure;

    // From TermStructure
    Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(Date, TermStructure, maxDate, );
    }
    
    // From Observer
    void update() override {
        PYBIND11_OVERRIDE(void, TermStructure, update, );
    }
};

// --- YieldTermStructure Trampoline ---
class PyYieldTermStructure : public YieldTermStructure
{
public:
    using YieldTermStructure::YieldTermStructure;

    // From TermStructure
    Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(Date, YieldTermStructure, maxDate, );
    }
    
    // From Observer
    void update() override
    {
        PYBIND11_OVERRIDE(
            void, // return type
            QuantLib::YieldTermStructure, // parent class
            update // function name (c++)
        );
    }

    // From YieldTermStructure
    DiscountFactor discountImpl(Time param_0) const override
    {
        PYBIND11_OVERRIDE_PURE_NAME(
            DiscountFactor, // return type
            QuantLib::YieldTermStructure, // parent class
            "discountImpl", // function name (python)
            discountImpl, // function name (c++)
            param_0 // params
        );
    }
};

// Trampoline for VolatilityTermStructure (Corrected Name)
class PyVolatilityTermStructure : public VolatilityTermStructure {
public:
    using VolatilityTermStructure::VolatilityTermStructure;
    // Overrides from the full hierarchy
    Date maxDate() const override { PYBIND11_OVERRIDE_PURE(Date, VolatilityTermStructure, maxDate, ); }
    BusinessDayConvention businessDayConvention() const override { PYBIND11_OVERRIDE_PURE(BusinessDayConvention, VolatilityTermStructure, businessDayConvention, ); }
    Real minStrike() const override { PYBIND11_OVERRIDE_PURE(Real, VolatilityTermStructure, minStrike, ); }
    Real maxStrike() const override { PYBIND11_OVERRIDE_PURE(Real, VolatilityTermStructure, maxStrike, ); }
    void update() override { PYBIND11_OVERRIDE(void, VolatilityTermStructure, update, ); }
};

// Trampoline for BlackVolTermStructure
class PyBlackVolTermStructure : public BlackVolTermStructure {
public:
    using BlackVolTermStructure::BlackVolTermStructure;
    // Overrides from the full hierarchy
    Date maxDate() const override { PYBIND11_OVERRIDE_PURE(Date, BlackVolTermStructure, maxDate, ); }
    BusinessDayConvention businessDayConvention() const override { PYBIND11_OVERRIDE_PURE(BusinessDayConvention, BlackVolTermStructure, businessDayConvention, ); }
    Real minStrike() const override { PYBIND11_OVERRIDE_PURE(Real, BlackVolTermStructure, minStrike, ); }
    Real maxStrike() const override { PYBIND11_OVERRIDE_PURE(Real, BlackVolTermStructure, maxStrike, ); }
    Volatility blackVolImpl(Time t, Real strike) const override { PYBIND11_OVERRIDE_PURE(Volatility, BlackVolTermStructure, blackVolImpl, t, strike); }
    void update() override { PYBIND11_OVERRIDE(void, BlackVolTermStructure, update, ); }
};

// Trampoline for BlackVolatilityTermStructure (the adapter class)
class PyBlackVolatilityTermStructure : public BlackVolatilityTermStructure {
public:
    using BlackVolatilityTermStructure::BlackVolatilityTermStructure;
    // This class is also abstract because it doesn't implement blackVolImpl.
    // We only need to provide the override for the pure virtual method from its parent.
    Volatility blackVolImpl(Time t, Real strike) const override { PYBIND11_OVERRIDE_PURE(Volatility, BlackVolatilityTermStructure, blackVolImpl, t, strike); }
};

// Trampoline for BlackVarianceTermStructure (the adapter class)
class PyBlackVarianceTermStructure : public BlackVarianceTermStructure {
public:
    using BlackVarianceTermStructure::BlackVarianceTermStructure;
    // This class is also abstract because it doesn't implement blackVolImpl.
    // We only need to provide the override for the pure virtual method from its parent.
    Volatility blackVolImpl(Time t, Real strike) const override { PYBIND11_OVERRIDE_PURE(Volatility, BlackVarianceTermStructure, blackVolImpl, t, strike); }
};

// Trampoline class for BlackVarianceSurface
class PyBlackVarianceSurface : public QuantLib::BlackVarianceSurface {
public:
    using QuantLib::BlackVarianceSurface::BlackVarianceSurface;

protected:
    QuantLib::Real blackVarianceImpl(QuantLib::Time t, QuantLib::Real strike) const override {
        PYBIND11_OVERRIDE(QuantLib::Real, QuantLib::BlackVarianceSurface, blackVarianceImpl, t, strike);
    }
};

// --- Trampoline for LocalVolTermStructure ---
class PyLocalVolTermStructure : public LocalVolTermStructure {
public:
    // Inherit constructors to allow Python subclasses to call them via super().__init__
    using LocalVolTermStructure::LocalVolTermStructure;

    // From LocalVolTermStructure itself
    Volatility localVolImpl(Time t, Real strike) const override {
        PYBIND11_OVERRIDE_PURE(Volatility, LocalVolTermStructure, localVolImpl, t, strike);
    }

    // From VolatilityTermStructure
    Date maxDate() const override {
        PYBIND11_OVERRIDE_PURE(Date, LocalVolTermStructure, maxDate, );
    }
    Real minStrike() const override {
        PYBIND11_OVERRIDE_PURE(Real, LocalVolTermStructure, minStrike, );
    }
    Real maxStrike() const override {
        PYBIND11_OVERRIDE_PURE(Real, LocalVolTermStructure, maxStrike, );
    }
    BusinessDayConvention businessDayConvention() const override {
        PYBIND11_OVERRIDE_PURE(BusinessDayConvention, LocalVolTermStructure, businessDayConvention, );
    }

    // From Observer (via TermStructure)
    void update() override {
        PYBIND11_OVERRIDE(void, LocalVolTermStructure, update, );
    }
};

// --- Trampoline for FixedLocalVolSurface ---
class PyFixedLocalVolSurface : public FixedLocalVolSurface {
public:
    using FixedLocalVolSurface::FixedLocalVolSurface;

    // Override virtual functions
    Date maxDate() const override {
        PYBIND11_OVERRIDE(Date, FixedLocalVolSurface, maxDate, );
    }
    
    Time maxTime() const override {
        PYBIND11_OVERRIDE(Time, FixedLocalVolSurface, maxTime, );
    }
    
    Real minStrike() const override {
        PYBIND11_OVERRIDE(Real, FixedLocalVolSurface, minStrike, );
    }
    
    Real maxStrike() const override {
        PYBIND11_OVERRIDE(Real, FixedLocalVolSurface, maxStrike, );
    }
    
    Volatility localVolImpl(Time t, Real strike) const override {
        PYBIND11_OVERRIDE(Volatility, FixedLocalVolSurface, localVolImpl, t, strike);
    }
};

// --- Exercise Trampoline ---
class PyExercise : public Exercise {
public:
    using Exercise::Exercise;
};

// --- Payoff Trampoline ---
class PyPayoff : public Payoff {
public:
    using Payoff::Payoff;
    PyPayoff() : Payoff() {}

    std::string name() const override {
        PYBIND11_OVERRIDE_PURE(std::string, Payoff, name, );
    }
    std::string description() const override {
        PYBIND11_OVERRIDE_PURE(std::string, Payoff, description, );
    }
    Real operator()(Real price) const override {
        PYBIND11_OVERRIDE_PURE(Real, Payoff, operator(), price);
    }
};

// --- StrikedTypePayoff Trampoline ---
class PyStrikedTypePayoff : public StrikedTypePayoff {
public:
    using StrikedTypePayoff::StrikedTypePayoff;

    // This public constructor can access the protected base constructor.
    // It provides the necessary hook for pybind11.
    PyStrikedTypePayoff(Option::Type type, Real strike)
      : StrikedTypePayoff(type, strike) {}

    std::string name() const override { PYBIND11_OVERRIDE_PURE(std::string, StrikedTypePayoff, name, ); }
    std::string description() const override { PYBIND11_OVERRIDE_PURE(std::string, StrikedTypePayoff, description, ); }
    Real operator()(Real price) const override { PYBIND11_OVERRIDE_PURE(Real, StrikedTypePayoff, operator(), price); }
};

// --- Trampolines for PricingEngine and its nested classes ---

// Trampoline for the nested abstract arguments class
class PyPricingEngineArguments : public PricingEngine::arguments {
public:
    using PricingEngine::arguments::arguments;

    void validate() const override {
        PYBIND11_OVERRIDE_PURE(void, PricingEngine::arguments, validate, );
    }
};

// Trampoline for the nested abstract results class
class PyPricingEngineResults : public PricingEngine::results {
public:
    using PricingEngine::results::results;

    void reset() override {
        PYBIND11_OVERRIDE_PURE(void, PricingEngine::results, reset, );
    }
};


// PricingEngine 
class PyPricingEngine : public PricingEngine {
public:
    using PricingEngine::PricingEngine;
    // Dummy constructor
    PyPricingEngine() : PricingEngine() {}

    PricingEngine::arguments* getArguments() const override {
        PYBIND11_OVERRIDE_PURE(PricingEngine::arguments*, PricingEngine, getArguments, );
    }
    const PricingEngine::results* getResults() const override {
        PYBIND11_OVERRIDE_PURE(const PricingEngine::results*, PricingEngine, getResults, );
    }
    void reset() override {
        PYBIND11_OVERRIDE_PURE(void, PricingEngine, reset, );
    }
    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, PricingEngine, calculate, );
    }
};

// Instrument
class PyInstrument : public Instrument {
public:
    using Instrument::Instrument;
    PyInstrument() : Instrument() {}

    bool isExpired() const override {
        PYBIND11_OVERRIDE_PURE(bool, Instrument, isExpired, );
    }
    void performCalculations() const override {
        PYBIND11_OVERRIDE(void, Instrument, performCalculations, );
    }
    void update() override {
        PYBIND11_OVERRIDE(void, Instrument, update, );
    }
};

// Trampoline for Option
class PyOption : public Option {
public:
    using Option::Option;

    bool isExpired() const override { PYBIND11_OVERRIDE_PURE(bool, Option, isExpired, ); }
    void performCalculations() const override { PYBIND11_OVERRIDE(void, Option, performCalculations, ); }
    void update() override { PYBIND11_OVERRIDE(void, Option, update, ); }
};

// Trampoline for OneAssetOption
class PyOneAssetOption : public OneAssetOption {
public:
    using OneAssetOption::OneAssetOption;
    
    bool isExpired() const override { PYBIND11_OVERRIDE_PURE(bool, OneAssetOption, isExpired, ); }
    void performCalculations() const override { PYBIND11_OVERRIDE(void, OneAssetOption, performCalculations, ); }
    void update() override { PYBIND11_OVERRIDE(void, OneAssetOption, update, ); }
};

using OneAssetGenericEngine = GenericEngine<OneAssetOption::arguments, OneAssetOption::results>;

class PyOneAssetGenericEngine : public OneAssetGenericEngine {
public:
    using OneAssetGenericEngine::OneAssetGenericEngine;
    // Provide the hook for the pure virtual calculate() method.
    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, OneAssetGenericEngine, calculate, );
    }
};

class PyOneAssetOptionEngine : public OneAssetOption::engine {
public:
    using OneAssetOption::engine::engine;
    // Also needs the override for the pure virtual calculate().
    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, OneAssetOption::engine, calculate, );
    }
};

// Trampoline for GenericHestonModelEngine
using GenericHestonModelEngine = GenericModelEngine<HestonModel, VanillaOption::arguments, VanillaOption::results>;

class PyGenericHestonModelEngine : public GenericHestonModelEngine {
public:
    using GenericHestonModelEngine::GenericHestonModelEngine;
    
    void calculate() const override {
        PYBIND11_OVERRIDE_PURE(void, GenericHestonModelEngine, calculate, );
    }
};

// Trampoline for StochasticProcess
class PyStochasticProcess : public StochasticProcess {
public:
    using StochasticProcess::StochasticProcess;
    PyStochasticProcess() : StochasticProcess() {}

    // Override pure virtual methods
    Size size() const override { PYBIND11_OVERRIDE_PURE(Size, StochasticProcess, size, ); }
    Size factors() const override { PYBIND11_OVERRIDE_PURE(Size, StochasticProcess, factors, ); }
    Array initialValues() const override { PYBIND11_OVERRIDE_PURE(Array, StochasticProcess, initialValues, ); }
    Array drift(Time t, const Array& x) const override { PYBIND11_OVERRIDE_PURE(Array, StochasticProcess, drift, t, x); }
    Matrix diffusion(Time t, const Array& x) const override { PYBIND11_OVERRIDE_PURE(Matrix, StochasticProcess, diffusion, t, x); }
    Array evolve(Time t0, const Array& x0, Time dt, const Array& dw) const override { PYBIND11_OVERRIDE_PURE(Array, StochasticProcess, evolve, t0, x0, dt, dw); }
    
    // Override for the virtual update() method from Observer
    void update() override { PYBIND11_OVERRIDE(void, StochasticProcess, update, ); }
};

// --- Trampoline for StochasticProcess1D::discretization ---
class PyDiscretization : public StochasticProcess1D::discretization {
public:
    using StochasticProcess1D::discretization::discretization;
    
    // Override the three pure virtual methods
    Real drift(const StochasticProcess1D& process, Time t0, Real x0, Time dt) const override {
        PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D::discretization, drift, process, t0, x0, dt);
    }
    Real diffusion(const StochasticProcess1D& process, Time t0, Real x0, Time dt) const override {
        PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D::discretization, diffusion, process, t0, x0, dt);
    }
    Real variance(const StochasticProcess1D& process, Time t0, Real x0, Time dt) const override {
        PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D::discretization, variance, process, t0, x0, dt);
    }
};

// Trampoline for StochasticProcess1D
class PyStochasticProcess1D : public StochasticProcess1D {
public:
    using StochasticProcess1D::StochasticProcess1D;
    PyStochasticProcess1D() : StochasticProcess1D() {}

    // Overrides from full hierarchy
    Real x0() const override { PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D, x0, ); }
    Real drift(Time t, Real x) const override { PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D, drift, t, x); }
    Real diffusion(Time t, Real x) const override { PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D, diffusion, t, x); }
    Real evolve(Time t0, Real x0, Time dt, Real dw) const override { PYBIND11_OVERRIDE_PURE(Real, StochasticProcess1D, evolve, t0, x0, dt, dw); }

    // Override for the virtual update() method inherited from StochasticProcess
    void update() override { PYBIND11_OVERRIDE(void, StochasticProcess1D, update, ); }
};

// CostFunction
class PyCostFunction : public CostFunction {
public:
    using CostFunction::CostFunction;
    Real value(const Array& x) const override { PYBIND11_OVERRIDE_PURE(Real, CostFunction, value, x); }
    Array values(const Array& x) const override { PYBIND11_OVERRIDE_PURE(Array, CostFunction, values, x); }
};

class PyOptimizationMethod : public OptimizationMethod {
public:
    using OptimizationMethod::OptimizationMethod;
    EndCriteria::Type minimize(Problem& P, const EndCriteria& criteria) override {
        PYBIND11_OVERRIDE_PURE(EndCriteria::Type, OptimizationMethod, minimize, P, criteria);
    }
};

// --- CalibrationHelper class ---
class PyCalibrationHelper : public CalibrationHelper {
public:
    using CalibrationHelper::CalibrationHelper; // Inherit constructors

    // Override the pure virtual method
    Real calibrationError() override {
        PYBIND11_OVERRIDE_PURE(Real, CalibrationHelper, calibrationError, );
    }
};

// Trampoline for the abstract CalibratedModel class
class PyCalibratedModel : public CalibratedModel {
public:
    // This public constructor can access the protected base constructor.
    // It provides the necessary hook for pybind11.
    PyCalibratedModel(Size nArguments) : CalibratedModel(nArguments) {}

    void calibrate(const std::vector<ext::shared_ptr<CalibrationHelper> >& instruments,
                   OptimizationMethod& method,
                   const EndCriteria& endCriteria,
                   const Constraint& constraint,
                   const std::vector<Real>& weights,
                   const std::vector<bool>& fixParameters
                ) override {
        PYBIND11_OVERRIDE(void, CalibratedModel, calibrate, instruments, method, endCriteria, constraint, weights, fixParameters);
    }

    // void calibrate(
    //     const std::vector<ext::shared_ptr<CalibrationHelper>>& helpers,
    //     OptimizationMethod& method,
    //     const EndCriteria& endCriteria,
    //     const Constraint& constraint,
    //     const std::vector<Real>& weights,
    //     const std::vector<bool>& fixParameters
    // ) override {
    //     PYBIND11_OVERRIDE(
    //         void,                                      // Return type
    //         CalibratedModel,                           // Base class
    //         calibrate,                                 // Method name
    //         helpers, method, endCriteria, constraint,  // Args
    //         weights, fixParameters                     // Args (continued)
    //     );
    // }

    void setParams(const Array& params) override {
        PYBIND11_OVERRIDE(void, CalibratedModel, setParams, params);
    }

    // Override from Observer
    void update() override {
        PYBIND11_OVERRIDE(void, CalibratedModel, update, );
    }
};