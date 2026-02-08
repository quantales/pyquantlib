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
#include <ql/instruments/assetswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::assetswap(py::module_& m) {
    py::class_<AssetSwap, Swap, ext::shared_ptr<AssetSwap>>(
        m, "AssetSwap",
        "Bullet bond vs Libor swap.")
        .def(py::init([](bool payBondCoupon,
                         ext::shared_ptr<Bond> bond,
                         Real bondCleanPrice,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         Spread spread,
                         Schedule floatSchedule,
                         const py::object& floatingDC,
                         bool parAssetSwap) {
            DayCounter dc;
            if (!floatingDC.is_none())
                dc = floatingDC.cast<DayCounter>();
            return ext::make_shared<AssetSwap>(
                payBondCoupon, std::move(bond), bondCleanPrice,
                iborIndex, spread, std::move(floatSchedule),
                dc, parAssetSwap);
        }),
            py::arg("payBondCoupon"),
            py::arg("bond"),
            py::arg("bondCleanPrice"),
            py::arg("iborIndex"),
            py::arg("spread"),
            py::arg("floatSchedule") = Schedule(),
            py::arg("floatingDayCount") = py::none(),
            py::arg("parAssetSwap") = true,
            "Constructs an asset swap.")
        // Inspectors
        .def("fairSpread", &AssetSwap::fairSpread, "Fair spread.")
        .def("floatingLegBPS", &AssetSwap::floatingLegBPS,
            "Floating leg BPS.")
        .def("floatingLegNPV", &AssetSwap::floatingLegNPV,
            "Floating leg NPV.")
        .def("fairCleanPrice", &AssetSwap::fairCleanPrice,
            "Fair clean price.")
        .def("fairNonParRepayment", &AssetSwap::fairNonParRepayment,
            "Fair non-par repayment.")
        .def("parSwap", &AssetSwap::parSwap, "Whether this is a par swap.")
        .def("spread", &AssetSwap::spread, "Spread.")
        .def("cleanPrice", &AssetSwap::cleanPrice, "Clean price.")
        .def("nonParRepayment", &AssetSwap::nonParRepayment,
            "Non-par repayment.")
        .def("bond", &AssetSwap::bond, "Underlying bond.")
        .def("payBondCoupon", &AssetSwap::payBondCoupon,
            "Whether bond coupons are paid.")
        .def("bondLeg", &AssetSwap::bondLeg, "Bond leg.")
        .def("floatingLeg", &AssetSwap::floatingLeg, "Floating leg.");
}
