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
#include <ql/math/array.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::array(py::module_& m) {
    py::class_<Array> pyArray(m, "Array", py::buffer_protocol(),
        "1-dimensional array of Real values.");

    // Constructors
    pyArray
        .def(py::init<>(),
            "Default constructor (empty array).")
        .def(py::init<Size>(),
            py::arg("size"),
            "Creates an array of given size.")
        .def(py::init<Size, Real>(),
            py::arg("size"), py::arg("value"),
            "Creates an array of given size with all elements set to value.")
        .def(py::init([](const py::iterable& it) {
                std::vector<Real> vals;
                vals.reserve(py::len_hint(it));
                for (py::handle obj : it) {
                    vals.push_back(obj.cast<Real>());
                }
                if (vals.empty()) {
                    return Array();
                }
                return Array(vals.begin(), vals.end());
            }),
            py::arg("iterable"),
            "Creates an array from a Python iterable.")
        .def(py::init([](py::array_t<Real, py::array::c_style | py::array::forcecast> np_arr) {
                if (np_arr.ndim() != 1) {
                    throw py::type_error("Input NumPy array must be 1-dimensional.");
                }
                Array arr(np_arr.size());
                std::memcpy(arr.begin(), np_arr.data(), np_arr.size() * sizeof(Real));
                return arr;
            }),
            py::arg("numpy_array"),
            "Creates an array from a 1D NumPy array.");

    // Buffer protocol
    pyArray.def_buffer([](Array& a) -> py::buffer_info {
        return py::buffer_info(
            a.begin(),
            sizeof(Real),
            py::format_descriptor<Real>::format(),
            1,
            { a.size() },
            { sizeof(Real) }
        );
    });

    // Size and capacity
    pyArray
        .def("size", &Array::size,
            "Returns the number of elements.")
        .def("empty", &Array::empty,
            "Returns true if the array is empty.")
        .def("resize", [](Array& a, Size n) { a.resize(n); },
            py::arg("size"),
            "Resizes the array.")
        .def("resize", [](Array& a, Size n, Real value) {
                Size old_size = a.size();
                a.resize(n);
                if (n > old_size) {
                    for (Size i = old_size; i < n; ++i) {
                        a[i] = value;
                    }
                }
            },
            py::arg("size"), py::arg("value"),
            "Resizes the array, filling new elements with value.")
        .def("swap", &Array::swap,
            py::arg("other"),
            "Swaps contents with another array.")
        .def("fill", [](Array& a, Real value) { std::fill(a.begin(), a.end(), value); },
            py::arg("value"),
            "Fills the array with a value.");

    // Element access
    pyArray
        .def("__getitem__", [](const Array& a, Size i) {
                if (i >= a.size()) throw py::index_error("Array index out of range");
                return a[i];
            },
            py::arg("i"))
        .def("__setitem__", [](Array& a, Size i, Real value) {
                if (i >= a.size()) throw py::index_error("Array index out of range");
                a[i] = value;
            },
            py::arg("i"), py::arg("value"))
        .def("at", [](const Array& a, Size i) {
                if (a.empty()) throw py::index_error("Array is empty");
                return a.at(i);
            },
            py::arg("i"),
            "Access element with bounds checking.")
        .def("front", [](const Array& a) {
                if (a.empty()) throw py::index_error("Array is empty");
                return a.front();
            },
            "Returns the first element.")
        .def("back", [](const Array& a) {
                if (a.empty()) throw py::index_error("Array is empty");
                return a.back();
            },
            "Returns the last element.");

    // Iteration and length
    pyArray
        .def("__len__", &Array::size)
        .def("__iter__", [](const Array& a) {
                return py::make_iterator(a.begin(), a.end());
            }, py::keep_alive<0, 1>());

    // String representation
    pyArray.def("__repr__", [](const Array& a) {
        std::ostringstream oss;
        oss << "Array([";
        for (Size i = 0; i < a.size(); ++i) {
            if (i > 10 && i < a.size() - 5) {
                oss << "..., ";
                i = a.size() - 6;
                continue;
            }
            oss << a[i];
            if (i < a.size() - 1) oss << ", ";
        }
        oss << "])";
        return oss.str();
    });

    // Operators
    pyArray
        .def(-py::self)
        .def(py::self += py::self)
        .def(py::self -= py::self)
        .def(py::self *= py::self)
        .def(py::self /= py::self)
        .def(py::self += Real())
        .def(py::self -= Real())
        .def(py::self *= Real())
        .def(py::self /= Real())
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def(py::self * py::self)
        .def(py::self / py::self)
        .def(py::self + Real())
        .def(py::self - Real())
        .def(py::self * Real())
        .def(py::self / Real())
        .def(Real() + py::self)
        .def(Real() - py::self)
        .def(Real() * py::self)
        .def(Real() / py::self)
        .def(py::self == py::self)
        .def(py::self != py::self);

    // Mathematical functions
    m.def("DotProduct", static_cast<Real (*)(const Array&, const Array&)>(&DotProduct),
        py::arg("a1"), py::arg("a2"),
        "Returns the dot product of two arrays.");

    m.def("Abs", py::overload_cast<const Array&>(&Abs),
        py::arg("array"),
        "Returns element-wise absolute values.");

    m.def("Sqrt", [](const Array& arr) {
            for (Size i = 0; i < arr.size(); ++i) {
                if (arr[i] < 0.0) {
                    throw py::value_error("Sqrt: negative value at index " + std::to_string(i));
                }
            }
            return Sqrt(arr);
        },
        py::arg("array"),
        "Returns element-wise square roots.");

    m.def("Log", py::overload_cast<const Array&>(&Log),
        py::arg("array"),
        "Returns element-wise natural logarithms.");

    m.def("Exp", py::overload_cast<const Array&>(&Exp),
        py::arg("array"),
        "Returns element-wise exponentials.");

    m.def("Pow", py::overload_cast<const Array&, Real>(&Pow),
        py::arg("array"), py::arg("exponent"),
        "Returns element-wise power.");

    // Enable implicit conversion from Python lists and numpy arrays
    // This allows passing lists/arrays directly to functions expecting Array
    py::implicitly_convertible<py::list, Array>();
    py::implicitly_convertible<py::array, Array>();
}
