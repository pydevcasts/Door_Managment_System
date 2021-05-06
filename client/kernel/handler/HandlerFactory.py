from client.kernel.handler.CommandHandler import commandHandler
from client.kernel.handler.DoorHandler import doorHandler
from client.kernel.handler.EnableMechanicalHandler import enableMechanicalHandler
from client.kernel.handler.InfoHandler import infoHandler
from client.kernel.handler.RecentErrorsHandler import recentErrorsHandler
from client.kernel.handler.SetNameHandler import setNameHandler
from client.kernel.handler.SetParamHandler import setParamHandler
from client.kernel.handler.SetParamsHandler import setParamsHandler
from client.kernel.handler.SetPasswordHandler import setPasswordHandler
from client.kernel.handler.SetProjectHandler import setProjectHandler
from client.kernel.handler.SetStatusHandler import setStatusHandler
from client.kernel.handler.SskHandler import sskHandler
from client.kernel.handler.WizardHandler import wizardHandler
from common.kernel.handler.HandlerFactory import HandlerFactory as CommonHandlerFactory
from common.kernel.request.ErrorResponse import ErrorResponse
from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class HandlerFactory(CommonHandlerFactory):
    """ isSerialConnected"""
    def __init__(self):
        CommonHandlerFactory.__init__(self)

    def validate(self, request, handler):
        disconnectHandling = False
        try:
            disconnectHandling = handler.disconnectHandling()
        except:
            ""

        from client.kernel.serial.SerialCommunicator import serialCommunicator
        if (not disconnectHandling) and not serialCommunicator.isSerialConnected():
            return ErrorResponse(Response.ERROR_DOOR_NOT_AVAILABLE)


####################################################################################
####################################################################################
####################################################################################

handlerFactory = HandlerFactory()
"""ای دی های هارد کد هندلر میجود اومدو رجیستر کردم
حالا من برای هر کدوم از فرامینی که دریافت میشه من میتونم 
برای هندلر خاص اون فرمان ریکویستمو 
رو پاس میدم و میگم هدلش کن
"""
handlerFactory.register(Request.INFO, infoHandler)
handlerFactory.register(Request.DOOR, doorHandler)
handlerFactory.register(Request.SET_STATUS, setStatusHandler)
handlerFactory.register(Request.SET_PARAM, setParamHandler)
handlerFactory.register(Request.SET_PASSWORD, setPasswordHandler)
handlerFactory.register(Request.SET_NAME, setNameHandler)
handlerFactory.register(Request.SET_PROJECT, setProjectHandler)
handlerFactory.register(Request.SSK, sskHandler)
handlerFactory.register(Request.COMMAND, commandHandler)
handlerFactory.register(Request.WIZARD, wizardHandler)
handlerFactory.register(Request.SET_PARAMS, setParamsHandler)
handlerFactory.register(Request.ENABLE_MECHANICAL, enableMechanicalHandler)
handlerFactory.register(Request.RECENT_ERRORS, recentErrorsHandler)
