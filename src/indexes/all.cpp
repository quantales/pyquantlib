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
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(indexes_bindings) {
    ADD_BASE_BINDING(ql_indexes::interestrateindex, "InterestRateIndex ABC");
    ADD_MAIN_BINDING(ql_indexes::iborindex, "IborIndex - IBOR index base class");
    ADD_MAIN_BINDING(ql_indexes::euribor, "Euribor - Euribor indexes");
    ADD_MAIN_BINDING(ql_indexes::sofr, "Sofr - SOFR overnight index");
    ADD_MAIN_BINDING(ql_indexes::eonia, "Eonia - EONIA overnight index");
    ADD_MAIN_BINDING(ql_indexes::estr, "Estr - ESTR overnight index");
    ADD_MAIN_BINDING(ql_indexes::sonia, "Sonia - SONIA overnight index");
    ADD_MAIN_BINDING(ql_indexes::swapindex,
        "SwapIndex, OvernightIndexedSwapIndex");
    ADD_MAIN_BINDING(ql_indexes::swapindexes,
        "Concrete swap index subclasses (Euribor/Libor swap rates)");
    // Inflation indexes
    ADD_MAIN_BINDING(ql_indexes::region, "Region - geographic region");
    ADD_BASE_BINDING(ql_indexes::inflationindex, "InflationIndex ABC");
    ADD_MAIN_BINDING(ql_indexes::cpi, "CPI interpolation enum and utilities");
    ADD_MAIN_BINDING(ql_indexes::zeroinflationindex, "ZeroInflationIndex");
    ADD_MAIN_BINDING(ql_indexes::yoyinflationindex, "YoYInflationIndex");
    ADD_MAIN_BINDING(ql_indexes::ukrpi, "UKRPI, YYUKRPI");
    ADD_MAIN_BINDING(ql_indexes::euhicp,
        "EUHICP, EUHICPXT, YYEUHICP, YYEUHICPXT");
    ADD_MAIN_BINDING(ql_indexes::uscpi, "USCPI, YYUSCPI");
    ADD_MAIN_BINDING(ql_indexes::aucpi, "AUCPI, YYAUCPI");
    ADD_MAIN_BINDING(ql_indexes::frhicp, "FRHICP, YYFRHICP");
    ADD_MAIN_BINDING(ql_indexes::zacpi, "ZACPI, YYZACPI");
    // Equity
    ADD_MAIN_BINDING(ql_indexes::equityindex,
        "EquityIndex - equity index base class");
}
