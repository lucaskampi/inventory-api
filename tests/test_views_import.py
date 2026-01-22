def test_views_import():
    # simple import test to cover views module
    import entities.views
    assert hasattr(entities.views, "render")
