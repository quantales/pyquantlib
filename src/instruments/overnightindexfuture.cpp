/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/instruments/overnightindexfuture.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::overnightindexfuture(py::module_& m) {
    py::class_<OvernightIndexFuture, Instrument,
               ext::shared_ptr<OvernightIndexFuture>>(
        m, "OvernightIndexFuture",
        "Future on a compounded or averaged overnight index.")
        .def(py::init<ext::shared_ptr<OvernightIndex>, const Date&, const Date&,
                      Handle<Quote>, RateAveraging::Type>(),
             py::arg("overnightIndex"),
             py::arg("valueDate"),
             py::arg("maturityDate"),
             py::arg("convexityAdjustment") = Handle<Quote>(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             "Constructs an overnight index future.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<OvernightIndex>& index,
                         const Date& valueDate, const Date& maturityDate,
                         const ext::shared_ptr<Quote>& convexityAdjustment,
                         RateAveraging::Type averagingMethod) {
            return ext::make_shared<OvernightIndexFuture>(
                index, valueDate, maturityDate,
                Handle<Quote>(convexityAdjustment), averagingMethod);
        }),
             py::arg("overnightIndex"),
             py::arg("valueDate"),
             py::arg("maturityDate"),
             py::arg("convexityAdjustment"),
             py::arg("averagingMethod") = RateAveraging::Compound,
             "Constructs an overnight index future (handle created internally).")
        .def("convexityAdjustment", &OvernightIndexFuture::convexityAdjustment,
             "Returns the convexity adjustment.")
        .def("overnightIndex", &OvernightIndexFuture::overnightIndex,
             "Returns the underlying overnight index.")
        .def("valueDate", &OvernightIndexFuture::valueDate,
             "Returns the first day of the reference period.")
        .def("maturityDate", &OvernightIndexFuture::maturityDate,
             "Returns the delivery date.");
}
