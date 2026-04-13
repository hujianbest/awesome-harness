from packs.metadata import PackCatalog, PackError


def test_pack_catalog_loads_reference_pack():
    catalog = PackCatalog()
    catalog.register({"id": "coding-pack", "kind": "reference", "version": "1.0"})
    pack = catalog.get("coding-pack")
    assert pack["kind"] == "reference"


def test_pack_catalog_rejects_invalid_pack_metadata():
    catalog = PackCatalog()
    try:
        catalog.register({"id": "bad-pack"})
    except PackError as exc:
        assert exc.code == "invalid_pack_metadata"
    else:
        raise AssertionError("expected invalid_pack_metadata")
