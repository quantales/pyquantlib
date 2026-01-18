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
#include <ql/pricingengines/vanilla/binomialengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>
#include <algorithm>
#include <cctype>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    std::string to_lower(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return result;
    }
}

void ql_pricingengines::binomialengine(py::module_& m) {
    m.def("BinomialVanillaEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& treeType,
           Size timeSteps) -> ext::shared_ptr<PricingEngine> {

            std::string lowerType = to_lower(treeType);

            if (lowerType == "jr" || lowerType == "jarrowrudd") {
                return ext::make_shared<BinomialVanillaEngine<JarrowRudd>>(
                    process, timeSteps);
            } else if (lowerType == "crr" || lowerType == "coxrossrubinstein") {
                return ext::make_shared<BinomialVanillaEngine<CoxRossRubinstein>>(
                    process, timeSteps);
            } else if (lowerType == "eqp" || lowerType == "additiveeqp") {
                return ext::make_shared<BinomialVanillaEngine<AdditiveEQPBinomialTree>>(
                    process, timeSteps);
            } else if (lowerType == "trigeorgis") {
                return ext::make_shared<BinomialVanillaEngine<Trigeorgis>>(
                    process, timeSteps);
            } else if (lowerType == "tian") {
                return ext::make_shared<BinomialVanillaEngine<Tian>>(
                    process, timeSteps);
            } else if (lowerType == "lr" || lowerType == "leisenreimer") {
                return ext::make_shared<BinomialVanillaEngine<LeisenReimer>>(
                    process, timeSteps);
            } else if (lowerType == "joshi" || lowerType == "joshi4") {
                return ext::make_shared<BinomialVanillaEngine<Joshi4>>(
                    process, timeSteps);
            } else {
                throw std::runtime_error(
                    "Unknown tree type: '" + treeType + "'. "
                    "Supported types: jr, crr, eqp, trigeorgis, tian, lr, joshi");
            }
        },
        py::arg("process"),
        py::arg("treeType"),
        py::arg("timeSteps"),
        "Binomial tree pricing engine for vanilla options.\n\n"
        "Parameters:\n"
        "  process: Black-Scholes process\n"
        "  treeType: Tree type - one of:\n"
        "    'jr' or 'jarrowrudd': Jarrow-Rudd\n"
        "    'crr' or 'coxrossrubinstein': Cox-Ross-Rubinstein\n"
        "    'eqp' or 'additiveeqp': Additive equal probabilities\n"
        "    'trigeorgis': Trigeorgis\n"
        "    'tian': Tian\n"
        "    'lr' or 'leisenreimer': Leisen-Reimer\n"
        "    'joshi' or 'joshi4': Joshi\n"
        "  timeSteps: Number of time steps (minimum 2)");
}
