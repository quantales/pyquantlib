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
    ADD_MAIN_BINDING(ql_methods::boundarycondition,
        "FdmBoundaryCondition - boundary condition for FDM operators");
    ADD_MAIN_BINDING(ql_methods::fdmlinearop,
        "FdmLinearOp - abstract FDM linear operator");
    ADD_MAIN_BINDING(ql_methods::fdmlinearopcomposite,
        "FdmLinearOpComposite - composite FDM linear operator");
    ADD_MAIN_BINDING(ql_methods::triplebandlinearop,
        "TripleBandLinearOp - tridiagonal linear operator");
    ADD_MAIN_BINDING(ql_methods::firstderivativeop,
        "FirstDerivativeOp - first derivative operator");
    ADD_MAIN_BINDING(ql_methods::secondderivativeop,
        "SecondDerivativeOp - second derivative operator");
    ADD_MAIN_BINDING(ql_methods::ninepointlinearop,
        "NinePointLinearOp - nine-point 2D linear operator");
    ADD_MAIN_BINDING(ql_methods::secondordermixedderivativeop,
        "SecondOrderMixedDerivativeOp - mixed derivative operator");
    ADD_MAIN_BINDING(ql_methods::fdmsquarerootfwdop,
        "FdmSquareRootFwdOp and TransformationType enum");
    ADD_MAIN_BINDING(ql_methods::fdmblackscholesop,
        "FdmBlackScholesOp - Black-Scholes FDM operator");
    ADD_MAIN_BINDING(ql_methods::fdmblackscholesfwdop,
        "FdmBlackScholesFwdOp - Black-Scholes forward operator");
    ADD_MAIN_BINDING(ql_methods::fdm2dblackscholesop,
        "Fdm2dBlackScholesOp - 2D Black-Scholes operator");
    ADD_MAIN_BINDING(ql_methods::fdmhestonop,
        "FdmHestonOp - Heston stochastic volatility operator");
    ADD_MAIN_BINDING(ql_methods::fdmhestonfwdop,
        "FdmHestonFwdOp - Heston forward operator");
    ADD_MAIN_BINDING(ql_methods::fdmhestonhullwhiteop,
        "FdmHestonHullWhiteOp - Heston-Hull-White operator");
    ADD_MAIN_BINDING(ql_methods::fdmbatesop,
        "FdmBatesOp - Bates jump-diffusion operator");
    ADD_MAIN_BINDING(ql_methods::fdmhullwhiteop,
        "FdmHullWhiteOp - Hull-White interest rate operator");
    ADD_MAIN_BINDING(ql_methods::fdmg2op,
        "FdmG2Op - G2++ two-factor interest rate operator");
    ADD_MAIN_BINDING(ql_methods::fdmcevop,
        "FdmCEVOp - constant elasticity of variance operator");
    ADD_MAIN_BINDING(ql_methods::fdmsabrop,
        "FdmSabrOp - SABR stochastic volatility operator");
    ADD_MAIN_BINDING(ql_methods::fdmlocalvolfwdop,
        "FdmLocalVolFwdOp - local volatility forward operator");
    ADD_MAIN_BINDING(ql_methods::fdmornsteinuhlenbeckop,
        "FdmOrnsteinUhlenbeckOp - Ornstein-Uhlenbeck operator");
    ADD_MAIN_BINDING(ql_methods::expliciteulerscheme,
        "ExplicitEulerScheme - explicit Euler time stepping");
    ADD_MAIN_BINDING(ql_methods::impliciteulerscheme,
        "ImplicitEulerScheme - implicit Euler time stepping");
    ADD_MAIN_BINDING(ql_methods::cranknicolsonscheme,
        "CrankNicolsonScheme - Crank-Nicolson time stepping");
    ADD_MAIN_BINDING(ql_methods::douglasscheme,
        "DouglasScheme - Douglas ADI time stepping");
    ADD_MAIN_BINDING(ql_methods::craigsneydscheme,
        "CraigSneydScheme - Craig-Sneyd ADI time stepping");
    ADD_MAIN_BINDING(ql_methods::hundsdorferscheme,
        "HundsdorferScheme - Hundsdorfer ADI time stepping");
    ADD_MAIN_BINDING(ql_methods::modifiedcraigsneydscheme,
        "ModifiedCraigSneydScheme - modified Craig-Sneyd ADI");
    ADD_MAIN_BINDING(ql_methods::methodoflinesscheme,
        "MethodOfLinesScheme - method of lines time stepping");
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
