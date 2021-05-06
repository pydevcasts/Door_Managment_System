from client.kernel.analyze.AnalyzerDummy import AnalyzerDummy
from client.kernel.core.CRC import crc


# AnalyzerFactory
class AnalyzerFactory:

    ##########################################################
    def __init__(self):
        self.aDummy = AnalyzerDummy()
        self.analyzerMap = {}

    ##########################################################
    def register(self, analyzer):
        self.analyzerMap[analyzer.getParamNo()] = analyzer

    ##########################################################
    def analyze(self, dataList):
        """و طی ایتحلیل میفهمه که چه جوابی بهش بده این متد داره تحلیل میکنه که کنترل باکس چه حرفی بهش زده"""
        if dataList is None:
            return

        if dataList[0] != 0x80:
            """    همون128 ده ده هستش 
           که میگه ریترن کن هیچی یعنی پیغام اشتباه بدست ما رسیده

            """
            return

        if len(dataList) != dataList[1]:
            """ و اگر طول ارایه مخالف دیتا لیست 1 بود """
            return

        if not crc.checkCRC(dataList):
            """ منطق crc 
            اینه که 2 تا از بایت ها که بین کنترل باکس و 
            
            و رزبری هستش چک میشن بین رزبری و کنترل باکس
            فرضا میگیم 15 بایت از رزبری به کنترل باکس بره 
            15 میشه طول ارایه و
            و 128 میشه یک بیت 
            و خود 15 میشه بیت دوم 
            و 13 تا دیگه میمونه که 2 تا از این بایتا میاد چک میشن که مقدار فرضا جمعشون برابر هم 
            باشه اینجوری بین کنترل باکس و رزبری 
            انالیز میشه
            """
            return

        wr = dataList[5]
        if not wr in {ord('?'), ord('*')}:  # 63 = '?' , 42 = '*'
            """ تا به حال استفاده نشده فقط منطش این بوده نوشته شده"""
            return

        if dataList[6] != ord('p'):  # 112 = 'p'
            """ تا به حال استفاده نشده فقط منطش این بوده نوشته شده"""
            return

        # und das Telegramm war nicht von mir selbst
        # and the message was not from myself
        # from client.kernel.core.SystemData import SystemData
        # if (dataList[7] == SystemData.steuerung) :
        #    return
        """ اون چیزی که مشخص میکنه که پیغامها به چه جهتی ارسال شده اند همین اینجاست 
        که منطق بین دی ام اسمون و کنترل باکس و پیامهای که میکه بیا استاتوست و چک کن
        مدلتو چک کن و.."""
        paramNo = dataList[10] * 256 + dataList[11]
        """ یعنی انگار یه عدد 2 بایتی داشتیم که 
        دیتا لیست 10 قسمت 
        lse  بوده
        و دیتا لیست 11 قسمت 
          بوده lse
          و این دوتا رو کنار هم گذاشتیم و 1 عدد 16 بیتی ساختیم
        """

        value = 0
        if wr == ord('?'):  # 63 = '?'
            value = 0
        elif dataList[8] == 0x50:
            value = dataList[12] * 256 + dataList[13]
        elif dataList[8] == 0x51:
            value = dataList[12] * 256 ** 3 + dataList[13] * 256 ** 2 + \
                    dataList[14] * 256 + dataList[15]

        return self.analyzerMap.get(paramNo, self.aDummy).analyze(dataList)
        """  میخاد واس من یه ابجکت انالایز بسازه که دیتای من و انالایز منه 
        یه هشت ستی  بیا یه هشت مپی با توجه به این پارامتر نامبر درست بکن
        و انالایز مناسبشو پیدا بکن و بهش بده که انالیز کنه
        اینجاش میهمه که میفمیم فرضا برای انالیز 1050 هستش و میدیم بهش و 
        میگه من از اینجا به بعد دیگه باهات کاری ندارم 
        """
    ########################################################################
    def get(self, paramNo):
        return self.analyzerMap.get(paramNo, self.aDummy)

    ########################################################################
    def _items(self):
        try:
            return self.analyzerMap.iteritems()
        except:
            return self.analyzerMap.items()

    ########################################################################
    def invalidate(self):
        for _, analyzer in self._items():
            analyzer.setValid(False)

    ########################################################################
    def isValid(self):
        for _, analyzer in self._items():
            if not analyzer.isValid():
                return False
        return True

    ########################################################################
    def getInvalidMap(self):
        result = set()
        for _, analyzer in self._items():
            if not analyzer.checkForValidity():
                result.add(analyzer.getParamNo())
                break
        return result


##########################################################
##########################################################
##########################################################
analyzerFactory = AnalyzerFactory()
