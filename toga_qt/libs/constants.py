from .qt import Qt


def get_scrollbar_policy(show):
    if show:
        return Qt.ScrollBarAsNeeded
    return Qt.ScrollBarAlwaysOff
