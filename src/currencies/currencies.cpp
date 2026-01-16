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

// Generated from QuantLib currency headers

#include "pyquantlib/pyquantlib.h"
#include <ql/currencies/all.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;


void ql_currencies::all_currencies(py::module_& m)
{
    auto pyClassAOACurrency =
        py::class_<QuantLib::AOACurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::AOACurrency>>
            (m, "AOACurrency", " Angolan kwanza\n/*! The ISO three-letter code is AOA; the numeric code is 973.\n     It is divided into 100 c�ntimo.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassBWPCurrency =
        py::class_<QuantLib::BWPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BWPCurrency>>
            (m, "BWPCurrency", " Botswanan Pula\n/*! The ISO three-letter code is BWP; the numeric code is 72.\n     It is divided into 100 thebe.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassEGPCurrency =
        py::class_<QuantLib::EGPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::EGPCurrency>>
            (m, "EGPCurrency", "! Egyptian pound\n/*! The ISO three-letter code is EGP; the numeric code is 818.\n     It is divided into 100 piastres.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassETBCurrency =
        py::class_<QuantLib::ETBCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ETBCurrency>>
            (m, "ETBCurrency", " Ethiopian birr\n/*! The ISO three-letter code is ETB; the numeric code is 230.\n     It is divided into 100 santim.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassGHSCurrency =
        py::class_<QuantLib::GHSCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::GHSCurrency>>
            (m, "GHSCurrency", "! Ghanaian cedi\n/*! The ISO three-letter code is GHS; the numeric code is 936.\n     It is divided into 100 pesewas.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassKESCurrency =
        py::class_<QuantLib::KESCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::KESCurrency>>
            (m, "KESCurrency", "! Kenyan shilling\n/*! The ISO three-letter code is KES; the numeric code is 404.\n     It is divided into 100 cents.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassMADCurrency =
        py::class_<QuantLib::MADCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MADCurrency>>
            (m, "MADCurrency", "! Moroccan dirham\n/*! The ISO three-letter code is MAD; the numeric code is 504.\n     It is divided into 100 santim.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassMURCurrency =
        py::class_<QuantLib::MURCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MURCurrency>>
            (m, "MURCurrency", "! Mauritian rupee\n/*! The ISO three-letter code is MUR; the numeric code is 480.\n     It is divided into 100 cents.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassNGNCurrency =
        py::class_<QuantLib::NGNCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::NGNCurrency>>
            (m, "NGNCurrency", "! Nigerian Naira\n/*! The ISO three-letter code is NGN; the numeric code is 566.\n     It is divided into 100 kobo.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassTNDCurrency =
        py::class_<QuantLib::TNDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::TNDCurrency>>
            (m, "TNDCurrency", "! Tunisian dinar\n/*! The ISO three-letter code is TND; the numeric code is 788.\n     It is divided into 1000 millim.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassUGXCurrency =
        py::class_<QuantLib::UGXCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::UGXCurrency>>
            (m, "UGXCurrency", "! Ugandan shilling\n/*! The ISO three-letter code is UGX; the numeric code is 800.\n    It is the smallest unit.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassXOFCurrency =
        py::class_<QuantLib::XOFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::XOFCurrency>>
            (m, "XOFCurrency", " West African CFA franc\n/*! The ISO three-letter code is XOF; the numeric code is 952.\n     It is divided into 100 centime.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassZARCurrency =
        py::class_<QuantLib::ZARCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ZARCurrency>>
            (m, "ZARCurrency", "! The ISO three-letter code is ZAR; the numeric code is 710.\n        It is divided into 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassZMWCurrency =
        py::class_<QuantLib::ZMWCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ZMWCurrency>>
            (m, "ZMWCurrency", "! Zambian kwacha\n/*! The ISO three-letter code is ZMW; the numeric code is 967.\n    It is divided into 100 ngwee.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassARSCurrency =
        py::class_<QuantLib::ARSCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ARSCurrency>>
            (m, "ARSCurrency", "! The ISO three-letter code is ARS; the numeric code is 32.\n        It is divided in 100 centavos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBRLCurrency =
        py::class_<QuantLib::BRLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BRLCurrency>>
            (m, "BRLCurrency", "! The ISO three-letter code is BRL; the numeric code is 986.\n        It is divided in 100 centavos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCADCurrency =
        py::class_<QuantLib::CADCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CADCurrency>>
            (m, "CADCurrency", "! The ISO three-letter code is CAD; the numeric code is 124.\n        It is divided into 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCLPCurrency =
        py::class_<QuantLib::CLPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CLPCurrency>>
            (m, "CLPCurrency", "! The ISO three-letter code is CLP; the numeric code is 152.\n        It is divided in 100 centavos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCOPCurrency =
        py::class_<QuantLib::COPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::COPCurrency>>
            (m, "COPCurrency", "! The ISO three-letter code is COP; the numeric code is 170.\n        It is divided in 100 centavos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassMXNCurrency =
        py::class_<QuantLib::MXNCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MXNCurrency>>
            (m, "MXNCurrency", "! The ISO three-letter code is MXN; the numeric code is 484.\n        It is divided in 100 centavos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPENCurrency =
        py::class_<QuantLib::PENCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PENCurrency>>
            (m, "PENCurrency", "! The ISO three-letter code is PEN; the numeric code is 604.\n        It is divided in 100 centimos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPEICurrency =
        py::class_<QuantLib::PEICurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PEICurrency>>
            (m, "PEICurrency", "! The ISO three-letter code was PEI.\n        It was divided in 100 centimos. A numeric code is not available;\n        as per ISO 3166-1, we assign 998 as a user-defined code.\n\n        Obsoleted by the nuevo sol since July 1991.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPEHCurrency =
        py::class_<QuantLib::PEHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PEHCurrency>>
            (m, "PEHCurrency", "! The ISO three-letter code was PEH. A numeric code is not available;\n        as per ISO 3166-1, we assign 999 as a user-defined code.\n        It was divided in 100 centavos.\n\n        Obsoleted by the inti since February 1985.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassTTDCurrency =
        py::class_<QuantLib::TTDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::TTDCurrency>>
            (m, "TTDCurrency", "! The ISO three-letter code is TTD; the numeric code is 780.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassUSDCurrency =
        py::class_<QuantLib::USDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::USDCurrency>>
            (m, "USDCurrency", "! The ISO three-letter code is USD; the numeric code is 840.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassVEBCurrency =
        py::class_<QuantLib::VEBCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::VEBCurrency>>
            (m, "VEBCurrency", "! The ISO three-letter code is VEB; the numeric code is 862.\n        It is divided in 100 centimos.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassMXVCurrency =
        py::class_<QuantLib::MXVCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MXVCurrency>>
            (m, "MXVCurrency", "! Mexican Unidad de Inversion\n/*! The ISO three-letter code is MXV; the numeric code is 979.\n     A unit of account used in Mexico.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassCOUCurrency =
        py::class_<QuantLib::COUCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::COUCurrency>>
            (m, "COUCurrency", "! Unidad de Valor Real\n/*! The ISO three-letter code is COU; the numeric code is 970.\n     A unit of account used in Colombia.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassCLFCurrency =
        py::class_<QuantLib::CLFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CLFCurrency>>
            (m, "CLFCurrency", "! Unidad de Fomento (funds code)\n/*! The ISO three-letter code is CLF; the numeric code is 990.\n     A unit of account used in Chile.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassUYUCurrency =
        py::class_<QuantLib::UYUCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::UYUCurrency>>
            (m, "UYUCurrency", "! Uruguayan peso\n/*! The ISO three-letter code is UYU; the numeric code is 858.\n     A unit of account used in Uruguay.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassBDTCurrency =
        py::class_<QuantLib::BDTCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BDTCurrency>>
            (m, "BDTCurrency", "! The ISO three-letter code is BDT; the numeric code is 50.\n        It is divided in 100 paisa.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCNYCurrency =
        py::class_<QuantLib::CNYCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CNYCurrency>>
            (m, "CNYCurrency", "! The ISO three-letter code is CNY; the numeric code is 156.\n        It is divided in 100 fen.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassHKDCurrency =
        py::class_<QuantLib::HKDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::HKDCurrency>>
            (m, "HKDCurrency", "! The ISO three-letter code is HKD; the numeric code is 344.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassIDRCurrency =
        py::class_<QuantLib::IDRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::IDRCurrency>>
            (m, "IDRCurrency", "! The ISO three-letter code is IDR; the numeric code is 360.\n        It is divided in 100 sen.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassILSCurrency =
        py::class_<QuantLib::ILSCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ILSCurrency>>
            (m, "ILSCurrency", "! The ISO three-letter code is ILS; the numeric code is 376.\n        It is divided in 100 agorot.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassINRCurrency =
        py::class_<QuantLib::INRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::INRCurrency>>
            (m, "INRCurrency", "! The ISO three-letter code is INR; the numeric code is 356.\n        It is divided in 100 paise.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassIQDCurrency =
        py::class_<QuantLib::IQDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::IQDCurrency>>
            (m, "IQDCurrency", "! The ISO three-letter code is IQD; the numeric code is 368.\n        It is divided in 1000 fils.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassIRRCurrency =
        py::class_<QuantLib::IRRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::IRRCurrency>>
            (m, "IRRCurrency", "! The ISO three-letter code is IRR; the numeric code is 364.\n        It has no subdivisions.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassJPYCurrency =
        py::class_<QuantLib::JPYCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::JPYCurrency>>
            (m, "JPYCurrency", "! The ISO three-letter code is JPY; the numeric code is 392.\n        It is divided into 100 sen.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassKRWCurrency =
        py::class_<QuantLib::KRWCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::KRWCurrency>>
            (m, "KRWCurrency", "! The ISO three-letter code is KRW; the numeric code is 410.\n        It is divided in 100 chon.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassKWDCurrency =
        py::class_<QuantLib::KWDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::KWDCurrency>>
            (m, "KWDCurrency", "! The ISO three-letter code is KWD; the numeric code is 414.\n        It is divided in 1000 fils.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassKZTCurrency =
        py::class_<QuantLib::KZTCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::KZTCurrency>>
            (m, "KZTCurrency", "")
        .def(py::init<>())
        ;


    auto pyClassMYRCurrency =
        py::class_<QuantLib::MYRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MYRCurrency>>
            (m, "MYRCurrency", "! The ISO three-letter code is MYR; the numeric code is 458.\n        It is divided in 100 sen.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassNPRCurrency =
        py::class_<QuantLib::NPRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::NPRCurrency>>
            (m, "NPRCurrency", "! The ISO three-letter code is NPR; the numeric code is 524.\n        It is divided in 100 paise.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPKRCurrency =
        py::class_<QuantLib::PKRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PKRCurrency>>
            (m, "PKRCurrency", "! The ISO three-letter code is PKR; the numeric code is 586.\n        It is divided in 100 paisa.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassSARCurrency =
        py::class_<QuantLib::SARCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::SARCurrency>>
            (m, "SARCurrency", "! The ISO three-letter code is SAR; the numeric code is 682.\n        It is divided in 100 halalat.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassSGDCurrency =
        py::class_<QuantLib::SGDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::SGDCurrency>>
            (m, "SGDCurrency", "! The ISO three-letter code is SGD; the numeric code is 702.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassTHBCurrency =
        py::class_<QuantLib::THBCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::THBCurrency>>
            (m, "THBCurrency", "! The ISO three-letter code is THB; the numeric code is 764.\n        It is divided in 100 stang.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassTWDCurrency =
        py::class_<QuantLib::TWDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::TWDCurrency>>
            (m, "TWDCurrency", "! The ISO three-letter code is TWD; the numeric code is 901.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassVNDCurrency =
        py::class_<QuantLib::VNDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::VNDCurrency>>
            (m, "VNDCurrency", "! The ISO three-letter code is VND; the numeric code is 704.\n        It was divided in 100 xu.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassQARCurrency =
        py::class_<QuantLib::QARCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::QARCurrency>>
            (m, "QARCurrency", "! Qatari riyal\n/*! The ISO three-letter code is QAR; the numeric code is 634.\n     It is divided into 100 diram.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassBHDCurrency =
        py::class_<QuantLib::BHDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BHDCurrency>>
            (m, "BHDCurrency", "! Bahraini dinar\n/*! The ISO three-letter code is BHD; the numeric code is 048.\n     It is divided into 1000 fils.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassOMRCurrency =
        py::class_<QuantLib::OMRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::OMRCurrency>>
            (m, "OMRCurrency", "! Omani rial\n/*! The ISO three-letter code is OMR; the numeric code is 512.\n     It is divided into 1000 baisa.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassJODCurrency =
        py::class_<QuantLib::JODCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::JODCurrency>>
            (m, "JODCurrency", "! Jordanian dinar\n/*! The ISO three-letter code is JOD; the numeric code is 400.\n     It is divided into 100 qirshes.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassAEDCurrency =
        py::class_<QuantLib::AEDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::AEDCurrency>>
            (m, "AEDCurrency", "! United Arab Emirates dirham\n/*! The ISO three-letter code is AED; the numeric code is 784.\n     It is divided into 100 fils.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassPHPCurrency =
        py::class_<QuantLib::PHPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PHPCurrency>>
            (m, "PHPCurrency", "! Philippine peso\n/*! The ISO three-letter code is PHP; the numeric code is 608.\n     It is divided into 100 centavo.\n     \\ingroup currencies\n     */")
        .def(py::init<>())
        ;


    auto pyClassCNHCurrency =
        py::class_<QuantLib::CNHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CNHCurrency>>
            (m, "CNHCurrency", "! Chinese yuan (Hong Kong)\n/*! The ISO three-letter code is CNH; there is no numeric code.\n     It is divided in 100 fen.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassLKRCurrency =
        py::class_<QuantLib::LKRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::LKRCurrency>>
            (m, "LKRCurrency", "! Sri Lankan rupee\n/*! The ISO three-letter code is LKR; there numeric code is 144.\n     It is divided into 100 cents.\n     \\ingroup currencies\n    */")
        .def(py::init<>())
        ;


    auto pyClassBTCCurrency =
        py::class_<QuantLib::BTCCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BTCCurrency>>
            (m, "BTCCurrency", "! https://bitcoin.org/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassETHCurrency =
        py::class_<QuantLib::ETHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ETHCurrency>>
            (m, "ETHCurrency", "! https://www.ethereum.org/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassETCCurrency =
        py::class_<QuantLib::ETCCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ETCCurrency>>
            (m, "ETCCurrency", "! https://ethereumclassic.github.io/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBCHCurrency =
        py::class_<QuantLib::BCHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BCHCurrency>>
            (m, "BCHCurrency", "! https://www.bitcoincash.org/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassXRPCurrency =
        py::class_<QuantLib::XRPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::XRPCurrency>>
            (m, "XRPCurrency", "! https://ripple.com/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassLTCCurrency =
        py::class_<QuantLib::LTCCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::LTCCurrency>>
            (m, "LTCCurrency", "! https://litecoin.com/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassDASHCurrency =
        py::class_<QuantLib::DASHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::DASHCurrency>>
            (m, "DASHCurrency", "! https://www.dash.org/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassZECCurrency =
        py::class_<QuantLib::ZECCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ZECCurrency>>
            (m, "ZECCurrency", "! https://z.cash/\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBGLCurrency =
        py::class_<QuantLib::BGLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BGLCurrency>>
            (m, "BGLCurrency", "! The ISO three-letter code is BGL; the numeric code is 100.\n        It is divided in 100 stotinki.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBGNCurrency =
        py::class_<QuantLib::BGNCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BGNCurrency>>
            (m, "BGNCurrency", "! The ISO three-letter code is BGN; the numeric code is 975.\n        It is divided into 100 stotinki.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBYRCurrency =
        py::class_<QuantLib::BYRCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BYRCurrency>>
            (m, "BYRCurrency", "! The ISO three-letter code is BYR; the numeric code is 974.\n        It has no subdivisions.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCHFCurrency =
        py::class_<QuantLib::CHFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CHFCurrency>>
            (m, "CHFCurrency", "! The ISO three-letter code is CHF; the numeric code is 756.\n        It is divided into 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCZKCurrency =
        py::class_<QuantLib::CZKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CZKCurrency>>
            (m, "CZKCurrency", "! The ISO three-letter code is CZK; the numeric code is 203.\n        It is divided in 100 haleru.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassDKKCurrency =
        py::class_<QuantLib::DKKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::DKKCurrency>>
            (m, "DKKCurrency", "! The ISO three-letter code is DKK; the numeric code is 208.\n        It is divided in 100 �re.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassEEKCurrency =
        py::class_<QuantLib::EEKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::EEKCurrency>>
            (m, "EEKCurrency", "! The ISO three-letter code is EEK; the numeric code is 233.\n        It is divided in 100 senti.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassEURCurrency =
        py::class_<QuantLib::EURCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::EURCurrency>>
            (m, "EURCurrency", "! The ISO three-letter code is EUR; the numeric code is 978.\n        It is divided into 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassGBPCurrency =
        py::class_<QuantLib::GBPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::GBPCurrency>>
            (m, "GBPCurrency", "! The ISO three-letter code is GBP; the numeric code is 826.\n        It is divided into 100 pence.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassGELCurrency =
        py::class_<QuantLib::GELCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::GELCurrency>>
            (m, "GELCurrency", "! The ISO three-letter code is GEL; the numeric code is 981.\n        It is divided into 100 tetri.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassHUFCurrency =
        py::class_<QuantLib::HUFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::HUFCurrency>>
            (m, "HUFCurrency", "! The ISO three-letter code is HUF; the numeric code is 348.\n        It has no subdivisions.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassISKCurrency =
        py::class_<QuantLib::ISKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ISKCurrency>>
            (m, "ISKCurrency", "! The ISO three-letter code is ISK; the numeric code is 352.\n        It is divided in 100 aurar.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassLTLCurrency =
        py::class_<QuantLib::LTLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::LTLCurrency>>
            (m, "LTLCurrency", "! The ISO three-letter code is LTL; the numeric code is 440.\n        It is divided in 100 centu.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassLVLCurrency =
        py::class_<QuantLib::LVLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::LVLCurrency>>
            (m, "LVLCurrency", "! The ISO three-letter code is LVL; the numeric code is 428.\n        It is divided in 100 santims.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassNOKCurrency =
        py::class_<QuantLib::NOKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::NOKCurrency>>
            (m, "NOKCurrency", "! The ISO three-letter code is NOK; the numeric code is 578.\n        It is divided in 100 �re.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPLNCurrency =
        py::class_<QuantLib::PLNCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PLNCurrency>>
            (m, "PLNCurrency", "! The ISO three-letter code is PLN; the numeric code is 985.\n        It is divided in 100 groszy.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassROLCurrency =
        py::class_<QuantLib::ROLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ROLCurrency>>
            (m, "ROLCurrency", "! The ISO three-letter code was ROL; the numeric code was 642.\n        It was divided in 100 bani.\n\n        Obsoleted by the new leu since July 2005.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassRONCurrency =
        py::class_<QuantLib::RONCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::RONCurrency>>
            (m, "RONCurrency", "! The ISO three-letter code is RON; the numeric code is 946.\n        It is divided in 100 bani.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassRSDCurrency =
        py::class_<QuantLib::RSDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::RSDCurrency>>
            (m, "RSDCurrency", "! The ISO three-letter code is RSD; the numeric code is 941.\n        It is divided into 100 para/napa.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassRUBCurrency =
        py::class_<QuantLib::RUBCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::RUBCurrency>>
            (m, "RUBCurrency", "! The ISO three-letter code is RUB; the numeric code is 643.\n        It is divided in 100 kopeyki.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassSEKCurrency =
        py::class_<QuantLib::SEKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::SEKCurrency>>
            (m, "SEKCurrency", "! The ISO three-letter code is SEK; the numeric code is 752.\n        It is divided in 100 �re.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassSITCurrency =
        py::class_<QuantLib::SITCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::SITCurrency>>
            (m, "SITCurrency", "! The ISO three-letter code is SIT; the numeric code is 705.\n        It is divided in 100 stotinov.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassTRLCurrency =
        py::class_<QuantLib::TRLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::TRLCurrency>>
            (m, "TRLCurrency", "! The ISO three-letter code was TRL; the numeric code was 792.\n        It was divided in 100 kurus.\n\n        Obsoleted by the new Turkish lira since 2005.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassTRYCurrency =
        py::class_<QuantLib::TRYCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::TRYCurrency>>
            (m, "TRYCurrency", "! The ISO three-letter code is TRY; the numeric code is 949.\n        It is divided in 100 new kurus.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassUAHCurrency =
        py::class_<QuantLib::UAHCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::UAHCurrency>>
            (m, "UAHCurrency", "! The ISO three-letter code is UAH; the numeric code is 980.\n        It is divided in 100 kopiykas.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassATSCurrency =
        py::class_<QuantLib::ATSCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ATSCurrency>>
            (m, "ATSCurrency", "! The ISO three-letter code was ATS; the numeric code was 40.\n        It was divided in 100 groschen.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassBEFCurrency =
        py::class_<QuantLib::BEFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::BEFCurrency>>
            (m, "BEFCurrency", "! The ISO three-letter code was BEF; the numeric code was 56.\n        It had no subdivisions.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassCYPCurrency =
        py::class_<QuantLib::CYPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::CYPCurrency>>
            (m, "CYPCurrency", "! The ISO three-letter code is CYP; the numeric code is 196.\n        It is divided in 100 cents.\n\n        Obsoleted by the Euro since 2008.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassDEMCurrency =
        py::class_<QuantLib::DEMCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::DEMCurrency>>
            (m, "DEMCurrency", "! The ISO three-letter code was DEM; the numeric code was 276.\n        It was divided into 100 pfennig.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassESPCurrency =
        py::class_<QuantLib::ESPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ESPCurrency>>
            (m, "ESPCurrency", "! The ISO three-letter code was ESP; the numeric code was 724.\n        It was divided in 100 centimos.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassFIMCurrency =
        py::class_<QuantLib::FIMCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::FIMCurrency>>
            (m, "FIMCurrency", "! The ISO three-letter code was FIM; the numeric code was 246.\n        It was divided in 100 penni�.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassFRFCurrency =
        py::class_<QuantLib::FRFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::FRFCurrency>>
            (m, "FRFCurrency", "! The ISO three-letter code was FRF; the numeric code was 250.\n        It was divided in 100 centimes.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassGRDCurrency =
        py::class_<QuantLib::GRDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::GRDCurrency>>
            (m, "GRDCurrency", "! The ISO three-letter code was GRD; the numeric code was 300.\n        It was divided in 100 lepta.\n\n        Obsoleted by the Euro since 2001.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassHRKCurrency =
        py::class_<QuantLib::HRKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::HRKCurrency>>
            (m, "HRKCurrency", "! The ISO three-letter code was HRK; the numeric code was 191.\n        It was divided into 100 lipa.\n\n        Obsoleted by the Euro since 2023.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassIEPCurrency =
        py::class_<QuantLib::IEPCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::IEPCurrency>>
            (m, "IEPCurrency", "! The ISO three-letter code was IEP; the numeric code was 372.\n        It was divided in 100 pence.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassITLCurrency =
        py::class_<QuantLib::ITLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::ITLCurrency>>
            (m, "ITLCurrency", "! The ISO three-letter code was ITL; the numeric code was 380.\n        It had no subdivisions.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassLUFCurrency =
        py::class_<QuantLib::LUFCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::LUFCurrency>>
            (m, "LUFCurrency", "! The ISO three-letter code was LUF; the numeric code was 442.\n        It was divided in 100 centimes.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassMTLCurrency =
        py::class_<QuantLib::MTLCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::MTLCurrency>>
            (m, "MTLCurrency", "! The ISO three-letter code is MTL; the numeric code is 470.\n        It was divided in 100 cents.\n\n        Obsoleted by the Euro since 2008.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassNLGCurrency =
        py::class_<QuantLib::NLGCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::NLGCurrency>>
            (m, "NLGCurrency", "! The ISO three-letter code was NLG; the numeric code was 528.\n        It was divided in 100 cents.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassPTECurrency =
        py::class_<QuantLib::PTECurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::PTECurrency>>
            (m, "PTECurrency", "! The ISO three-letter code was PTE; the numeric code was 620.\n        It was divided in 100 centavos.\n\n        Obsoleted by the Euro since 1999.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassSKKCurrency =
        py::class_<QuantLib::SKKCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::SKKCurrency>>
            (m, "SKKCurrency", "! The ISO three-letter code is SKK; the numeric code is 703.\n        It was divided in 100 halierov.\n\n        Obsoleted by the Euro since 2009.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassAUDCurrency =
        py::class_<QuantLib::AUDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::AUDCurrency>>
            (m, "AUDCurrency", "! The ISO three-letter code is AUD; the numeric code is 36.\n        It is divided into 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;


    auto pyClassNZDCurrency =
        py::class_<QuantLib::NZDCurrency, QuantLib::Currency, ext::shared_ptr<QuantLib::NZDCurrency>>
            (m, "NZDCurrency", "! The ISO three-letter code is NZD; the numeric code is 554.\n        It is divided in 100 cents.\n\n        \\ingroup currencies\n")
        .def(py::init<>())
        ;
}