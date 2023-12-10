import urllib.error
from unittest.mock import MagicMock, patch

import pytest
import toga

from fi_widgets.app import FIWidgets


@pytest.fixture
def app():
    return FIWidgets(formal_name='FI Widgets', app_id='com.test')


# Test load_webview()
def test_load_webview_displays_main_window(app):
    app.main_window = MagicMock()
    app.webview = MagicMock()
    app.load_webview()
    app.main_window.content == app.webview
    app.main_window.show.assert_called_once()


# Test connected()
@patch('urllib.request.urlopen')
def test_connected_good_connection(mock_urlopen, app):
    mock_urlopen.return_value = True
    assert app.connected() is True


@patch('urllib.request.urlopen', side_effect=urllib.error.URLError('Test reason'))
def test_connected_without_internet_url_error(mock_urlopen, app):
    assert app.connected() is False


@patch('urllib.request.urlopen', side_effect=TimeoutError)
def test_connected_without_internet_timeout_error(mock_urlopen, app):
    assert app.connected() is False


@patch(
    'urllib.request.urlopen',
    side_effect=urllib.error.HTTPError(
        'https://fi-widgets.com/', 404, 'Not Found', {}, None
    ),
)
def test_connected_with_404_not_found(mock_urlopen, app):
    assert app.connected() is False


# Test refresh_page()
def test_refresh_page_connected(app):
    app.connected = MagicMock(return_value=True)
    app.webview = MagicMock()
    app.load_webview = MagicMock()
    app.refresh_page(MagicMock())
    assert app.webview.url == app.url
    app.load_webview.assert_called_once()


def test_refresh_page_not_connected(app):
    app.connected = MagicMock(return_value=False)
    app.get_refresh_button = MagicMock()
    app.refresh_page(MagicMock())
    app.get_refresh_button.assert_called_once()


# Test get_refresh_button()
def test_get_refresh_button_displays_correct_elements(app):
    app.main_window = MagicMock()
    app.get_refresh_button()
    main_window_content = app.main_window.content

    assert isinstance(main_window_content, toga.Box)
    assert len(main_window_content.children) == 2
    assert isinstance(main_window_content.children[0], toga.Label)
    assert isinstance(main_window_content.children[1], toga.Button)

    app.main_window.show.assert_called_once()


# Test startup()
def test_startup_connected_on_non_android_platform(app, monkeypatch):
    app.connected = MagicMock(return_value=True)
    toga.MainWindow = MagicMock()
    toga.WebView = MagicMock()
    app.main_window = MagicMock()
    app.main_window.show = MagicMock()
    monkeypatch.setattr(toga.platform, 'current_platform', 'some_non_android_platform')
    app.startup()
    toga.MainWindow.assert_called_once_with(title=app.formal_name)
    toga.WebView.assert_called_once()
    assert toga.WebView.return_value.url == app.url
    assert len(app.app.commands) == 1
    app.connected.assert_called_once()
    assert app.main_window.content == toga.WebView.return_value
    app.main_window.show.assert_called_once()


def test_startup_not_connected_on_non_android_platform(app, monkeypatch):
    app.connected = MagicMock(return_value=False)
    app.get_refresh_button = MagicMock()
    monkeypatch.setattr(toga.platform, 'current_platform', 'some_non_android_platform')
    app.startup()
    app.connected.assert_called_once()
    app.get_refresh_button.assert_called_once()


def test_startup_on_android_should_not_have_full_screen_command(app, monkeypatch):
    app.connected = MagicMock(return_value=True)
    monkeypatch.setattr(toga.platform, 'current_platform', 'android')
    app.startup()
    assert len(app.app.commands) == 0
    app.connected.assert_called_once()
    assert app.main_window.content == toga.WebView.return_value
