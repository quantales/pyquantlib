# Instruments

Bindings for the `Instrument` class hierarchy: bonds, swaps, swaptions, caps and floors, options of every kind (vanilla, barrier, Asian, lookback, cliquet, compound, chooser, Margrabe, forward-start, quanto, basket), inflation products, credit derivatives, plus the supporting payoff and exercise classes that parameterise them.

Every instrument exposes the same `setPricingEngine(engine)` / `NPV()` interface; specialised methods (`cleanPrice`, `bondYield`, `OAS`, `fairSpread`, `delta`, `vega`, ...) become available once the matching engine is attached. See {doc}`/concepts/pricing-engines` for the instrument / engine separation.

## At a glance

| Family | Classes |
|---|---|
| Bonds | {py:class}`pyquantlib.Bond`, {py:class}`pyquantlib.ZeroCouponBond`, {py:class}`pyquantlib.FixedRateBond`, {py:class}`pyquantlib.FloatingRateBond`, {py:class}`pyquantlib.AmortizingFixedRateBond`, {py:class}`pyquantlib.AmortizingFloatingRateBond`, {py:class}`pyquantlib.CmsRateBond`, {py:class}`pyquantlib.CPIBond` |
| Callable / convertible bonds | {py:class}`pyquantlib.Callability`, {py:class}`pyquantlib.CallableFixedRateBond`, {py:class}`pyquantlib.CallableZeroCouponBond`, {py:class}`pyquantlib.SoftCallability`, {py:class}`pyquantlib.ConvertibleBond`, {py:class}`pyquantlib.ConvertibleZeroCouponBond`, {py:class}`pyquantlib.ConvertibleFixedCouponBond`, {py:class}`pyquantlib.ConvertibleFloatingRateBond` |
| Swaps | {py:class}`pyquantlib.VanillaSwap`, {py:class}`pyquantlib.MakeVanillaSwap`, {py:class}`pyquantlib.OvernightIndexedSwap`, {py:class}`pyquantlib.ZeroCouponSwap`, {py:class}`pyquantlib.AssetSwap`, {py:class}`pyquantlib.EquityTotalReturnSwap` |
| Cross-currency swaps | {py:class}`pyquantlib.ConstNotionalCrossCurrencySwap`, {py:class}`pyquantlib.ConstNotionalCrossCurrencyBasisSwap`, {py:class}`pyquantlib.ConstNotionalCrossCurrencyFixedVsFloatingSwap` |
| Inflation swaps | {py:class}`pyquantlib.ZeroCouponInflationSwap`, {py:class}`pyquantlib.YearOnYearInflationSwap` |
| Exotic swaps / swaptions | {py:class}`pyquantlib.NonstandardSwap`, {py:class}`pyquantlib.FloatFloatSwap`, {py:class}`pyquantlib.MultipleResetsSwap`, {py:class}`pyquantlib.NonstandardSwaption`, {py:class}`pyquantlib.FloatFloatSwaption` |
| Caps / floors / collars | {py:class}`pyquantlib.CapFloor`, {py:class}`pyquantlib.Cap`, {py:class}`pyquantlib.Floor`, {py:class}`pyquantlib.Collar`, {py:class}`pyquantlib.YoYInflationCap`, {py:class}`pyquantlib.YoYInflationFloor`, {py:class}`pyquantlib.YoYInflationCollar`, {py:class}`pyquantlib.YoYInflationCapFloor`, {py:class}`pyquantlib.MakeYoYInflationCapFloor` |
| Swaptions | {py:class}`pyquantlib.Swaption`, {py:class}`pyquantlib.MakeSwaption` |
| FRAs / forwards | {py:class}`pyquantlib.ForwardRateAgreement`, {py:class}`pyquantlib.FxForward`, {py:class}`pyquantlib.BondForward`, {py:class}`pyquantlib.ForwardTypePayoff` |
| Futures | {py:class}`pyquantlib.OvernightIndexFuture`, {py:class}`pyquantlib.PerpetualFutures`, {py:class}`pyquantlib.Futures` (date-rule enum) |
| Vanilla options | {py:class}`pyquantlib.VanillaOption`, {py:class}`pyquantlib.BasketOption` |
| Barrier options | {py:class}`pyquantlib.BarrierOption`, {py:class}`pyquantlib.DoubleBarrierOption`, {py:class}`pyquantlib.PartialTimeBarrierOption`, {py:class}`pyquantlib.SoftBarrierOption`, {py:class}`pyquantlib.TwoAssetBarrierOption` |
| Path-dependent | {py:class}`pyquantlib.ContinuousAveragingAsianOption`, {py:class}`pyquantlib.DiscreteAveragingAsianOption`, {py:class}`pyquantlib.ContinuousFloatingLookbackOption`, {py:class}`pyquantlib.ContinuousFixedLookbackOption`, {py:class}`pyquantlib.ContinuousPartialFloatingLookbackOption`, {py:class}`pyquantlib.ContinuousPartialFixedLookbackOption`, {py:class}`pyquantlib.CliquetOption` |
| Compound / chooser / exchange | {py:class}`pyquantlib.CompoundOption`, {py:class}`pyquantlib.SimpleChooserOption`, {py:class}`pyquantlib.ComplexChooserOption`, {py:class}`pyquantlib.MargrabeOption` |
| Forward-start / quanto | {py:class}`pyquantlib.ForwardVanillaOption`, {py:class}`pyquantlib.QuantoVanillaOption` |
| Swing options | {py:class}`pyquantlib.VanillaSwingOption`, {py:class}`pyquantlib.SwingExercise`, {py:class}`pyquantlib.VanillaForwardPayoff` |
| Payoffs | {py:class}`pyquantlib.PlainVanillaPayoff`, {py:class}`pyquantlib.CashOrNothingPayoff`, {py:class}`pyquantlib.AssetOrNothingPayoff`, {py:class}`pyquantlib.GapPayoff`, {py:class}`pyquantlib.PercentageStrikePayoff`, {py:class}`pyquantlib.SuperFundPayoff`, {py:class}`pyquantlib.SuperSharePayoff`, {py:class}`pyquantlib.FloatingTypePayoff`, {py:class}`pyquantlib.MinBasketPayoff`, {py:class}`pyquantlib.MaxBasketPayoff`, {py:class}`pyquantlib.AverageBasketPayoff`, {py:class}`pyquantlib.SpreadBasketPayoff` |
| Exercise | {py:class}`pyquantlib.EuropeanExercise`, {py:class}`pyquantlib.AmericanExercise`, {py:class}`pyquantlib.BermudanExercise` |
| Variance / credit / composite | {py:class}`pyquantlib.VarianceSwap`, {py:class}`pyquantlib.CreditDefaultSwap`, {py:class}`pyquantlib.FaceValueClaim`, {py:class}`pyquantlib.FaceValueAccrualClaim`, {py:class}`pyquantlib.CompositeInstrument` |

## Common patterns

### Build a vanilla European option

```python
import pyquantlib as ql

payoff   = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option   = ql.VanillaOption(payoff, exercise)

option.setPricingEngine(engine)
print(option.NPV(), option.delta())
```

The same `(payoff, exercise)` constructor pattern parameterises most option classes; what differs across instruments is which `Payoff` subclasses are accepted (e.g. `BarrierOption` extends with barrier level, `MargrabeOption` carries two notionals).

### Price a fixed-rate bond

```python
bond = ql.FixedRateBond(
    settlementDays=2, faceAmount=100.0,
    schedule=schedule, coupons=[0.05],
    accrualDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
)
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))

print(bond.cleanPrice())
print(bond.bondYield(
    ql.Thirty360(ql.Thirty360.BondBasis), ql.Compounded, ql.Annual,
))
```

`Bond` exposes `cleanPrice`, `dirtyPrice`, `accruedAmount`, `bondYield`, `duration`, `convexity`, etc., once a discount engine is attached. For callable bonds with a tree engine, `OAS` and `cleanPriceOAS` become available too.

### Build a swap with `MakeVanillaSwap`

```python
swap = ql.MakeVanillaSwap(
    ql.Period(5, ql.Years), euribor6m, 0.04,
    nominal=10_000_000.0,
    fixedLegDayCount=ql.Thirty360(ql.Thirty360.BondBasis),
    floatingLegSpread=0.001,
)
```

`MakeVanillaSwap` and `MakeSwaption` are keyword-argument builders mirroring QuantLib's C++ `Make*` pattern. Constructor arguments are positional, builder options keyword-only.

### Set up a barrier option

```python
payoff   = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(expiry)

option = ql.BarrierOption(
    ql.BarrierType.DownOut, barrier=80.0, rebate=0.0,
    payoff=payoff, exercise=exercise,
)
option.setPricingEngine(ql.AnalyticBarrierEngine(process))
print(option.NPV())
```

`BarrierType` values: `DownIn`, `UpIn`, `DownOut`, `UpOut`. `DoubleBarrierOption` adds two-sided variants (`KnockOut`, `KnockIn`, `KIKO`, `KOKI`).

### Build an OIS

```python
sofr = ql.Sofr(curve_handle)
ois = ql.OvernightIndexedSwap(
    ql.SwapType.Receiver, 1_000_000.0, schedule,
    fixedRate=0.035, fixedDC=ql.Actual360(), overnightIndex=sofr,
)
ois.setPricingEngine(ql.DiscountingSwapEngine(curve_handle))
print(ois.NPV(), ois.fairRate())
```

## Reference

### Bonds

```{eval-rst}
.. autoclass:: pyquantlib.Bond
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponBond
```

```python
bond = ql.ZeroCouponBond(2, ql.TARGET(), 100.0, maturity_date)
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
```

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateBond
```

```{eval-rst}
.. autoclass:: pyquantlib.FloatingRateBond
```

```python
bond = ql.FloatingRateBond(2, 100.0, schedule, euribor6m,
                            ql.Actual360(), spreads=[0.005])
```

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingFixedRateBond
```

```python
notionals = ql.sinkingNotionals(ql.Period(5, ql.Years), ql.Annual, 0.05, 100.0)
schedule  = ql.sinkingSchedule(issue_date, ql.Period(5, ql.Years), ql.Annual, ql.TARGET())
bond = ql.AmortizingFixedRateBond(2, notionals, schedule, [0.05],
                                   ql.Thirty360(ql.Thirty360.BondBasis))
```

```{eval-rst}
.. autofunction:: pyquantlib.sinkingSchedule
.. autofunction:: pyquantlib.sinkingNotionals
```

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingFloatingRateBond
```

```{eval-rst}
.. autoclass:: pyquantlib.CmsRateBond
```

```{eval-rst}
.. autoclass:: pyquantlib.CPIBond
```

```python
bond = ql.CPIBond(2, 100.0, 315.0, ql.Period(3, ql.Months),
                   cpi_index, ql.CPI.Flat, schedule, [0.02],
                   ql.Actual365Fixed())
```

### Callable bonds

```{eval-rst}
.. autoclass:: pyquantlib.Callability
```

```{eval-rst}
.. autoclass:: pyquantlib.CallabilityType
   :members:
   :undoc-members:
```

| Value | Side |
|---|---|
| `Call` | Issuer can redeem early |
| `Put` | Holder can sell back early |

```python
call = ql.Callability(
    ql.BondPrice(100.0, ql.BondPriceType.Clean),
    ql.CallabilityType.Call,
    ql.Date(15, ql.June, 2030),
)
```

```{eval-rst}
.. autoclass:: pyquantlib.CallableFixedRateBond
```

```python
schedule = [
    ql.Callability(ql.BondPrice(100.0, ql.BondPriceType.Clean),
                    ql.CallabilityType.Call, call_date)
    for call_date in call_dates
]
bond = ql.CallableFixedRateBond(2, 100.0, schedule, [0.05],
                                 ql.Actual365Fixed(),
                                 putCallSchedule=schedule)
bond.setPricingEngine(ql.TreeCallableFixedRateBondEngine(hw_model, 100))
print(bond.cleanPrice())
print(bond.OAS(clean_price, curve, dc, ql.Continuous, ql.Annual))
```

```{eval-rst}
.. autoclass:: pyquantlib.CallableZeroCouponBond
```

### Convertible bonds

```{eval-rst}
.. autoclass:: pyquantlib.SoftCallability
```

Callability with a trigger level.

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleBond
   :members:
```

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
```

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleFixedCouponBond
```

```{eval-rst}
.. autoclass:: pyquantlib.ConvertibleFloatingRateBond
```

```{eval-rst}
.. autoclass:: pyquantlib.EquityTotalReturnSwap
```

```python
trs = ql.EquityTotalReturnSwap(
    ql.SwapType.Payer, 1_000_000.0, schedule,
    equity_index, ibor_index, ql.Actual360(), 0.005,
)
trs.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(trs.fairMargin())
```

### Swaps

```{eval-rst}
.. autoclass:: pyquantlib.VanillaSwap
```

```{eval-rst}
.. autoclass:: pyquantlib.MakeVanillaSwap
```

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedSwap
```

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponSwap
```

```python
swap = ql.ZeroCouponSwap(
    ql.SwapType.Receiver, 1_000_000.0, start_date, maturity_date,
    0.04, ql.Actual365Fixed(), schedule, euribor6m,
)
swap.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(swap.fairFixedPayment(curve))
```

```{eval-rst}
.. autoclass:: pyquantlib.AssetSwap
```

```python
asset_swap = ql.AssetSwap(False, bond, 100.0, schedule, euribor6m, 0.0)
asset_swap.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(asset_swap.fairSpread())
```

### Inflation swaps

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponInflationSwap
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.YearOnYearInflationSwap
   :members:
   :undoc-members:
```

### Caps, floors, collars

```{eval-rst}
.. autoclass:: pyquantlib.CapFloor
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.Cap
.. autoclass:: pyquantlib.Floor
.. autoclass:: pyquantlib.Collar
```

```python
leg = ql.IborLeg(schedule, euribor).withNotionals([1_000_000.0]).build()

cap   = ql.Cap(leg, [0.05])
floor = ql.Floor(leg, [0.03])
clr   = ql.Collar(leg, [0.05], [0.03])

cap.setPricingEngine(ql.BlackCapFloorEngine(curve, 0.20))
print(cap.NPV(), cap.impliedVolatility(cap.NPV(), curve_handle, 0.20))
```

#### YoY inflation caps and floors

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCapFloor
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.YoYInflationCapFloorType
   :members:
   :undoc-members:
```

| Value | Variant |
|---|---|
| `Cap` | YoY inflation cap |
| `Floor` | YoY inflation floor |
| `Collar` | YoY inflation collar |

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCap
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.YoYInflationFloor
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.YoYInflationCollar
   :members:
   :undoc-members:

.. autofunction:: pyquantlib.MakeYoYInflationCapFloor
```

### Forward rate agreement

```{eval-rst}
.. autoclass:: pyquantlib.ForwardRateAgreement
   :members:
```

```python
fra = ql.ForwardRateAgreement(
    euribor, value_date, ql.PositionType.Long,
    0.04, 1_000_000.0, curve,
)
print(fra.NPV(), fra.forwardRate())
```

### Swaptions

```{eval-rst}
.. autoclass:: pyquantlib.Swaption
```

```{eval-rst}
.. autoclass:: pyquantlib.MakeSwaption
```

```python
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years), curve, curve)
swaption = ql.MakeSwaption(
    swap_index, ql.Period(1, ql.Years), 0.04,
    pricingEngine=engine,
)
```

### Composite instruments

```{eval-rst}
.. autoclass:: pyquantlib.CompositeInstrument
```

```python
composite = ql.CompositeInstrument()
composite.add(option1)              # weight = 1.0
composite.add(option2)
composite.subtract(option3)         # weight = -1.0
composite.add(option4, 0.5)         # weight = 0.5
print(composite.NPV())
```

### Credit instruments

```{eval-rst}
.. autoclass:: pyquantlib.FaceValueClaim
.. autoclass:: pyquantlib.FaceValueAccrualClaim
```

```python
claim = ql.FaceValueClaim()
loss  = claim.amount(default_date, 1_000_000.0, 0.4)   # 600,000
```

```{eval-rst}
.. autoclass:: pyquantlib.CreditDefaultSwap
```

```python
cds = ql.CreditDefaultSwap(
    ql.ProtectionSide.Buyer, 10_000_000.0, 0.01,
    schedule, ql.Following, ql.Actual360(),
)
cds.setPricingEngine(ql.MidPointCdsEngine(default_curve, 0.4, discount_curve))
print(cds.fairSpread())
```

```{eval-rst}
.. autofunction:: pyquantlib.cdsMaturity
```

### Vanilla and basket options

```{eval-rst}
.. autoclass:: pyquantlib.VanillaOption
```

```{eval-rst}
.. autoclass:: pyquantlib.BasketOption
```

### Barrier options

```{eval-rst}
.. autoclass:: pyquantlib.BarrierOption
```

| Barrier type | Activation |
|---|---|
| `DownIn` | Activated when spot falls below barrier |
| `UpIn` | Activated when spot rises above barrier |
| `DownOut` | Knocked out when spot falls below barrier |
| `UpOut` | Knocked out when spot rises above barrier |

```{eval-rst}
.. autoclass:: pyquantlib.DoubleBarrierOption
```

| Type | Activation |
|---|---|
| `KnockOut` | Knocked out if either barrier is hit |
| `KnockIn` | Activated if either barrier is hit |
| `KIKO` | Lower KI, upper KO |
| `KOKI` | Lower KO, upper KI |

```{eval-rst}
.. autoclass:: pyquantlib.PartialTimeBarrierOption
```

Barrier monitored over a partial time window.

```{eval-rst}
.. autoclass:: pyquantlib.SoftBarrierOption
```

Soft barrier with proportional knock-in / out over a barrier range.

```{eval-rst}
.. autoclass:: pyquantlib.TwoAssetBarrierOption
```

Barrier monitoring on a second (correlated) asset.

### Asian options

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousAveragingAsianOption
```

```{eval-rst}
.. autoclass:: pyquantlib.DiscreteAveragingAsianOption
```

```python
fixing_dates = [today + ql.Period(f"{i}M") for i in range(1, 13)]

asian_geom = ql.DiscreteAveragingAsianOption(
    ql.AverageType.Geometric, 0.0, 0, fixing_dates, payoff, exercise,
)
asian_geom.setPricingEngine(
    ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(process)
)

asian_arith = ql.DiscreteAveragingAsianOption(
    ql.AverageType.Arithmetic, 0.0, 0, fixing_dates, payoff, exercise,
)
asian_arith.setPricingEngine(ql.TurnbullWakemanAsianEngine(process))
```

### Lookback options

```{eval-rst}
.. autoclass:: pyquantlib.ContinuousFloatingLookbackOption
.. autoclass:: pyquantlib.ContinuousFixedLookbackOption
.. autoclass:: pyquantlib.ContinuousPartialFloatingLookbackOption
.. autoclass:: pyquantlib.ContinuousPartialFixedLookbackOption
```

### Cliquet options

```{eval-rst}
.. autoclass:: pyquantlib.CliquetOption
```

```python
payoff   = ql.PercentageStrikePayoff(ql.Call, 1.0)
exercise = ql.EuropeanExercise(expiry)
resets   = [today + ql.Period(f"{i}M") for i in range(3, 12, 3)]
option   = ql.CliquetOption(payoff, exercise, resets)
```

### Compound, chooser, exchange options

```{eval-rst}
.. autoclass:: pyquantlib.CompoundOption
```

```{eval-rst}
.. autoclass:: pyquantlib.SimpleChooserOption
.. autoclass:: pyquantlib.ComplexChooserOption
```

```{eval-rst}
.. autoclass:: pyquantlib.MargrabeOption
```

```python
option = ql.MargrabeOption(1, 1, exercise)
option.setPricingEngine(engine)
print(option.delta1(), option.delta2(), option.gamma1(), option.gamma2())
```

### Forward-start and quanto options

```{eval-rst}
.. autoclass:: pyquantlib.ForwardVanillaOption
```

```{eval-rst}
.. autoclass:: pyquantlib.QuantoVanillaOption
```

Quanto-specific Greeks: `qvega()`, `qrho()`, `qlambda()`.

### Variance swaps

```{eval-rst}
.. autoclass:: pyquantlib.VarianceSwap
```

### Exotic swaps and swaptions

```{eval-rst}
.. autoclass:: pyquantlib.NonstandardSwap
.. autoclass:: pyquantlib.FloatFloatSwap
```

`FloatFloatSwap` exposes `fairSpread1()` and `fairSpread2()` for the two floating legs once a pricing engine is attached.

```{eval-rst}
.. autoclass:: pyquantlib.MultipleResetsSwap
```

A swap in which each floating coupon is computed from multiple fixings within the coupon period, either compounded or averaged. Used for term SOFR / SONIA structures.

```python
index = ql.Euribor3M(curve)
index.addFixing(ql.Date(11, ql.January, 2024), 0.05)

swap = ql.MultipleResetsSwap(
    ql.VanillaSwap.Payer,
    1_000_000.0, fixed_schedule, 0.04, ql.Thirty360(ql.Thirty360.BondBasis),
    float_schedule, index, 2, 0.0, ql.Actual360(),
)
swap.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(swap.NPV())
```

```{eval-rst}
.. autoclass:: pyquantlib.NonstandardSwaption
.. autoclass:: pyquantlib.FloatFloatSwaption
```

### FX forward

```{eval-rst}
.. autoclass:: pyquantlib.FxForward
```

`FxForward` supports two constructors: a nominal-based form (two currency notionals) and a rate-based form (source notional, rate, and maturity). The engine is {py:class}`pyquantlib.DiscountingFxForwardEngine`.

```python
eur = ql.EURCurrency()
usd = ql.USDCurrency()

# Nominal form: receive EUR 1M, pay USD 1.08M in 1Y
fwd = ql.FxForward(
    1_000_000.0, eur,
    1_080_000.0, usd,
    ql.Date(15, ql.June, 2026),
    paySourceCurrency=False,
)

# Rate form: buy EUR 1M at forward rate 1.09
fwd2 = ql.FxForward(
    1_000_000.0, eur, usd,
    ql.SimpleQuote(1.09),
    ql.Date(15, ql.June, 2026),
    paySourceCurrency=False,
)

engine = ql.DiscountingFxForwardEngine(eur_curve, usd_curve, spot_fx)
fwd.setPricingEngine(engine)
print(fwd.NPV(), fwd.fairForwardRate())
```

### Cross-currency swaps

```{eval-rst}
.. autoclass:: pyquantlib.ConstNotionalCrossCurrencySwap
.. autoclass:: pyquantlib.ConstNotionalCrossCurrencyBasisSwap
.. autoclass:: pyquantlib.ConstNotionalCrossCurrencyFixedVsFloatingSwap
```

Notionals are constant and exchanged at inception and maturity. Each leg carries its own
currency, and the engine is
{py:class}`pyquantlib.DiscountingConstNotionalCrossCurrencySwapEngine`, which discounts each
leg on its own curve and reports the NPV in the domestic currency. Per-leg results are
available in the leg currency through `inCcyLegNPV()` and `inCcyLegBPS()`, alongside the
converted `legNPV()` and `legBPS()` inherited from {py:class}`pyquantlib.Swap`.

```python
eur = ql.EURCurrency()
usd = ql.USDCurrency()

# Pay EUR 3M Euribor + 10bp, receive USD 3M Libor
basis = ql.ConstNotionalCrossCurrencyBasisSwap(
    10_000_000.0, eur, eur_schedule, ql.Euribor3M(eur_curve), 0.0010, 1.0,
    10_500_000.0, usd, usd_schedule, ql.USDLibor(ql.Period(3, ql.Months), usd_curve), 0.0, 1.0,
)

# NPV in USD: USD is the domestic currency of the engine
engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
    usd, usd_curve, eur, eur_curve, spot_fx,
)
basis.setPricingEngine(engine)
print(basis.NPV(), basis.fairPaySpread())
print(basis.inCcyLegNPV(0), basis.legCurrency(0).code())
```

The arguments following the two gearings apply only when a leg's index is an overnight index:
`payLookbackDays` and `recLookbackDays` accept `None` for the QuantLib default, and the
averaging method is set through {py:class}`pyquantlib.RateAveraging`.

### Bond forwards

```{eval-rst}
.. autoclass:: pyquantlib.base.Forward
.. autoclass:: pyquantlib.ForwardTypePayoff
.. autoclass:: pyquantlib.BondForward
```

### Payoffs

```{eval-rst}
.. autoclass:: pyquantlib.PlainVanillaPayoff
```

| Type | Payoff |
|---|---|
| `Call` | $\max(S - K, 0)$ |
| `Put` | $\max(K - S, 0)$ |

```{eval-rst}
.. autoclass:: pyquantlib.CashOrNothingPayoff
```

| Type | Payoff |
|---|---|
| `Call` | $C$ if $S > K$, else $0$ |
| `Put` | $C$ if $S < K$, else $0$ |

```{eval-rst}
.. autoclass:: pyquantlib.AssetOrNothingPayoff
```

| Type | Payoff |
|---|---|
| `Call` | $S$ if $S > K$, else $0$ |
| `Put` | $S$ if $S < K$, else $0$ |

```{eval-rst}
.. autoclass:: pyquantlib.GapPayoff
```

| Type | Payoff |
|---|---|
| `Call` | $S - K_2$ if $S > K_1$, else $0$ |
| `Put` | $K_2 - S$ if $S < K_1$, else $0$ |

```{eval-rst}
.. autoclass:: pyquantlib.PercentageStrikePayoff
```

Strike expressed as a moneyness ratio of the asset price.

```{eval-rst}
.. autoclass:: pyquantlib.SuperFundPayoff
.. autoclass:: pyquantlib.SuperSharePayoff
.. autoclass:: pyquantlib.FloatingTypePayoff
```

```{eval-rst}
.. autoclass:: pyquantlib.MinBasketPayoff
.. autoclass:: pyquantlib.MaxBasketPayoff
.. autoclass:: pyquantlib.AverageBasketPayoff
.. autoclass:: pyquantlib.SpreadBasketPayoff
```

### Exercise types

```{eval-rst}
.. autoclass:: pyquantlib.EuropeanExercise
.. autoclass:: pyquantlib.AmericanExercise
.. autoclass:: pyquantlib.BermudanExercise
```

```python
european = ql.EuropeanExercise(expiry)
american = ql.AmericanExercise(today, expiry)
bermudan = ql.BermudanExercise([d1, d2, d3])
```

### Futures

```{eval-rst}
.. autoclass:: pyquantlib.Futures
```

`Futures` carries the date-rule conventions used by futures rate helpers: `IMM` (third Wednesday of March, June, September, December), `ASX` (second Friday of the same months), and `Custom`.

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexFuture
   :members:
```

```python
sofr = ql.Sofr(curve)
future = ql.OvernightIndexFuture(sofr,
                                 ql.Date(17, 9, 2025),   # value date
                                 ql.Date(17, 12, 2025))  # delivery date
```

The averaging method defaults to `RateAveraging.Compound`; pass `RateAveraging.Simple` for an averaged contract. A convexity-adjustment quote may be supplied either as a handle or as a plain quote.

```{eval-rst}
.. autoclass:: pyquantlib.PerpetualFutures
   :members:
```

```python
perp = ql.PerpetualFutures(ql.PerpetualFutures.Linear,
                           ql.PerpetualFutures.FundingWithCurrentSpot)
perp.setPricingEngine(engine)
```

`PayoffType` selects the settlement currency (`Linear`, `Inverse`, `Quanto`); `FundingType` selects whether funding accrues against the previous or current spot. Pricing requires {py:class}`pyquantlib.DiscountingPerpetualFuturesEngine`.

### Swing options

```{eval-rst}
.. autoclass:: pyquantlib.SwingExercise
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.VanillaForwardPayoff
```

```{eval-rst}
.. autoclass:: pyquantlib.VanillaSwingOption
```

```python
dates = [today + ql.Period(f"{m}M") for m in range(1, 13)]
exercise = ql.SwingExercise(dates)
payoff = ql.VanillaForwardPayoff(ql.Call, 100.0)
option = ql.VanillaSwingOption(payoff, exercise,
                               minExerciseRights=1, maxExerciseRights=5)
option.setPricingEngine(ql.FdSimpleBSSwingEngine(process))
```

`SwingExercise` restricts exercise to a fixed set of date-times; `minExerciseRights` / `maxExerciseRights` bound how many of those dates may be exercised over the option's life.

## See also

- {doc}`/concepts/pricing-engines`: instrument / engine separation and the bridge pattern
- {doc}`pricingengines`: engines that consume these instruments
- {doc}`cashflows`: legs and coupons that feed swaps and bonds
- {doc}`/cookbook/compare-engines`: same option, three engines
