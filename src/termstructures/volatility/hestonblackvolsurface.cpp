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
#include <ql/termstructures/volatility/equityfx/hestonblackvolsurface.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::hestonblackvolsurface(py::module_& m) {
    py::class_<HestonBlackVolSurface, BlackVolTermStructure,
               ext::shared_ptr<HestonBlackVolSurface>>(
        m, "HestonBlackVolSurface",
        "Black volatility surface implied by a Heston model.")
        // Handle constructor (required args only to avoid enum default ordering issues)
        .def(py::init<const Handle<HestonModel>&>(),
            py::arg("hestonModel"),
            "Constructs from Heston model handle with default formula and integration.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<HestonModel>& model) {
            return ext::make_shared<HestonBlackVolSurface>(
                Handle<HestonModel>(model));
        }),
            py::arg("hestonModel"),
            "Constructs from Heston model (handle created internally).");
}
