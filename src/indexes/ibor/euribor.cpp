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
#include <ql/indexes/ibor/euribor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::euribor(py::module_& m) {
    // Euribor base class
    py::class_<Euribor, IborIndex, ext::shared_ptr<Euribor>>(
        m, "Euribor",
        "Euribor index fixed by the ECB.")
        // Constructor without term structure
        .def(py::init([](const Period& tenor) {
            return ext::make_shared<Euribor>(tenor);
        }),
            py::arg("tenor"),
            "Constructs Euribor index with given tenor.")
        // Constructor with handle
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
            py::arg("tenor"),
            py::arg("h"),
            "Constructs Euribor index with forwarding term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const Period& tenor,
                        const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor>(tenor, Handle<YieldTermStructure>(ts));
        }),
            py::arg("tenor"),
            py::arg("forwardingTermStructure"),
            "Constructs Euribor index with forwarding term structure.");

    // Euribor365 class
    py::class_<Euribor365, IborIndex, ext::shared_ptr<Euribor365>>(
        m, "Euribor365",
        "Actual/365 Euribor index.")
        .def(py::init([](const Period& tenor) {
            return ext::make_shared<Euribor365>(tenor);
        }),
            py::arg("tenor"),
            "Constructs Euribor365 index with given tenor.")
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
            py::arg("tenor"),
            py::arg("h"),
            "Constructs Euribor365 index with forwarding term structure handle.");

    // Convenience classes for standard tenors
    py::class_<Euribor1W, Euribor, ext::shared_ptr<Euribor1W>>(
        m, "Euribor1W",
        "1-week Euribor index.")
        .def(py::init([]() { return ext::make_shared<Euribor1W>(); }))
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"))
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor1W>(Handle<YieldTermStructure>(ts));
        }),
            py::arg("forwardingTermStructure"));

    py::class_<Euribor1M, Euribor, ext::shared_ptr<Euribor1M>>(
        m, "Euribor1M",
        "1-month Euribor index.")
        .def(py::init([]() { return ext::make_shared<Euribor1M>(); }))
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"))
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor1M>(Handle<YieldTermStructure>(ts));
        }),
            py::arg("forwardingTermStructure"));

    py::class_<Euribor3M, Euribor, ext::shared_ptr<Euribor3M>>(
        m, "Euribor3M",
        "3-month Euribor index.")
        .def(py::init([]() { return ext::make_shared<Euribor3M>(); }))
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"))
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor3M>(Handle<YieldTermStructure>(ts));
        }),
            py::arg("forwardingTermStructure"));

    py::class_<Euribor6M, Euribor, ext::shared_ptr<Euribor6M>>(
        m, "Euribor6M",
        "6-month Euribor index.")
        .def(py::init([]() { return ext::make_shared<Euribor6M>(); }))
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"))
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor6M>(Handle<YieldTermStructure>(ts));
        }),
            py::arg("forwardingTermStructure"));

    py::class_<Euribor1Y, Euribor, ext::shared_ptr<Euribor1Y>>(
        m, "Euribor1Y",
        "1-year Euribor index.")
        .def(py::init([]() { return ext::make_shared<Euribor1Y>(); }))
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"))
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Euribor1Y>(Handle<YieldTermStructure>(ts));
        }),
            py::arg("forwardingTermStructure"));
}
