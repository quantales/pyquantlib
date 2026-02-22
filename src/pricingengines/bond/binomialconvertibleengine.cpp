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
#include <ql/pricingengines/bond/binomialconvertibleengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/cashflows/dividend.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
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

void ql_pricingengines::binomialconvertibleengine(py::module_& m) {
    // Hidden handle: shared_ptr<Quote> creditSpread
    m.def("BinomialConvertibleEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& treeType,
           Size timeSteps,
           const ext::shared_ptr<Quote>& creditSpread,
           const DividendSchedule& dividends) -> ext::shared_ptr<PricingEngine> {

            Handle<Quote> csHandle(creditSpread);
            std::string lowerType = to_lower(treeType);

            if (lowerType == "jr" || lowerType == "jarrowrudd") {
                return ext::make_shared<BinomialConvertibleEngine<JarrowRudd>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "crr" || lowerType == "coxrossrubinstein") {
                return ext::make_shared<BinomialConvertibleEngine<CoxRossRubinstein>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "eqp" || lowerType == "additiveeqp") {
                return ext::make_shared<BinomialConvertibleEngine<AdditiveEQPBinomialTree>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "trigeorgis") {
                return ext::make_shared<BinomialConvertibleEngine<Trigeorgis>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "tian") {
                return ext::make_shared<BinomialConvertibleEngine<Tian>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "lr" || lowerType == "leisenreimer") {
                return ext::make_shared<BinomialConvertibleEngine<LeisenReimer>>(
                    process, timeSteps, csHandle, dividends);
            } else if (lowerType == "joshi" || lowerType == "joshi4") {
                return ext::make_shared<BinomialConvertibleEngine<Joshi4>>(
                    process, timeSteps, csHandle, dividends);
            } else {
                throw std::runtime_error(
                    "Unknown tree type: '" + treeType + "'. "
                    "Supported types: jr, crr, eqp, trigeorgis, tian, lr, joshi");
            }
        },
        py::arg("process"),
        py::arg("treeType"),
        py::arg("timeSteps"),
        py::arg("creditSpread"),
        py::arg("dividends") = DividendSchedule(),
        "Binomial Tsiveriotis-Fernandes engine for convertible bonds.\n\n"
        "Parameters:\n"
        "  process: Black-Scholes process for the underlying equity\n"
        "  treeType: Tree type - one of:\n"
        "    'jr' or 'jarrowrudd': Jarrow-Rudd\n"
        "    'crr' or 'coxrossrubinstein': Cox-Ross-Rubinstein\n"
        "    'eqp' or 'additiveeqp': Additive equal probabilities\n"
        "    'trigeorgis': Trigeorgis\n"
        "    'tian': Tian\n"
        "    'lr' or 'leisenreimer': Leisen-Reimer\n"
        "    'joshi' or 'joshi4': Joshi\n"
        "  timeSteps: Number of time steps\n"
        "  creditSpread: Credit spread quote\n"
        "  dividends: Dividend schedule (optional)");

    // Handle<Quote> version
    m.def("BinomialConvertibleEngine",
        [](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
           const std::string& treeType,
           Size timeSteps,
           const Handle<Quote>& creditSpread,
           const DividendSchedule& dividends) -> ext::shared_ptr<PricingEngine> {

            std::string lowerType = to_lower(treeType);

            if (lowerType == "jr" || lowerType == "jarrowrudd") {
                return ext::make_shared<BinomialConvertibleEngine<JarrowRudd>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "crr" || lowerType == "coxrossrubinstein") {
                return ext::make_shared<BinomialConvertibleEngine<CoxRossRubinstein>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "eqp" || lowerType == "additiveeqp") {
                return ext::make_shared<BinomialConvertibleEngine<AdditiveEQPBinomialTree>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "trigeorgis") {
                return ext::make_shared<BinomialConvertibleEngine<Trigeorgis>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "tian") {
                return ext::make_shared<BinomialConvertibleEngine<Tian>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "lr" || lowerType == "leisenreimer") {
                return ext::make_shared<BinomialConvertibleEngine<LeisenReimer>>(
                    process, timeSteps, creditSpread, dividends);
            } else if (lowerType == "joshi" || lowerType == "joshi4") {
                return ext::make_shared<BinomialConvertibleEngine<Joshi4>>(
                    process, timeSteps, creditSpread, dividends);
            } else {
                throw std::runtime_error(
                    "Unknown tree type: '" + treeType + "'. "
                    "Supported types: jr, crr, eqp, trigeorgis, tian, lr, joshi");
            }
        },
        py::arg("process"),
        py::arg("treeType"),
        py::arg("timeSteps"),
        py::arg("creditSpread"),
        py::arg("dividends") = DividendSchedule(),
        "Binomial Tsiveriotis-Fernandes engine for convertible bonds (Handle version).");
}
