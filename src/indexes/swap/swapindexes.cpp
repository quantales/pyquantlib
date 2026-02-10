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
#include <ql/indexes/swap/euriborswap.hpp>
#include <ql/indexes/swap/eurliborswap.hpp>
#include <ql/indexes/swap/usdliborswap.hpp>
#include <ql/indexes/swap/jpyliborswap.hpp>
#include <ql/indexes/swap/gbpliborswap.hpp>
#include <ql/indexes/swap/chfliborswap.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

namespace {

template <typename T>
void bindSwapIndexSubclass(py::module_& m, const char* name, const char* doc) {
    py::class_<T, SwapIndex, ext::shared_ptr<T>>(m, name, doc)
        // Tenor only (lambda to avoid Handle default arg issue)
        .def(py::init([](const Period& tenor) {
            return ext::make_shared<T>(tenor);
        }),
            py::arg("tenor"),
            "Constructs with given tenor.")
        // Tenor + explicit Handle<YTS>
        .def(py::init<const Period&, const Handle<YieldTermStructure>&>(),
            py::arg("tenor"), py::arg("h"),
            "Constructs with forwarding term structure handle.")
        // Tenor + two explicit Handles
        .def(py::init<const Period&, const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&>(),
            py::arg("tenor"), py::arg("forwarding"), py::arg("discounting"),
            "Constructs with forwarding and discounting term structure handles.")
        // Hidden handle: tenor + shared_ptr<YTS>
        .def(py::init([](const Period& tenor,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<T>(tenor, Handle<YieldTermStructure>(ts));
        }),
            py::arg("tenor"), py::arg("forwardingTermStructure"),
            "Constructs with forwarding term structure.")
        // Hidden handle: tenor + two shared_ptrs
        .def(py::init([](const Period& tenor,
                         const ext::shared_ptr<YieldTermStructure>& fwd,
                         const ext::shared_ptr<YieldTermStructure>& disc) {
            return ext::make_shared<T>(tenor,
                Handle<YieldTermStructure>(fwd),
                Handle<YieldTermStructure>(disc));
        }),
            py::arg("tenor"), py::arg("forwardingTermStructure"),
            py::arg("discountingTermStructure"),
            "Constructs with forwarding and discounting term structures.");
}

} // anonymous namespace

void ql_indexes::swapindexes(py::module_& m) {
    // Euribor swap indexes (euriborswap.hpp)
    bindSwapIndexSubclass<EuriborSwapIsdaFixA>(m,
        "EuriborSwapIsdaFixA", "Euribor swap rate (ISDA fix A).");
    bindSwapIndexSubclass<EuriborSwapIsdaFixB>(m,
        "EuriborSwapIsdaFixB", "Euribor swap rate (ISDA fix B).");
    bindSwapIndexSubclass<EuriborSwapIfrFix>(m,
        "EuriborSwapIfrFix", "Euribor swap rate (IFR fix).");

    // EUR LIBOR swap indexes (eurliborswap.hpp)
    bindSwapIndexSubclass<EurLiborSwapIsdaFixA>(m,
        "EurLiborSwapIsdaFixA", "EUR LIBOR swap rate (ISDA fix A).");
    bindSwapIndexSubclass<EurLiborSwapIsdaFixB>(m,
        "EurLiborSwapIsdaFixB", "EUR LIBOR swap rate (ISDA fix B).");
    bindSwapIndexSubclass<EurLiborSwapIfrFix>(m,
        "EurLiborSwapIfrFix", "EUR LIBOR swap rate (IFR fix).");

    // USD LIBOR swap indexes (usdliborswap.hpp)
    bindSwapIndexSubclass<UsdLiborSwapIsdaFixAm>(m,
        "UsdLiborSwapIsdaFixAm", "USD LIBOR swap rate (ISDA fix AM).");
    bindSwapIndexSubclass<UsdLiborSwapIsdaFixPm>(m,
        "UsdLiborSwapIsdaFixPm", "USD LIBOR swap rate (ISDA fix PM).");

    // JPY LIBOR swap indexes (jpyliborswap.hpp)
    bindSwapIndexSubclass<JpyLiborSwapIsdaFixAm>(m,
        "JpyLiborSwapIsdaFixAm", "JPY LIBOR swap rate (ISDA fix AM).");
    bindSwapIndexSubclass<JpyLiborSwapIsdaFixPm>(m,
        "JpyLiborSwapIsdaFixPm", "JPY LIBOR swap rate (ISDA fix PM).");

    // GBP LIBOR swap index (gbpliborswap.hpp)
    bindSwapIndexSubclass<GbpLiborSwapIsdaFix>(m,
        "GbpLiborSwapIsdaFix", "GBP LIBOR swap rate (ISDA fix).");

    // CHF LIBOR swap index (chfliborswap.hpp)
    bindSwapIndexSubclass<ChfLiborSwapIsdaFix>(m,
        "ChfLiborSwapIsdaFix", "CHF LIBOR swap rate (ISDA fix).");
}
