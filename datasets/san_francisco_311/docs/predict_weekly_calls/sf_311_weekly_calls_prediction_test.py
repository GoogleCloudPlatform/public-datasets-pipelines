from testbook import testbook


@testbook('./sf_311_weekly_calls_prediction.ipynb')
def test_get_details(tb):
    tb.inject(
        """
        from unittest import mock
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
        run=False
    )

    tb.execute()
    dataframe = tb.get('dataframe')
    assert dataframe.shape == (50, 3)

    train_predict_plot = tb.get('train_predict_plot')
    print(train_predict_plot)
    assert train_predict_plot is not None

