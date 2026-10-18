/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(indexes_bindings) {
    ADD_BASE_BINDING(ql_indexes::interestrateindex, "InterestRateIndex ABC");
    ADD_MAIN_BINDING(ql_indexes::iborindex, "IborIndex - IBOR index base class");
    ADD_MAIN_BINDING(ql_indexes::euribor, "Euribor - Euribor indexes");
    ADD_MAIN_BINDING(ql_indexes::libor, "Libor, DailyTenorLibor - ICE LIBOR bases");
    ADD_MAIN_BINDING(ql_indexes::usdlibor, "USDLibor, DailyTenorUSDLibor, USDLiborON");
    ADD_MAIN_BINDING(ql_indexes::sofr, "Sofr - SOFR overnight index");
    ADD_MAIN_BINDING(ql_indexes::eonia, "Eonia - EONIA overnight index");
    ADD_MAIN_BINDING(ql_indexes::estr, "Estr - ESTR overnight index");
    ADD_MAIN_BINDING(ql_indexes::sonia, "Sonia - SONIA overnight index");
    ADD_MAIN_BINDING(ql_indexes::nibor, "Nibor - NOK-NIBOR index");
    ADD_MAIN_BINDING(ql_indexes::shir, "Shir - SHIR overnight index");
    ADD_MAIN_BINDING(ql_indexes::zaronia, "Zaronia - ZARONIA overnight index");
    ADD_MAIN_BINDING(ql_indexes::aonia, "Aonia index");
    ADD_MAIN_BINDING(ql_indexes::bbsw, "Bbsw family index");
    ADD_MAIN_BINDING(ql_indexes::bibor, "Bibor family index");
    ADD_MAIN_BINDING(ql_indexes::bkbm, "Bkbm family index");
    ADD_MAIN_BINDING(ql_indexes::cdi, "Cdi index");
    ADD_MAIN_BINDING(ql_indexes::cdor, "Cdor index");
    ADD_MAIN_BINDING(ql_indexes::corra, "Corra index");
    ADD_MAIN_BINDING(ql_indexes::destr, "Destr index");
    ADD_MAIN_BINDING(ql_indexes::fedfunds, "FedFunds index");
    ADD_MAIN_BINDING(ql_indexes::jibar, "Jibar index");
    ADD_MAIN_BINDING(ql_indexes::kofr, "Kofr index");
    ADD_MAIN_BINDING(ql_indexes::nzocr, "Nzocr index");
    ADD_MAIN_BINDING(ql_indexes::robor, "Robor index");
    ADD_MAIN_BINDING(ql_indexes::saron, "Saron index");
    ADD_MAIN_BINDING(ql_indexes::shibor, "Shibor index");
    ADD_MAIN_BINDING(ql_indexes::swestr, "Swestr index");
    ADD_MAIN_BINDING(ql_indexes::tonar, "Tonar index");
    ADD_MAIN_BINDING(ql_indexes::zibor, "Zibor index");
    ADD_MAIN_BINDING(ql_indexes::swapindex,
        "SwapIndex, OvernightIndexedSwapIndex");
    ADD_MAIN_BINDING(ql_indexes::swapindexes,
        "Concrete swap index subclasses (Euribor/Libor swap rates)");

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

    ADD_MAIN_BINDING(ql_indexes::equityindex,
        "EquityIndex - equity index base class");

    ADD_MAIN_BINDING(ql_indexes::bmaindex,
        "BMAIndex - Bond Market Association index");
    ADD_MAIN_BINDING(ql_indexes::swapspreadindex,
        "SwapSpreadIndex - spread between two swap rates");
}
