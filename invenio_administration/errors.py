from flask_babelex import gettext as _


class InvalidResource(Exception):
    def __init__(self, resource, view):
        """Initialise error."""
        super().__init__(
            _(
                f"Invalid resource {resource} configured for view {view}."
            )
        )
