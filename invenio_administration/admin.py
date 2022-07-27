from invenio_administration.dashboard import AdminDashboardView


class Administration:
    """Admin views core manager."""

    def __init__(
        self,
        app=None,
        name=None,
        url=None,
        dashboard_view=None,
        ui_endpoint=None,
        base_template=None,
    ):
        """Constructor.

        :param app: flask application
        :param name: application name, defaults to "Admin"
        :param url: base admin url to register the dashboard view and subviews
        :param dashboard_view: home page view
        :param ui_endpoint: base UI endpoint,
                         leaves flexibility to implement two different admin apps,
                         or to provide custom endpoint.
        :param base_template: base admin template. Defaults to "admin/base.html"
        """
        super().__init__()

        self.app = app

        self._views = []
        self._menu = []
        self._menu_categories = dict()
        self._menu_links = []

        if name is None:
            name = "Administration"
        self.name = name

        self.dashboard_view = dashboard_view or AdminDashboardView(
            endpoint=ui_endpoint, url=url
        )
        # self.ui_endpoint = ui_endpoint or self.dashboard_view.endpoint
        self.ui_endpoint = ui_endpoint or "administration"
        self.url = url or self.dashboard_view.url
        self.url = url or "/administration"
        self.base_template = base_template or "invenio_administration/base.html"

        if self.dashboard_view is not None:

            self._add_dashboard_view(
                dashboard_view=self.dashboard_view, endpoint=ui_endpoint, url=url
            )
        # import ipdb;ipdb.set_trace()
        # if app is not None:
        #     self._init_extension()

    def add_view(self, view, *args, **kwargs):
        """
        Add a view to the collection.
        :param view:
            View to add.
        """
        # Add to views
        self._views.append(view)

        # If app was provided in constructor, register view with Flask app
        if self.app is not None:
            self.app.register_blueprint(view.create_blueprint(self))

        # self._add_view_to_menu(view)

    def add_views(self, *args):
        """Add multiple views."""
        for view in args:
            self.add_view(view)

    def _add_dashboard_view(self, dashboard_view=None, endpoint=None, url=None):
        """
          Add the admin index view.
        :param index_view:
             Home page view to use. Defaults to `AdminIndexView`.
         :param url:
             Base URL
        :param endpoint:
             Base endpoint name for index view. If you use multiple instances of the `Admin` class with
             a single Flask application, you have to set a unique endpoint name for each instance.
        """
        from invenio_administration.dashboard import AdminDashboardView

        self.dashboard_view = dashboard_view or AdminDashboardView(
            endpoint=endpoint, url=url
        )
        self.endpoint = endpoint or self.dashboard_view.endpoint
        self.url = url or self.dashboard_view.url

        # Add predefined index view
        # assume index view is always the first element of views.
        if len(self._views) > 0:
            self._views[0] = self.dashboard_view
            ## TODO menus
            # self._menu[0] = MenuView(self.dashboard_view.name, self.index_view)
        else:
            self.add_view(self.dashboard_view)
