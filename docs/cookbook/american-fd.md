# American option via finite difference

Demonstrates the binding pattern for early-exercise pricing. Building an American option only differs from a European one in the `Exercise` object: `AmericanExercise(earliest, latest)` instead of `EuropeanExercise(maturity)`. The `FdBlackScholesVanillaEngine` reads the exercise type and wires in `FdmAmericanStepCondition` automatically.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
div  = ql.SimpleQuote(0.03)
vol  = ql.SimpleQuote(0.20)
rf  = ql.FlatForward(today, rate, dc)
dq  = ql.FlatForward(today, div, dc)
v   = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
process = ql.GeneralizedBlackScholesProcess(spot, dq, rf, v)

# ATM 1Y put. With a positive dividend yield, early exercise has value.
payoff   = ql.PlainVanillaPayoff(ql.Put, 100.0)
maturity = today + ql.Period("1Y")

european = ql.VanillaOption(payoff, ql.EuropeanExercise(maturity))
american = ql.VanillaOption(payoff, ql.AmericanExercise(today, maturity))

# Reference: European put has no early-exercise component.
european.setPricingEngine(ql.AnalyticEuropeanEngine(process))
print(f"European put (analytic):                 {european.NPV():.4f}")

# American put via finite difference. The engine inspects the option's
# AmericanExercise and adds an FdmAmericanStepCondition: at every time
# step, it takes max(continuation, intrinsic).
fd_engine = ql.FdBlackScholesVanillaEngine(process, tGrid=200, xGrid=200)
american.setPricingEngine(fd_engine)
print(f"American put (FD 200x200):               {american.NPV():.4f}")

# Grid convergence: small grids underprice early exercise.
print()
print("FD grid convergence:")
for t, x in [(50, 50), (100, 100), (200, 200), (400, 400)]:
    american.setPricingEngine(
        ql.FdBlackScholesVanillaEngine(process, tGrid=t, xGrid=x)
    )
    print(f"  tGrid={t:>3}  xGrid={x:>3}                    {american.NPV():.4f}")

# Cross-check against other engines that handle American exercise.
print()
print("Same American option, different engines:")

american.setPricingEngine(ql.BjerksundStenslandApproximationEngine(process))
print(f"  Bjerksund-Stensland 2002 (analytic):     {american.NPV():.4f}")

american.setPricingEngine(ql.BaroneAdesiWhaleyApproximationEngine(process))
print(f"  Barone-Adesi-Whaley (analytic):          {american.NPV():.4f}")

american.setPricingEngine(ql.QdPlusAmericanEngine(process))
print(f"  QdPlus (analytic-ish):                   {american.NPV():.4f}")

american.setPricingEngine(ql.BinomialVanillaEngine(process, "crr", 1000))
print(f"  Binomial CRR (n=1000):                   {american.NPV():.4f}")
```

## Output

```
European put (analytic):                 6.7309
American put (FD 200x200):               6.9710

FD grid convergence:
  tGrid= 50  xGrid= 50                    6.9607
  tGrid=100  xGrid=100                    6.9684
  tGrid=200  xGrid=200                    6.9710
  tGrid=400  xGrid=400                    6.9721

Same American option, different engines:
  Bjerksund-Stensland 2002 (analytic):     6.9057
  Barone-Adesi-Whaley (analytic):          6.9883
  QdPlus (analytic-ish):                   6.9785
  Binomial CRR (n=1000):                   6.9719
```

The early-exercise premium on this option is roughly `6.97 − 6.73 = 0.24`, i.e. about 3.5% of the European price.

## Key points

- **`AmericanExercise(earliest, latest)`** is the only structural difference from the European pricing setup. Everything else (payoff, process, engine constructor) stays the same.
- **`FdBlackScholesVanillaEngine` is exercise-aware.** It does not take a separate "American" flag; it reads the option's exercise object at pricing time and attaches an `FdmAmericanStepCondition` to the FD scheme when the exercise is American. See {doc}`/concepts/finite-difference` for the underlying piece-wise wiring.
- **Several engines accept American exercise.** Analytic approximations (Bjerksund-Stensland, Barone-Adesi-Whaley, QdPlus) bypass the PDE entirely and return a closed-form answer; binomial trees (`BinomialVanillaEngine`) use a Cox-Ross-Rubinstein lattice; FD discretizes the PDE on a (time, spot) grid. From the option's perspective they are all engines and are all attached the same way.
- **A European option with the FD engine still works.** `FdBlackScholesVanillaEngine` reads `EuropeanExercise` too; it simply skips the step condition.

## Pitfalls

- **Discrete dividends need wiring.** This recipe uses a *continuous* dividend yield via `FlatForward`. For *discrete* dividends, the FD engine has a separate constructor that accepts a `DividendSchedule` and adds an `FdmDividendHandler`. Skipping that handler produces a price wrong by a clean dividend amount. See {doc}`/concepts/finite-difference` (FD common pitfalls).
- **Grid sizes are not free.** `tGrid=400, xGrid=400` is ~16x slower than `tGrid=100, xGrid=100`. Convergence is monotonic and smooth for vanilla payoffs; pick the smallest grid where the price has stabilised to the required tolerance.
- **The earliest-exercise date matters.** `AmericanExercise(today, maturity)` allows exercise from now. `AmericanExercise(today + ql.Period("3M"), maturity)` is technically a Bermudan-American hybrid: no exercise in the first three months, then continuous exercise to maturity. The FD step condition respects the earliest date.

## See also

- {doc}`/concepts/finite-difference`: meshers, operators, schemes, and step conditions
- {doc}`/api/pricingengines`: all American engines (FD, binomial, analytic approximations)
- {doc}`compare-engines`: the same pattern with European exercise
