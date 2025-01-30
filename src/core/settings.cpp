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
#include <ql/settings.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::settings(py::module_& m) {
    py::class_<Settings, std::unique_ptr<Settings, py::nodelete>>(m, "Settings",
        "Global repository for run-time library settings.")
        .def_static("instance", &Settings::instance, py::return_value_policy::reference,
            "Returns the singleton instance.")
        .def_property("evaluationDate",
            [](const Settings& self) { return static_cast<Date>(self.evaluationDate()); },
            [](Settings& self, const Date& d) { self.evaluationDate() = d; },
            "The evaluation date for pricing calculations.")
        .def("setEvaluationDate",
            [](Settings& self, const Date& d) { self.evaluationDate() = d; },
            py::arg("date"),
            "Sets the evaluation date.")
        .def("anchorEvaluationDate", &Settings::anchorEvaluationDate,
            "Prevents the evaluation date from advancing automatically.")
        .def("resetEvaluationDate", &Settings::resetEvaluationDate,
            "Resets the evaluation date to today and allows automatic advancement.")
        .def_property("includeReferenceDateEvents",
            [](const Settings& self) { return self.includeReferenceDateEvents(); },
            [](Settings& self, bool value) { self.includeReferenceDateEvents() = value; },
            "Whether events on the reference date are included.")
        .def_property("includeTodaysCashFlows",
            [](const Settings& self) { return self.includeTodaysCashFlows(); },
            [](Settings& self, const std::optional<bool>& value) {
                self.includeTodaysCashFlows() = value;
            },
            "Whether to include today's cash flows (optional).")
        .def_property("enforcesTodaysHistoricFixings",
            [](const Settings& self) { return self.enforcesTodaysHistoricFixings(); },
            [](Settings& self, bool value) { self.enforcesTodaysHistoricFixings() = value; },
            "Whether to enforce historic fixings for today.");

    py::class_<SavedSettings>(m, "SavedSettings",
        "Temporarily stores and restores global settings.")
        .def(py::init<>())
        .def("__enter__", [](SavedSettings& self) -> SavedSettings& { return self; })
        .def("__exit__", [](SavedSettings&, py::object, py::object, py::object) {});
}
