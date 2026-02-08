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
#include <ql/instruments/creditdefaultswap.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::cdspricingmodel(py::module_& m) {
    py::enum_<CreditDefaultSwap::PricingModel>(m, "CdsPricingModel",
        "CDS pricing model.")
        .value("Midpoint", CreditDefaultSwap::Midpoint, "Midpoint model.")
        .value("ISDA", CreditDefaultSwap::ISDA, "ISDA standard model.");
}
