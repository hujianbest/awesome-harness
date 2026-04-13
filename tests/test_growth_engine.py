from continuity.stores import ContinuityStore, ContinuityError


def test_continuity_store_reads_written_memory_bucket():
    store = ContinuityStore()
    store.write("memory", "k1", {"value": "v1"})
    item = store.read("memory", "k1")
    assert item["value"] == "v1"


def test_continuity_store_rejects_unknown_bucket():
    store = ContinuityStore()
    try:
        store.write("unknown", "k1", {"value": "v1"})
    except ContinuityError as exc:
        assert exc.code == "unknown_bucket"
    else:
        raise AssertionError("expected unknown_bucket")
