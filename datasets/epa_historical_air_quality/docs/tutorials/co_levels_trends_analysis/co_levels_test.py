import pytest
from testbook import testbook


@pytest.mark.timeout(900)
@testbook(
    "datasets/epa_historical_air_quality/docs/tutorials/co_levels_trends_analysis/co_levels.ipynb"
)
def test_run_notebook(tb):
    tb.inject(
        """
        from unittest import mock
        import pandas as pd
        import datetime
        import random
        mock_client = mock.MagicMock()
        mock_df = pd.DataFrame()
        dates = []
        for year in [1990, 1991, 1992]:
            for month in range(1, 13):
                for day in range(1, 28):
                    d = datetime.date(year, month, day)
                    dates.append(d)
        mock_df['date'] = dates
        mock_df["co_level"] = [random.uniform(0.5, 2.5) for _ in range(len(dates))]
        p1 = mock.patch.object(bigquery, 'Client', return_value=mock_client)
        mock_client.query().result().to_dataframe.return_value = mock_df
        p1.start()
        """,
        before=4,
        run=False,
    )

    tb.execute()
    dataframe = tb.get("dataframe")
    mock_df = tb.get("mock_df")
    assert dataframe.shape == mock_df.shape

    year_df = tb.get("year_df")
    print(year_df)
    assert year_df is not None
    assert len(year_df) == 3
