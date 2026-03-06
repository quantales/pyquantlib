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
#include <ql/termstructures/yield/compositezeroyieldstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::compositezeroyieldstructure(py::module_& m) {
    using BinaryFunc = std::function<Real(Real, Real)>;
    using CompositeZero = CompositeZeroYieldStructure<BinaryFunc>;

    py::class_<CompositeZero, YieldTermStructure,
               ext::shared_ptr<CompositeZero>>(
        m, "CompositeZeroYieldStructure",
        "Composite zero-yield term structure from two curves and a binary function.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>, Handle<YieldTermStructure>,
                      const BinaryFunc&, Compounding, Frequency>(),
            py::arg("curve1"), py::arg("curve2"),
            py::arg("composer"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = NoFrequency,
            "Constructs from yield curve handles and a composer function.")
        // Hidden handle: shared_ptr overload
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& c1,
                         const ext::shared_ptr<YieldTermStructure>& c2,
                         const BinaryFunc& f,
                         Compounding comp,
                         Frequency freq) {
            return ext::make_shared<CompositeZero>(
                Handle<YieldTermStructure>(c1),
                Handle<YieldTermStructure>(c2),
                f, comp, freq);
        }),
            py::arg("curve1"), py::arg("curve2"),
            py::arg("composer"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = NoFrequency,
            "Constructs from yield curves and composer (handles created internally).");
}
