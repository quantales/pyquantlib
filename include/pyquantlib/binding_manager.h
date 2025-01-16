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

#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <functional>
#include <vector>
#include <string>
#include <unordered_map>

namespace py = pybind11;

/**
 * @brief Orchestrates PyQuantLib module organization and binding registration.
 * 
 * The BindingManager provides a clean API structure by organizing QuantLib classes
 * into logical submodules. Abstract base classes are placed in pyquantlib.base 
 * while concrete implementations remain in the main module.
 * 
 * This ensures users can easily find the classes they need:
 * - `from pyquantlib import Date, SimpleQuote` (concrete classes)
 * - `from pyquantlib.base import Observer` (abstract classes for inheritance)
 * 
 * @note This class is part of PyQuantLib's internal architecture and is primarily
 *       of interest to contributors adding new QuantLib bindings.
 */
class BindingManager {
public:
    using BindingFunction = std::function<void(py::module_&)>;

    /**
     * @brief Constructs a BindingManager for the given module.
     * 
     * @param module The main pybind11 module (typically _pyquantlib)
     * @param package_name Package name for submodule registration (default: "pyquantlib")
     */
    explicit BindingManager(py::module_& module, const std::string& package_name = "pyquantlib")
        : module_(module), package_name_(package_name) {}

    /**
     * @brief Registers a binding function for execution during finalize().
     * 
     * This is the primary method for adding QuantLib class bindings to PyQuantLib.
     * Functions are executed in registration order, so ensure base classes are
     * registered before derived classes.
     * 
     * @param register_func Function containing pybind11 binding code
     * @param target_module Module where classes should be registered
     * @param description Human-readable description for error reporting
     * 
     * @example
     * ```cpp
     * manager.addFunction(ql_core::quote, base_module, "Quote ABC");
     * manager.addFunction(ql_core::simple_quote, main_module, "SimpleQuote implementation");
     * ```
     */
    void addFunction(void(*register_func)(py::module_&), py::module_& target_module, 
                     const std::string& description = "") {
        // Copy module safely to avoid lifetime issues
        py::object target_copy = target_module;
        
        bindings_.emplace_back([register_func, target_copy, description]() {
            try {
                // Store cast result in local variable to avoid binding
                // non-const reference to temporary (MSVC C4239)
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
     * @brief Creates or retrieves a submodule for organizing related classes.
     * 
     * Submodules provide logical organization within PyQuantLib. The most common
     * use case is the "base" submodule for abstract base classes that users
     * typically inherit from rather than instantiate directly.
     * 
     * @param name Submodule name (must be a valid Python identifier)
     * @param doc Documentation string shown in Python help()
     * @return The created or existing submodule
     * 
     * @throws std::invalid_argument if name is empty or invalid
     * 
     * @example
     * ```cpp
     * auto base = manager.getOrCreateSubmodule("base", "Abstract base classes");
     * ```
     */
    py::module_ getOrCreateSubmodule(const std::string& name, const std::string& doc = "") {
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
     * @brief Retrieves a previously created submodule.
     * 
     * @param name Submodule name to retrieve
     * @return The existing submodule
     * @throws std::out_of_range if submodule was not previously created
     * 
     * @note Submodules should be created in submodules_bindings() before use
     */
    py::module_ getSubmodule(const std::string& name) const {
        auto it = submodules_.find(name);
        if (it == submodules_.end()) {
            throw std::out_of_range("Submodule not found: " + name + 
                                   ". Did you forget to create it in submodules_bindings()?");
        }
        return it->second;
    }

    /**
     * @brief Executes all registered binding functions.
     * 
     * This method should be called exactly once after all modules have been
     * registered via addFunction(). Binding functions are executed in the order
     * they were registered.
     * 
     * @warning Ensure module binding functions are registered in dependency order:
     *          base classes before derived classes, core modules before dependent modules.
     */
    void finalize() {
        for (auto& binding : bindings_) {
            binding();
        }
        bindings_.clear();  // Allow multiple finalize() calls
    }

    /**
     * @brief Access the main pybind11 module.
     * @return Reference to the main module where most classes are registered
     */
    py::module_& module() { return module_; }
    
    /** @brief Const access to the main module. */
    const py::module_& module() const { return module_; }

    /**
     * @brief Get the package name used for submodule registration.
     * @return The package name (typically "pyquantlib")
     */
    const std::string& packageName() const { return package_name_; }

private:
    py::module_& module_;
    std::string package_name_;
    std::vector<std::function<void()>> bindings_;
    std::unordered_map<std::string, py::module_> submodules_;
};

/**
 * @brief Convenience macro for declaring module binding functions.
 * 
 * This macro standardizes the signature of module binding functions throughout
 * PyQuantLib. Each QuantLib module (patterns, time, math, etc.) should use this
 * macro to declare its main binding function.
 * 
 * @param name Function name (typically ends with "_bindings")
 * 
 * @example
 * ```cpp
 * DECLARE_MODULE_BINDINGS(core_bindings) {
 *     auto base = manager.getOrCreateSubmodule("base", "Abstract base classes");
 *     manager.addFunction(ql_core::quote, base, "Quote ABC");
 *     manager.addFunction(ql_core::simple_quote, manager.module(), "SimpleQuote");
 * }
 * ```
 */
#define DECLARE_MODULE_BINDINGS(name) \
    void name(BindingManager& manager)

/**
 * @brief Helper macros for common binding patterns.
 * 
 * These macros reduce boilerplate when registering classes in standard locations.
 * Most abstract base classes go to the "base" submodule, while concrete
 * implementations go to the main module.
 */
#define ADD_BASE_BINDING(manager, register_func, description) \
    manager.addFunction(register_func, manager.getSubmodule("base"), description)

#define ADD_MAIN_BINDING(manager, register_func, description) \
    manager.addFunction(register_func, manager.module(), description)

/**
 * @brief Helper for binding QuantLib Handle<T> types.
 * 
 * Provides the complete Handle<T> interface including constructors, empty(),
 * currentLink(), get(), asObservable(), and comparison operators. This eliminates
 * boilerplate code when binding Handle specializations.
 * 
 * @tparam T The underlying QuantLib type (e.g., Quote, SimpleQuote, YieldTermStructure)
 * @param m Target module for registration
 * @param class_name Python class name (e.g., "QuoteHandle", "SimpleQuoteHandle")  
 * @param doc_string Documentation string for the class
 * @return pybind11 class object for additional customization
 * 
 * @example
 * ```cpp
 * void ql_core::quotehandle(py::module_& m) {
 *     bindHandle<QuantLib::Quote>(m, "QuoteHandle", "Handle to Quote objects");
 * }
 * ```
 */
template<typename T>
auto bindHandle(py::module_& m, const std::string& class_name, const std::string& doc_string = "") {
    using HandleType = QuantLib::Handle<T>;
    
    return py::class_<HandleType>(m, class_name.c_str(), doc_string.c_str())
        .def(py::init<>(), "Creates an empty handle.")
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(), 
            py::arg("ptr"), py::arg("registerAsObserver") = true,
            "Creates a handle linked to the given object.")
        .def("empty", &HandleType::empty, 
            "Returns true if the handle is empty.")
        .def("__bool__", [](const HandleType& h) { return !h.empty(); },
            "Checks if the handle is non-empty.")
        .def("currentLink", &HandleType::currentLink,
            "Returns the shared_ptr to the current object link.")
        .def("get", [](const HandleType& h) -> QuantLib::ext::shared_ptr<T> { return *h; },
            py::return_value_policy::copy,
            "Returns the underlying shared_ptr. Raises error if empty.")
        .def("asObservable", [](const HandleType& self) {
            return QuantLib::ext::shared_ptr<QuantLib::Observable>(self);
        }, py::return_value_policy::copy,
            "Converts to Observable for observer registration.")
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self);
}

/**
 * @brief Helper for binding QuantLib RelinkableHandle<T> types.
 * 
 * Provides the complete RelinkableHandle<T> interface including inheritance from
 * Handle<T> and the additional linkTo() method for relinking to new objects.
 * 
 * @tparam T The underlying QuantLib type (e.g., Quote, SimpleQuote, YieldTermStructure)
 * @param m Target module for registration
 * @param class_name Python class name (e.g., "RelinkableQuoteHandle")
 * @param doc_string Documentation string for the class
 * @return pybind11 class object for additional customization
 * 
 * @example
 * ```cpp
 * void ql_core::relinkablequotehandle(py::module_& m) {
 *     bindRelinkableHandle<QuantLib::Quote>(m, "RelinkableQuoteHandle",
 *                                           "Relinkable handle to Quote objects");
 * }
 * ```
 */
template<typename T>
auto bindRelinkableHandle(py::module_& m, const std::string& class_name, const std::string& doc_string = "") {
    using RelinkableHandleType = QuantLib::RelinkableHandle<T>;
    using HandleType = QuantLib::Handle<T>;
    
    return py::class_<RelinkableHandleType, HandleType>(m, class_name.c_str(), doc_string.c_str())
        .def(py::init<>(), "Creates an empty relinkable handle.")
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(),
            py::arg("ptr"), py::arg("registerAsObserver") = true,
            "Creates a relinkable handle linked to the given object.")
        .def("linkTo",
            static_cast<void (RelinkableHandleType::*)(const QuantLib::ext::shared_ptr<T>&, bool)>(&RelinkableHandleType::linkTo),
            py::arg("ptr"), py::arg("registerAsObserver") = true,
            "Links the handle to a new object instance. Notifies observers.");
}
