from toga import constants
from .qt import Qt


def get_alignment(toga_constant):
    lookup = {
        constants.LEFT_ALIGNED: Qt.AlignLeft,
        constants.RIGHT_ALIGNED: Qt.AlignRight,
        constants.CENTER_ALIGNED: Qt.AlignHCenter,
        constants.JUSTIFIED_ALIGNED: Qt.AlignJustify,
        constants.NATURAL_ALIGNED: 0,
    }
    return lookup[toga_constant]


def get_scrollbar_policy(show):
    if show:
        return Qt.ScrollBarAsNeeded
    return Qt.ScrollBarAlwaysOff
