/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/trampolines.h"
#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


namespace py = pybind11;
using namespace QuantLib;

void ql_patterns::lazyobject(py::module_& m) {

    py::class_<LazyObject, PyLazyObject, ext::shared_ptr<LazyObject>,
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