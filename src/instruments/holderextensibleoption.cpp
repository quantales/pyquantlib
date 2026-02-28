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
#include <ql/instruments/holderextensibleoption.hpp>
#include <ql/instruments/payoffs.hpp>
#include <ql/exercise.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::holderextensibleoption(py::module_& m) {
    py::class_<HolderExtensibleOption, OneAssetOption,
               ext::shared_ptr<HolderExtensibleOption>>(
        m, "HolderExtensibleOption",
        "Holder-extensible option.")
        .def(py::init<Option::Type, Real, Date, Real,
                      const ext::shared_ptr<StrikedTypePayoff>&,
                      const ext::shared_ptr<Exercise>&>(),
             py::arg("type"),
             py::arg("premium"),
             py::arg("secondExpiryDate"),
             py::arg("secondStrike"),
             py::arg("payoff"),
             py::arg("exercise"));
}
