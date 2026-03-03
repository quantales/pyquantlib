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

#pragma once

#include <ql/math/interpolation.hpp>
#include <ql/math/interpolations/interpolation2d.hpp>
#include <ql/shared_ptr.hpp>
#include <ql/errors.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>

namespace py = pybind11;
using namespace QuantLib;

namespace pyquantlib {
namespace detail {

    /**
     * Data holder that serves as a custom deleter for shared_ptr.
     *
     * This struct stores the x and y vectors that QuantLib interpolations
     * reference via iterators. By using it as a shared_ptr deleter, the data
     * lifetime is tied to the interpolation object's lifetime.
     *
     * The templated operator() allows this single struct to work with any
     * interpolation type.
     */
    struct InterpolationDataHolder {
        std::vector<Real> x, y;

        template <typename T>
        void operator()(T* p) const {
            delete p;
        }
    };

} // namespace detail

/**
 * Creates a safe shared_ptr for any interpolation type.
 *
 * This function handles the data lifetime issue by:
 * 1. Moving the input vectors into an InterpolationDataHolder
 * 2. Constructing the interpolation using iterators to the holder's data
 * 3. Returning a shared_ptr with the holder as a custom deleter
 *
 * The holder lives in the shared_ptr's control block, ensuring the data
 * outlives the interpolation.
 *
 * @tparam T The interpolation type (e.g., LinearInterpolation)
 * @tparam Args Additional constructor argument types
 * @param x The x values (will be moved)
 * @param y The y values (will be moved)
 * @param requiredPoints Minimum number of points required
 * @param args Additional constructor arguments (forwarded)
 * @return A shared_ptr to the interpolation with safe data lifetime
 */
template <typename T, typename... Args>
ext::shared_ptr<T> make_safe_interpolation(
    std::vector<Real> x,
    std::vector<Real> y,
    Size requiredPoints,
    Args&&... args)
{
    QL_REQUIRE(x.size() == y.size(), "x and y must have the same size");
    QL_REQUIRE(x.size() >= requiredPoints,
               "at least " << requiredPoints << " points required, "
               << x.size() << " provided");

    detail::InterpolationDataHolder holder{std::move(x), std::move(y)};

    auto* ptr = new T(
        holder.x.begin(), holder.x.end(), holder.y.begin(),
        std::forward<Args>(args)...
    );

    return ext::shared_ptr<T>(ptr, std::move(holder));
}

/**
 * Binds a simple interpolation class with the standard (x, y) constructor.
 *
 * This template function creates a pybind11 class binding for interpolation
 * types that only require x and y arrays. It automatically handles the data
 * lifetime issue using the custom deleter pattern.
 *
 * @tparam T The interpolation type
 * @tparam RequiredPoints Minimum number of points (default: 2)
 * @param m The pybind11 module
 * @param name The Python class name
 * @param doc The docstring
 */
template <typename T, Size RequiredPoints = 2>
void bind_simple_interpolation(
    py::module_& m,
    const char* name,
    const char* doc)
{
    py::class_<T, Interpolation, ext::shared_ptr<T>>(m, name, doc)
        .def(py::init([](std::vector<Real> x, std::vector<Real> y) {
            return make_safe_interpolation<T>(
                std::move(x), std::move(y), RequiredPoints);
        }),
        py::arg("x"), py::arg("y"),
        "Constructs interpolation from x and y arrays.");
}

// ---------------------------------------------------------------------------
// 2-D interpolation helpers
// ---------------------------------------------------------------------------

namespace detail {

    /**
     * Data holder for 2-D interpolations.
     *
     * Stores x, y vectors and a heap-allocated Matrix. The Matrix must be
     * heap-allocated because Interpolation2D::templateImpl stores
     * `const M& zData_` (a reference), so it needs a stable address.
     */
    struct Interpolation2DDataHolder {
        std::vector<Real> x, y;
        ext::shared_ptr<Matrix> z;

        template <typename T>
        void operator()(T* p) const {
            delete p;
        }
    };

} // namespace detail

/**
 * Creates a safe shared_ptr for any 2-D interpolation type.
 *
 * @tparam T The 2-D interpolation type (e.g., BilinearInterpolation)
 * @param x The x values (will be moved)
 * @param y The y values (will be moved)
 * @param z The z matrix (will be copied to heap)
 * @param requiredPoints Minimum points in each dimension
 * @return A shared_ptr to the interpolation with safe data lifetime
 */
template <typename T>
ext::shared_ptr<T> make_safe_interpolation2d(
    std::vector<Real> x,
    std::vector<Real> y,
    const Matrix& z,
    Size requiredPoints = 2)
{
    QL_REQUIRE(x.size() >= requiredPoints && y.size() >= requiredPoints,
               "at least " << requiredPoints
               << " points required in each dimension");
    QL_REQUIRE(z.rows() == y.size() && z.columns() == x.size(),
               "z matrix dimensions must match: "
               "rows = y.size(), columns = x.size()");

    auto zPtr = ext::make_shared<Matrix>(z);
    detail::Interpolation2DDataHolder holder{
        std::move(x), std::move(y), zPtr};

    auto* ptr = new T(
        holder.x.begin(), holder.x.end(),
        holder.y.begin(), holder.y.end(),
        *holder.z);

    return ext::shared_ptr<T>(ptr, std::move(holder));
}

/**
 * Binds a simple 2-D interpolation class with the (x, y, z) constructor.
 *
 * Returns the py::class_ object so callers can chain additional .def() calls
 * (e.g., derivative methods on BicubicSpline).
 *
 * @tparam T The 2-D interpolation type
 * @tparam RequiredPoints Minimum points in each dimension (default: 2)
 * @param m The pybind11 module
 * @param name The Python class name
 * @param doc The docstring
 */
template <typename T, Size RequiredPoints = 2>
py::class_<T, Interpolation2D, ext::shared_ptr<T>>
bind_simple_interpolation2d(
    py::module_& m,
    const char* name,
    const char* doc)
{
    return py::class_<T, Interpolation2D, ext::shared_ptr<T>>(m, name, doc)
        .def(py::init([](std::vector<Real> x, std::vector<Real> y,
                         const Matrix& z) {
            return make_safe_interpolation2d<T>(
                std::move(x), std::move(y), z, RequiredPoints);
        }),
        py::arg("x"), py::arg("y"), py::arg("z"),
        "Constructs from x, y arrays and z matrix.");
}

} // namespace pyquantlib
