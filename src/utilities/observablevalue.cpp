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
#include <ql/time/date.hpp>
#include <ql/utilities/observablevalue.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_utilities::observablevalue(py::module_& m)
{
    py::class_<QuantLib::ObservableValue<Date>>(m, "ObservableValue_Date",
        "Observable and assignable proxy to a Date value.\n\n"
        "Observers can be registered with instances of this class so that they "
        "are notified when a different value is assigned. Client code can copy "
        "the contained value or pass it to functions via implicit conversion.\n\n"
        "Note: It is not possible to call non-const methods on the returned value. "
        "This is by design, as this would bypass the notification mechanism; "
        "modify the value via re-assignment instead.")
        .def(py::init<>())
        .def(py::init<const Date &>(),
            py::arg("date"))
        .def(py::init<const QuantLib::ObservableValue<Date> &>(),
            py::arg("other"))
        .def("value", &QuantLib::ObservableValue<Date>::value,
            "Returns the current value.")
        ;
}
