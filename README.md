# Bootstrap Confidence Intervals for Quantile Regression under Heavy-Tailed Heteroscedasticity

Replication material for Husain, Wijayanti & Agustina, submitted to *REVSTAT — Statistical Journal*.

## Contents

| File | Description |
|---|---|
| `bootstrap_qr_fixed.ipynb` | Annotated notebook: simulation, VaR backtesting, figures |
| `regenerate_figures.py` | Rebuilds both figures from `simulation_results.json` in seconds |
| `Indo Tambangraya Stock Price History.csv` | ITMG daily prices |
| `Bank Central Asia Stock Price History.csv` | BBCA daily prices |
| `Indofood Stock Price History.csv` | INDF daily prices |
| `Jakarta Stock Exchange Composite Index Historical Data.csv` | Market index |

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
- `var_ratio_vs_coverage.png` → Figure 1
- `coverage_by_scenario.png` → Figure 2

Seeds are fixed (`SEED = 20260825`) and drawn per replication via
`numpy.random.SeedSequence.spawn`, so results are identical regardless of how many
cores are used. The full run takes several hours; set `TEST_MODE = True` first to
verify the environment in about a minute.

## Bootstrap schemes implemented

`pairs`, `residual`, `wild` (Feng, He & Hu 2011, with their finite-sample
correction), `wild_nofs` (the same without the correction), `wild_mammen`,
`wild_cluster`, `adaptive`. The FHH continuous weight density of their equation (3)
is also implemented, and is used automatically when 1/8 < tau < 7/8.

## Data

Daily price series were downloaded from Investing.com. Please check their terms of
use before redistributing these files; if redistribution is not permitted, replace
them with a download script and keep only the derived return series.

## Reference

Feng, X., He, X. and Hu, J. (2011). Wild bootstrap for quantile regression.
*Biometrika* **98**(4), 995–999.
