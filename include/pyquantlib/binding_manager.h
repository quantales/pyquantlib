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

#include <ql/handle.hpp>
#include <ql/patterns/observable.hpp>
#include <ql/shared_ptr.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <functional>
#include <vector>
#include <string>
#include <unordered_map>

namespace py = pybind11;

/**
 * Orchestrates PyQuantLib module organization and binding registration.
 *
 * The BindingManager provides a clean API structure by organizing QuantLib
 * classes into logical submodules. Abstract base classes are placed in
 * pyquantlib.base while concrete implementations remain in the main module.
 *
 * Usage:
 *   from pyquantlib import Date, SimpleQuote     # concrete classes
 *   from pyquantlib.base import Observer         # abstract classes
 */
class BindingManager {
public:
    using BindingFunction = std::function<void(py::module_&)>;

    /**
     * Constructs a BindingManager for the given module.
     */
    explicit BindingManager(py::module_& module,
                            const std::string& package_name = "pyquantlib")
        : module_(module), package_name_(package_name) {}

    /**
     * Registers a binding function for execution during finalize().
     */
    void addFunction(void (*register_func)(py::module_&),
                     py::module_& target_module,
                     const std::string& description = "") {
        py::object target_copy = target_module;

        bindings_.emplace_back([register_func, target_copy, description]() {
            try {
                py::module_ target = target_copy.cast<py::module_>();
                register_func(target);
            } catch (const std::exception& e) {
                std::string error_msg = "Failed to execute binding";
                if (!description.empty()) {
                    error_msg += " '" + description + "'";
                }
                error_msg += ": " + std::string(e.what());
                throw std::runtime_error(error_msg);
            }
        });
    }

    /**
     * Creates or retrieves a submodule for organizing related classes.
     */
    py::module_ getOrCreateSubmodule(const std::string& name,
                                     const std::string& doc = "") {
        auto it = submodules_.find(name);
        if (it != submodules_.end()) {
            return it->second;
        }

        py::module_ submod = module_.def_submodule(name.c_str(), doc.c_str());
        submodules_[name] = submod;

        // Register in sys.modules for proper Python importing
        std::string full_path = package_name_ + "." + name;
        py::module_ sys = py::module_::import("sys");
        sys.attr("modules")[full_path.c_str()] = submod;
        module_.attr(name.c_str()) = submod;

        return submod;
    }

    /**
     * Retrieves a previously created submodule.
     */
    py::module_ getSubmodule(const std::string& name) const {
        auto it = submodules_.find(name);
        if (it == submodules_.end()) {
            throw std::out_of_range(
                "Submodule not found: " + name +
                ". Did you forget to create it in submodules_bindings()?");
        }
        return it->second;
    }

    /**
     * Executes all registered binding functions.
     */
    void finalize() {
        for (auto& binding : bindings_) {
            binding();
        }
        bindings_.clear();
    }

    py::module_& module() { return module_; }
    const py::module_& module() const { return module_; }
    const std::string& packageName() const { return package_name_; }

private:
    py::module_& module_;
    std::string package_name_;
    std::vector<std::function<void()>> bindings_;
    std::unordered_map<std::string, py::module_> submodules_;
};

// Convenience macro for declaring module binding functions
#define DECLARE_MODULE_BINDINGS(name) void name(BindingManager& manager)

// Helper macros for common binding patterns
#define ADD_BASE_BINDING(manager, register_func, description) \
    manager.addFunction(register_func, manager.getSubmodule("base"), description)

#define ADD_MAIN_BINDING(manager, register_func, description) \
    manager.addFunction(register_func, manager.module(), description)

/**
 * Helper for binding QuantLib Handle<T> types.
 */
template <typename T>
auto bindHandle(py::module_& m,
                const std::string& class_name,
                const std::string& doc_string = "") {
    using HandleType = QuantLib::Handle<T>;

    return py::class_<HandleType>(m, class_name.c_str(), doc_string.c_str())
        .def(py::init<>(), "Creates an empty handle.")
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(),
             py::arg("ptr"),
             py::arg("registerAsObserver") = true,
             "Creates a handle linked to the given object.")
        .def("empty", &HandleType::empty, "Returns true if the handle is empty.")
        .def("__bool__",
             [](const HandleType& h) { return !h.empty(); },
             "Checks if the handle is non-empty.")
        .def("currentLink",
             &HandleType::currentLink,
             "Returns the shared_ptr to the current object link.")
        .def("get",
             [](const HandleType& h) -> QuantLib::ext::shared_ptr<T> {
                 return *h;
             },
             py::return_value_policy::copy,
             "Returns the underlying shared_ptr. Raises error if empty.")
        .def("asObservable",
             [](const HandleType& self) {
                 return QuantLib::ext::shared_ptr<QuantLib::Observable>(self);
             },
             py::return_value_policy::copy,
             "Converts to Observable for observer registration.")
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self);
}

/**
 * Helper for binding QuantLib RelinkableHandle<T> types.
 */
template <typename T>
auto bindRelinkableHandle(py::module_& m,
                          const std::string& class_name,
                          const std::string& doc_string = "") {
    using RelinkableHandleType = QuantLib::RelinkableHandle<T>;
    using HandleType = QuantLib::Handle<T>;

    return py::class_<RelinkableHandleType, HandleType>(
               m, class_name.c_str(), doc_string.c_str())
        .def(py::init<>(), "Creates an empty relinkable handle.")
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(),
             py::arg("ptr"),
             py::arg("registerAsObserver") = true,
             "Creates a relinkable handle linked to the given object.")
        .def("linkTo",
             static_cast<void (RelinkableHandleType::*)(
                 const QuantLib::ext::shared_ptr<T>&, bool)>(
                 &RelinkableHandleType::linkTo),
             py::arg("ptr"),
             py::arg("registerAsObserver") = true,
             "Links the handle to a new object instance. Notifies observers.");
}
