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
#include "pyquantlib/trampolines.h"
#include <ql/instruments/bond.hpp>
#include <ql/pricingengine.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::bond(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // Bond::Price::Type enum
    py::enum_<Bond::Price::Type>(m, "BondPriceType",
        "Bond price type: Clean or Dirty.")
        .value("Clean", Bond::Price::Clean,
            "Clean price (excluding accrued interest).")
        .value("Dirty", Bond::Price::Dirty,
            "Dirty price (including accrued interest).");

    // Bond::Price
    py::class_<Bond::Price>(m, "BondPrice",
        "Bond price with type (clean or dirty).")
        .def(py::init<Real, Bond::Price::Type>(),
            py::arg("amount"), py::arg("type"),
            "Constructs a bond price.")
        .def("amount", &Bond::Price::amount,
            "Returns the price amount.")
        .def("type", &Bond::Price::type,
            "Returns the price type (Clean or Dirty).");

    // Bond class
    auto pyBond = py::class_<Bond, Instrument, ext::shared_ptr<Bond>>(
        m, "Bond",
        "Base class for bonds.")
        // Constructor: settlementDays, calendar, issueDate, coupons
        .def(py::init<Natural, const Calendar&, const Date&, const Leg&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("issueDate") = Date(),
            py::arg("coupons") = Leg(),
            "Constructs from settlement days, calendar, issue date, and coupons.")
        // Constructor: settlementDays, calendar, faceAmount, maturityDate, issueDate, cashflows
        .def(py::init<Natural, const Calendar&, Real, const Date&,
                       const Date&, const Leg&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("faceAmount"),
            py::arg("maturityDate"),
            py::arg("issueDate") = Date(),
            py::arg("cashflows") = Leg(),
            "Constructs from settlement days, calendar, face amount, maturity, issue date, and cashflows.")
        // Inspectors
        .def("settlementDays", &Bond::settlementDays,
            "Returns the number of settlement days.")
        .def("calendar", &Bond::calendar,
            py::return_value_policy::reference_internal,
            "Returns the calendar.")
        .def("notionals", &Bond::notionals,
            py::return_value_policy::reference_internal,
            "Returns the notional amounts.")
        .def("notional", &Bond::notional,
            py::arg("d") = Date(),
            "Returns the notional amount at date d.")
        .def("cashflows", &Bond::cashflows,
            py::return_value_policy::reference_internal,
            "Returns all cash flows.")
        .def("redemptions", &Bond::redemptions,
            py::return_value_policy::reference_internal,
            "Returns the redemption cash flows.")
        .def("redemption", &Bond::redemption,
            "Returns the single redemption cash flow.")
        .def("startDate", &Bond::startDate,
            "Returns the start date.")
        .def("maturityDate", &Bond::maturityDate,
            "Returns the maturity date.")
        .def("issueDate", &Bond::issueDate,
            "Returns the issue date.")
        .def("isTradable", &Bond::isTradable,
            py::arg("d") = Date(),
            "Returns True if the bond is tradable at date d.")
        .def("settlementDate", &Bond::settlementDate,
            py::arg("d") = Date(),
            "Returns the settlement date for trade date d.")
        // Pricing methods (no args - require pricing engine)
        .def("cleanPrice",
            py::overload_cast<>(&Bond::cleanPrice, py::const_),
            "Returns the clean price (requires pricing engine).")
        .def("dirtyPrice",
            py::overload_cast<>(&Bond::dirtyPrice, py::const_),
            "Returns the dirty price (requires pricing engine).")
        .def("settlementValue",
            py::overload_cast<>(&Bond::settlementValue, py::const_),
            "Returns the settlement value (requires pricing engine).")
        // Pricing methods (with yield)
        .def("cleanPrice",
            py::overload_cast<Rate, const DayCounter&, Compounding,
                              Frequency, Date>(&Bond::cleanPrice, py::const_),
            py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlement") = Date(),
            "Returns the clean price given a yield.")
        .def("dirtyPrice",
            py::overload_cast<Rate, const DayCounter&, Compounding,
                              Frequency, Date>(&Bond::dirtyPrice, py::const_),
            py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlement") = Date(),
            "Returns the dirty price given a yield.")
        // settlementValue(Real cleanPrice)
        .def("settlementValue",
            py::overload_cast<Real>(&Bond::settlementValue, py::const_),
            py::arg("cleanPrice"),
            "Returns the settlement value for a given clean price.")
        // yield -> bondYield (Python reserved keyword)
        .def("bondYield",
            py::overload_cast<const DayCounter&, Compounding, Frequency,
                              Real, Size, Real, Bond::Price::Type>(
                &Bond::yield, py::const_),
            py::arg("dayCounter"), py::arg("compounding"),
            py::arg("frequency"),
            py::arg("accuracy") = 1.0e-8,
            py::arg("maxEvaluations") = 100,
            py::arg("guess") = 0.05,
            py::arg("priceType") = Bond::Price::Clean,
            "Calculates the yield from the engine price.")
        .def("bondYield",
            py::overload_cast<Bond::Price, const DayCounter&, Compounding,
                              Frequency, Date, Real, Size, Real>(
                &Bond::yield, py::const_),
            py::arg("price"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlement") = Date(),
            py::arg("accuracy") = 1.0e-8,
            py::arg("maxEvaluations") = 100,
            py::arg("guess") = 0.05,
            "Calculates the yield from a given price.")
        // Accrual
        .def("accruedAmount", &Bond::accruedAmount,
            py::arg("d") = Date(),
            "Returns the accrued amount at date d.")
        .def("isExpired", &Bond::isExpired,
            "Returns True if the bond has expired.");

    // Bond::engine (GenericEngine<Bond::arguments, Bond::results>)
    py::class_<BondGenericEngine, PyBondGenericEngine,
               ext::shared_ptr<BondGenericEngine>, PricingEngine, Observer>(
        base, "BondGenericEngine",
        "Generic base engine for bonds.")
        .def(py::init_alias<>());

    py::class_<Bond::engine, PyBondEngine,
               ext::shared_ptr<Bond::engine>, BondGenericEngine>(
        pyBond, "engine",
        "Pricing engine for bonds.")
        .def(py::init_alias<>());
}
