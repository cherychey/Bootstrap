# Why the Default Wild Bootstrap Fails for Quantile Regression

Replication material for **H. S. Husain, U. Wijayanti and F. Agustina**, *Why the
Default Wild Bootstrap Fails for Quantile Regression: A Reproducible Simulation Study
of Six Resampling Schemes*, submitted to **Communications in Statistics – Simulation
and Computation** (2026), manuscript ID 264585674.

Earlier circulated under the title *Bootstrap Confidence Intervals for Quantile
Regression under Heavy-Tailed Heteroscedasticity*.

## Contents

| File | Description |
|---|---|
| `bootstrap_qr_fixed.ipynb` | Annotated notebook: simulation, VaR backtesting, figures |
| `regenerate_figures.py` | Rebuilds both figures from `simulation_results.json` in seconds |
| `Indo Tambangraya Stock Price History.csv` | ITMG daily prices |
| `Bank Central Asia Stock Price History.csv` | BBCA daily prices |
| `Indofood Stock Price History.csv` | INDF daily prices |
| `Jakarta Stock Exchange Composite Index Historical Data.csv` | Market index |
| `DATA.md` | Provenance, format and licensing of the four CSV files |
| `LICENSE` | MIT, covering the code only |

`simulation_results.json` is **not** committed — the notebook writes it on the first
full run (see below).

**Quick reference:** code is MIT (`LICENSE`); the four price CSVs are third-party data
and are *not* covered by that licence (`DATA.md`).

## Reproducing the paper

```bash
pip install numpy pandas scipy statsmodels scikit-learn joblib matplotlib jupyter
jupyter notebook bootstrap_qr_fixed.ipynb
```

In the `CONFIG` cell set `TEST_MODE = False` and point `DATA_DIR` at this folder,
then run all cells. Outputs land in `output/`:

- `point_estimator_summary.csv` → Table 1
- `interval_summary.csv` → Table 2
- `backtest_summary.csv` → Table 3
- `simulation_results.json` → input for the figure script below
- `var_ratio_vs_coverage.png` → Figure 1
- `coverage_by_scenario.png` → Figure 2

Seeds are fixed (`SEED = 20260825`) and drawn per replication via
`numpy.random.SeedSequence.spawn`, so results are identical regardless of how many
cores are used. The full run takes several hours; set `TEST_MODE = True` first to
verify the environment in about a minute.

> **Do not leave `DATA_DIR = None`.** The notebook then falls back to
> `make_synthetic_panel()` and will happily produce a complete `backtest_summary.csv`
> from *simulated* returns. It prints a warning, but it does not stop. Check that the
> printed observation counts match the figures in `DATA.md` before trusting Table 3.

To rebuild only the figures from an existing run, without redoing any simulation:

```bash
python regenerate_figures.py output/simulation_results.json
```

Note that the two PNGs are written to the working directory, not to `output/`.

## The error law — read this before re-implementing the DGP

Section 3 of the paper describes the errors as a *standardised skewed-t with ν = 4 and
skewness parameter λ = −0.4* without naming the family. The family used here is the
**two-piece (Fernández–Steel) skewed-t**, implemented in `generate_skewed_t()`:

```python
def generate_skewed_t(n, nu, lam, rng):
    """Skewed-t terstandardisasi (mean 0, varians 1)."""
    e = stats.t.rvs(df=nu, size=n, random_state=rng)
    e = np.where(e < 0, e / (1 - lam), e / (1 + lam))
    e = e - np.mean(e)
    sd = np.std(e)
    return e / sd if sd > 0 else e
```

Two properties are worth knowing before you replace it with something from a library:

- **Sign convention.** With this construction `lam < 0` gives a **right**-skewed law:
  positive draws are stretched by `1/(1 + lam) = 1.67` and negative draws compressed
  by `1/(1 - lam) = 0.71`. This is the opposite of the Azzalini family used by
  Azzalini & Capitanio (2003), where `lam < 0` gives a *left*-skewed law. Passing the
  same ν and λ to an Azzalini skew-t therefore produces a materially different design.
- **Discontinuity at zero.** For `lam != 0` the density jumps at 0 — on the
  standardised scale the left limit is about 0.525 against about 0.225 on the right.
  Kernel estimates of the density at zero (as used by the finite-sample correction of
  Feng, He & Hu) will consequently depend on the bandwidth.

Reference values for the standardised error law used in the paper: sample skewness
≈ 2.4, f(median) ≈ 0.649, f at the 0.05 quantile ≈ 0.139, f at the 0.95 quantile
≈ 0.059.

## Bootstrap schemes implemented

`pairs`, `residual`, `wild` (Feng, He & Hu 2011, with their finite-sample
correction), `wild_nofs` (the same without the correction), `wild_mammen`,
`wild_cluster`, `adaptive`. The FHH continuous weight density of their equation (3)
is also implemented, and is used automatically when 1/8 < tau < 7/8.

Cell 10 of the notebook is an exploratory check written against an earlier
specification (ν = 4.2) and is **not** part of the reported results. Skip it, or run
the notebook with `Run All` and ignore its output.

## Data

Daily price series were downloaded from Investing.com. See `DATA.md` for coverage,
file format, the observation counts that identify this snapshot, and the terms under
which the files may be redistributed.

## Licence

The code — `bootstrap_qr_fixed.ipynb`, `regenerate_figures.py`, and the derived
outputs written to `output/` — is released under the MIT licence, see `LICENSE`.

The four price CSV files are third-party data and are **not** covered by that licence;
see `DATA.md`.

## References

Feng, X., He, X. and Hu, J. (2011). Wild bootstrap for quantile regression.
*Biometrika* **98**(4), 995–999. doi:10.1093/biomet/asr052

Azzalini, A. and Capitanio, A. (2003). Distributions generated by perturbation of
symmetry with emphasis on a multivariate skew t-distribution. *Journal of the Royal
Statistical Society: Series B* **65**(2), 367–389. doi:10.1111/1467-9868.00391
