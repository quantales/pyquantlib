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
#include <ql/time/calendars/all.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;


void ql_time::calendars(py::module_& m)
{
    auto pyClassArgentina =
        py::class_<QuantLib::Argentina, QuantLib::Calendar, ext::shared_ptr<QuantLib::Argentina>>
            (m, "Argentina", "! Holidays for the Buenos Aires stock exchange\n        (data from <http://www.merval.sba.com.ar/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Holy Thursday</li>\n        <li>Good Friday</li>\n        <li>Labour Day, May 1st</li>\n        <li>May Revolution, May 25th</li>\n        <li>Death of General Manuel Belgrano, third Monday of June</li>\n        <li>Independence Day, July 9th</li>\n        <li>Death of General Jos� de San Mart�n, third Monday of August</li>\n        <li>Columbus Day, October 12th (moved to preceding Monday if\n            on Tuesday or Wednesday and to following if on Thursday\n            or Friday)</li>\n        <li>Immaculate Conception, December 8th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>New Year's Eve, December 31th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Argentina
        auto pyEnumMarket =
            py::enum_<QuantLib::Argentina::Market>(pyClassArgentina, "Market", py::arithmetic(), "")
                .value("Merval", QuantLib::Argentina::Merval, "!< Buenos Aires stock exchange calendar")
            .export_values();
    } // end of inner classes & enums of Argentina

    pyClassArgentina
        .def(py::init<QuantLib::Argentina::Market>(),
            py::arg("m") = QuantLib::Argentina::Merval)
        ;


    auto pyClassAustralia =
        py::class_<QuantLib::Australia, QuantLib::Calendar, ext::shared_ptr<QuantLib::Australia>>
            (m, "Australia", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Australia Day, January 26th (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>ANZAC Day. April 25th (possibly moved to Monday)</li>\n        <li>Queen's Birthday, second Monday in June</li>\n        <li>Bank Holiday, first Monday in August</li>\n        <li>Labour Day, first Monday in October</li>\n        <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        <li>National Day of Mourning for Her Majesty, September 22, 2022</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Australia
        auto pyEnumMarket =
            py::enum_<QuantLib::Australia::Market>(pyClassAustralia, "Market", py::arithmetic(), "")
                .value("Settlement", QuantLib::Australia::Settlement, "!< generic settlement calendar")
                .value("ASX", QuantLib::Australia::ASX, "!< Australia ASX calendar")
            .export_values();
    } // end of inner classes & enums of Australia

    pyClassAustralia
        .def(py::init<QuantLib::Australia::Market>(),
            py::arg("market") = QuantLib::Australia::Settlement)
        ;


    auto pyClassAustria =
        py::class_<QuantLib::Austria, QuantLib::Calendar, ext::shared_ptr<QuantLib::Austria>>
            (m, "Austria", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th</li>\n        <li>Easter Monday</li>\n        <li>Ascension Thursday</li>\n        <li>Whit Monday</li>\n        <li>Corpus Christi</li>\n        <li>Labour Day, May 1st</li>\n        <li>Assumption Day, August 15th</li>\n        <li>National Holiday, October 26th, since 1967</li>\n        <li>All Saints Day, November 1st</li>\n        <li>National Holiday, November 12th, 1919-1934</li>\n        <li>Immaculate Conception Day, December 8th</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen, December 26th</li>\n        </ul>\n\n        Holidays for the stock exchange (data from https://www.wienerborse.at/en/trading/trading-information/trading-calendar/):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Whit Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>National Holiday, October 26th, since 1967</li>\n        <li>National Holiday, November 12th, 1919-1934</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen, December 26th</li>\n        <li>Exchange Holiday</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Austria
        auto pyEnumMarket =
            py::enum_<QuantLib::Austria::Market>(pyClassAustria, "Market", py::arithmetic(), "! Austrian calendars")
                .value("Settlement", QuantLib::Austria::Settlement, "!< generic settlement calendar")
                .value("Exchange", QuantLib::Austria::Exchange, "!< Vienna stock-exchange calendar")
            .export_values();
    } // end of inner classes & enums of Austria

    pyClassAustria
        .def(py::init<>()) // implicit default constructor
        ;


    auto pyClassBespokeCalendar =
        py::class_<QuantLib::BespokeCalendar, QuantLib::Calendar, ext::shared_ptr<QuantLib::BespokeCalendar>>
            (m, "BespokeCalendar", "! This calendar has no predefined set of business days. Holidays\n        and weekdays can be defined by means of the provided\n        interface. Instances constructed by copying remain linked to\n        the original one; adding a new holiday or weekday will affect\n        all linked instances.\n\n        \\ingroup calendars\n")
        .def(py::init<const std::string &>(),
            py::arg("name") = "")
        .def("addWeekend",
            &QuantLib::BespokeCalendar::addWeekend,
            py::arg("param_0"),
            "! marks the passed day as part of the weekend")
        ;


    auto pyClassBotswana =
        py::class_<QuantLib::Botswana, QuantLib::Calendar, ext::shared_ptr<QuantLib::Botswana>>
            (m, "Botswana", "! Holidays:\n    From the Botswana <a href=\"http://www.ilo.org/dyn/travail/docs/1766/Public%20Holidays%20Act.pdf\">Public Holidays Act</a>\n    The days named in the Schedule shall be public holidays within Botswana:\n    Provided that\n    <ul>\n    <li>when any of the said days fall on a Sunday the following Monday shall be observed as a public holiday;</li>\n    <li>if 2nd January, 1st October or Boxing Day falls on a Monday, the following Tuesday shall be observed as a public holiday;</li>\n    <li>when Botswana Day referred to in the Schedule falls on a Saturday, the next following Monday shall be observed as a public holiday.</li>\n    </ul>\n    <ul>\n    <li>Saturdays</li>\n    <li>Sundays</li>\n    <li>New Year's Day, January 1st</li>\n    <li>Good Friday</li>\n    <li>Easter Monday</li>\n    <li>Labour Day, May 1st</li>\n    <li>Ascension</li>\n    <li>Sir Seretse Khama Day, July 1st</li>\n    <li>Presidents' Day</li>\n    <li>Independence Day, September 30th</li>\n    <li>Botswana Day, October 1st</li>\n    <li>Christmas, December 25th </li>\n    <li>Boxing Day, December 26th</li>\n    </ul>\n\n    \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassBrazil =
        py::class_<QuantLib::Brazil, QuantLib::Calendar, ext::shared_ptr<QuantLib::Brazil>>
            (m, "Brazil", "! Banking holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Tiradentes's Day, April 21th</li>\n        <li>Labour Day, May 1st</li>\n        <li>Independence Day, September 7th</li>\n        <li>Nossa Sra. Aparecida Day, October 12th</li>\n        <li>All Souls Day, November 2nd</li>\n        <li>Republic Day, November 15th</li>\n        <li>Black Awareness Day, November 20th (since 2024)</li>\n        <li>Christmas, December 25th</li>\n        <li>Passion of Christ</li>\n        <li>Carnival</li>\n        <li>Corpus Christi</li>\n        </ul>\n\n        Holidays for the Bovespa stock exchange\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Sao Paulo City Day, January 25th (up to 2021 included)</li>\n        <li>Tiradentes's Day, April 21th</li>\n        <li>Labour Day, May 1st</li>\n        <li>Revolution Day, July 9th (up to 2021 included)</li>\n        <li>Independence Day, September 7th</li>\n        <li>Nossa Sra. Aparecida Day, October 12th</li>\n        <li>All Souls Day, November 2nd</li>\n        <li>Republic Day, November 15th</li>\n        <li>Black Consciousness Day, November 20th (since 2007, except 2022 and 2023)</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Passion of Christ</li>\n        <li>Carnival</li>\n        <li>Corpus Christi</li>\n        <li>the last business day of the year</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n");

    { // inner classes & enums of Brazil
        auto pyEnumMarket =
            py::enum_<QuantLib::Brazil::Market>(pyClassBrazil, "Market", py::arithmetic(), "! Brazilian calendars")
                .value("Settlement", QuantLib::Brazil::Settlement, "!< generic settlement calendar")
                .value("Exchange", QuantLib::Brazil::Exchange, "!< BOVESPA calendar")
            .export_values();
    } // end of inner classes & enums of Brazil

    pyClassBrazil
        .def(py::init<QuantLib::Brazil::Market>(),
            py::arg("market") = QuantLib::Brazil::Settlement)
        ;


    auto pyClassCanada =
        py::class_<QuantLib::Canada, QuantLib::Calendar, ext::shared_ptr<QuantLib::Canada>>
            (m, "Canada", "! Banking holidays\n        (data from <http://www.bankofcanada.ca/en/about/holiday.html>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Family Day, third Monday of February (since 2008)</li>\n        <li>Good Friday</li>\n        <li>Victoria Day, the Monday on or preceding May 24th</li>\n        <li>Canada Day, July 1st (possibly moved to Monday)</li>\n        <li>Provincial Holiday, first Monday of August</li>\n        <li>Labour Day, first Monday of September</li>\n        <li>National Day for Truth and Reconciliation, September 30th (possibly moved to Monday)</li>\n        <li>Thanksgiving Day, second Monday of October</li>\n        <li>Remembrance Day, November 11th (possibly moved to Monday)</li>\n        <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        </ul>\n\n        Holidays for the Toronto stock exchange\n        (data from <http://www.tsx.com/en/about_tsx/market_hours.html>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Family Day, third Monday of February (since 2008)</li>\n        <li>Good Friday</li>\n        <li>Victoria Day, the Monday on or preceding May 24th</li>\n        <li>Canada Day, July 1st (possibly moved to Monday)</li>\n        <li>Provincial Holiday, first Monday of August</li>\n        <li>Labour Day, first Monday of September</li>\n        <li>Thanksgiving Day, second Monday of October</li>\n        <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Canada
        auto pyEnumMarket =
            py::enum_<QuantLib::Canada::Market>(pyClassCanada, "Market", py::arithmetic(), "")
                .value("Settlement", QuantLib::Canada::Settlement, "!< generic settlement calendar")
                .value("TSX", QuantLib::Canada::TSX, "!< Toronto stock exchange calendar")
            .export_values();
    } // end of inner classes & enums of Canada

    pyClassCanada
        .def(py::init<QuantLib::Canada::Market>(),
            py::arg("market") = QuantLib::Canada::Settlement)
        ;


    auto pyClassChile =
        py::class_<QuantLib::Chile, QuantLib::Calendar, ext::shared_ptr<QuantLib::Chile>>
            (m, "Chile", "! Holidays for the Santiago Stock Exchange\n        (data from <https://en.wikipedia.org/wiki/Public_holidays_in_Chile>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>January 2nd, when falling on a Monday (since 2017)</li>\n        <li>Good Friday</li>\n        <li>Easter Saturday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Navy Day, May 21st</li>\n        <li>Day of Aboriginal People, around June 21st (observed on each Winter Solstice) (since 2021)</li>\n        <li>Saint Peter and Saint Paul, June 29th (moved to the nearest Monday if it falls on a weekday)</li>\n        <li>Our Lady of Mount Carmel, July 16th</li>\n        <li>Assumption Day, August 15th</li>\n        <li>Independence Day, September 18th (also the 17th if the latter falls on a Monday or Friday)</li>\n        <li>Army Day, September 19th (also the 20th if the latter falls on a Friday)</li>\n        <li>Discovery of Two Worlds, October 12th (moved to the nearest Monday if it falls on a weekday)</li>\n        <li>Reformation Day, October 31st (since 2008; moved to the preceding Friday if it falls on a Tuesday,\n            or to the following Friday if it falls on a Wednesday)</li>\n        <li>All Saints' Day, November 1st</li>\n        <li>Immaculate Conception, December 8th</li>\n        <li>Christmas Day, December 25th</li>\n        <li>New Year's Eve, December 31st; (see https://www.cmfchile.cl/portal/prensa/615/w3-article-49984.html)</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Chile
        auto pyEnumMarket =
            py::enum_<QuantLib::Chile::Market>(pyClassChile, "Market", py::arithmetic(), "")
                .value("SSE", QuantLib::Chile::SSE, "!< Santiago Stock Exchange")
            .export_values();
    } // end of inner classes & enums of Chile

    pyClassChile
        .def(py::init<QuantLib::Chile::Market>(),
            py::arg("m") = QuantLib::Chile::SSE)
        ;


    auto pyClassChina =
        py::class_<QuantLib::China, QuantLib::Calendar, ext::shared_ptr<QuantLib::China>>
            (m, "China", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's day, January 1st (possibly followed by one or\n            two more holidays)</li>\n        <li>Labour Day, first week in May</li>\n        <li>National Day, one week from October 1st</li>\n        </ul>\n\n        Other holidays for which no rule is given (data available for\n        2004-2019 only):\n        <ul>\n        <li>Chinese New Year</li>\n        <li>Ching Ming Festival</li>\n        <li>Tuen Ng Festival</li>\n        <li>Mid-Autumn Festival</li>\n        <li>70th anniversary of the victory of anti-Japaneses war</li>\n        </ul>\n\n        SSE data from <http://www.sse.com.cn/>\n        IB data from <http://www.chinamoney.com.cn/>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of China
        auto pyEnumMarket =
            py::enum_<QuantLib::China::Market>(pyClassChina, "Market", py::arithmetic(), "")
                .value("SSE", QuantLib::China::SSE, "!< Shanghai stock exchange")
                .value("IB", QuantLib::China::IB, "!< Interbank calendar")
            .export_values();
    } // end of inner classes & enums of China

    pyClassChina
        .def(py::init<QuantLib::China::Market>(),
            py::arg("m") = QuantLib::China::SSE)
        ;


    auto pyClassCzechRepublic =
        py::class_<QuantLib::CzechRepublic, QuantLib::Calendar, ext::shared_ptr<QuantLib::CzechRepublic>>
            (m, "CzechRepublic", "! Holidays for the Prague stock exchange (see http://www.pse.cz/):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Liberation Day, May 8th</li>\n        <li>SS. Cyril and Methodius, July 5th</li>\n        <li>Jan Hus Day, July 6th</li>\n        <li>Czech Statehood Day, September 28th</li>\n        <li>Independence Day, October 28th</li>\n        <li>Struggle for Freedom and Democracy Day, November 17th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of CzechRepublic
        auto pyEnumMarket =
            py::enum_<QuantLib::CzechRepublic::Market>(pyClassCzechRepublic, "Market", py::arithmetic(), "")
                .value("PSE", QuantLib::CzechRepublic::PSE, "!< Prague stock exchange")
            .export_values();
    } // end of inner classes & enums of CzechRepublic

    pyClassCzechRepublic
        .def(py::init<QuantLib::CzechRepublic::Market>(),
            py::arg("m") = QuantLib::CzechRepublic::PSE)
        ;


    auto pyClassDenmark =
        py::class_<QuantLib::Denmark, QuantLib::Calendar, ext::shared_ptr<QuantLib::Denmark>>
            (m, "Denmark", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Maunday Thursday</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>General Prayer Day, 25 days after Easter Monday (up until 2023)</li>\n        <li>Ascension</li>\n        <li>Day after Ascension (from 2009)</li>\n        <li>Whit (Pentecost) Monday </li>\n        <li>New Year's Day, January 1st</li>\n        <li>Constitution Day, June 5th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        <li>New Year's Eve, December 31st</li>\n        </ul>\n\n        See: https://www.nasdaqomxnordic.com/tradinghours,\n        and: https://www.nationalbanken.dk/da/Kontakt/aabningstider/Sider/default.aspx\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassFinland =
        py::class_<QuantLib::Finland, QuantLib::Calendar, ext::shared_ptr<QuantLib::Finland>>
            (m, "Finland", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Ascension Thursday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Midsummer Eve (Friday between June 19-25)</li>\n        <li>Independence Day, December 6th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassFrance =
        py::class_<QuantLib::France, QuantLib::Calendar, ext::shared_ptr<QuantLib::France>>
            (m, "France", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Armistice 1945, May 8th</li>\n        <li>Ascension, May 10th</li>\n        <li>Pentec�te, May 21st</li>\n        <li>F�te nationale, July 14th</li>\n        <li>Assumption, August 15th</li>\n        <li>All Saint's Day, November 1st</li>\n        <li>Armistice 1918, November 11th</li>\n        <li>Christmas Day, December 25th</li>\n        </ul>\n\n        Holidays for the stock exchange (data from https://www.stockmarketclock.com/exchanges/euronext-paris/market-holidays/):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas Day, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        <li>New Year's Eve, December 31st</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of France
        auto pyEnumMarket =
            py::enum_<QuantLib::France::Market>(pyClassFrance, "Market", py::arithmetic(), "! French calendars")
                .value("Settlement", QuantLib::France::Settlement, "!< generic settlement calendar")
                .value("Exchange", QuantLib::France::Exchange, "!< Paris stock-exchange calendar")
            .export_values();
    } // end of inner classes & enums of France

    pyClassFrance
        .def(py::init<>()) // implicit default constructor
        ;


    auto pyClassGermany =
        py::class_<QuantLib::Germany, QuantLib::Calendar, ext::shared_ptr<QuantLib::Germany>>
            (m, "Germany", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Ascension Thursday</li>\n        <li>Whit Monday</li>\n        <li>Corpus Christi</li>\n        <li>Labour Day, May 1st</li>\n        <li>National Day, October 3rd</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        </ul>\n\n        Holidays for the Frankfurt Stock exchange\n        (data from http://deutsche-boerse.com/):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Christmas' Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Christmas Holiday, December 26th</li>\n        </ul>\n\n        Holidays for the Xetra exchange\n        (data from http://deutsche-boerse.com/):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Christmas' Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Christmas Holiday, December 26th</li>\n        </ul>\n\n        Holidays for the Eurex exchange\n        (data from http://www.eurexchange.com/index.html):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Christmas' Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Christmas Holiday, December 26th</li>\n        <li>New Year's Eve, December 31st</li>\n        </ul>\n\n        Holidays for the Euwax exchange\n        (data from http://www.boerse-stuttgart.de):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Whit Monday</li>\n        <li>Christmas' Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Christmas Holiday, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n");

    { // inner classes & enums of Germany
        auto pyEnumMarket =
            py::enum_<QuantLib::Germany::Market>(pyClassGermany, "Market", py::arithmetic(), "! German calendars")
                .value("Settlement", QuantLib::Germany::Settlement, "!< generic settlement calendar")
                .value("FrankfurtStockExchange", QuantLib::Germany::FrankfurtStockExchange, "!< Frankfurt stock-exchange")
                .value("Xetra", QuantLib::Germany::Xetra, "!< Xetra")
                .value("Eurex", QuantLib::Germany::Eurex, "!< Eurex")
                .value("Euwax", QuantLib::Germany::Euwax, "!< Euwax")
            .export_values();
    } // end of inner classes & enums of Germany

    pyClassGermany
        .def(py::init<QuantLib::Germany::Market>(),
            py::arg("market") = QuantLib::Germany::FrankfurtStockExchange)
        ;


    auto pyClassHongKong =
        py::class_<QuantLib::HongKong, QuantLib::Calendar, ext::shared_ptr<QuantLib::HongKong>>
            (m, "HongKong", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labor Day, May 1st (possibly moved to Monday)</li>\n        <li>SAR Establishment Day, July 1st (possibly moved to Monday)</li>\n        <li>National Day, October 1st (possibly moved to Monday)</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2004-2015 only:)\n        <ul>\n        <li>Lunar New Year</li>\n        <li>Chinese New Year</li>\n        <li>Ching Ming Festival</li>\n        <li>Buddha's birthday</li>\n        <li>Tuen NG Festival</li>\n        <li>Mid-autumn Festival</li>\n        <li>Chung Yeung Festival</li>\n        </ul>\n\n        Data from <http://www.hkex.com.hk>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of HongKong
        auto pyEnumMarket =
            py::enum_<QuantLib::HongKong::Market>(pyClassHongKong, "Market", py::arithmetic(), "")
                .value("HKEx", QuantLib::HongKong::HKEx, "!< Hong Kong stock exchange")
            .export_values();
    } // end of inner classes & enums of HongKong

    pyClassHongKong
        .def(py::init<QuantLib::HongKong::Market>(),
            py::arg("m") = QuantLib::HongKong::HKEx)
        ;


    auto pyClassHungary =
        py::class_<QuantLib::Hungary, QuantLib::Calendar, ext::shared_ptr<QuantLib::Hungary>>
            (m, "Hungary", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Good Friday (since 2017)</li>\n        <li>Easter Monday</li>\n        <li>Whit(Pentecost) Monday </li>\n        <li>New Year's Day, January 1st</li>\n        <li>National Day, March 15th</li>\n        <li>Labour Day, May 1st</li>\n        <li>Constitution Day, August 20th</li>\n        <li>Republic Day, October 23rd</li>\n        <li>All Saints Day, November 1st</li>\n        <li>Christmas, December 25th</li>\n        <li>2nd Day of Christmas, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassIceland =
        py::class_<QuantLib::Iceland, QuantLib::Calendar, ext::shared_ptr<QuantLib::Iceland>>
            (m, "Iceland", "! Holidays for the Iceland stock exchange\n        (data from <http://www.icex.is/is/calendar?languageID=1>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Holy Thursday</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>First day of Summer (third or fourth Thursday in April)</li>\n        <li>Labour Day, May 1st</li>\n        <li>Ascension Thursday</li>\n        <li>Pentecost Monday</li>\n        <li>Independence Day, June 17th</li>\n        <li>Commerce Day, first Monday in August</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Iceland
        auto pyEnumMarket =
            py::enum_<QuantLib::Iceland::Market>(pyClassIceland, "Market", py::arithmetic(), "")
                .value("ICEX", QuantLib::Iceland::ICEX, "!< Iceland stock exchange")
            .export_values();
    } // end of inner classes & enums of Iceland

    pyClassIceland
        .def(py::init<QuantLib::Iceland::Market>(),
            py::arg("m") = QuantLib::Iceland::ICEX)
        ;


    auto pyClassIndia =
        py::class_<QuantLib::India, QuantLib::Calendar, ext::shared_ptr<QuantLib::India>>
            (m, "India", "! Clearing holidays for the National Stock Exchange\n        (data from <http://www.nse-india.com/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Republic Day, January 26th</li>\n        <li>Good Friday</li>\n        <li>Ambedkar Jayanti, April 14th</li>\n        <li>May Day, May 1st</li>\n        <li>Independence Day, August 15th</li>\n        <li>Gandhi Jayanti, October 2nd</li>\n        <li>Christmas, December 25th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2005-2014, 2019-2025 only:)\n        <ul>\n        <li>Bakri Id</li>\n        <li>Moharram</li>\n        <li>Mahashivratri</li>\n        <li>Holi</li>\n        <li>Ram Navami</li>\n        <li>Mahavir Jayanti</li>\n        <li>Id-E-Milad</li>\n        <li>Maharashtra Day</li>\n        <li>Buddha Pournima</li>\n        <li>Ganesh Chaturthi</li>\n        <li>Dasara</li>\n        <li>Laxmi Puja</li>\n        <li>Bhaubeej</li>\n        <li>Ramzan Id</li>\n        <li>Guru Nanak Jayanti</li>\n        </ul>\n\n        Note: The holidays Ramzan Id, Bakri Id and Id-E-Milad rely on estimates for 2024-2025.\n        \\ingroup calendars\n");

    { // inner classes & enums of India
        auto pyEnumMarket =
            py::enum_<QuantLib::India::Market>(pyClassIndia, "Market", py::arithmetic(), "")
                .value("NSE", QuantLib::India::NSE, "!< National Stock Exchange")
            .export_values();
    } // end of inner classes & enums of India

    pyClassIndia
        .def(py::init<QuantLib::India::Market>(),
            py::arg("m") = QuantLib::India::NSE)
        ;


    auto pyClassIndonesia =
        py::class_<QuantLib::Indonesia, QuantLib::Calendar, ext::shared_ptr<QuantLib::Indonesia>>
            (m, "Indonesia", "! Holidays for the Indonesia stock exchange\n        (data from <http://www.idx.co.id/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Ascension of Jesus Christ</li>\n        <li>Independence Day, August 17th</li>\n        <li>Christmas, December 25th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2005-2014 only:)\n        <ul>\n        <li>Idul Adha</li>\n        <li>Ied Adha</li>\n        <li>Imlek</li>\n        <li>Moslem's New Year Day</li>\n        <li>Chinese New Year</li>\n        <li>Nyepi (Saka's New Year)</li>\n        <li>Birthday of Prophet Muhammad SAW</li>\n        <li>Waisak</li>\n        <li>Ascension of Prophet Muhammad SAW</li>\n        <li>Idul Fitri</li>\n        <li>Ied Fitri</li>\n        <li>Other national leaves</li>\n        </ul>\n        \\ingroup calendars\n");

    { // inner classes & enums of Indonesia
        auto pyEnumMarket =
            py::enum_<QuantLib::Indonesia::Market>(pyClassIndonesia, "Market", py::arithmetic(), "")
                .value("BEJ", QuantLib::Indonesia::BEJ, "!< Jakarta stock exchange (merged into IDX)")
                .value("JSX", QuantLib::Indonesia::JSX, "!< Jakarta stock exchange (merged into IDX)")
                .value("IDX", QuantLib::Indonesia::IDX, "!< Indonesia stock exchange")
            .export_values();
    } // end of inner classes & enums of Indonesia

    pyClassIndonesia
        .def(py::init<QuantLib::Indonesia::Market>(),
            py::arg("m") = QuantLib::Indonesia::IDX)
        ;


    auto pyClassIsrael =
        py::class_<QuantLib::Israel, QuantLib::Calendar, ext::shared_ptr<QuantLib::Israel>>
            (m, "Israel", "! Due to the lack of reliable sources, the settlement calendar\n        has the same holidays as the Tel Aviv stock-exchange.\n\n        Holidays for the Tel-Aviv Stock Exchange\n        (data from <http://www.tase.co.il>):\n        <ul>\n        <li>Friday</li>\n        <li>Saturday</li>\n        </ul>\n        Other holidays for wich no rule is given\n        (data available for 2013-2044 only:)\n        <ul>\n        <li>Purim, Adar 14th (between Feb 24th & Mar 26th)</li>\n        <li>Passover I, Nisan 15th (between Mar 26th & Apr 25th)</li>\n        <li>Passover VII, Nisan 21st (between Apr 1st & May 1st)</li>\n        <li>Memorial Day, Nisan 27th (between Apr 7th & May 7th)</li>\n        <li>Indipendence Day, Iyar 5th (between Apr 15th & May 15th)</li>\n        <li>Pentecost (Shavuot), Sivan 6th (between May 15th & June 14th)</li>\n        <li>Fast Day</li>\n        <li>Jewish New Year, Tishrei 1st & 2nd (between Sep 5th & Oct 5th)</li>\n        <li>Yom Kippur, Tishrei 10th (between Sep 14th & Oct 14th)</li>\n        <li>Sukkoth, Tishrei 15th (between Sep 19th & Oct 19th)</li>\n        <li>Simchat Tora, Tishrei 22nd (between Sep 26th & Oct 26th)</li>\n        </ul>\n\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Israel
        auto pyEnumMarket =
            py::enum_<QuantLib::Israel::Market>(pyClassIsrael, "Market", py::arithmetic(), "")
                .value("Settlement", QuantLib::Israel::Settlement, "!< generic settlement calendar")
                .value("TASE", QuantLib::Israel::TASE, "!< Tel-Aviv stock exchange calendar")
            .export_values();
    } // end of inner classes & enums of Israel

    pyClassIsrael
        .def(py::init<QuantLib::Israel::Market>(),
            py::arg("market") = QuantLib::Israel::Settlement)
        ;


    auto pyClassItaly =
        py::class_<QuantLib::Italy, QuantLib::Calendar, ext::shared_ptr<QuantLib::Italy>>
            (m, "Italy", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th</li>\n        <li>Easter Monday</li>\n        <li>Liberation Day, April 25th</li>\n        <li>Labour Day, May 1st</li>\n        <li>Republic Day, June 2nd (since 2000)</li>\n        <li>Assumption, August 15th</li>\n        <li>All Saint's Day, November 1st</li>\n        <li>Immaculate Conception Day, December 8th</li>\n        <li>Christmas Day, December 25th</li>\n        <li>St. Stephen's Day, December 26th</li>\n        </ul>\n\n        Holidays for the stock exchange (data from http://www.borsaitalia.it):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>Assumption, August 15th</li>\n        <li>Christmas' Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen, December 26th</li>\n        <li>New Year's Eve, December 31st</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested against a\n              list of known holidays.\n");

    { // inner classes & enums of Italy
        auto pyEnumMarket =
            py::enum_<QuantLib::Italy::Market>(pyClassItaly, "Market", py::arithmetic(), "! Italian calendars")
                .value("Settlement", QuantLib::Italy::Settlement, "!< generic settlement calendar")
                .value("Exchange", QuantLib::Italy::Exchange, "!< Milan stock-exchange calendar")
            .export_values();
    } // end of inner classes & enums of Italy

    pyClassItaly
        .def(py::init<QuantLib::Italy::Market>(),
            py::arg("market") = QuantLib::Italy::Settlement)
        ;


    auto pyClassJapan =
        py::class_<QuantLib::Japan, QuantLib::Calendar, ext::shared_ptr<QuantLib::Japan>>
            (m, "Japan", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Bank Holiday, January 2nd</li>\n        <li>Bank Holiday, January 3rd</li>\n        <li>Coming of Age Day, 2nd Monday in January</li>\n        <li>National Foundation Day, February 11th</li>\n        <li>Emperor's Birthday, February 23rd since 2020 and December 23rd before</li>\n        <li>Vernal Equinox</li>\n        <li>Greenery Day, April 29th</li>\n        <li>Constitution Memorial Day, May 3rd</li>\n        <li>Holiday for a Nation, May 4th</li>\n        <li>Children's Day, May 5th</li>\n        <li>Marine Day, 3rd Monday in July</li>\n        <li>Mountain Day, August 11th (from 2016 onwards)</li>\n        <li>Respect for the Aged Day, 3rd Monday in September</li>\n        <li>Autumnal Equinox</li>\n        <li>Health and Sports Day, 2nd Monday in October</li>\n        <li>National Culture Day, November 3rd</li>\n        <li>Labor Thanksgiving Day, November 23rd</li>\n        <li>Bank Holiday, December 31st</li>\n        <li>a few one-shot holidays</li>\n        </ul>\n        Holidays falling on a Sunday are observed on the Monday following\n        except for the bank holidays associated with the new year.\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyEnumJointCalendarRule =
        py::enum_<QuantLib::JointCalendarRule>(m, "JointCalendarRule", py::arithmetic(), "! rules for joining calendars")
            .value("JoinHolidays", QuantLib::JoinHolidays, "!< A date is a holiday\n                                                   for the joint calendar\n                                                   if it is a holiday\n                                                   for any of the given\n                                                   calendars")
            .value("JoinBusinessDays", QuantLib::JoinBusinessDays, "!< A date is a business day\n                                                   for the joint calendar\n                                                   if it is a business day\n                                                   for any of the given\n                                                   calendars")
        .export_values();


    auto pyClassJointCalendar =
        py::class_<QuantLib::JointCalendar, QuantLib::Calendar, ext::shared_ptr<QuantLib::JointCalendar>>
            (m, "JointCalendar", "! Depending on the chosen rule, this calendar has a set of\n        business days given by either the union or the intersection\n        of the sets of business days of the given calendars.\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested by\n              reproducing the calculations.\n")
        .def(py::init<const Calendar &, const Calendar &, QuantLib::JointCalendarRule>(),
            py::arg("param_0"), py::arg("param_1"), py::arg("param_2") = QuantLib::JoinHolidays)
        .def(py::init<const Calendar &, const Calendar &, const Calendar &, QuantLib::JointCalendarRule>(),
            py::arg("param_0"), py::arg("param_1"), py::arg("param_2"), py::arg("param_3") = QuantLib::JoinHolidays)
        .def(py::init<const Calendar &, const Calendar &, const Calendar &, const Calendar &, QuantLib::JointCalendarRule>(),
            py::arg("param_0"), py::arg("param_1"), py::arg("param_2"), py::arg("param_3"), py::arg("param_4") = QuantLib::JoinHolidays)

        // Bind using py::list
        .def(py::init([](const py::list& calendars, QuantLib::JointCalendarRule rule = QuantLib::JoinHolidays) {
                std::vector<QuantLib::Calendar> cals;
                cals.reserve(calendars.size());
                for (const auto& cal : calendars) {
                    cals.push_back(cal.cast<QuantLib::Calendar>());
                }
                return new QuantLib::JointCalendar(cals, rule);
            }), py::arg("calendars"), py::arg("rule") = QuantLib::JoinHolidays)            
        ;


    auto pyClassMexico =
        py::class_<QuantLib::Mexico, QuantLib::Calendar, ext::shared_ptr<QuantLib::Mexico>>
            (m, "Mexico", "! Holidays for the Mexican stock exchange\n        (data from <http://www.bmv.com.mx/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Constitution Day, first Monday in February\n            (February 5th before 2006)</li>\n        <li>Birthday of Benito Juarez, third Monday in February\n            (March 21st before 2006)</li>\n        <li>Holy Thursday</li>\n        <li>Good Friday</li>\n        <li>Labour Day, May 1st</li>\n        <li>National Day, September 16th</li>\n        <li>Inauguration Day, October 1st, every sixth year starting 2024</li>\n        <li>All Souls Day, November 2nd (bank holiday, not a public one)</li>\n        <li>Revolution Day, third Monday in November\n            (November 20th before 2006)</li>\n        <li>Our Lady of Guadalupe, December 12th</li>\n        <li>Christmas, December 25th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Mexico
        auto pyEnumMarket =
            py::enum_<QuantLib::Mexico::Market>(pyClassMexico, "Market", py::arithmetic(), "")
                .value("BMV", QuantLib::Mexico::BMV, "!< Mexican stock exchange")
            .export_values();
    } // end of inner classes & enums of Mexico

    pyClassMexico
        .def(py::init<QuantLib::Mexico::Market>(),
            py::arg("m") = QuantLib::Mexico::BMV)
        ;


    auto pyClassNewZealand =
        py::class_<QuantLib::NewZealand, QuantLib::Calendar, ext::shared_ptr<QuantLib::NewZealand>>
            (m, "NewZealand", "! Common holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday or Tuesday)</li>\n        <li>Day after New Year's Day, January 2st (possibly moved to Monday or Tuesday)</li>\n        <li>Waitangi Day. February 6th (possibly moved to Monday since 2013)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>ANZAC Day. April 25th (possibly moved to Monday since 2013)</li>\n        <li>Queen's Birthday, first Monday in June</li>\n        <li>Labour Day, fourth Monday in October</li>\n        <li>Christmas, December 25th (possibly moved to Monday or Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or Tuesday)</li>\n        <li>Matariki, in June or July, official calendar released for years 2022-2052</li>\n        </ul>\n\n        Additional holidays for Wellington:\n        <ul>\n        <li>Anniversary Day, Monday nearest January 22nd</li>\n        </ul>\n\n        Additional holidays for Auckland:\n        <ul>\n        <li>Anniversary Day, Monday nearest January 29nd</li>\n        </ul>\n\n        \note The holiday rules for New Zealand were documented by\n              David Gilbert for IDB (http://www.jrefinery.com/ibd/)\n              The Matariki holiday calendar has been released by the NZ Government\n              (https://www.legislation.govt.nz/act/public/2022/0014/latest/LMS557893.html)\n\n        \\ingroup calendars\n");

    { // inner classes & enums of NewZealand
        auto pyEnumMarket =
            py::enum_<QuantLib::NewZealand::Market>(pyClassNewZealand, "Market", py::arithmetic(), "! NZ calendars")
                .value("Wellington", QuantLib::NewZealand::Wellington, "")
                .value("Auckland", QuantLib::NewZealand::Auckland, "")
            .export_values();
    } // end of inner classes & enums of NewZealand

    pyClassNewZealand
        .def(py::init<>()) // implicit default constructor
        ;


    auto pyClassNorway =
        py::class_<QuantLib::Norway, QuantLib::Calendar, ext::shared_ptr<QuantLib::Norway>>
            (m, "Norway", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Holy Thursday</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Ascension</li>\n        <li>Whit(Pentecost) Monday </li>\n        <li>New Year's Day, January 1st</li>\n        <li>May Day, May 1st</li>\n        <li>National Independence Day, May 17th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassNullCalendar =
        py::class_<QuantLib::NullCalendar, QuantLib::Calendar, ext::shared_ptr<QuantLib::NullCalendar>>
            (m, "NullCalendar", "! This calendar has no holidays. It ensures that dates at\n        whole-month distances have the same day of month.\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassPoland =
        py::class_<QuantLib::Poland, QuantLib::Calendar, ext::shared_ptr<QuantLib::Poland>>
            (m, "Poland", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Easter Monday</li>\n        <li>Corpus Christi</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th (since 2011)</li>\n        <li>May Day, May 1st</li>\n        <li>Constitution Day, May 3rd</li>\n        <li>Assumption of the Blessed Virgin Mary, August 15th</li>\n        <li>All Saints Day, November 1st</li>\n        <li>Independence Day, November 11th</li>\n        <li>Christmas, December 25th</li>\n        <li>2nd Day of Christmas, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Poland
        auto pyEnumMarket =
            py::enum_<QuantLib::Poland::Market>(pyClassPoland, "Market", py::arithmetic(), "! PL calendars")
                .value("Settlement", QuantLib::Poland::Settlement, "!< Settlement calendar")
                .value("WSE", QuantLib::Poland::WSE, "!< Warsaw stock exchange calendar")
            .export_values();
    } // end of inner classes & enums of Poland

    pyClassPoland
        .def(py::init<>()) // implicit default constructor
        ;


    auto pyClassRomania =
        py::class_<QuantLib::Romania, QuantLib::Calendar, ext::shared_ptr<QuantLib::Romania>>
            (m, "Romania", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li> Day after New Year's Day, January 2nd</li>\n        <li>Unification Day, January 24th</li>\n        <li>Orthodox Easter (only Sunday and Monday)</li>\n        <li>Labour Day, May 1st</li>\n        <li>Pentecost with Monday (50th and 51st days after the\n            Othodox Easter)</li>\n        <li>Children's Day, June 1st (since 2017)</li>\n        <li>St Marys Day, August 15th</li>\n        <li>Feast of St Andrew, November 30th</li>\n        <li>National Day, December 1st</li>\n        <li>Christmas, December 25th</li>\n        <li>2nd Day of Christmas, December 26th</li>\n        </ul>\n\n        Holidays for the Bucharest stock exchange\n        (data from <http://www.bvb.ro/Marketplace/TradingCalendar/index.aspx>):\n        all public holidays, plus a few one-off closing days (2014 only).\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Romania
        auto pyEnumMarket =
            py::enum_<QuantLib::Romania::Market>(pyClassRomania, "Market", py::arithmetic(), "")
                .value("Public", QuantLib::Romania::Public, "!< Public holidays")
                .value("BVB", QuantLib::Romania::BVB, "!< Bucharest stock-exchange")
            .export_values();
    } // end of inner classes & enums of Romania

    pyClassRomania
        .def(py::init<QuantLib::Romania::Market>(),
            py::arg("market") = QuantLib::Romania::BVB)
        ;


    auto pyClassRussia =
        py::class_<QuantLib::Russia, QuantLib::Calendar, ext::shared_ptr<QuantLib::Russia>>
            (m, "Russia", "! Public holidays (see <http://www.cbr.ru/eng/>:):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year holidays, January 1st to 5th (only 1st and 2nd\n            until 2005)</li>\n        <li>Christmas, January 7th (possibly moved to Monday)</li>\n        <li>Defender of the Fatherland Day, February 23rd (possibly\n            moved to Monday)</li>\n        <li>International Women's Day, March 8th (possibly moved to\n            Monday)</li>\n        <li>Labour Day, May 1st (possibly moved to Monday)</li>\n        <li>Victory Day, May 9th (possibly moved to Monday)</li>\n        <li>Russia Day, June 12th (possibly moved to Monday)</li>\n        <li>Unity Day, November 4th (possibly moved to Monday)</li>\n        </ul>\n\n        Holidays for the Moscow Exchange (MOEX) taken from\n        <http://moex.com/s726> and related pages.  These holidays are\n        <em>not</em> consistent year-to-year, may or may not correlate\n        to public holidays, and are only available for dates since the\n        introduction of the MOEX 'brand' (a merger of the stock and\n        futures markets).\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Russia
        auto pyEnumMarket =
            py::enum_<QuantLib::Russia::Market>(pyClassRussia, "Market", py::arithmetic(), "! Russian calendars")
                .value("Settlement", QuantLib::Russia::Settlement, "!< generic settlement calendar")
                .value("MOEX", QuantLib::Russia::MOEX, "!< Moscow Exchange calendar")
            .export_values();
    } // end of inner classes & enums of Russia

    pyClassRussia
        .def(py::init<QuantLib::Russia::Market>(),
            py::arg("param_0") = QuantLib::Russia::Settlement)
        ;


    auto pyClassSaudiArabia =
        py::class_<QuantLib::SaudiArabia, QuantLib::Calendar, ext::shared_ptr<QuantLib::SaudiArabia>>
            (m, "SaudiArabia", "! Holidays for the Tadawul financial market\n        (data from <http://www.tadawul.com.sa>):\n        <ul>\n        <li>Thursdays</li>\n        <li>Fridays</li>\n        <li>National Day of Saudi Arabia, September 23rd</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available sparsely for 2004-2011 only:)\n        <ul>\n        <li>Eid Al-Adha</li>\n        <li>Eid Al-Fitr</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of SaudiArabia
        auto pyEnumMarket =
            py::enum_<QuantLib::SaudiArabia::Market>(pyClassSaudiArabia, "Market", py::arithmetic(), "")
                .value("Tadawul", QuantLib::SaudiArabia::Tadawul, "!< Tadawul financial market")
            .export_values();
    } // end of inner classes & enums of SaudiArabia

    pyClassSaudiArabia
        .def(py::init<QuantLib::SaudiArabia::Market>(),
            py::arg("m") = QuantLib::SaudiArabia::Tadawul)
        ;


    auto pyClassSingapore =
        py::class_<QuantLib::Singapore, QuantLib::Calendar, ext::shared_ptr<QuantLib::Singapore>>
            (m, "Singapore", "! Holidays for the Singapore exchange\n        (data from\n         <http://www.sgx.com/wps/portal/sgxweb/home/trading/securities/trading_hours_calendar>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's day, January 1st</li>\n        <li>Good Friday</li>\n        <li>Labour Day, May 1st</li>\n        <li>National Day, August 9th</li>\n        <li>Christmas, December 25th </li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2004-2010, 2012-2014, 2019-2024 only:)\n        <ul>\n        <li>Chinese New Year</li>\n        <li>Hari Raya Haji</li>\n        <li>Vesak Poya Day</li>\n        <li>Deepavali</li>\n        <li>Diwali</li>\n        <li>Hari Raya Puasa</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Singapore
        auto pyEnumMarket =
            py::enum_<QuantLib::Singapore::Market>(pyClassSingapore, "Market", py::arithmetic(), "")
                .value("SGX", QuantLib::Singapore::SGX, "!< Singapore exchange")
            .export_values();
    } // end of inner classes & enums of Singapore

    pyClassSingapore
        .def(py::init<QuantLib::Singapore::Market>(),
            py::arg("m") = QuantLib::Singapore::SGX)
        ;


    auto pyClassSlovakia =
        py::class_<QuantLib::Slovakia, QuantLib::Calendar, ext::shared_ptr<QuantLib::Slovakia>>
            (m, "Slovakia", "! Holidays for the Bratislava stock exchange\n        (data from <http://www.bsse.sk/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>May Day, May 1st</li>\n        <li>Liberation of the Republic, May 8th</li>\n        <li>SS. Cyril and Methodius, July 5th</li>\n        <li>Slovak National Uprising, August 29th</li>\n        <li>Constitution of the Slovak Republic, September 1st</li>\n        <li>Our Lady of the Seven Sorrows, September 15th</li>\n        <li>All Saints Day, November 1st</li>\n        <li>Freedom and Democracy of the Slovak Republic, November 17th</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Slovakia
        auto pyEnumMarket =
            py::enum_<QuantLib::Slovakia::Market>(pyClassSlovakia, "Market", py::arithmetic(), "")
                .value("BSSE", QuantLib::Slovakia::BSSE, "!< Bratislava stock exchange")
            .export_values();
    } // end of inner classes & enums of Slovakia

    pyClassSlovakia
        .def(py::init<QuantLib::Slovakia::Market>(),
            py::arg("m") = QuantLib::Slovakia::BSSE)
        ;


    auto pyClassSouthAfrica =
        py::class_<QuantLib::SouthAfrica, QuantLib::Calendar, ext::shared_ptr<QuantLib::SouthAfrica>>
            (m, "SouthAfrica", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Family Day, Easter Monday</li>\n        <li>Human Rights Day, March 21st (possibly moved to Monday)</li>\n        <li>Freedom Day, April 27th (possibly moved to Monday)</li>\n        <li>Workers Day, May 1st (possibly moved to Monday)</li>\n        <li>Youth Day, June 16th (possibly moved to Monday)</li>\n        <li>National Women's Day, August 9th\n        (possibly moved to Monday)</li>\n        <li>Heritage Day, September 24th (possibly moved to Monday)</li>\n        <li>Day of Reconciliation, December 16th\n        (possibly moved to Monday)</li>\n        <li>Christmas, December 25th </li>\n        <li>Day of Goodwill, December 26th (possibly moved to Monday)</li>\n        <li>Election Days</li>\n        </ul>\n\n        Note that there are some one-off holidays not listed above.\n        See the implementation for the complete list.\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassSouthKorea =
        py::class_<QuantLib::SouthKorea, QuantLib::Calendar, ext::shared_ptr<QuantLib::SouthKorea>>
            (m, "SouthKorea", "! Public holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Independence Day, March 1st</li>\n        <li>Arbour Day, April 5th (until 2005)</li>\n        <li>Labour Day, May 1st</li>\n        <li>Children's Day, May 5th</li>\n        <li>Memorial Day, June 6th</li>\n        <li>Constitution Day, July 17th (until 2007)</li>\n        <li>Liberation Day, August 15th</li>\n        <li>National Fondation Day, October 3th</li>\n        <li>Hangeul Day, October 9th (from 2013)</li>\n        <li>Christmas Day, December 25th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2004-2050 only:)\n        <ul>\n        <li>Lunar New Year, the last day of the previous lunar year</li>\n        <li>Election Days</li>\n        <li>National Assemblies</li>\n        <li>Presidency</li>\n        <li>Regional Election Days</li>\n        <li>Buddha's birthday</li>\n        <li>Harvest Moon Day</li>\n        </ul>\n\n        Holidays for the Korea exchange\n        (data from\n        <http://eng.krx.co.kr/> or\n        <http://www.dooriworld.com/daishin/holiday/holiday.html>\n        <https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B4%80%EA%B3%B5%EC%84%9C%EC%9D%98%20%EA%B3%B5%ED%9C%B4%EC%9D%BC%EC%97%90%20%EA%B4%80%ED%95%9C%20%EA%B7%9C%EC%A0%95>):\n        <ul>\n        <li>Public holidays as listed above</li>\n        <li>Year-end closing</li>\n        <li>Occasional closing days</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of SouthKorea
        auto pyEnumMarket =
            py::enum_<QuantLib::SouthKorea::Market>(pyClassSouthKorea, "Market", py::arithmetic(), "")
                .value("Settlement", QuantLib::SouthKorea::Settlement, "!< Public holidays")
                .value("KRX", QuantLib::SouthKorea::KRX, "!< Korea exchange")
            .export_values();
    } // end of inner classes & enums of SouthKorea

    pyClassSouthKorea
        .def(py::init<QuantLib::SouthKorea::Market>(),
            py::arg("m") = QuantLib::SouthKorea::KRX)
        ;


    auto pyClassSweden =
        py::class_<QuantLib::Sweden, QuantLib::Calendar, ext::shared_ptr<QuantLib::Sweden>>
            (m, "Sweden", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Epiphany, January 6th</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Ascension</li>\n        <li>Whit(Pentecost) Monday (until 2004)</li>\n        <li>May Day, May 1st</li>\n        <li>National Day, June 6th</li>\n        <li>Midsummer Eve (Friday between June 19-25)</li>\n        <li>Christmas Eve, December 24th</li>\n        <li>Christmas Day, December 25th</li>\n        <li>Boxing Day, December 26th</li>\n        <li>New Year's Eve, December 31th</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassSwitzerland =
        py::class_<QuantLib::Switzerland, QuantLib::Calendar, ext::shared_ptr<QuantLib::Switzerland>>
            (m, "Switzerland", "! Holidays:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Berchtoldstag, January 2nd</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Ascension Day</li>\n        <li>Whit Monday</li>\n        <li>Labour Day, May 1st</li>\n        <li>National Day, August 1st</li>\n        <li>Christmas, December 25th</li>\n        <li>St. Stephen's Day, December 26th</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassTaiwan =
        py::class_<QuantLib::Taiwan, QuantLib::Calendar, ext::shared_ptr<QuantLib::Taiwan>>
            (m, "Taiwan", "! Holidays for the Taiwan stock exchange\n        (data from <https://www.twse.com.tw/en/trading/holiday.html>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Peace Memorial Day, February 28</li>\n        <li>Labor Day, May 1st</li>\n        <li>Double Tenth National Day, October 10th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2002-2024 only:)\n        <ul>\n        <li>Chinese Lunar New Year</li>\n        <li>Tomb Sweeping Day</li>\n        <li>Dragon Boat Festival</li>\n        <li>Moon Festival</li>\n        </ul>\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Taiwan
        auto pyEnumMarket =
            py::enum_<QuantLib::Taiwan::Market>(pyClassTaiwan, "Market", py::arithmetic(), "")
                .value("TSEC", QuantLib::Taiwan::TSEC, "!< Taiwan stock exchange")
            .export_values();
    } // end of inner classes & enums of Taiwan

    pyClassTaiwan
        .def(py::init<QuantLib::Taiwan::Market>(),
            py::arg("m") = QuantLib::Taiwan::TSEC)
        ;


    auto pyClassTARGET =
        py::class_<QuantLib::TARGET, QuantLib::Calendar, ext::shared_ptr<QuantLib::TARGET>>
            (m, "TARGET", "! Holidays (see http://www.ecb.int):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Good Friday (since 2000)</li>\n        <li>Easter Monday (since 2000)</li>\n        <li>Labour Day, May 1st (since 2000)</li>\n        <li>Christmas, December 25th</li>\n        <li>Day of Goodwill, December 26th (since 2000)</li>\n        <li>December 31st (1998, 1999, and 2001)</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n")
        .def(py::init<>())
        ;


    auto pyClassThailand =
        py::class_<QuantLib::Thailand, QuantLib::Calendar, ext::shared_ptr<QuantLib::Thailand>>
            (m, "Thailand", "! Holidays for the Thailand exchange\n        Holidays observed by financial institutions (not to be confused with bank holidays in the United Kingdom) are regulated by the Bank of Thailand.\n        If a holiday fall on a weekend the government will announce a replacement day (usually the following Monday).\n\n        Sometimes the government add one or two extra holidays in a year.\n\n        (data from\n         https://www.bot.or.th/en/financial-institutions-holiday.html:\n        Fixed holidays\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>Chakri Memorial Day, April 6th</li>\n        <li>Songkran holiday, April 13th - 15th</li>\n        <li>Labour Day, May 1st</li>\n        <li>H.M. the King's Birthday, July 28th (from 2017)</li>\n        <li>H.M. the Queen's Birthday, August 12th </li>\n        <li>The Passing of H.M. the Late King Bhumibol Adulyadej (Rama IX), October 13th (from 2017) </li>\n        <li>H.M. the Late King Bhumibol Adulyadej's Birthday, December 5th</li>\n        <li>Constitution Day, December 10th</li>\n        <li>New Year's Eve, December 31th</li>\n        </ul>\n\n        Other holidays for which no rule is given\n        (data available for 2000-2024 with some years missing)\n        <ul>\n        <li>Makha Bucha Day</li>\n        <li>Wisakha Bucha Day</li>\n        <li>Buddhist Lent Day (until 2006)</li>\n        <li>Asarnha Bucha Day (from 2007)</li>\n        <li>Chulalongkorn Day</li>\n        <li>Other special holidays</li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassTurkey =
        py::class_<QuantLib::Turkey, QuantLib::Calendar, ext::shared_ptr<QuantLib::Turkey>>
            (m, "Turkey", "! Holidays for the Istanbul Stock Exchange:\n        (data from\n         <https://borsaistanbul.com/en/sayfa/3631/official-holidays>\n		 and\n		 <https://feiertagskalender.ch/index.php?geo=3539&hl=en>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>National Sovereignty and Children�s Day, April 23rd</li>\n        <li>Labour and Solidarity Day, May 1st</li>\n        <li>Youth and Sports Day, May 19th</li>\n        <li>Democracy and National Unity Day, July 15th</li>\n        <li>Victory Day, August 30th</li>\n        <li>Republic Day, October 29th</li>\n        <li>Local Holidays (Kurban, Ramadan - dates need further validation for >= 2024) </li>\n        </ul>\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;


    auto pyClassUkraine =
        py::class_<QuantLib::Ukraine, QuantLib::Calendar, ext::shared_ptr<QuantLib::Ukraine>>
            (m, "Ukraine", "! Holidays for the Ukrainian stock exchange\n        (data from <http://www.ukrse.kiev.ua/eng/>):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st</li>\n        <li>Orthodox Christmas, January 7th</li>\n        <li>International Women's Day, March 8th</li>\n        <li>Easter Monday</li>\n        <li>Holy Trinity Day, 50 days after Easter</li>\n        <li>International Workers' Solidarity Days, May 1st and 2nd</li>\n        <li>Victory Day, May 9th</li>\n        <li>Constitution Day, June 28th</li>\n        <li>Independence Day, August 24th</li>\n        <li>Defender's Day, October 14th (since 2015)</li>\n        </ul>\n        Holidays falling on a Saturday or Sunday might be moved to the\n        following Monday.\n\n        \\ingroup calendars\n");

    { // inner classes & enums of Ukraine
        auto pyEnumMarket =
            py::enum_<QuantLib::Ukraine::Market>(pyClassUkraine, "Market", py::arithmetic(), "")
                .value("USE", QuantLib::Ukraine::USE, "!< Ukrainian stock exchange")
            .export_values();
    } // end of inner classes & enums of Ukraine

    pyClassUkraine
        .def(py::init<QuantLib::Ukraine::Market>(),
            py::arg("m") = QuantLib::Ukraine::USE)
        ;


    auto pyClassUnitedKingdom =
        py::class_<QuantLib::UnitedKingdom, QuantLib::Calendar, ext::shared_ptr<QuantLib::UnitedKingdom>>
            (m, "UnitedKingdom", "! Repeating Public holidays (data from https://www.gov.uk/bank-holidays):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Early May Bank Holiday, first Monday of May</li>\n        <li>Spring Bank Holiday, last Monday of May</li>\n        <li>Summer Bank Holiday, last Monday of August</li>\n        <li>Christmas Day, December 25th (possibly moved to Monday or\n            Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        </ul>\n\n        Holidays for the stock exchange:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Early May Bank Holiday, first Monday of May</li>\n        <li>Spring Bank Holiday, last Monday of May</li>\n        <li>Summer Bank Holiday, last Monday of August</li>\n        <li>Christmas Day, December 25th (possibly moved to Monday or\n            Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        </ul>\n\n        Holidays for the metals exchange:\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday)</li>\n        <li>Good Friday</li>\n        <li>Easter Monday</li>\n        <li>Early May Bank Holiday, first Monday of May</li>\n        <li>Spring Bank Holiday, last Monday of May</li>\n        <li>Summer Bank Holiday, last Monday of August</li>\n        <li>Christmas Day, December 25th (possibly moved to Monday or\n            Tuesday)</li>\n        <li>Boxing Day, December 26th (possibly moved to Monday or\n            Tuesday)</li>\n        </ul>\n\n        Note that there are some one-off holidays not listed above.\n        See the implementation for the complete list.\n\n        \\ingroup calendars\n\n        \todo add LIFFE\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n");

    { // inner classes & enums of UnitedKingdom
        auto pyEnumMarket =
            py::enum_<QuantLib::UnitedKingdom::Market>(pyClassUnitedKingdom, "Market", py::arithmetic(), "! UK calendars")
                .value("Settlement", QuantLib::UnitedKingdom::Settlement, "!< generic settlement calendar")
                .value("Exchange", QuantLib::UnitedKingdom::Exchange, "!< London stock-exchange calendar")
                .value("Metals", QuantLib::UnitedKingdom::Metals, "|< London metals-exchange calendar")
            .export_values();
    } // end of inner classes & enums of UnitedKingdom

    pyClassUnitedKingdom
        .def(py::init<QuantLib::UnitedKingdom::Market>(),
            py::arg("market") = QuantLib::UnitedKingdom::Settlement)
        ;


    auto pyClassUnitedStates =
        py::class_<QuantLib::UnitedStates, QuantLib::Calendar, ext::shared_ptr<QuantLib::UnitedStates>>
            (m, "UnitedStates", "! Public holidays (see https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday if\n            actually on Sunday, or to Friday if on Saturday)</li>\n        <li>Martin Luther King's birthday, third Monday in January (since\n            1983)</li>\n        <li>Presidents' Day (a.k.a. Washington's birthday),\n            third Monday in February</li>\n        <li>Memorial Day, last Monday in May</li>\n        <li>Juneteenth, June 19th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Independence Day, July 4th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Labor Day, first Monday in September</li>\n        <li>Columbus Day, second Monday in October</li>\n        <li>Veterans' Day, November 11th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Thanksgiving Day, fourth Thursday in November</li>\n        <li>Christmas, December 25th (moved to Monday if Sunday or Friday\n            if Saturday)</li>\n        </ul>\n\n        Note that since 2015 Independence Day only impacts Libor if it\n        falls on a  weekday (see <https://www.theice.com/iba/libor>,\n        <https://www.theice.com/marketdata/reports/170> and\n        <https://www.theice.com/publicdocs/LIBOR_Holiday_Calendar_2015.pdf>\n        for the fixing and value date calendars).\n\n        Holidays for the stock exchange (data from http://www.nyse.com):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday if\n            actually on Sunday)</li>\n        <li>Martin Luther King's birthday, third Monday in January (since\n            1998)</li>\n        <li>Presidents' Day (a.k.a. Washington's birthday),\n            third Monday in February</li>\n        <li>Good Friday</li>\n        <li>Memorial Day, last Monday in May</li>\n        <li>Independence Day, July 4th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Labor Day, first Monday in September</li>\n        <li>Thanksgiving Day, fourth Thursday in November</li>\n        <li>Presidential election day, first Tuesday in November of election\n            years (until 1980)</li>\n        <li>Christmas, December 25th (moved to Monday if Sunday or Friday\n            if Saturday)</li>\n        <li>Special historic closings (see\n            http://www.nyse.com/pdfs/closings.pdf)</li>\n        </ul>\n\n        Holidays for the government bond market (data from\n        http://www.bondmarkets.com):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday if\n            actually on Sunday)</li>\n        <li>Martin Luther King's birthday, third Monday in January (since\n            1983)</li>\n        <li>Presidents' Day (a.k.a. Washington's birthday),\n            third Monday in February</li>\n        <li>Good Friday</li>\n        <li>Memorial Day, last Monday in May</li>\n        <li>Independence Day, July 4th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Labor Day, first Monday in September</li>\n        <li>Columbus Day, second Monday in October</li>\n        <li>Veterans' Day, November 11th (moved to Monday if Sunday or\n            Friday if Saturday)</li>\n        <li>Thanksgiving Day, fourth Thursday in November</li>\n        <li>Christmas, December 25th (moved to Monday if Sunday or Friday\n            if Saturday)</li>\n        </ul>\n\n        Holidays for the North American Energy Reliability Council\n        (data from http://www.nerc.com/~oc/offpeaks.html):\n        <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday if\n            actually on Sunday)</li>\n        <li>Memorial Day, last Monday in May</li>\n        <li>Independence Day, July 4th (moved to Monday if Sunday)</li>\n        <li>Labor Day, first Monday in September</li>\n        <li>Thanksgiving Day, fourth Thursday in November</li>\n        <li>Christmas, December 25th (moved to Monday if Sunday)</li>\n        </ul>\n\n        Holidays for the Federal Reserve Bankwire System\n        (data from https://www.federalreserve.gov/aboutthefed/k8.htm\n        and https://www.frbservices.org/about/holiday-schedules):\n         <ul>\n        <li>Saturdays</li>\n        <li>Sundays</li>\n        <li>New Year's Day, January 1st (possibly moved to Monday if\n            actually on Sunday)</li>\n        <li>Martin Luther King's birthday, third Monday in January (since\n            1983)</li>\n        <li>Presidents' Day (a.k.a. Washington's birthday),\n            third Monday in February</li>\n        <li>Memorial Day, last Monday in May</li>\n        <li>Juneteenth, June 19th (moved to Monday if Sunday)</li>\n        <li>Independence Day, July 4th (moved to Monday if Sunday)</li>\n        <li>Labor Day, first Monday in September</li>\n        <li>Columbus Day, second Monday in October</li>\n        <li>Veterans' Day, November 11th (moved to Monday if Sunday)</li>\n        <li>Thanksgiving Day, fourth Thursday in November</li>\n        <li>Christmas, December 25th (moved to Monday if Sunday)</li>\n        </ul>\n\n        \\ingroup calendars\n\n        \test the correctness of the returned results is tested\n              against a list of known holidays.\n");

    { // inner classes & enums of UnitedStates
        auto pyEnumMarket =
            py::enum_<QuantLib::UnitedStates::Market>(pyClassUnitedStates, "Market", py::arithmetic(), "! US calendars")
                .value("Settlement", QuantLib::UnitedStates::Settlement, "!< generic settlement calendar")
                .value("NYSE", QuantLib::UnitedStates::NYSE, "!< New York stock exchange calendar")
                .value("GovernmentBond", QuantLib::UnitedStates::GovernmentBond, "!< government-bond calendar")
                .value("NERC", QuantLib::UnitedStates::NERC, "!< off-peak days for NERC")
                .value("LiborImpact", QuantLib::UnitedStates::LiborImpact, "!< Libor impact calendar")
                .value("FederalReserve", QuantLib::UnitedStates::FederalReserve, "!< Federal Reserve Bankwire System")
                .value("SOFR", QuantLib::UnitedStates::SOFR, "!< SOFR fixing calendar")
            .export_values();
    } // end of inner classes & enums of UnitedStates

    pyClassUnitedStates
        .def(py::init<QuantLib::UnitedStates::Market>(), 
            py::arg("market") = QuantLib::UnitedStates::Settlement)
        ;


    auto pyClassWeekendsOnly =
        py::class_<QuantLib::WeekendsOnly, QuantLib::Calendar, ext::shared_ptr<QuantLib::WeekendsOnly>>
            (m, "WeekendsOnly", "! This calendar has no bank holidays except for weekends\n        (Saturdays and Sundays) as required by ISDA for calculating\n        conventional CDS spreads.\n\n        \\ingroup calendars\n")
        .def(py::init<>())
        ;
}