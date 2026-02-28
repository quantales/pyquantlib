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
#include <ql/models/shortrate/onefactormodels/gaussian1dmodel.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::gaussian1dmodel(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // Gaussian1dModel ABC
    py::class_<Gaussian1dModel, TermStructureConsistentModel, LazyObject,
               ext::shared_ptr<Gaussian1dModel>>(
        base, "Gaussian1dModel",
        "Abstract base class for Gaussian 1-D short-rate models.")
        .def("stateProcess", &Gaussian1dModel::stateProcess,
            "Returns the state process.")
        // numeraire overloads
        .def("numeraire",
            py::overload_cast<Time, Real, const Handle<YieldTermStructure>&>(
                &Gaussian1dModel::numeraire, py::const_),
            py::arg("t"), py::arg("y") = 0.0,
            py::arg("yts") = Handle<YieldTermStructure>(),
            "Returns numeraire at time t for state y.")
        .def("numeraire",
            py::overload_cast<const Date&, Real, const Handle<YieldTermStructure>&>(
                &Gaussian1dModel::numeraire, py::const_),
            py::arg("referenceDate"), py::arg("y") = 0.0,
            py::arg("yts") = Handle<YieldTermStructure>(),
            "Returns numeraire at date for state y.")
        // zerobond overloads
        .def("zerobond",
            py::overload_cast<Time, Time, Real, const Handle<YieldTermStructure>&>(
                &Gaussian1dModel::zerobond, py::const_),
            py::arg("T"), py::arg("t") = 0.0, py::arg("y") = 0.0,
            py::arg("yts") = Handle<YieldTermStructure>(),
            "Returns zero-coupon bond price P(T) at time t for state y.")
        .def("zerobond",
            py::overload_cast<const Date&, const Date&, Real,
                              const Handle<YieldTermStructure>&>(
                &Gaussian1dModel::zerobond, py::const_),
            py::arg("maturity"), py::arg("referenceDate") = Date(),
            py::arg("y") = 0.0,
            py::arg("yts") = Handle<YieldTermStructure>(),
            "Returns zero-coupon bond price at maturity date.")
        // zerobondOption
        .def("zerobondOption", &Gaussian1dModel::zerobondOption,
            py::arg("type"), py::arg("expiry"), py::arg("valueDate"),
            py::arg("maturity"), py::arg("strike"),
            py::arg("referenceDate") = Date(), py::arg("y") = 0.0,
            py::arg("yts") = Handle<YieldTermStructure>(),
            py::arg("yStdDevs") = 7.0, py::arg("yGridPoints") = 64,
            py::arg("extrapolatePayoff") = true,
            py::arg("flatPayoffExtrapolation") = false,
            "Returns zero-coupon bond option price.")
        // forwardRate
        .def("forwardRate", &Gaussian1dModel::forwardRate,
            py::arg("fixing"), py::arg("referenceDate") = Date(),
            py::arg("y") = 0.0,
            py::arg("iborIdx") = ext::shared_ptr<IborIndex>(),
            "Returns forward rate for fixing date.")
        // swapRate
        .def("swapRate", &Gaussian1dModel::swapRate,
            py::arg("fixing"), py::arg("tenor"),
            py::arg("referenceDate") = Date(), py::arg("y") = 0.0,
            py::arg("swapIdx") = ext::shared_ptr<SwapIndex>(),
            "Returns swap rate for fixing date and tenor.")
        // swapAnnuity
        .def("swapAnnuity", &Gaussian1dModel::swapAnnuity,
            py::arg("fixing"), py::arg("tenor"),
            py::arg("referenceDate") = Date(), py::arg("y") = 0.0,
            py::arg("swapIdx") = ext::shared_ptr<SwapIndex>(),
            "Returns swap annuity for fixing date and tenor.")
        // yGrid
        .def("yGrid", &Gaussian1dModel::yGrid,
            py::arg("yStdDevs"), py::arg("gridPoints"),
            py::arg("T") = 1.0, py::arg("t") = 0.0, py::arg("y") = 0.0,
            "Returns state variable grid.")
        // static methods
        .def_static("gaussianPolynomialIntegral",
            &Gaussian1dModel::gaussianPolynomialIntegral,
            py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"),
            py::arg("e"), py::arg("x0"), py::arg("x1"),
            "Computes Gaussian polynomial integral.")
        .def_static("gaussianShiftedPolynomialIntegral",
            &Gaussian1dModel::gaussianShiftedPolynomialIntegral,
            py::arg("a"), py::arg("b"), py::arg("c"), py::arg("d"),
            py::arg("e"), py::arg("h"), py::arg("x0"), py::arg("x1"),
            "Computes shifted Gaussian polynomial integral.");

    // Handle<Gaussian1dModel>
    bindHandle<Gaussian1dModel>(m, "Gaussian1dModelHandle",
        "Handle to a Gaussian 1-D model.");
}
