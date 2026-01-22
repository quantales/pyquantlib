# PyQuantLib: Python bindings for QuantLib
# Copyright (c) 2025, 2026 Yassine Idyiahia
# Licensed under the BSD 3-Clause License. See LICENSE file for details.

"""
Pure Python implementation of SVI Smile Section.

This module demonstrates how to extend QuantLib functionality in pure Python
by subclassing the SmileSection abstract base class. The implementation can
be validated against the C++ SviSmileSection from QuantLib's experimental folder.

The SVI (Stochastic Volatility Inspired) model parametrizes total variance as:

    w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))

where k = log(K/F) is the log-moneyness.

References
----------
- Gatheral, J. (2004). "A parsimonious arbitrage-free implied volatility
  parameterization with application to the valuation of volatility derivatives."
- Gatheral, J., & Jacquier, A. (2014). "Arbitrage-free SVI volatility surfaces."
  Quantitative Finance, 14(1), 59-71.
"""

from __future__ import annotations

import math
from typing import List

import pyquantlib as ql


def check_svi_parameters(
    a: float, b: float, sigma: float, rho: float, m: float
) -> None:
    """
    Validate SVI parameters for no-arbitrage conditions.

    Parameters
    ----------
    a : float
        Vertical translation (level).
    b : float
        Slope of the wings.
    sigma : float
        ATM curvature.
    rho : float
        Rotation/skew parameter.
    m : float
        Horizontal translation.

    Raises
    ------
    ValueError
        If any constraint is violated.
    """
    if b < 0:
        raise ValueError(f"b ({b}) must be non-negative")
    if abs(rho) >= 1:
        raise ValueError(f"rho ({rho}) must be in (-1, 1)")
    if sigma <= 0:
        raise ValueError(f"sigma ({sigma}) must be positive")
    if a + b * sigma * math.sqrt(1 - rho * rho) < 0:
        raise ValueError(
            f"a + b * sigma * sqrt(1 - rho^2) must be non-negative "
            f"(a={a}, b={b}, sigma={sigma}, rho={rho})"
        )
    if b * (1 + abs(rho)) > 4:
        raise ValueError(
            f"b * (1 + |rho|) must be <= 4 (b={b}, rho={rho})"
        )


def svi_total_variance(
    a: float, b: float, sigma: float, rho: float, m: float, k: float
) -> float:
    """
    Compute SVI total variance.

    Parameters
    ----------
    a : float
        Vertical translation.
    b : float
        Slope.
    sigma : float
        ATM curvature.
    rho : float
        Rotation.
    m : float
        Horizontal translation.
    k : float
        Log-moneyness, log(K/F).

    Returns
    -------
    float
        Total variance w(k).
    """
    return a + b * (rho * (k - m) + math.sqrt((k - m) ** 2 + sigma ** 2))


class SviSmileSection(ql.base.SmileSection):
    """
    Pure Python implementation of SVI smile section.

    This class demonstrates extending QuantLib in Python without C++ compilation.
    It can be validated against ql.SviSmileSection from QuantLib's experimental
    folder.

    The SVI total variance formula is:

        w(k) = a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))

    where k = log(K/F) is the log-moneyness.

    Parameters
    ----------
    time_to_expiry : float
        Time to expiry in years.
    forward : float
        Forward price.
    svi_params : list of float
        SVI parameters [a, b, sigma, rho, m].
    validate : bool, optional
        Whether to validate parameters (default True).

    Examples
    --------
    >>> from pyquantlib.extensions import SviSmileSection
    >>> params = [0.04, 0.1, 0.3, -0.4, 0.0]
    >>> smile = SviSmileSection(1.0, 100.0, params)
    >>> print(f"ATM vol: {smile.volatility(100.0):.4f}")
    """

    def __init__(
        self,
        time_to_expiry: float,
        forward: float,
        svi_params: List[float],
        validate: bool = True,
    ) -> None:
        super().__init__()
        if len(svi_params) != 5:
            raise ValueError(f"Expected 5 SVI parameters, got {len(svi_params)}")

        self._time_to_expiry = time_to_expiry
        self._forward = forward
        self._a, self._b, self._sigma, self._rho, self._m = svi_params

        if validate:
            check_svi_parameters(
                self._a, self._b, self._sigma, self._rho, self._m
            )

    def minStrike(self) -> float:
        """Return minimum strike (0)."""
        return 0.0

    def maxStrike(self) -> float:
        """Return maximum strike (effectively infinite)."""
        return float("inf")

    def atmLevel(self) -> float:
        """Return ATM level (forward price)."""
        return self._forward

    def volatilityImpl(self, strike: float) -> float:
        """
        Compute implied volatility at the given strike.

        Parameters
        ----------
        strike : float
            Option strike price.

        Returns
        -------
        float
            Implied volatility.
        """
        if strike <= 0:
            strike = 1e-10  # Avoid log(0)

        # Log-moneyness
        k = math.log(strike / self._forward)

        # Total variance from SVI formula
        w = svi_total_variance(
            self._a, self._b, self._sigma, self._rho, self._m, k
        )

        # Ensure non-negative variance
        w = max(w, 1e-10)

        # Convert total variance to volatility: w = sigma^2 * T
        return math.sqrt(w / self._time_to_expiry)

    # Accessors for parameters
    @property
    def a(self) -> float:
        """Vertical translation parameter."""
        return self._a

    @property
    def b(self) -> float:
        """Slope parameter."""
        return self._b

    @property
    def sigma(self) -> float:
        """ATM curvature parameter."""
        return self._sigma

    @property
    def rho(self) -> float:
        """Rotation/skew parameter."""
        return self._rho

    @property
    def m(self) -> float:
        """Horizontal translation parameter."""
        return self._m

    @property
    def params(self) -> List[float]:
        """Return all SVI parameters as a list."""
        return [self._a, self._b, self._sigma, self._rho, self._m]
