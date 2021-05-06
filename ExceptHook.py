import sys
import traceback
import threading


class MyExceptionHook:

    ###################################################################################
    def __init__(self):
        self.handles = []
        self.addHandle(self.webHandle)

    ###################################################################################
    def addHandle(self, handle):
        self.handles = [handle] + self.handles

    ###################################################################################
    def excepthook(self, exc_type, exc_value, exc_traceback):
        """ handle all exceptions """

        # KeyboardInterrupt is a special case.
        # We don't raise the error dialog when it occurs.
        if issubclass(exc_type, KeyboardInterrupt):
            from PyQtImports import QtWidgets
            if QtWidgets.qApp:
                QtWidgets.qApp.quit()
            return

        """
        import os.path
        filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
        filename = os.path.basename(filename)
        error = "%s: %s" % (exc_type.__name__, exc_value)
        QtGui.QMessageBox.critical(None, "Error",
                                   "<html>A critical error has occurred.<br/> "
                                   + "<b>%s</b><br/><br/>" % error
                                   + "It occurred at <b>line %d</b> of file <b>%s</b>.<br/>" % (line, filename)
                                   + "</html>")
        """

        errorText = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        for handle in self.handles:
            threading.Thread(target=self.callHandle, args=[handle, errorText]).start()

    ###################################################################################
    def callHandle(self, handle, error):
        try:
            handle(error)
        except:
            pass

    ###################################################################################
    def webHandle(self, error):

        errorMap = {"error": error, "application": "DMS+ Desktop"}

        # print("Closed due to an error. This is the full error report:")
        # print()
        # print(exceptionFullText)

        projectKey = "None"
        try:
            from Globals import ini
            projectKey = ini.getProjectKey()
        except:
            pass
        errorMap["project"] = projectKey

        import json
        errorJson = json.dumps(errorMap)

        try:
            import requests
            # headers = {'content-type': 'application/json'}
            # data = {} #get parameters
            params = {"error": errorJson}  # post parameters
            httpResponse = requests.post("http://116.203.233.44/submiterror", params=params, timeout=(2, 8))  # , data=data, headers=headers
            print(httpResponse.text)
        except:
            # print(traceback.format_exc())
            pass


def installThreadExcepthook():
    """
    Workaround for sys.excepthook thread bug
    From
    http://spyced.blogspot.com/2007/06/workaround-for-sysexcepthook-bug.html

    (https://sourceforge.net/tracker/?func=detail&atid=105470&aid=1230540&group_id=5470).
    Call once from __main__ before creating any threads.
    If using psyco, call psyco.cannotcompile(threading.Thread.run)
    since this replaces a new-style class method.
    """
    init_old = threading.Thread.__init__

    def init(self, *args, **kwargs):
        init_old(self, *args, **kwargs)
        run_old = self.run

        def run_with_except_hook(*args, **kw):
            try:
                run_old(*args, **kw)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                sys.excepthook(*sys.exc_info())

        self.run = run_with_except_hook

    threading.Thread.__init__ = init


###########################################################################################
###########################################################################################
###########################################################################################
myExceptionHook = MyExceptionHook()
sys.excepthook = myExceptionHook.excepthook
installThreadExcepthook()
