import threading
import time

from Globals import interface, ini, logger
from common.kernel.event.EventLogger import eventLogger
from common.kernel.request.DoorRequest import DoorRequest
from common.kernel.request.RecentErrorsRequest import RecentErrorsRequest
from common.kernel.request.Request import Request
from common.kernel.request.WebCommunicationRequest import WebCommunicationRequest
from common.kernel.request.WebCommunicationResponse import WebCommunicationResponse

class WebServerCommunicator(threading.Thread):
    """get and set wer server url comunicate door request update door error
    """
    """ کثا بلوتوث سوکت بازی نمیکنیم حالا که ای پی در و میدونم با یه اچ تی تی پی
        ریکویست میفرستم و ریسپانس میگیرم وب سرور کوچیکی رو درم رانه و یعنی روی درم یه 
        ما یه ای پی داریم که هارد کد ولیده 
        و ما باید به اون کانکت بشیم
        و گوشی موبایلمونم به همون کانکت میشه
       و بعد گوشیه میبینه که درها بهش کانکت شدن دوباره ریکویست میفرسته  
       و بالا خره از مسیر وب میرسه به در و در دوباره هندلش میکنه و بعد ریسپانس میده
       
    """
    ######################################################################
    def __init__(self):
        threading.Thread.__init__(self, name="WebServerCommunicator")
        self.setDaemon(True)
        """threading library
        """

        self.doorRequest = DoorRequest()
        self.errorRequest = RecentErrorsRequest()

        self.dirty = True  # to be sure of a new log on application start

        self.liveTime = 0

        self.lock = threading.Lock()

        self.initialCheck()

        interface.get().addDoorErrorListener(self)

        from Exit import exit
        exit.register(self.cleanUp)

    ######################################################################
    def initialCheck(self):
        self.enabled = True
        try:
            import requests
        except:
            self.enabled = False
            logger.error("Web communication features are not installed. Contact your vendor.")
            logger.develop("'requests' library is not installed. Execute: 'sudo pip install requests'")

    ######################################################################
    def cleanUp(self):
        self.enabled = False

    ######################################################################
    def run(self):

        if not self.enabled:
            return

        # warm-up waiting
        time.sleep(3)

        # Constants
        LOOP_PERIOD = 2
        MAX_WAIT_TIME = 10
        LIVE_WAIT_TIME = 4

        previousTime = 0
        lastUpdateTime = 0

        while self.enabled:

            time.sleep(LOOP_PERIOD)

            url = self.getWebServerUrl()
            if url is None or len(url) == 0:
                continue

            now = time.time()

            # Maybe the system clock has been change manually, so we'll consider a new start-up
            if abs((now - previousTime) - LOOP_PERIOD) > (LOOP_PERIOD / 2):
                lastUpdateTime = 0

            self.lock.acquire()

            waitTime = MAX_WAIT_TIME if not self.isLive() else LIVE_WAIT_TIME
            if self.dirty or ((now - lastUpdateTime) > waitTime):
                if self.communicate():
                    lastUpdateTime = now
                    self.dirty = False

            self.lock.release()

            previousTime = time.time()

    #####################################################################
    def setDirty(self, d=True):
        self.lock.acquire()
        self.dirty = d
        self.lock.release()

    #####################################################################
    def getProject(self):
        from client.kernel.core.DoorInfo import doorInfo
        return doorInfo.getProject()

    #####################################################################
    def communicate(self):
        doorResponse = interface.get().handle(self.doorRequest, security=False)
        errorResponse = interface.get().handle(self.errorRequest, security=False)
        doorEventLogs = eventLogger.removeAll()
        request = WebCommunicationRequest(self.getProject(), self.dirty, doorResponse, errorResponse, doorEventLogs)

        response = self.send(request)
        if response is None:
            eventLogger.push(doorEventLogs)
            return False

        self.handle(response)
        return response.isSuccessful()

    #####################################################################
    def send(self, request):
        import requests

        response = None
        try:
            url = self.getWebServerUrl()
            if url is None or len(url) == 0:
                return None

            while url[-1:] == "/":
                url = url[:-1]

            # headers = {'content-type': 'application/json'}
            # data = {} #get parameters
            params = {"request": request.toJson()}  # post parameters
            response = requests.post(url + "/request/", params=params, timeout=(2, 8))  # , data=data, headers=headers
        except:
            # http error, server might not be available.
            # import traceback
            # logger.exception(traceback.format_exc())
            return None

        try:
            # print(time.time(), self.isLive(), response.__dict__['_content'])
            # f = open('../error.html', 'wb')
            # f.write(response.__dict__['_content'])
            # f.close()
            return WebCommunicationResponse(response.json())
        except:
            # response format error
            return None

    #####################################################################
    def handle(self, response):
        if response.live:
            self.liveTime = time.time()

        if response.requests is not None and len(response.requests) > 0:
            threading.Thread(target=self.handleRequests, args=[response.requests]).start()

    #####################################################################
    def handleRequests(self, requests):
        for requestStr in requests:
            request = Request(Request.UNDEFINED, requestStr)
            interface.get().handle(request, security=False)

    ############################################################################
    def statusChanged(self, value):
        self.setDirty()

    ############################################################################
    def settingChanged(self, parameterCode, value):
        self.setDirty()

    ############################################################################
    def mechanicalChanged(self, mechanical):
        self.setDirty()

    ####################################################################################
    def updateDoorError(self, errorCode, errorTime):
        self.setDirty()

    ############################################################################
    def setWebServerUrl(self, url):
        ini.setWebServerUrl(url)
        ini.save()

    ############################################################################
    def getWebServerUrl(self):
        dummyUrl = "dummyUrl"
        url = ini.getWebServerUrl(dummyUrl)

        if url == dummyUrl:
            url = "http://116.203.233.44"
            ini.setWebServerUrl(url)
            ini.save()

        return url

    ############################################################################
    def isLive(self):
        return time.time() - self.liveTime <= 15


######################################################################
######################################################################
######################################################################
webServerCommunicator = WebServerCommunicator()
