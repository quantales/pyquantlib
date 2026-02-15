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
#include <ql/indexes/region.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::region(py::module_& m) {
    // Region base class (bridge pattern, like Calendar)
    py::class_<Region, ext::shared_ptr<Region>>(m, "Region",
        "Geographic region for inflation indexes.")
        .def("name", &Region::name,
            "Returns the region name.")
        .def("code", &Region::code,
            "Returns the ISO region code.")
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("__str__", [](const Region& r) { return r.name(); })
        .def("__repr__", [](const Region& r) {
            return "Region('" + r.name() + "', '" + r.code() + "')";
        });

    // CustomRegion
    py::class_<CustomRegion, Region, ext::shared_ptr<CustomRegion>>(
        m, "CustomRegion", "Custom region with user-defined name and code.")
        .def(py::init<const std::string&, const std::string&>(),
            py::arg("name"), py::arg("code"),
            "Constructs a custom region.");

    // Concrete regions
    py::class_<AustraliaRegion, Region, ext::shared_ptr<AustraliaRegion>>(
        m, "AustraliaRegion", "Australia region.")
        .def(py::init<>());

    py::class_<EURegion, Region, ext::shared_ptr<EURegion>>(
        m, "EURegion", "European Union region.")
        .def(py::init<>());

    py::class_<FranceRegion, Region, ext::shared_ptr<FranceRegion>>(
        m, "FranceRegion", "France region.")
        .def(py::init<>());

    py::class_<UKRegion, Region, ext::shared_ptr<UKRegion>>(
        m, "UKRegion", "United Kingdom region.")
        .def(py::init<>());

    py::class_<USRegion, Region, ext::shared_ptr<USRegion>>(
        m, "USRegion", "United States region.")
        .def(py::init<>());

    py::class_<ZARegion, Region, ext::shared_ptr<ZARegion>>(
        m, "ZARegion", "South Africa region.")
        .def(py::init<>());
}
