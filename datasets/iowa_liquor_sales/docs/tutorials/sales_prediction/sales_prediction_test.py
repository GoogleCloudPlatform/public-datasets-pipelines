import pytest
from testbook import testbook


@pytest.mark.timeout(900)
@testbook(
    "datasets/iowa_liquor_sales/docs/tutorials/sales_prediction/liquor_sales_predictions.ipynb"
)
def test_run_notebook(tb):
    tb.inject(
        """
        from unittest import mock
        import pandas as pd
        import random
        mock_client = mock.MagicMock()
        mock_df = pd.DataFrame()
        mock_df['date'] = ['2020-12-15' for x in range(25)] + ['2021-5-15' for x in range(25)]
        mock_df['city'] = ['des_moines'] * 50
        mock_df['category_name'] = ['straight rye whiskies'] * 50
        mock_df['pack'] = [random.randint(1, 12) for x in range(50)]
        mock_df['state_bottle_retail'] = [random.uniform(1, 11) for x in range(50)]
        mock_df['bottles_sold'] = [random.randint(1, 12) for x in range(50)]
        mock_df['sale_dollars'] = [random.uniform(1, 50) for x in range(50)]
        p1 = mock.patch.object(bigquery, 'Client', return_value=mock_client)
        mock_client.query().result().to_dataframe.return_value = mock_df
        p1.start()
        """,
        before=5,
        run=False,
    )

    tb.execute()
    dataframe = tb.get("dataframe")
    assert dataframe.shape == (50, 6)

    feat_importances = tb.get("feat_importances")
    print(feat_importances)
    assert feat_importances is not None
