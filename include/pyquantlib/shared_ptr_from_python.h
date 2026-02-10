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

#include <ql/shared_ptr.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

/**
 * Creates a shared_ptr<T> from a Python object.
 *
 * Defensive bridge for extracting shared_ptr<T> from Python objects that
 * may use py::classh (smart_holder). Sidesteps known pybind11 smart_holder
 * bugs with diamond/virtual inheritance (see pybind11 PR #5836).
 *
 * MECHANISM:
 * 1. Extracts the raw pointer T* via obj.cast<T*>(), which uses pybind11's
 *    registered cast functions and correctly handles virtual base offsets.
 * 2. Wraps it in a shared_ptr with a custom deleter that captures the
 *    py::object by value, preventing GC while the shared_ptr is alive.
 * 3. The deleter acquires the GIL to safely decrement the Python refcount.
 */
template <typename T>
QuantLib::ext::shared_ptr<T> shared_ptr_from_python(py::object obj) {
    if (obj.is_none()) {
        return QuantLib::ext::shared_ptr<T>();
    }

    T* ptr = obj.cast<T*>();

    // Capturing 'obj' by value increments its refcount, keeping the
    // Python object (and its C++ payload) alive while the shared_ptr exists.
    return QuantLib::ext::shared_ptr<T>(ptr, [obj](T*) mutable {
        py::gil_scoped_acquire gil;
        obj = py::object();
    });
}
