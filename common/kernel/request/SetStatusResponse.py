from common.kernel.request.Request import Request
from common.kernel.request.Response import Response


class SetStatusResponse(Response):

    def __init__(self, status):
        Response.__init__(self, Request.SET_STATUS)
        """یه پیغامی از گوشی یا وب یا بلوتوث برای ما ارسال میشه و پاسخ ما همون رسپانسه
        یعنی ممکنه از اندروید پیامی برا ما ارسال بشه و جیسانش دقیقا جیسان همین ابجکتیه که دارم میفرستم
        
        
        """

        self.status = status
