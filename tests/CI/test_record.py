from feo.client.record import RecordCollection

TEST_DATUM_DETAIL = "forest_landuse"


def test_record_collection_search():
    records = RecordCollection()
    assert isinstance(records, RecordCollection)
    resp = records.search(datum_detail=TEST_DATUM_DETAIL)

    assert len(resp) == 10  # Default page limit
    assert resp.datum_detail.unique() == TEST_DATUM_DETAIL
