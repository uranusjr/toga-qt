from ..libs import qt


class Dialog(object):

    @staticmethod
    def info(title, message):
        qt.QMessageBox.information(None, title, message)

    @staticmethod
    def question(title, message):
        result = qt.QMessageBox.question(
            None, title, message,
            qt.QMessageBox.Yes | qt.QMessageBox.No,
            qt.QMessageBox.Yes,
        )
        return result == qt.QMessageBox.Yes

    @staticmethod
    def confirm(title, message):
        result = qt.QMessageBox.warning(
            None, title, message,
            qt.QMessageBox.Ok | qt.QMessageBox.Cancel,
            qt.QMessageBox.Cancel,
        )
        return result == qt.QMessageBox.Ok

    @staticmethod
    def error(title, message):
        qt.QMessageBox.critical(None, title, message)

    @staticmethod
    def stack_trace(title, message, content, retry=False):
        impl = qt.QMessageBox()
        impl.setIcon(qt.QMessageBox.Critical)
        impl.setText(title)
        impl.setInformativeText(message)
        impl.setDetailedText(content)
        if retry:
            impl.addButton(qt.QMessageBox.Retry)
            impl.addButton(qt.QMessageBox.Cancel)
            result = impl.exec_()
            return result == qt.QMessageBox.Retry
        impl.exec_()
