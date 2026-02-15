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
#include <ql/indexes/inflationindex.hpp>
#include <ql/termstructures/inflationtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::inflationindex(py::module_& m) {
    // InflationIndex ABC
    py::class_<InflationIndex, PyInflationIndex,
               ext::shared_ptr<InflationIndex>, Index>(
        m, "InflationIndex",
        "Abstract base class for inflation indexes.")
        .def(py::init_alias<std::string, Region, bool, Frequency,
                            const Period&, Currency>(),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"),
            "Constructs an inflation index.")
        .def("familyName", &InflationIndex::familyName,
            "Returns the family name.")
        .def("region", &InflationIndex::region,
            "Returns the geographic region.")
        .def("revised", &InflationIndex::revised,
            "Returns true if the index is revised after publication.")
        .def("frequency", &InflationIndex::frequency,
            "Returns the publication frequency.")
        .def("availabilityLag", &InflationIndex::availabilityLag,
            "Returns the availability lag.")
        .def("currency", &InflationIndex::currency,
            "Returns the currency.")
        .def("pastFixing", &InflationIndex::pastFixing,
            py::arg("fixingDate"),
            "Returns the past fixing for the given date.");
}

void ql_indexes::cpi(py::module_& m) {
    // CPI struct with InterpolationType enum and static methods
    py::class_<CPI> cpi(m, "CPI",
        "CPI interpolation methods and utilities.");

    py::enum_<CPI::InterpolationType>(cpi, "InterpolationType",
        "CPI interpolation type.")
        .value("AsIndex", CPI::AsIndex, "Same interpolation as the index.")
        .value("Flat", CPI::Flat, "Flat from previous fixing.")
        .value("Linear", CPI::Linear, "Linearly between bracketing fixings.")
        .export_values();

    cpi.def_static("laggedFixing", &CPI::laggedFixing,
        py::arg("index"), py::arg("date"),
        py::arg("observationLag"), py::arg("interpolationType"),
        "Returns the lagged CPI fixing.");
}

void ql_indexes::zeroinflationindex(py::module_& m) {
    // ZeroInflationIndex
    py::class_<ZeroInflationIndex, InflationIndex,
               ext::shared_ptr<ZeroInflationIndex>>(
        m, "ZeroInflationIndex",
        "Zero-coupon inflation index.")
        // Constructor without term structure
        .def(py::init([](const std::string& familyName, const Region& region,
                        bool revised, Frequency frequency,
                        const Period& availabilityLag, const Currency& currency) {
            return ext::make_shared<ZeroInflationIndex>(
                familyName, region, revised, frequency,
                availabilityLag, currency);
        }),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"),
            "Constructs a zero inflation index without a term structure.")
        // Constructor with explicit handle
        .def(py::init<const std::string&, const Region&, bool, Frequency,
                      const Period&, const Currency&,
                      Handle<ZeroInflationTermStructure>>(),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"), py::arg("h"),
            "Constructs a zero inflation index with term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const std::string& familyName, const Region& region,
                        bool revised, Frequency frequency,
                        const Period& availabilityLag, const Currency& currency,
                        const ext::shared_ptr<ZeroInflationTermStructure>& ts) {
            return ext::make_shared<ZeroInflationIndex>(
                familyName, region, revised, frequency,
                availabilityLag, currency,
                Handle<ZeroInflationTermStructure>(ts));
        }),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"), py::arg("zeroInflationTermStructure"),
            "Constructs a zero inflation index with term structure.")
        .def("zeroInflationTermStructure",
            &ZeroInflationIndex::zeroInflationTermStructure,
            "Returns the zero inflation term structure handle.")
        .def("clone", &ZeroInflationIndex::clone,
            py::arg("h"),
            "Returns a copy linked to a different term structure.")
        .def("lastFixingDate", &ZeroInflationIndex::lastFixingDate,
            "Returns the last available fixing date.");
}

void ql_indexes::yoyinflationindex(py::module_& m) {
    // YoYInflationIndex
    py::class_<YoYInflationIndex, InflationIndex,
               ext::shared_ptr<YoYInflationIndex>>(
        m, "YoYInflationIndex",
        "Year-on-year inflation index.")
        // Constructor from ZeroInflationIndex (ratio-based)
        .def(py::init([](const ext::shared_ptr<ZeroInflationIndex>& underlyingIndex) {
            return ext::make_shared<YoYInflationIndex>(underlyingIndex);
        }),
            py::arg("underlyingIndex"),
            "Constructs a year-on-year index as a ratio of a zero index.")
        // Constructor from ZeroInflationIndex with explicit handle
        .def(py::init<const ext::shared_ptr<ZeroInflationIndex>&,
                      Handle<YoYInflationTermStructure>>(),
            py::arg("underlyingIndex"), py::arg("h"),
            "Constructs a year-on-year index with term structure handle.")
        // Constructor from ZeroInflationIndex with hidden handle
        .def(py::init([](const ext::shared_ptr<ZeroInflationIndex>& underlyingIndex,
                        const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YoYInflationIndex>(
                underlyingIndex, Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("underlyingIndex"), py::arg("yoyInflationTermStructure"),
            "Constructs a year-on-year index with term structure.")
        // Quoted YoY constructor (standalone, no underlying zero index)
        .def(py::init([](const std::string& familyName, const Region& region,
                        bool revised, Frequency frequency,
                        const Period& availabilityLag, const Currency& currency) {
            return ext::make_shared<YoYInflationIndex>(
                familyName, region, revised, frequency,
                availabilityLag, currency);
        }),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"),
            "Constructs a quoted year-on-year index without a term structure.")
        // Quoted YoY with explicit handle
        .def(py::init<const std::string&, const Region&, bool, Frequency,
                      const Period&, const Currency&,
                      Handle<YoYInflationTermStructure>>(),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"), py::arg("h"),
            "Constructs a quoted year-on-year index with term structure handle.")
        // Quoted YoY with hidden handle
        .def(py::init([](const std::string& familyName, const Region& region,
                        bool revised, Frequency frequency,
                        const Period& availabilityLag, const Currency& currency,
                        const ext::shared_ptr<YoYInflationTermStructure>& ts) {
            return ext::make_shared<YoYInflationIndex>(
                familyName, region, revised, frequency,
                availabilityLag, currency,
                Handle<YoYInflationTermStructure>(ts));
        }),
            py::arg("familyName"), py::arg("region"), py::arg("revised"),
            py::arg("frequency"), py::arg("availabilityLag"),
            py::arg("currency"), py::arg("yoyInflationTermStructure"),
            "Constructs a quoted year-on-year index with term structure.")
        .def("ratio", &YoYInflationIndex::ratio,
            "Returns true if index is defined as a ratio of zero index fixings.")
        .def("interpolated", &YoYInflationIndex::interpolated,
            "Returns true if the index interpolates between fixings.")
        .def("underlyingIndex", &YoYInflationIndex::underlyingIndex,
            "Returns the underlying zero inflation index (if ratio-based).")
        .def("yoyInflationTermStructure",
            &YoYInflationIndex::yoyInflationTermStructure,
            "Returns the YoY inflation term structure handle.")
        .def("clone", &YoYInflationIndex::clone,
            py::arg("h"),
            "Returns a copy linked to a different term structure.")
        .def("lastFixingDate", &YoYInflationIndex::lastFixingDate,
            "Returns the last available fixing date.");
}
