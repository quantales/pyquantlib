# Finite Difference Methods

QuantLib's finite-difference framework is modular. An FD engine is composed of four pieces: a **mesher** (the grid), a **linear operator** (the discretized PDE), a **time-stepping scheme** (how to march backward), and a set of **boundary conditions** (what happens at the grid edges). PyQuantLib exposes each piece as its own set of bindings, plus pre-built engines that wire them up.

## The four pieces

```{mermaid}
flowchart TB
    Mesher[Mesher<br/>Uniform1d / Concentrating1d / FdmBlackScholesMesher]
    Op[Linear Operator<br/>FdmBlackScholesOp / FdmHestonOp / ...]
    Scheme[Time-stepping Scheme<br/>Douglas / CraigSneyd / Hundsdorfer / ...]
    BC[Boundary Conditions<br/>FdmDirichlet / Neumann / TimeDep variants]
    Inner[Inner-value calculator<br/>FdmLogInnerValue / Cell averaging]
    Step[Step conditions<br/>American early exercise / Bermudan / Dividends]

    Mesher --> Op
    Mesher --> Inner
    Op --> Scheme
    BC --> Scheme
    Step --> Scheme
    Inner --> Scheme
    Scheme --> Solver[FdmBackwardSolver]
    Solver --> Result[Option NPV + Greeks]
```

## Pre-built FD engines

Assembling the pieces directly is rarely necessary. The bindings include pre-built engines for the common cases:

| Engine | Underlying PDE |
|---|---|
| `FdBlackScholesVanillaEngine` | 1D BS PDE |
| `FdBlackScholesShoutEngine` | 1D BS PDE + shout step condition |
| `FdBlackScholesAsianEngine` | 2D (spot + average) |
| `FdHestonVanillaEngine` | 2D Heston PDE |
| `FdHestonBarrierEngine` | 2D Heston + barrier BCs |
| `FdHestonRebateEngine` | 2D Heston + rebate handling |
| `FdSabrVanillaEngine` | 2D SABR PDE |
| `FdCEVVanillaEngine` | 1D CEV PDE |
| `Fdm2dBlackScholesSolver` | 2D BS (two assets) |

`MakeFdHestonVanillaEngine` is the keyword-argument builder for the Heston engine. It mirrors QuantLib's C++ `Make*` builder pattern as a single Python call.

## Step conditions

Some payoffs need an action at every time step, not just at expiry. **Step conditions** are the mechanism:

- `FdmAmericanStepCondition`: at every step, check if early-exercise value > continuation value.
- `FdmBermudanStepCondition`: same, but only on a list of exercise dates.
- `FdmDividendHandler`: apply a discrete dividend (jump in spot) at the dividend date.
- `FdmArithmeticAverageCondition`: evolve the running-average state.

Pre-built engines wire these in based on the instrument's exercise type and dividend schedule.

## Common pitfalls

- **Forgetting dividends**: instruments with discrete dividends require an `FdmDividendHandler` to be wired into the FD engine. The pre-built engines do this from the instrument's dividend schedule. Custom engines that skip it produce a price wrong by a clean dividend amount.
- **Reference-member lifetimes**: a few FD operator classes store constructor arguments by reference. The bindings extend their lifetimes via custom holders, but custom Python operators that mimic the C++ pattern can dangle.

## See also

- {doc}`/api/methods`: full FD module reference (meshers, operators, schemes, BCs, step conditions)
- {doc}`/api/pricingengines`: pre-built FD engines
