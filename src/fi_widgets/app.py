"""
A wrapper for the FI Widgets website.
"""
import urllib.request

import toga
from toga.constants import BOLD, CENTER
from toga.style import Pack
from toga.style.pack import COLUMN


class FIWidgets(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://fi-widgets.com/'
        self.primary_color = '#3F9EBD'
        self.font_color = '#ffffff'

    def connected(self):
        """Check to see if there's an internet connection.

        Returns:
            bool"""
        try:
            urllib.request.urlopen(self.url, timeout=3)
            return True
        except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError):
            return False

    def load_webview(self):
        """Load and display a webview in the main window. Sets the content of the
        main window to the specified webview and displays the main window."""
        self.main_window.content = self.webview
        self.main_window.show()

    def get_refresh_button(self):
        """Create and display a refresh button in the main window."""
        label = toga.Label(
            text="No Internet\n:-(",
            style=Pack(
                text_align=CENTER,
                color=self.font_color,
                font_family='sans-serif',
                font_size=25,
                font_weight=BOLD,
                padding=100,
            ),
        )
        refresh_button = toga.Button(
            'Try Again',
            on_press=self.refresh_page,
            style=Pack(
                padding=10, color=self.primary_color, background_color=self.font_color
            ),
        )
        box = toga.Box(
            children=[label, refresh_button],
            style=Pack(
                background_color=self.primary_color,
                direction=COLUMN,
                alignment='center',
            ),
        )
        self.main_window.content = box
        self.main_window.show()

    def refresh_page(self, widget):
        """Refresh the web page in the main window. Checks if the object is currently
        connected to the specified URL. If connected, updates the webview URL to the
        specified URL and reloads the webview by calling `load_webview()`. If not
        connected, displays a refresh button by calling `get_refresh_button()`.

        Args:
            self: The instance of the object.
            widget: The widget triggering the refresh."""
        if self.connected():
            self.webview.url = self.url
            self.load_webview()
        else:
            self.get_refresh_button()

    def full_screen(self, widget):
        """Make the main window full screen if it's currently not, otherwise take
        the main window out of full screen mode if it's full screen already."""
        if self.is_full_screen:
            self.exit_full_screen()
        else:
            self.set_full_screen(self.main_window)

    def startup(self):
        """Initialize and display the main window during application startup.
        Creates a main window with a title using the formal name of the application.
        Initializes a webview and sets its URL. Adds a full screen command to the
        application window on platforms other than Android. Checks if the object is
        connected to the specified URL and displays either the webview or a refresh
        button accordingly."""
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.webview = toga.WebView()
        self.webview.url = self.url

        if toga.platform.current_platform != 'android':
            cmd_full_screen = toga.Command(
                self.full_screen,
                text='Full screen',
                group=toga.Group.APP,
            )
            self.app.commands.add(cmd_full_screen)

        if self.connected():
            self.main_window.content = self.webview
            self.main_window.show()
        else:
            self.get_refresh_button()


def main():
    return FIWidgets()
