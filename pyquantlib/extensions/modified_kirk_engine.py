# PyQuantLib: Python bindings for QuantLib
# Copyright (c) 2025, 2026 Yassine Idyiahia
# Licensed under the BSD 3-Clause License. See LICENSE file for details.

"""
Modified Kirk Engine for spread option pricing.

This module implements the Modified Kirk approximation from:
    Alòs, E., & León, J.A. (2015). "On the short-maturity behaviour of the
    implied volatility skew for random strike options and applications to
    option pricing approximation." Quantitative Finance, 16(1), 31-42.

The modification adds a skew correction term to Kirk's formula, significantly
improving accuracy for high correlation cases (ρ close to 1).

References
----------
- Kirk, E. (1995). "Correlation in the energy markets." Managing Energy Price Risk.
- Alòs & León (2015). Quantitative Finance, 16(1), 31-42.
- Harutyunyan & Masip Borrás (2018). arXiv:1812.04272 (numerical analysis)
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pyquantlib as ql

if TYPE_CHECKING:
    from pyquantlib import GeneralizedBlackScholesProcess


class ModifiedKirkEngine(ql.base.SpreadBlackScholesVanillaEngine):
    """
    Modified Kirk engine for spread option pricing.

    This engine implements the Modified Kirk approximation which adds a
    volatility skew correction to the standard Kirk formula. The correction
    is derived using Malliavin calculus and significantly improves accuracy
    when the correlation between the two underlying assets is high (ρ > 0.9).

    The spread option payoff is: max(S1 - S2 - K, 0) for a call.

    Parameters
    ----------
    process1 : GeneralizedBlackScholesProcess
        Black-Scholes process for the first asset (S1).
    process2 : GeneralizedBlackScholesProcess
        Black-Scholes process for the second asset (S2).
    correlation : float
        Correlation between the two assets, in [-1, 1].

    References
    ----------
    .. [1] Alòs, E., & León, J.A. (2015). Quantitative Finance, 16(1), 31-42.

    Examples
    --------
    >>> import pyquantlib as ql
    >>> from pyquantlib.extensions import ModifiedKirkEngine
    >>>
    >>> engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
    >>> option.setPricingEngine(engine)
    >>> print(f"NPV: {option.NPV():.4f}")
    """

    def __init__(
        self,
        process1: GeneralizedBlackScholesProcess,
        process2: GeneralizedBlackScholesProcess,
        correlation: float,
    ) -> None:
        if not -1.0 <= correlation <= 1.0:
            raise ValueError(f"Correlation must be in [-1, 1], got {correlation}")
        super().__init__(process1, process2, correlation)
        self._process1 = process1
        self._process2 = process2
        self._rho = correlation

    def calculate(self, *args):
        """Calculate spread option price using Modified Kirk approximation."""
        if len(args) == 0:
            self._calculate_from_instrument()
        elif len(args) == 7:
            f1, f2, strike, optionType, variance1, variance2, df = args
            return self._calculate_price(f1, f2, strike, optionType, variance1, variance2, df)
        else:
            raise TypeError(f"calculate() takes 0 or 7 arguments, got {len(args)}")

    def _calculate_from_instrument(self):
        """Extract parameters from instrument and compute price."""
        args = self.getArguments()
        exercise = args.exercise
        payoff = args.payoff

        exercise_date = exercise.lastDate()
        ref_date = ql.Settings.instance().evaluationDate
        dc = ql.Actual365Fixed()
        T = dc.yearFraction(ref_date, exercise_date)

        if T <= 0:
            results = self.getResults()
            results.value = 0.0
            return

        process1 = self._process1
        process2 = self._process2

        S1 = process1.x0()
        S2 = process2.x0()

        r1 = process1.riskFreeRate().currentLink()
        q1 = process1.dividendYield().currentLink()
        r2 = process2.riskFreeRate().currentLink()
        q2 = process2.dividendYield().currentLink()

        df = r1.discount(T)
        f1 = S1 * q1.discount(T) / r1.discount(T)
        f2 = S2 * q2.discount(T) / r2.discount(T)

        vol1 = process1.blackVolatility().currentLink().blackVol(T, f1)
        vol2 = process2.blackVolatility().currentLink().blackVol(T, f2)
        variance1 = vol1 * vol1 * T
        variance2 = vol2 * vol2 * T

        strike = payoff.basePayoff().strike()
        optionType = payoff.basePayoff().optionType()

        price = self._calculate_price(f1, f2, strike, optionType, variance1, variance2, df)

        results = self.getResults()
        results.value = price

    def _calculate_price(
        self,
        f1: float,
        f2: float,
        strike: float,
        optionType: ql.OptionType,
        variance1: float,
        variance2: float,
        df: float,
    ) -> float:
        """Calculate spread option price using Modified Kirk approximation."""
        sigma1 = math.sqrt(variance1) if variance1 > 0 else 0.0
        sigma2 = math.sqrt(variance2) if variance2 > 0 else 0.0

        K_eff = f2 + strike

        if K_eff <= 0:
            if optionType == ql.OptionType.Call:
                return df * max(f1 - f2 - strike, 0.0)
            else:
                return df * max(f2 + strike - f1, 0.0)

        w = f2 / K_eff

        # Kirk's volatility
        a_squared = sigma1**2 - 2.0 * self._rho * sigma1 * sigma2 * w + (sigma2 * w) ** 2
        if a_squared <= 0:
            a_squared = 1e-10
        sigma_kirk = math.sqrt(a_squared)

        # Skew correction (Alòs & León 2015)
        numerator_term = (sigma2 * w - self._rho * sigma1) ** 2
        skew_factor = (sigma2**2 * f2 * strike) / (K_eff**2)

        if sigma_kirk > 1e-10:
            skew_slope = 0.5 * numerator_term * skew_factor / (sigma_kirk**3)
        else:
            skew_slope = 0.0

        # Log-moneyness adjustment
        if f1 > 0 and K_eff > 0:
            x = math.log(f1)
            x_atm = math.log(K_eff)
            sigma_modified = sigma_kirk + skew_slope * (x - x_atm)
        else:
            sigma_modified = sigma_kirk

        sigma_modified = max(sigma_modified, 1e-10)

        # Price using QuantLib's Black formula
        return ql.blackFormula(optionType, K_eff, f1, sigma_modified, df)

    @staticmethod
    def kirk_volatility(
        F1: float, F2: float, K: float, sigma1: float, sigma2: float, rho: float
    ) -> float:
        """Calculate Kirk's approximation volatility (without skew correction)."""
        K_eff = F2 + K
        if K_eff <= 0:
            return sigma1
        w = F2 / K_eff
        a_squared = sigma1**2 - 2.0 * rho * sigma1 * sigma2 * w + (sigma2 * w)**2
        return math.sqrt(max(a_squared, 1e-10))

    @staticmethod
    def skew_slope(
        F1: float, F2: float, K: float, sigma1: float, sigma2: float, rho: float
    ) -> float:
        """Calculate the skew slope correction term from Alòs & León (2015)."""
        K_eff = F2 + K
        if K_eff <= 0:
            return 0.0
        w = F2 / K_eff
        sigma_kirk = ModifiedKirkEngine.kirk_volatility(F1, F2, K, sigma1, sigma2, rho)
        if sigma_kirk < 1e-10:
            return 0.0
        numerator_term = (sigma2 * w - rho * sigma1) ** 2
        skew_factor = (sigma2**2 * F2 * K) / (K_eff**2)
        return 0.5 * numerator_term * skew_factor / (sigma_kirk**3)
