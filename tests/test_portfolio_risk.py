import unittest
from unittest.mock import patch

import pandas as pd

import main


class PortfolioRiskTests(unittest.TestCase):
    def history(self, values):
        return pd.DataFrame(
            {"Close": values},
            index=pd.date_range("2026-10-19", periods=len(values), freq="D"),
        )

    def fake_download(self, ticker, period="5d"):
        if ticker == "USDCNH=X":
            return self.history([7.0, 7.1])
        if ticker == "NVDA":
            return self.history([100.0, 110.0])
        if ticker == "000300.SS":
            return self.history([100.0, 105.0])
        return self.history([100.0, 110.0])

    def test_fx_conversion_and_normalized_portfolio_return(self):
        with patch.object(main, "safe_yf_download", side_effect=self.fake_download):
            rows, total_return_pct, usd_cnh, alerts = main.evaluate_portfolio_fx_and_drift()

        self.assertEqual(len(rows), 5)
        self.assertAlmostEqual(usd_cnh, 7.1)
        # 80% USD-denominated holdings earn the local 10% return plus FX move;
        # the 20% RMB index earns 5%, all combined on normalized weights.
        self.assertAlmostEqual(total_return_pct, 10.2571428571, places=6)
        self.assertEqual(alerts, [])

    def test_missing_holding_data_fails_closed(self):
        def missing_nvda(ticker, period="5d"):
            if ticker == "NVDA":
                return None
            return self.fake_download(ticker, period)

        with patch.object(main, "safe_yf_download", side_effect=missing_nvda):
            rows, total_return_pct, usd_cnh, alerts = main.evaluate_portfolio_fx_and_drift()

        self.assertEqual(rows, [])
        self.assertEqual(total_return_pct, 0.0)
        self.assertEqual(usd_cnh, 7.1)
        self.assertIn("NVDA", [item["ticker"] for item in alerts])


if __name__ == "__main__":
    unittest.main()
