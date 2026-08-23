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
#include "pyquantlib/trampolines.h"
#include <ql/patterns/lazyobject.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace py = pybind11;
using namespace QuantLib;

void ql_patterns::lazyobject(py::module_& m) {

    py::classh<LazyObject, PyLazyObject,
            Observer, Observable>(m, "LazyObject",
        "Framework for lazy object calculation.\n\n"
        "Derived classes must implement performCalculations().")
        .def(py::init_alias<>())
        
        .def("recalculate", &LazyObject::recalculate,
            "Force recalculation of the object.")
        .def("freeze", &LazyObject::freeze,
            "Freeze the object, preventing automatic recalculation.")
        .def("unfreeze", &LazyObject::unfreeze,
            "Unfreeze the object, allowing automatic recalculation.")

        .attr("multiple_inheritance") = py::bool_(true)
        ;
        
}