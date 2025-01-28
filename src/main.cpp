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

#include <ql/version.hpp>
#include <ql/errors.hpp>
#include <pybind11/pybind11.h>
#include "pyquantlib/version.h"
#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"
#include "pyquantlib/type_casters/date.h"

namespace py = pybind11;

PYBIND11_MODULE(_pyquantlib, m) {
    // Module metadata
    m.doc() = "PyQuantLib: Python bindings for QuantLib";
    m.attr("__version__") = PYQUANTLIB_VERSION;
    m.attr("__ql_version__") = QL_VERSION;
    m.attr("__ql_hexversion__") = QL_HEX_VERSION;
    m.attr("__boost_version__") = QuantLib::compiledBoostVersion();

    // Pybind11 exception translation for QuantLib exceptions
    py::register_exception<QuantLib::Error>(m, "Error");
    
    // Initialize binding manager
    BindingManager manager(m, "pyquantlib");    
    
    submodules_bindings(manager);        // Creates "base" submodule
    patterns_bindings(manager);          // Observer/Observable pattern
    utilities_bindings(manager);         // Utility classes
    time_bindings(manager);              // Date, Calendar, Period, etc.
    core_bindings(manager);              // Constants, Settings, etc.

    // Finalize all bindings
    manager.finalize();

}
