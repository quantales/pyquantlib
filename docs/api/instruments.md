# Instruments Module

## Bonds

### Bond

```{eval-rst}
.. autoclass:: pyquantlib.Bond
   :members:
```

### ZeroCouponBond

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponBond
```

```python
bond = ql.ZeroCouponBond(2, ql.TARGET(), 100.0, maturity_date)
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
```

### FixedRateBond

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateBond
```

```python
bond = ql.FixedRateBond(2, 100.0, schedule, [0.05],
                         ql.Thirty360(ql.Thirty360.BondBasis))
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
print(bond.bondYield(ql.Thirty360(ql.Thirty360.BondBasis),
                      ql.Compounded, ql.Annual))
```

### FloatingRateBond

```{eval-rst}
.. autoclass:: pyquantlib.FloatingRateBond
```

```python
bond = ql.FloatingRateBond(2, 100.0, schedule, euribor6m,
                            ql.Actual360(), spreads=[0.005])
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
```

### AmortizingFixedRateBond

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingFixedRateBond
```

```python
notionals = ql.sinkingNotionals(ql.Period(5, ql.Years), ql.Annual, 0.05, 100.0)
schedule = ql.sinkingSchedule(issue_date, ql.Period(5, ql.Years), ql.Annual, ql.TARGET())
bond = ql.AmortizingFixedRateBond(2, notionals, schedule, [0.05],
                                   ql.Thirty360(ql.Thirty360.BondBasis))
```

### sinkingSchedule

```{eval-rst}
.. autofunction:: pyquantlib.sinkingSchedule
```

### sinkingNotionals

```{eval-rst}
.. autofunction:: pyquantlib.sinkingNotionals
```

### AmortizingFloatingRateBond

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingFloatingRateBond
```

### CmsRateBond

```{eval-rst}
.. autoclass:: pyquantlib.CmsRateBond
```

### CPIBond

```{eval-rst}
.. autoclass:: pyquantlib.CPIBond
```

```python
bond = ql.CPIBond(2, 100.0, 315.0, ql.Period(3, ql.Months),
                   cpi_index, ql.CPI.Flat, schedule, [0.02],
                   ql.Actual365Fixed())
```

## Callable Bonds

### Callability

```{eval-rst}
.. autoclass:: pyquantlib.Callability
```

```{eval-rst}
.. autoclass:: pyquantlib.CallabilityType
   :members:
   :undoc-members:
```

| Value | Description |
|-------|-------------|
| `Call` | Issuer can call (redeem early) |
| `Put` | Holder can put (sell back early) |

```python
call_price = ql.BondPrice(100.0, ql.BondPriceType.Clean)
call = ql.Callability(call_price, ql.CallabilityType.Call,
                       ql.Date(15, ql.June, 2030))
```

### CallableFixedRateBond

```{eval-rst}
.. autoclass:: pyquantlib.CallableFixedRateBond
```

```python
call_schedule = [
    ql.Callability(ql.BondPrice(100.0, ql.BondPriceType.Clean),
                    ql.CallabilityType.Call, call_date)
    for call_date in call_dates
]
bond = ql.CallableFixedRateBond(2, 100.0, schedule, [0.05],
                                 ql.Actual365Fixed(),
                                 putCallSchedule=call_schedule)
bond.setPricingEngine(ql.TreeCallableFixedRateBondEngine(hw_model, 100))
print(bond.cleanPrice())
print(bond.OAS(clean_price, curve, dc, ql.Continuous, ql.Annual))
```

### CallableZeroCouponBond

```{eval-rst}
.. autoclass:: pyquantlib.CallableZeroCouponBond
```

## Convertible Bonds

### SoftCallability

```{eval-rst}
.. autoclass:: pyquantlib.SoftCallability
```

Callability with a trigger level for soft-call provisions.

```python
soft_call = ql.SoftCallability(
    ql.BondPrice(110.0, ql.BondPriceType.Clean),
    call_date, 1.20,
)
```

### ConvertibleBond

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleBond
   :members:
```

Base class for convertible bonds (not directly constructible).

### ConvertibleZeroCouponBond

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleZeroCouponBond
```

```python
exercise = ql.AmericanExercise(today, maturity)
bond = ql.ConvertibleZeroCouponBond(
    exercise, 1.0, [], issue_date, 2,
    ql.Actual365Fixed(), schedule,
)
bond.setPricingEngine(ql.BinomialConvertibleEngine(process, "crr", 801))
print(bond.NPV())
```

### ConvertibleFixedCouponBond

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleFixedCouponBond
```

```python
bond = ql.ConvertibleFixedCouponBond(
    exercise, 1.0, call_schedule, issue_date, 2,
    [0.05], ql.Thirty360(ql.Thirty360.BondBasis), schedule,
)
```

### ConvertibleFloatingRateBond

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleFloatingRateBond
```

```python
bond = ql.ConvertibleFloatingRateBond(
    exercise, 1.0, [], issue_date, 2,
    euribor6m, 2, [0.005], ql.Actual360(), schedule,
)
```

### EquityTotalReturnSwap

```{eval-rst}
.. autoclass:: pyquantlib.EquityTotalReturnSwap
```

Equity total return swap: equity leg vs interest rate leg.

```python
trs = ql.EquityTotalReturnSwap(
    ql.SwapType.Payer, 1_000_000.0, schedule,
    equity_index, ibor_index, ql.Actual360(), 0.005,
)
trs.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(trs.NPV())
print(trs.fairMargin())
```

## Swaps

### VanillaSwap

```{eval-rst}
.. autoclass:: pyquantlib.VanillaSwap
```

### MakeVanillaSwap

```{eval-rst}
.. autoclass:: pyquantlib.MakeVanillaSwap
```

Pythonic builder for VanillaSwap. Constructor arguments are positional; builder options are keyword arguments.

```python
swap = ql.MakeVanillaSwap(
    ql.Period(5, ql.Years), euribor6m, 0.04,
    nominal=10_000_000.0,
    fixedLegDayCount=ql.Thirty360(ql.Thirty360.BondBasis),
    floatingLegSpread=0.001,
)
```

### OvernightIndexedSwap

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedSwap
```

Overnight indexed swap: fixed vs overnight floating leg.

```python
sofr = ql.Sofr(curve)
ois = ql.OvernightIndexedSwap(
    ql.SwapType.Receiver, 1_000_000.0, schedule,
    0.035, ql.Actual360(), sofr,
)
ois.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(ois.NPV())
print(ois.fairRate())
```

### ZeroCouponSwap

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponSwap
```

Zero-coupon swap: single fixed payment vs floating leg.

```python
swap = ql.ZeroCouponSwap(
    ql.SwapType.Receiver, 1_000_000.0, start_date, maturity_date,
    0.04, ql.Actual365Fixed(), schedule, euribor6m,
)
swap.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(swap.NPV())
print(swap.fairFixedPayment(curve))
```

### AssetSwap

```{eval-rst}
.. autoclass:: pyquantlib.AssetSwap
```

Asset swap exchanging a bond for a floating rate leg.

```python
asset_swap = ql.AssetSwap(False, bond, 100.0, schedule, euribor6m, 0.0)
asset_swap.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(asset_swap.NPV())
print(asset_swap.fairSpread())
```

## Caps, Floors, and Collars

### CapFloor

```{eval-rst}
.. autoclass:: pyquantlib.CapFloor
   :members:
```

### Cap

```{eval-rst}
.. autoclass:: pyquantlib.Cap
```

### Floor

```{eval-rst}
.. autoclass:: pyquantlib.Floor
```

### Collar

```{eval-rst}
.. autoclass:: pyquantlib.Collar
```

```python
leg = ql.IborLeg(schedule, euribor).withNotionals([1_000_000.0]).build()

cap = ql.Cap(leg, [0.05])
floor = ql.Floor(leg, [0.03])
collar = ql.Collar(leg, [0.05], [0.03])

cap.setPricingEngine(ql.BlackCapFloorEngine(curve, 0.20))
print(cap.NPV())
print(cap.impliedVolatility(cap.NPV(), curve_handle, 0.20))
```

## Forward Rate Agreement

### ForwardRateAgreement

```{eval-rst}
.. autoclass:: pyquantlib.ForwardRateAgreement
   :members:
```

```python
fra = ql.ForwardRateAgreement(
    euribor, value_date, ql.PositionType.Long,
    0.04, 1_000_000.0, curve,
)
print(fra.NPV())
print(fra.forwardRate())
```

## Swaptions

### Swaption

```{eval-rst}
.. autoclass:: pyquantlib.Swaption
```

### MakeSwaption

```{eval-rst}
.. autoclass:: pyquantlib.MakeSwaption
```

Pythonic builder for Swaption. Constructor arguments are positional; builder options are keyword arguments.

```python
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years), curve, curve)
swaption = ql.MakeSwaption(
    swap_index, ql.Period(1, ql.Years), 0.04,
    pricingEngine=engine,
)
```

## Composite Instruments

### CompositeInstrument

```{eval-rst}
.. autoclass:: pyquantlib.CompositeInstrument
```

Instrument composed of weighted sub-instruments.

```python
composite = ql.CompositeInstrument()
composite.add(option1)           # weight = 1.0
composite.add(option2)
composite.subtract(option3)      # weight = -1.0
composite.add(option4, 0.5)      # weight = 0.5
print(composite.NPV())
```

## Credit Instruments

### Claims

```{eval-rst}
.. autoclass:: pyquantlib.FaceValueClaim
```

```{eval-rst}
.. autoclass:: pyquantlib.FaceValueAccrualClaim
```

Claim objects define the loss amount on a default event. `FaceValueClaim` returns
`notional * (1 - recoveryRate)`. `FaceValueAccrualClaim` adds accrued interest
from a reference bond.

```python
claim = ql.FaceValueClaim()
loss = claim.amount(default_date, 1_000_000.0, 0.4)  # 600,000
```

### CreditDefaultSwap

```{eval-rst}
.. autoclass:: pyquantlib.CreditDefaultSwap
```

Credit default swap quoted as running spread or upfront + spread.

```python
cds = ql.CreditDefaultSwap(
    ql.ProtectionSide.Buyer, 10_000_000.0, 0.01,
    schedule, ql.Following, ql.Actual360(),
)
cds.setPricingEngine(ql.MidPointCdsEngine(
    default_curve, 0.4, discount_curve,
))
print(cds.NPV())
print(cds.fairSpread())
```

### cdsMaturity

```{eval-rst}
.. autofunction:: pyquantlib.cdsMaturity
```

## Inflation Swaps

### ZeroCouponInflationSwap

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponInflationSwap
   :members:
   :undoc-members:
```

Zero-coupon inflation swap: fixed rate vs zero-coupon inflation leg.

### YearOnYearInflationSwap

```{eval-rst}
.. autoclass:: pyquantlib.YearOnYearInflationSwap
   :members:
   :undoc-members:
```

Year-on-year inflation swap: fixed rate vs YoY inflation leg.

## YoY Inflation Caps, Floors, and Collars

### YoYInflationCapFloor

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCapFloor
   :members:
   :undoc-members:
```

### YoYInflationCapFloorType

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCapFloorType
   :members:
   :undoc-members:
```

| Value | Description |
|-------|-------------|
| `Cap` | YoY inflation cap |
| `Floor` | YoY inflation floor |
| `Collar` | YoY inflation collar |

### YoYInflationCap

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCap
   :members:
   :undoc-members:
```

### YoYInflationFloor

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationFloor
   :members:
   :undoc-members:
```

### YoYInflationCollar

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCollar
   :members:
   :undoc-members:
```

### MakeYoYInflationCapFloor

```{eval-rst}
.. autofunction:: pyquantlib.MakeYoYInflationCapFloor
```

Pythonic builder function for YoY inflation caps and floors. Constructor arguments are positional; builder options are keyword arguments.

```python
cap = ql.MakeYoYInflationCapFloor(
    ql.YoYInflationCapFloorType.Cap, yoy_leg, [0.03],
    pricingEngine=engine,
)
```

## Options

### VanillaOption

```{eval-rst}
.. autoclass:: pyquantlib.VanillaOption
```

```python
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
```

### BasketOption

```{eval-rst}
.. autoclass:: pyquantlib.BasketOption
```

## Barrier Options

### BarrierOption

```{eval-rst}
.. autoclass:: pyquantlib.BarrierOption
```

| Barrier Type | Description |
|-------------|-------------|
| `DownIn` | Activated when spot falls below barrier |
| `UpIn` | Activated when spot rises above barrier |
| `DownOut` | Knocked out when spot falls below barrier |
| `UpOut` | Knocked out when spot rises above barrier |

```python
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(expiry)

option = ql.BarrierOption(ql.BarrierType.DownOut, 80.0, 0.0, payoff, exercise)
option.setPricingEngine(ql.AnalyticBarrierEngine(process))
print(option.NPV())
```

### DoubleBarrierOption

```{eval-rst}
.. autoclass:: pyquantlib.DoubleBarrierOption
```

| Type | Description |
|------|-------------|
| `KnockOut` | Knocked out if either barrier is hit |
| `KnockIn` | Activated if either barrier is hit |
| `KIKO` | Lower KI, upper KO |
| `KOKI` | Lower KO, upper KI |

```python
option = ql.DoubleBarrierOption(
    ql.DoubleBarrierType.KnockOut, 80.0, 120.0, 0.0, payoff, exercise,
)
option.setPricingEngine(ql.AnalyticDoubleBarrierEngine(process))
print(option.NPV())
```

## Asian Options

### ContinuousAveragingAsianOption

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousAveragingAsianOption
```

### DiscreteAveragingAsianOption

```{eval-rst}
.. autoclass:: pyquantlib.DiscreteAveragingAsianOption
```

```python
fixing_dates = [today + ql.Period(f"{i}M") for i in range(1, 13)]

# Geometric average (analytic)
asian_geom = ql.DiscreteAveragingAsianOption(
    ql.AverageType.Geometric, 0.0, 0, fixing_dates, payoff, exercise,
)
asian_geom.setPricingEngine(
    ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
)

# Arithmetic average (Turnbull-Wakeman approximation)
asian_arith = ql.DiscreteAveragingAsianOption(
    ql.AverageType.Arithmetic, 0.0, 0, fixing_dates, payoff, exercise,
)
asian_arith.setPricingEngine(ql.TurnbullWakemanAsianEngine(process))
```

## Lookback Options

### ContinuousFloatingLookbackOption

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousFloatingLookbackOption
```

Continuous floating-strike lookback option. The strike is determined at expiry as the minimum (call) or maximum (put) of the asset price over the option's life.

```python
payoff = ql.FloatingTypePayoff(ql.Call)
exercise = ql.EuropeanExercise(expiry)
option = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)
```

### ContinuousFixedLookbackOption

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousFixedLookbackOption
```

Continuous fixed-strike lookback option. The payoff is based on the maximum (call) or minimum (put) of the asset price over the option's life.

```python
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(expiry)
option = ql.ContinuousFixedLookbackOption(100.0, payoff, exercise)
```

### ContinuousPartialFloatingLookbackOption

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousPartialFloatingLookbackOption
```

Partial floating-strike lookback option with a lookback period ending before expiry.

```python
option = ql.ContinuousPartialFloatingLookbackOption(
    100.0, 1.0, lookback_end, payoff, exercise,
)
```

### ContinuousPartialFixedLookbackOption

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousPartialFixedLookbackOption
```

Partial fixed-strike lookback option with a lookback period starting after inception.

```python
option = ql.ContinuousPartialFixedLookbackOption(
    lookback_start, payoff, exercise,
)
```

## Cliquet Options

### CliquetOption

```{eval-rst}
.. autoclass:: pyquantlib.CliquetOption
```

Cliquet (ratchet) option with periodic resets. The strike resets at each reset date to the then-current spot price.

```python
payoff = ql.PercentageStrikePayoff(ql.Call, 1.0)
exercise = ql.EuropeanExercise(expiry)
reset_dates = [today + ql.Period(f"{i}M") for i in range(3, 12, 3)]
option = ql.CliquetOption(payoff, exercise, reset_dates)
```

## Compound Options

### CompoundOption

```{eval-rst}
.. autoclass:: pyquantlib.CompoundOption
```

Compound option (option on an option). The mother option gives the right to buy/sell the daughter option.

```python
mother_payoff = ql.PlainVanillaPayoff(ql.Call, 5.0)
mother_exercise = ql.EuropeanExercise(today + ql.Period("6M"))
daughter_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
daughter_exercise = ql.EuropeanExercise(expiry)
option = ql.CompoundOption(
    mother_payoff, mother_exercise, daughter_payoff, daughter_exercise,
)
```

## Chooser Options

### SimpleChooserOption

```{eval-rst}
.. autoclass:: pyquantlib.SimpleChooserOption
```

Simple chooser option. The holder chooses at a future date whether the option is a call or put.

```python
option = ql.SimpleChooserOption(choosing_date, 100.0, exercise)
```

### ComplexChooserOption

```{eval-rst}
.. autoclass:: pyquantlib.ComplexChooserOption
```

Complex chooser option with different strikes and exercise dates for the call and put legs.

```python
option = ql.ComplexChooserOption(
    choosing_date, call_strike, put_strike, call_exercise, put_exercise,
)
```

## Margrabe Options

### MargrabeOption

```{eval-rst}
.. autoclass:: pyquantlib.MargrabeOption
```

Margrabe option (exchange option): the right to exchange one asset for another.

```python
option = ql.MargrabeOption(1, 1, exercise)
option.setPricingEngine(engine)
print(option.delta1(), option.delta2())
print(option.gamma1(), option.gamma2())
```

## Forward-Start Options

### ForwardVanillaOption

```{eval-rst}
.. autoclass:: pyquantlib.ForwardVanillaOption
```

Forward-start vanilla option. The strike is set at a future reset date based on a moneyness ratio.

```python
option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
```

## Quanto Options

### QuantoVanillaOption

```{eval-rst}
.. autoclass:: pyquantlib.QuantoVanillaOption
```

Quanto vanilla option with currency adjustment. Provides quanto-specific greeks: `qvega()`, `qrho()`, `qlambda()`.

```python
option = ql.QuantoVanillaOption(payoff, exercise)
option.setPricingEngine(engine)
print(option.qvega(), option.qrho(), option.qlambda())
```

## Payoffs

### FloatingTypePayoff

```{eval-rst}
.. autoclass:: pyquantlib.FloatingTypePayoff
```

Floating-strike payoff for lookback options.

```python
payoff = ql.FloatingTypePayoff(ql.Call)
```

### PlainVanillaPayoff

```{eval-rst}
.. autoclass:: pyquantlib.PlainVanillaPayoff
```

| Type | Payoff |
|------|--------|
| `Call` | $\max(S - K, 0)$ |
| `Put` | $\max(K - S, 0)$ |

```python
call_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
put_payoff = ql.PlainVanillaPayoff(ql.Put, 100.0)
```

### CashOrNothingPayoff

```{eval-rst}
.. autoclass:: pyquantlib.CashOrNothingPayoff
```

Binary payoff: pays a fixed cash amount if in the money, zero otherwise.

| Type | Payoff |
|------|--------|
| `Call` | $C$ if $S > K$, else $0$ |
| `Put` | $C$ if $S < K$, else $0$ |

```python
digital_call = ql.CashOrNothingPayoff(ql.Call, 100.0, 10.0)
```

### AssetOrNothingPayoff

```{eval-rst}
.. autoclass:: pyquantlib.AssetOrNothingPayoff
```

Binary payoff: pays the asset value if in the money, zero otherwise.

| Type | Payoff |
|------|--------|
| `Call` | $S$ if $S > K$, else $0$ |
| `Put` | $S$ if $S < K$, else $0$ |

```python
digital = ql.AssetOrNothingPayoff(ql.Call, 100.0)
```

### GapPayoff

```{eval-rst}
.. autoclass:: pyquantlib.GapPayoff
```

Gap payoff with two strikes. Equivalent to a vanilla minus a digital.

| Type | Payoff |
|------|--------|
| `Call` | $S - K_2$ if $S > K_1$, else $0$ |
| `Put` | $K_2 - S$ if $S < K_1$, else $0$ |

```python
gap = ql.GapPayoff(ql.Call, 100.0, 90.0)
```

### PercentageStrikePayoff

```{eval-rst}
.. autoclass:: pyquantlib.PercentageStrikePayoff
```

Payoff with strike expressed as a moneyness percentage of the asset price.

```python
payoff = ql.PercentageStrikePayoff(ql.Call, 1.05)
```

### SuperFundPayoff

```{eval-rst}
.. autoclass:: pyquantlib.SuperFundPayoff
```

Binary superfund payoff: pays $S / K_1$ if $K_1 < S < K_2$, zero otherwise.

```python
payoff = ql.SuperFundPayoff(90.0, 110.0)
```

### SuperSharePayoff

```{eval-rst}
.. autoclass:: pyquantlib.SuperSharePayoff
```

Binary supershare payoff: pays a fixed cash amount if $K_1 < S < K_2$, zero otherwise.

```python
payoff = ql.SuperSharePayoff(90.0, 110.0, 5.0)
```

### MinBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.MinBasketPayoff
```

### MaxBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.MaxBasketPayoff
```

### AverageBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.AverageBasketPayoff
```

### SpreadBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.SpreadBasketPayoff
```

## Variance Swaps

### VarianceSwap

```{eval-rst}
.. autoclass:: pyquantlib.VarianceSwap
```

## Exotic Swaps

### NonstandardSwap

```{eval-rst}
.. autoclass:: pyquantlib.NonstandardSwap
```

### FloatFloatSwap

```{eval-rst}
.. autoclass:: pyquantlib.FloatFloatSwap
```

### NonstandardSwaption

```{eval-rst}
.. autoclass:: pyquantlib.NonstandardSwaption
```

### FloatFloatSwaption

```{eval-rst}
.. autoclass:: pyquantlib.FloatFloatSwaption
```

## Bond Forwards

### Forward

```{eval-rst}
.. autoclass:: pyquantlib.base.Forward
```

### ForwardTypePayoff

```{eval-rst}
.. autoclass:: pyquantlib.ForwardTypePayoff
```

### BondForward

```{eval-rst}
.. autoclass:: pyquantlib.BondForward
```

## Exercise Types

### EuropeanExercise

```{eval-rst}
.. autoclass:: pyquantlib.EuropeanExercise
```

### AmericanExercise

```{eval-rst}
.. autoclass:: pyquantlib.AmericanExercise
```

### BermudanExercise

```{eval-rst}
.. autoclass:: pyquantlib.BermudanExercise
```

```python
european = ql.EuropeanExercise(expiry)
american = ql.AmericanExercise(today, expiry)
bermudan = ql.BermudanExercise([date1, date2, date3])
```
