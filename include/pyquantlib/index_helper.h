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

#pragma once

#include "pyquantlib/pyquantlib.h"
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

/*!
 * Binding helpers for the rate indexes that share one of three constructor
 * shapes. Each helper registers the plain, explicit-handle, and hidden-handle
 * constructors, so the per-index binding files only state the class and its
 * docstring.
 */

/*! Overnight index constructed from an optional forwarding curve. */
template <typename T>
py::class_<T, QuantLib::OvernightIndex, QuantLib::ext::shared_ptr<T>>
bindOvernightIndex(py::module_& m, const char* name, const char* doc) {
    using namespace QuantLib;
    return py::class_<T, OvernightIndex, ext::shared_ptr<T>>(m, name, doc)
        .def(py::init<>(),
            "Constructs the index without forwarding curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs the index with forwarding term structure handle.")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<T>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs the index with forwarding term structure.");
}

/*! IBOR index constructed from a tenor and an optional forwarding curve. */
template <typename T>
py::class_<T, QuantLib::IborIndex, QuantLib::ext::shared_ptr<T>>
bindTenorIborIndex(py::module_& m, const char* name, const char* doc) {
    using namespace QuantLib;
    return py::class_<T, IborIndex, ext::shared_ptr<T>>(m, name, doc)
        .def(py::init([](const Period& tenor) {
            return ext::make_shared<T>(tenor);
        }),
            py::arg("tenor"),
            "Constructs the index with given tenor.")
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
            py::arg("tenor"), py::arg("h"),
            "Constructs the index with forwarding term structure handle.")
        .def(py::init([](const Period& tenor,
                         const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<T>(tenor, Handle<YieldTermStructure>(curve));
        }),
            py::arg("tenor"), py::arg("forwardingTermStructure"),
            "Constructs the index with forwarding term structure.");
}

/*! Fixed-tenor convenience subclass of a tenor-based index (e.g. Bbsw3M). */
template <typename T, typename Base>
py::class_<T, Base, QuantLib::ext::shared_ptr<T>>
bindFixedTenorIndex(py::module_& m, const char* name, const char* doc) {
    using namespace QuantLib;
    return py::class_<T, Base, ext::shared_ptr<T>>(m, name, doc)
        .def(py::init<>(),
            "Constructs the index without forwarding curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("h"),
            "Constructs the index with forwarding term structure handle.")
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve) {
            return ext::make_shared<T>(Handle<YieldTermStructure>(curve));
        }),
            py::arg("forwardingTermStructure"),
            "Constructs the index with forwarding term structure.");
}
