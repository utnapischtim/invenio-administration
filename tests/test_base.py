import pytest
from mock_module.administration.mock import MockView, MockViewAlternate

from invenio_administration.views.base import AdminBaseView


class TestCustomView(AdminBaseView):
    name = "Test Custom View"
    extension_name = "test-custom-view"
    category = "Test category"


def test_view_registration_from_entry_point(
    mock_extension, current_admin_core, test_app
):
    """Test view registration from entry point."""
    # Validate extension is registered
    assert mock_extension is not None

    # Assert view registration
    registered_view = list(
        filter(lambda x: x.view_class == MockView, current_admin_core.views)
    )
    assert len(registered_view) == 1
    assert registered_view[0].view_class == MockView

    # Assert url is registered
    custom_view_rule = [
        x
        for x in test_app.url_map.iter_rules()
        if x.rule == f"{current_admin_core.url}/{MockView.url}"
    ]
    assert len(custom_view_rule) == 1

    # Validate that two views are registered from the same module
    # Assert view registration
    registered_view = list(
        filter(lambda x: x.view_class == MockViewAlternate, current_admin_core.views)
    )
    assert len(registered_view) == 1
    assert registered_view[0].view_class == MockViewAlternate

    # Assert url is registered
    custom_view_rule = [
        x
        for x in test_app.url_map.iter_rules()
        if x.rule == f"{current_admin_core.url}/{MockViewAlternate.url}"
    ]
    assert len(custom_view_rule) == 1


def test_view_registration_duplicated(current_admin_ext, test_app, mock_extension_name):
    """Test duplicated view registration."""
    dup_cls = MockView
    dup_cls.extension_name = mock_extension_name

    with pytest.raises(ValueError):
        current_admin_ext.register_view(
            MockView, extension_name=dup_cls.extension_name, app=test_app
        )
