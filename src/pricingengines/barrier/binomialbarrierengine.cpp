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
#include <ql/pricingengines/barrier/binomialbarrierengine.hpp>
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

    template <class D>
    ext::shared_ptr<PricingEngine> make_engine(
        const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
        const std::string& treeType, Size timeSteps, Size maxTimeSteps) {

        if (treeType == "jr" || treeType == "jarrowrudd") {
            return ext::make_shared<BinomialBarrierEngine<JarrowRudd, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "crr" || treeType == "coxrossrubinstein") {
            return ext::make_shared<BinomialBarrierEngine<CoxRossRubinstein, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "eqp" || treeType == "additiveeqp") {
            return ext::make_shared<BinomialBarrierEngine<AdditiveEQPBinomialTree, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "trigeorgis") {
            return ext::make_shared<BinomialBarrierEngine<Trigeorgis, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "tian") {
            return ext::make_shared<BinomialBarrierEngine<Tian, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "lr" || treeType == "leisenreimer") {
            return ext::make_shared<BinomialBarrierEngine<LeisenReimer, D>>(
                process, timeSteps, maxTimeSteps);
        } else if (treeType == "joshi" || treeType == "joshi4") {
            return ext::make_shared<BinomialBarrierEngine<Joshi4, D>>(
                process, timeSteps, maxTimeSteps);
        } else {
            throw std::runtime_error(
                "Unknown tree type: '" + treeType + "'. "
                "Supported types: jr, crr, eqp, trigeorgis, tian, lr, joshi");
        }
    }
}

void ql_pricingengines::binomialbarrierengine(py::module_& m) {
    m.def("BinomialBarrierEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& treeType,
           Size timeSteps,
           Size maxTimeSteps,
           const std::string& discretization) -> ext::shared_ptr<PricingEngine> {

            std::string lowerTree = to_lower(treeType);
            std::string lowerDisc = to_lower(discretization);

            if (lowerDisc == "dermankani") {
                return make_engine<DiscretizedDermanKaniBarrierOption>(
                    process, lowerTree, timeSteps, maxTimeSteps);
            } else {
                return make_engine<DiscretizedBarrierOption>(
                    process, lowerTree, timeSteps, maxTimeSteps);
            }
        },
        py::arg("process"),
        py::arg("treeType"),
        py::arg("timeSteps"),
        py::arg("maxTimeSteps") = 0,
        py::arg("discretization") = "default",
        "Binomial tree barrier option engine.\n\n"
        "Parameters:\n"
        "  treeType: jr, crr, eqp, trigeorgis, tian, lr, joshi\n"
        "  discretization: 'default' or 'dermankani'");
}
