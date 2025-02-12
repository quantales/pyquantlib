/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/math/matrix.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/operators.h>
#include <sstream>

namespace py = pybind11;
using namespace QuantLib;

namespace {

std::string matrix_repr(const Matrix& m) {
    if (m.empty()) {
        return "Matrix(" + std::to_string(m.rows()) + ", " +
               std::to_string(m.columns()) + ")";
    }
    std::ostringstream oss;
    oss << "Matrix(" << m.rows() << ", " << m.columns() << ")[\n";

    Size max_rows = 10;
    Size max_cols = 10;

    for (Size i = 0; i < std::min(m.rows(), max_rows); ++i) {
        oss << "  [";
        for (Size j = 0; j < std::min(m.columns(), max_cols); ++j) {
            oss << m(i, j);
            if (j < std::min(m.columns(), max_cols) - 1) oss << ", ";
        }
        if (m.columns() > max_cols) oss << ", ...";
        oss << "]";
        if (i < std::min(m.rows(), max_rows) - 1) oss << ",\n";
    }
    if (m.rows() > max_rows) oss << "\n  ...";
    oss << "\n]";
    return oss.str();
}

} // anonymous namespace

void ql_math::matrix(py::module_& m) {
    py::class_<Matrix, ext::shared_ptr<Matrix>>(m, "Matrix", py::buffer_protocol(),
        "2-dimensional matrix of Real values.")

        // Constructors
        .def(py::init<>(),
            "Default constructor (empty matrix).")
        .def(py::init<Size, Size>(),
            py::arg("rows"), py::arg("columns"),
            "Creates a zero-filled matrix.")
        .def(py::init<Size, Size, Real>(),
            py::arg("rows"), py::arg("columns"), py::arg("value"),
            "Creates a matrix filled with value.")
        .def(py::init([](py::array_t<Real, py::array::c_style | py::array::forcecast> arr) {
                if (arr.ndim() != 2) {
                    throw py::value_error("Input array must be 2-dimensional.");
                }
                Size rows = arr.shape(0);
                Size cols = arr.shape(1);
                auto mat = ext::make_shared<Matrix>(rows, cols);
                if (rows > 0 && cols > 0) {
                    const Real* data = arr.data();
                    for (Size i = 0; i < rows; ++i) {
                        for (Size j = 0; j < cols; ++j) {
                            (*mat)[i][j] = data[i * cols + j];
                        }
                    }
                }
                return mat;
            }),
            py::arg("numpy_array"),
            "Creates a matrix from a 2D NumPy array.")
        .def(py::init([](const py::list& rows_list) {
                if (rows_list.empty()) {
                    return ext::make_shared<Matrix>();
                }
                if (!py::isinstance<py::list>(rows_list[0])) {
                    throw py::type_error("Input must be a list of lists.");
                }
                Size num_rows = rows_list.size();
                Size num_cols = rows_list[0].cast<py::list>().size();
                auto mat = ext::make_shared<Matrix>(num_rows, num_cols);
                for (Size i = 0; i < num_rows; ++i) {
                    if (!py::isinstance<py::list>(rows_list[i])) {
                        throw py::type_error("All elements of the outer list must be lists.");
                    }
                    const py::list& row = rows_list[i].cast<const py::list&>();
                    if (row.size() != num_cols) {
                        throw py::value_error("Inconsistent number of columns in input lists.");
                    }
                    for (Size j = 0; j < num_cols; ++j) {
                        (*mat)[i][j] = row[j].cast<Real>();
                    }
                }
                return mat;
            }),
            py::arg("list_of_lists"),
            "Creates a matrix from a list of lists.")

        // Properties
        .def("rows", &Matrix::rows,
            "Returns the number of rows.")
        .def("columns", &Matrix::columns,
            "Returns the number of columns.")
        .def_property_readonly("shape", [](const Matrix& m) {
                return py::make_tuple(m.rows(), m.columns());
            },
            "Returns (rows, columns) tuple.")
        .def("empty", &Matrix::empty,
            "Returns true if the matrix is empty.")

        // Element access
        .def("__getitem__", [](Matrix& m, Size row) -> py::array_t<Real> {
                if (row >= m.rows()) {
                    throw py::index_error("Row index out of bounds");
                }
                Real* row_ptr = (m.columns() > 0) ? m[row] : nullptr;
                return py::array_t<Real>(
                    {m.columns()},
                    {sizeof(Real)},
                    row_ptr,
                    py::cast(m)
                );
            }, py::is_operator(),
            "Gets a row as a NumPy array view.")
        .def("__getitem__", [](const Matrix& m, std::pair<Size, Size> p) {
                if (p.first >= m.rows() || p.second >= m.columns()) {
                    throw py::index_error("Index out of bounds");
                }
                return m(p.first, p.second);
            }, py::is_operator(),
            "Gets element at (row, column).")
        .def("__setitem__", [](Matrix& m, std::pair<Size, Size> p, Real value) {
                if (p.first >= m.rows() || p.second >= m.columns()) {
                    throw py::index_error("Index out of bounds");
                }
                m[p.first][p.second] = value;
            }, py::is_operator(),
            "Sets element at (row, column).")

        // Iteration
        .def("__iter__", [](const Matrix& m) {
                return py::make_iterator(m.begin(), m.end(),
                    py::return_value_policy::reference_internal);
            }, py::keep_alive<0, 1>(),
            "Iterates over elements in row-major order.")

        // Buffer protocol
        .def_buffer([](Matrix& m) -> py::buffer_info {
            return py::buffer_info(
                m.begin(),
                sizeof(Real),
                py::format_descriptor<Real>::format(),
                2,
                {m.rows(), m.columns()},
                {sizeof(Real) * m.columns(), sizeof(Real)}
            );
        })

        // Methods
        .def("swap", &Matrix::swap,
            py::arg("other"),
            "Swaps contents with another matrix.")
        .def("diagonal", &Matrix::diagonal,
            "Returns the diagonal as an Array.")
        .def("column", [](const Matrix& m, Size j) {
                if (j >= m.columns()) {
                    throw py::index_error("Column index out of bounds");
                }
                Array col(m.rows());
                for (Size i = 0; i < m.rows(); ++i) {
                    col[i] = m(i, j);
                }
                return col;
            },
            py::arg("index"),
            "Returns a column as an Array.")

        // Operators
        .def(py::self += py::self)
        .def(py::self -= py::self)
        .def(py::self *= Real())
        .def("__itruediv__", [](Matrix& m, Real x) -> Matrix& {
                if (x == 0.0) throw py::value_error("division by zero");
                m /= x;
                return m;
            }, py::is_operator())
        .def(py::self + py::self)
        .def(py::self - py::self)
        .def(py::self * py::self)
        .def(py::self * Real())
        .def(Real() * py::self)
        .def("__truediv__", [](const Matrix& m, Real x) {
                if (x == 0.0) throw py::value_error("division by zero");
                return m / x;
            }, py::is_operator())

        // String representation
        .def("__repr__", &matrix_repr)
        .def("__str__", &matrix_repr);

    // Free functions
    m.def("outerProduct", static_cast<Matrix (*)(const Array&, const Array&)>(&outerProduct),
        py::arg("a1"), py::arg("a2"),
        "Returns the outer product of two arrays.");
    m.def("transpose", &transpose,
        py::arg("matrix"),
        "Returns the transpose of a matrix.");
}
