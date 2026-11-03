# Data

Four CSV files in this repository are third-party market data. They are **not**
covered by the MIT licence in `LICENSE` — see [Licensing](#licensing) below.

## What is committed

| File | Instrument | Rows | Coverage |
|---|---|---|---|
| `Indo Tambangraya Stock Price History.csv` | ITMG (IDX) | 2 794 | 2015-01-05 → 2026-07-31 |
| `Bank Central Asia Stock Price History.csv` | BBCA (IDX) | 2 794 | 2015-01-05 → 2026-07-31 |
| `Indofood Stock Price History.csv` | INDF (IDX) | 2 794 | 2015-01-05 → 2026-07-31 |
| `Jakarta Stock Exchange Composite Index Historical Data.csv` | JKSE / IHSG | 2 796 | 2015-01-05 → 2026-07-31 |

## Format

These are raw exports, not tidy tables. Each file has the columns
`Date, Price, Open, High, Low, Vol., Change %`, with

- dates as `MM/DD/YYYY` (US order),
- thousands separators in the price columns (`24,575`),
- abbreviated volumes with an `M` / `B` suffix (`153.17M`),
- a `%` sign on `Change %`,
- rows in **descending** date order.

`load_price_csv()` in `bootstrap_qr_fixed.ipynb` handles all of this: it reads with
`thousands=","`, parses dates, sorts ascending, and computes daily **log** returns as
`log(Price_t / Price_{t-1})`. Nothing downstream uses the raw price levels.

## Consistency check

Use this to confirm you are holding the same snapshot the paper used. Starting from
2 794 price observations per stock, the differencing yields 2 793 daily returns, and
after the 500-day warm-up window the rolling backtest produces exactly **2 293**
out-of-sample forecasts per stock and quantile — the count reported in Table 3.

If your reconstruction yields a different number, the snapshot differs (different
download date, or a trading halt filled in differently), and the Table 3 figures will
not reproduce exactly.

## Synthetic fallback — please read

If `DATA_DIR` is left at `None`, the notebook does **not** stop. It prints a warning
and substitutes `make_synthetic_panel()`, a simulated four-asset panel with Student-t
shocks. The VaR backtest then runs to completion and writes a full
`backtest_summary.csv` from **simulated** returns.

The numbers produced in that mode are not the paper's. Before running, set

```python
"DATA_DIR": r"<path to this folder>"
```

and check that the printed observation counts match the table above.

## Licensing

The four CSV files are third-party data obtained from **Investing.com**. The authors
grant no licence over these files, and the MIT licence in `LICENSE` does not extend to
them.

**This has not been verified by us:** the terms of use of Investing.com were not read
when these files were committed. Check them before redistributing, mirroring, or
publishing this repository as an archive.

If redistribution turns out not to be permitted, the alternative is to remove the four
CSVs and ship only a download script plus the derived return series (which the authors
can license). Record the download date alongside the script, because historical price
files are revised after corporate actions and the reconstructed returns will drift.

## Takedown

If you hold rights in these price series and want them removed, open an issue on this
repository or write to the corresponding author, and the files will be removed
promptly.
