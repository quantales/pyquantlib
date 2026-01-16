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
#include <ql/pricingengines/genericmodelengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::genericmodelengine(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // GenericHestonModelEngine is defined in trampolines.h
    // Inherits from GenericEngine which inherits from PricingEngine
    py::class_<GenericHestonModelEngine, PyGenericHestonModelEngine,
               ext::shared_ptr<GenericHestonModelEngine>, PricingEngine>(
        base, "GenericHestonModelEngine",
        "Generic pricing engine for Heston model.")
        .def(py::init<const Handle<HestonModel>&>(),
             py::arg("model") = Handle<HestonModel>())
        .def(py::init<const ext::shared_ptr<HestonModel>&>(),
             py::arg("model"));
}
