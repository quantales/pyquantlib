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
#include <ql/instrument.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::instrument(py::module_& m) {
    auto pyInstrument = py::class_<Instrument, PyInstrument,
        ext::shared_ptr<Instrument>, LazyObject>(m, "Instrument",
        "Abstract base class for financial instruments.")
        .def(py::init_alias<>())
        .def("NPV", &Instrument::NPV,
            "Returns the net present value of the instrument.")
        .def("isExpired", &Instrument::isExpired,
            "Returns true if the instrument has expired.")
        .def("setPricingEngine", &Instrument::setPricingEngine,
            py::arg("engine"),
            "Sets the pricing engine for valuation.");

    py::class_<Instrument::results, PricingEngine::results,
        ext::shared_ptr<Instrument::results>>(pyInstrument, "results",
        "Results from instrument valuation.")
        .def(py::init<>())
        .def_readwrite("value", &Instrument::results::value,
            "The calculated NPV.");
}
