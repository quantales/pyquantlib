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

DECLARE_MODULE_BINDINGS(methods_bindings) {
    // finitedifferences
    ADD_MAIN_BINDING(ql_methods::fdmbackwardsolver,
        "FdmSchemeDesc and FdmSchemeType from fdmbackwardsolver.hpp");
    ADD_MAIN_BINDING(ql_methods::fdmhestongreensfct,
        "FdmHestonGreensFctAlgorithm - Heston Green's function algorithm enum");
    ADD_MAIN_BINDING(ql_methods::fdmsquarerootfwdop,
        "FdmSquareRootFwdOpTransformationType - square-root FD transformation enum");
    ADD_MAIN_BINDING(ql_methods::fdmlinearopiterator,
        "FdmLinearOpIterator - iterator for FDM linear operator layout");
    ADD_MAIN_BINDING(ql_methods::fdmlinearoplayout,
        "FdmLinearOpLayout - memory layout of FDM linear operator");
    ADD_MAIN_BINDING(ql_methods::fdm1dmesher,
        "Fdm1dMesher - base class for 1D FDM meshers");
    ADD_MAIN_BINDING(ql_methods::uniform1dmesher,
        "Uniform1dMesher - uniform grid mesher");
    ADD_MAIN_BINDING(ql_methods::concentrating1dmesher,
        "Concentrating1dMesher - grid concentrating around critical points");
    ADD_MAIN_BINDING(ql_methods::predefined1dmesher,
        "Predefined1dMesher - mesher from predefined points");
    ADD_MAIN_BINDING(ql_methods::fdmquantohelper,
        "FdmQuantoHelper - quanto adjustment helper");
    ADD_MAIN_BINDING(ql_methods::fdmblackscholesmesher,
        "FdmBlackScholesMesher - Black-Scholes process mesher");
    ADD_MAIN_BINDING(ql_methods::fdmhestonvariancemesher,
        "FdmHestonVarianceMesher and FdmHestonLocalVolatilityVarianceMesher");
    ADD_MAIN_BINDING(ql_methods::fdmcev1dmesher,
        "FdmCEV1dMesher - CEV model mesher");
    ADD_MAIN_BINDING(ql_methods::fdmsimpleprocess1dmesher,
        "FdmSimpleProcess1dMesher - generic 1D process mesher");
    ADD_MAIN_BINDING(ql_methods::fdmmesher,
        "FdmMesher - abstract multi-dimensional mesher");
    ADD_MAIN_BINDING(ql_methods::fdmmeshercomposite,
        "FdmMesherComposite - composite multi-dimensional mesher");
    // Monte Carlo
    ADD_MAIN_BINDING(ql_methods::lsmbasissystem,
        "LsmBasisSystem - polynomial type enum for LSM basis systems");
    ADD_MAIN_BINDING(ql_methods::path,
        "Path - single-factor random walk");
    ADD_MAIN_BINDING(ql_methods::multipath,
        "MultiPath - correlated multiple asset paths");
    ADD_MAIN_BINDING(ql_methods::sample,
        "Sample - weighted sample types for MC simulation");
    ADD_MAIN_BINDING(ql_methods::brownianbridge,
        "BrownianBridge - Brownian bridge path construction");
    ADD_MAIN_BINDING(ql_methods::pathgenerator,
        "PathGenerator - single-factor path generation");
    ADD_MAIN_BINDING(ql_methods::multipathgenerator,
        "MultiPathGenerator - multi-factor path generation");
}
