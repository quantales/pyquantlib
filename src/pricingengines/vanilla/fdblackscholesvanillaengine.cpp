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
#include <ql/pricingengines/vanilla/fdblackscholesvanillaengine.hpp>
#include <ql/pricingengines/vanilla/cashdividendeuropeanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdblackscholesvanillaengine(py::module_& m) {
    // CashDividendModel enum is registered by cashdividendeuropeanengine
    // FdBlackScholesVanillaEngine reuses it.

    // FdBlackScholesVanillaEngine
    py::class_<FdBlackScholesVanillaEngine,
               ext::shared_ptr<FdBlackScholesVanillaEngine>,
               PricingEngine>(
        m, "FdBlackScholesVanillaEngine",
        "Finite-differences Black-Scholes vanilla option engine.")
        .def(py::init([](ext::shared_ptr<GeneralizedBlackScholesProcess> process,
                         Size tGrid, Size xGrid, Size dampingSteps,
                         const FdmSchemeDesc& schemeDesc,
                         bool localVol, Real illegalLocalVolOverwrite,
                         CashDividendEuropeanEngine::CashDividendModel cashDividendModel) {
            return ext::make_shared<FdBlackScholesVanillaEngine>(
                std::move(process), tGrid, xGrid, dampingSteps,
                schemeDesc, localVol, illegalLocalVolOverwrite,
                static_cast<FdBlackScholesVanillaEngine::CashDividendModel>(cashDividendModel));
        }),
            py::arg("process"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = -Null<Real>(),
            py::arg("cashDividendModel") = CashDividendEuropeanEngine::Spot,
            "Constructs a finite-difference Black-Scholes engine.\n\n"
            "Parameters:\n"
            "  process: Black-Scholes process\n"
            "  tGrid: Number of time steps\n"
            "  xGrid: Number of spatial grid points\n"
            "  dampingSteps: Damping steps near maturity\n"
            "  schemeDesc: FD scheme (Douglas, CrankNicolson, etc.)\n"
            "  localVol: Use local volatility\n"
            "  illegalLocalVolOverwrite: Override for illegal local vol values\n"
            "  cashDividendModel: Spot or Escrowed");
}
