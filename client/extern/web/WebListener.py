#!/usr/bin/env python
import threading
from client.extern.web.RequestHandler import RequestHandler


class WebListener(threading.Thread):
    """یعنی حالا گوشی منو شناخت بیاد 
        میتونه یه ریکوست اچ تی تی پی  به ای پی در بده و ما ریسپانس بدیم
    """
    ##################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="WebListener")
        self.setDaemon(True)

        self.webApp = None
        try:
            import web
            urls = ('/deutschtec/request', 'RequestHandler')
            self.webApp = web.application(urls, globals())
        except:
            from Globals import logger
            logger.error("Wi-Fi features are not installed. Contact your vendor.")
            logger.develop("'WebPy' library is not installed. install from https://pypi.python.org/pypi/web.py")

        from Exit import exit
        exit.register(self.cleanUp)

    ##################################################################
    def run(self):
        if self.webApp is not None:
            self.webApp.run()

    ##################################################################
    def cleanUp(self):
        if self.webApp is not None:
            self.webApp.stop()


######################################################################
######################################################################
######################################################################
webListener = WebListener()
