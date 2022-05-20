import pytest
from testbook import testbook


@pytest.mark.timeout(900)
@testbook("datasets/gbif/docs/tutorials/biodiversity_map/australia.ipynb")
def test_run_notebook(tb):
    tb.inject(
        """
        from unittest import mock
        import pandas as pd
        mock_client = mock.MagicMock()
        mock_df = pd.DataFrame()
        mock_df['decimallatitude'] = [-20 + (x / 10000.0) for x in range(10000)]
        mock_df['decimallongitude'] = [120 + (x / 10000.0) for x in range(10000)]
        mock_df['kingdom'] = 'Animalia'
        p1 = mock.patch.object(bigquery, 'Client', return_value=mock_client)
        mock_client.query().result().to_dataframe.return_value = mock_df
        p1.start()
        """,
        before=3,
        run=False,
    )

    tb.execute()
    dataframe = tb.get("dataframe")
    assert dataframe.shape == (10000, 3)

    ax = tb.get("ax")
    print(ax)
    assert ax is not None
