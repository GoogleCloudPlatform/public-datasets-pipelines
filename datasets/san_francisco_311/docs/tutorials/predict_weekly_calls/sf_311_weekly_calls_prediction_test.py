import pytest
from testbook import testbook


@pytest.mark.timeout(900)
@testbook(
    "datasets/san_francisco_311/docs/tutorials/predict_weekly_calls/sf_311_weekly_calls_prediction.ipynb"
)
def test_run_notebook(tb):
    tb.inject(
        """
        from unittest import mock
        import pandas as pd
        mock_client = mock.MagicMock()
        mock_df = pd.DataFrame()
        mock_df['week'] = range(50)
        mock_df['count'] = range(50)
        mock_df['category'] = 'Tree Maintenance'
        p1 = mock.patch.object(bigquery, 'Client', return_value=mock_client)
        mock_client.query().result().to_dataframe.return_value = mock_df
        p1.start()
        """,
        before=3,
        run=False,
    )

    tb.execute()
    dataframe = tb.get("dataframe")
    assert dataframe.shape == (50, 3)

    train_pred_plot = tb.get("train_pred_plot")
    print(train_pred_plot)
    assert train_pred_plot is not None
