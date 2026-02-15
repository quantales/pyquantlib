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
#include <ql/termstructures/bootstraphelper.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::inflationhelper(py::module_& m) {
    // BootstrapHelper<ZeroInflationTermStructure> base class
    using ZeroHelper = BootstrapHelper<ZeroInflationTermStructure>;
    py::class_<ZeroHelper, ext::shared_ptr<ZeroHelper>,
               Observer, Observable>(
        m, "ZeroInflationHelper",
        "Bootstrap helper for zero-inflation term structures.")
        .def("quote", &ZeroHelper::quote,
            "Returns the market quote handle.")
        .def("impliedQuote", &ZeroHelper::impliedQuote,
            "Returns the implied quote.")
        .def("quoteError", &ZeroHelper::quoteError,
            "Returns the difference between market and implied quotes.")
        .def("earliestDate", &ZeroHelper::earliestDate,
            "Returns the earliest date.")
        .def("maturityDate", &ZeroHelper::maturityDate,
            "Returns the maturity date.")
        .def("latestDate", &ZeroHelper::latestDate,
            "Returns the latest date.")
        .def("latestRelevantDate", &ZeroHelper::latestRelevantDate,
            "Returns the latest relevant date.");

    // RelativeDateBootstrapHelper<ZeroInflationTermStructure>
    using RelZeroHelper = RelativeDateBootstrapHelper<ZeroInflationTermStructure>;
    py::class_<RelZeroHelper, ZeroHelper, ext::shared_ptr<RelZeroHelper>>(
        m, "RelativeDateZeroInflationHelper",
        "Zero-inflation helper with dates relative to evaluation date.");

    // BootstrapHelper<YoYInflationTermStructure> base class
    using YoYHelper = BootstrapHelper<YoYInflationTermStructure>;
    py::class_<YoYHelper, ext::shared_ptr<YoYHelper>,
               Observer, Observable>(
        m, "YoYInflationHelper",
        "Bootstrap helper for year-on-year inflation term structures.")
        .def("quote", &YoYHelper::quote,
            "Returns the market quote handle.")
        .def("impliedQuote", &YoYHelper::impliedQuote,
            "Returns the implied quote.")
        .def("quoteError", &YoYHelper::quoteError,
            "Returns the difference between market and implied quotes.")
        .def("earliestDate", &YoYHelper::earliestDate,
            "Returns the earliest date.")
        .def("maturityDate", &YoYHelper::maturityDate,
            "Returns the maturity date.")
        .def("latestDate", &YoYHelper::latestDate,
            "Returns the latest date.")
        .def("latestRelevantDate", &YoYHelper::latestRelevantDate,
            "Returns the latest relevant date.");

    // RelativeDateBootstrapHelper<YoYInflationTermStructure>
    using RelYoYHelper = RelativeDateBootstrapHelper<YoYInflationTermStructure>;
    py::class_<RelYoYHelper, YoYHelper, ext::shared_ptr<RelYoYHelper>>(
        m, "RelativeDateYoYInflationHelper",
        "YoY inflation helper with dates relative to evaluation date.");
}
