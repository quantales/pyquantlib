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


DECLARE_MODULE_BINDINGS(math_bindings) {
    ADD_MAIN_BINDING(ql_math::array, "Mathematical array for vector operations");
    ADD_MAIN_BINDING(ql_math::matrix, "Mathematical matrix for linear algebra");
    ADD_MAIN_BINDING(ql_math::rounding, "Rounding conventions");
    ADD_BASE_BINDING(ql_math::constraint, "Constraint ABC");
    ADD_MAIN_BINDING(ql_math::constraints, "Concrete constraint implementations");
    ADD_BASE_BINDING(ql_math::costfunction, "CostFunction ABC");
    ADD_BASE_BINDING(ql_math::optimizationmethod, "OptimizationMethod ABC");
    ADD_MAIN_BINDING(ql_math::endcriteria, "End criteria for optimization");
    ADD_MAIN_BINDING(ql_math::problem, "Optimization problem");
    ADD_MAIN_BINDING(ql_math::levenbergmarquardt, "Levenberg-Marquardt optimizer");
    ADD_BASE_BINDING(ql_math::extrapolation, "Extrapolator base class");
    ADD_BASE_BINDING(ql_math::interpolation, "Interpolation base class");
    ADD_MAIN_BINDING(ql_math::linearinterpolation, "Linear interpolation");
    ADD_MAIN_BINDING(ql_math::loglinearinterpolation, "Log-linear interpolation");
    ADD_MAIN_BINDING(ql_math::backwardflatinterpolation, "Backward-flat interpolation");
    ADD_MAIN_BINDING(ql_math::cubicinterpolation, "Cubic interpolation");
    ADD_MAIN_BINDING(ql_math::normaldistribution, "Normal distribution functions");
    ADD_MAIN_BINDING(ql_math::bivariatenormaldistribution, "Bivariate cumulative normal distribution");
    ADD_MAIN_BINDING(ql_math::solvers1d, "1-D root-finding solvers");

    // Statistics
    ADD_MAIN_BINDING(ql_math::statistics,
        "Statistics - empirical-distribution risk measures");
    ADD_MAIN_BINDING(ql_math::incrementalstatistics,
        "IncrementalStatistics - online statistics via boost accumulators");
    ADD_MAIN_BINDING(ql_math::sequencestatistics,
        "SequenceStatistics - N-dimensional statistics with covariance");

    // Random number generators
    ADD_MAIN_BINDING(ql_math::mt19937uniformrng,
        "MersenneTwisterUniformRng - MT19937 uniform RNG");
    ADD_MAIN_BINDING(ql_math::sobolrsg,
        "SobolRsg - Sobol low-discrepancy sequence generator");
    ADD_MAIN_BINDING(ql_math::haltonrsg,
        "HaltonRsg - Halton low-discrepancy sequence generator");
    ADD_MAIN_BINDING(ql_math::burley2020sobolrsg,
        "Burley2020SobolRsg - scrambled Sobol sequence generator");
    ADD_MAIN_BINDING(ql_math::boxmullergaussianrng,
        "BoxMullerGaussianRng - Box-Muller Gaussian RNG");
    ADD_MAIN_BINDING(ql_math::inversecumulativerng,
        "GaussianRandomGenerator - inverse cumulative Gaussian RNG");
    ADD_MAIN_BINDING(ql_math::randomsequencegenerator,
        "UniformRandomSequenceGenerator - uniform random sequence generator");
    ADD_MAIN_BINDING(ql_math::inversecumulativersg,
        "Gaussian random and low-discrepancy sequence generators");
    // Registered here (not models/all.cpp) because SobolBrownianBridgeRsg
    // needs the Ordering enum for a default arg, and math runs before models.
    ADD_MAIN_BINDING(ql_models::sobolbrowniangenerator,
        "Ordering enum for Sobol Brownian generators");
    ADD_MAIN_BINDING(ql_math::sobolbrownianbridgersg,
        "Sobol Brownian bridge sequence generators");
}
