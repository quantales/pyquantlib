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

#pragma once

#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>
#include <stdexcept>
#include <string>
#include <typeinfo>

namespace py = pybind11;

/**
 * Converts a Python object to a QuantLib type, handling Null values.
 * Accepts None, Null<T>, or a direct T value.
 */
template <typename T>
T from_python_with_null(const py::object& obj) {
    if (obj.is_none()) {
        return QuantLib::Null<T>();
    }
    try {
        return obj.cast<T>();
    } catch (const py::cast_error&) {
        try {
            auto null_obj = obj.cast<QuantLib::Null<T>>();
            return static_cast<T>(null_obj);
        } catch (const py::cast_error&) {
            throw std::runtime_error("Expected " +
                                     std::string(typeid(T).name()) +
                                     ", None, or Null object");
        }
    }
}

/**
 * Checks if a Python object represents a Null value.
 */
template <typename T>
bool is_null(const py::object& obj) {
    if (obj.is_none()) {
        return true;
    }
    try {
        obj.cast<QuantLib::Null<T>>();
        return true;
    } catch (const py::cast_error&) {
        return false;
    }
}
