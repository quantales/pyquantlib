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
#include <ql/pricingengines/bond/bondfunctions.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::bondfunctions(py::module_& m) {
    py::class_<BondFunctions>(m, "BondFunctions",
        "Static bond analytics functions.")
        // Date inspectors
        .def_static("startDate", &BondFunctions::startDate,
            py::arg("bond"), "Start date of the bond.")
        .def_static("maturityDate", &BondFunctions::maturityDate,
            py::arg("bond"), "Maturity date of the bond.")
        .def_static("isTradable", &BondFunctions::isTradable,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Whether the bond is tradable at the given date.")
        // Cashflow inspectors
        .def_static("previousCashFlowDate", &BondFunctions::previousCashFlowDate,
            py::arg("bond"), py::arg("refDate") = Date(),
            "Date of the previous cash flow.")
        .def_static("nextCashFlowDate", &BondFunctions::nextCashFlowDate,
            py::arg("bond"), py::arg("refDate") = Date(),
            "Date of the next cash flow.")
        .def_static("previousCashFlowAmount",
            &BondFunctions::previousCashFlowAmount,
            py::arg("bond"), py::arg("refDate") = Date(),
            "Amount of the previous cash flow.")
        .def_static("nextCashFlowAmount", &BondFunctions::nextCashFlowAmount,
            py::arg("bond"), py::arg("refDate") = Date(),
            "Amount of the next cash flow.")
        // Coupon inspectors
        .def_static("previousCouponRate", &BondFunctions::previousCouponRate,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Previous coupon rate.")
        .def_static("nextCouponRate", &BondFunctions::nextCouponRate,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Next coupon rate.")
        .def_static("accrualStartDate", &BondFunctions::accrualStartDate,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrual start date.")
        .def_static("accrualEndDate", &BondFunctions::accrualEndDate,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrual end date.")
        .def_static("accrualPeriod", &BondFunctions::accrualPeriod,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrual period as a year fraction.")
        .def_static("accrualDays", &BondFunctions::accrualDays,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrual days.")
        .def_static("accruedPeriod", &BondFunctions::accruedPeriod,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrued period as a year fraction.")
        .def_static("accruedDays", &BondFunctions::accruedDays,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrued days.")
        .def_static("accruedAmount", &BondFunctions::accruedAmount,
            py::arg("bond"), py::arg("settlementDate") = Date(),
            "Accrued amount.")
        // Yield from discount curve
        .def_static("cleanPrice",
            static_cast<Real (*)(const Bond&, const YieldTermStructure&, Date)>(
                &BondFunctions::cleanPrice),
            py::arg("bond"), py::arg("discountCurve"),
            py::arg("settlementDate") = Date(),
            "Clean price from discount curve.")
        .def_static("dirtyPrice",
            static_cast<Real (*)(const Bond&, const YieldTermStructure&, Date)>(
                &BondFunctions::dirtyPrice),
            py::arg("bond"), py::arg("discountCurve"),
            py::arg("settlementDate") = Date(),
            "Dirty price from discount curve.")
        .def_static("bps",
            static_cast<Real (*)(const Bond&, const YieldTermStructure&, Date)>(
                &BondFunctions::bps),
            py::arg("bond"), py::arg("discountCurve"),
            py::arg("settlementDate") = Date(),
            "Basis point sensitivity from discount curve.")
        // Yield from rate
        .def_static("cleanPriceFromYield",
            static_cast<Real (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Date)>(
                &BondFunctions::cleanPrice),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Clean price from yield.")
        .def_static("dirtyPriceFromYield",
            static_cast<Real (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Date)>(
                &BondFunctions::dirtyPrice),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Dirty price from yield.")
        // Yield calculation
        .def_static("bondYield",
            static_cast<Rate (*)(const Bond&, Bond::Price, const DayCounter&,
                                 Compounding, Frequency, Date,
                                 Real, Size, Rate)>(
                &BondFunctions::yield),
            py::arg("bond"), py::arg("price"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            py::arg("accuracy") = 1.0e-10,
            py::arg("maxIterations") = 100,
            py::arg("guess") = 0.05,
            "Bond yield (IRR) from price.")
        // Duration
        .def_static("duration",
            static_cast<Time (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Duration::Type,
                                 Date)>(
                &BondFunctions::duration),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("type") = Duration::Modified,
            py::arg("settlementDate") = Date(),
            "Bond duration.")
        // Convexity
        .def_static("convexity",
            static_cast<Real (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Date)>(
                &BondFunctions::convexity),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Bond convexity.")
        // Basis point value
        .def_static("basisPointValue",
            static_cast<Real (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Date)>(
                &BondFunctions::basisPointValue),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Basis point value (DV01).")
        // Yield value of basis point
        .def_static("yieldValueBasisPoint",
            static_cast<Real (*)(const Bond&, Rate, const DayCounter&,
                                 Compounding, Frequency, Date)>(
                &BondFunctions::yieldValueBasisPoint),
            py::arg("bond"), py::arg("yield"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Yield value of a basis point.")
        // Z-spread
        .def_static("zSpread",
            static_cast<Spread (*)(const Bond&, Bond::Price,
                                   const ext::shared_ptr<YieldTermStructure>&,
                                   const DayCounter&, Compounding, Frequency,
                                   Date, Real, Size, Rate)>(
                &BondFunctions::zSpread),
            py::arg("bond"), py::arg("price"), py::arg("discountCurve"),
            py::arg("dayCounter"), py::arg("compounding"),
            py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            py::arg("accuracy") = 1.0e-10,
            py::arg("maxIterations") = 100,
            py::arg("guess") = 0.0,
            "Z-spread over a discount curve.");
}
