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


void ql_patterns::observable(py::module_& m)
{
    py::class_<Observable, PyObservable, ext::shared_ptr<Observable>>(m, "Observable",
        "Core observable class in QuantLib's Observer pattern\n\n"
        "Maintains a list of observers and notifies them of state changes.")

        .def(py::init<>(), "Default constructor for the Observable.")
        .def("notifyObservers",
            static_cast<void (Observable::*)()>(
                &Observable::notifyObservers),
            "Notify all registered observers of state changes.\n"
            "This version broadcasts a generic notification without event details.")
            ;
}

void ql_patterns::observer(py::module_& m)
{
    py::class_<Observer, PyObserver, ext::shared_ptr<Observer>>(m, "Observer",
        "Observer in QuantLib's Observer pattern\n\n"
        "Receives updates from Observable objects. Must implement update().")
        .def(py::init_alias<>())
        .def("update", &Observer::update,
            "This method is called by the observable when it changes. "
            "Derived classes must implement this method.")
        .def("registerWith",
            [](Observer &self, const ext::shared_ptr<Observable>& observable) {
                self.registerWith(observable); // Call the original method, discard return value
            },
            py::arg("observable"),
            "Register this observer with the given observable. "
            "The observer will then be notified when the observable changes.")

        .def("unregisterWith", &Observer::unregisterWith,
            py::arg("observable"),
            "Unregister this observer from the given observable. "
            "The observer will no longer be notified by this observable.")

        .def("unregisterWithAll", &Observer::unregisterWithAll,
            "Unregister this observer from all observables it is currently registered with.")
        ;
}

