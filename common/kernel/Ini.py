import json
import traceback

from pyDes import *



from Globals import logger


######################################################################################################
######################################################################################################
class IniEncoder(json.JSONEncoder):

    ############################################################################
    def default(self, dictionary):
        d = {}
        d.update(dictionary)
        return d


######################################################################################################
######################################################################################################
class IniDecoder(json.JSONDecoder):
    """ برای دی کد کردن کدهای جیسان و ذخیره ان"""
    ############################################################################
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.loadDict)

    ############################################################################
    def loadDict(self, d):
        return d


######################################################################################################
######################################################################################################
class Ini:
    DummyKey = "DATA00"

    ############################################################################
    def __init__(self):
        self.encryptor = des("DESCRYPT", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        self.decoder = IniDecoder()
        self.load()

    ############################################################################
    def getFileName(self):
        raise Exception("Must be implemented in extended Ini classes")

    ############################################################################
    def load(self):
        self.dict = {Ini.DummyKey: Ini.DummyKey}

        try:
            with open(self.getFileName(), "rb") as f:
                fileBytes = f.read()
                decryptedText = self.encryptor.decrypt(fileBytes)
                """ (decrypt)  متد pyDesاز الگوریتم رمز نگاری کتابخانه  """
                self.dict = self.decoder.decode(decryptedText.decode("utf-8"))
                logger.debug("Ini.load: " + str(self.dict))
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.dict = {}
            self.set(Ini.DummyKey, Ini.DummyKey)

    ############################################################################
    def save(self):
        """   رمز نگاری شده بصورت جیسان نمایش میدیم یا دامپ میکنیم"""
        encodedDict = json.dumps(self.dict, cls=IniEncoder)
        encryptedDict = self.encryptor.encrypt(encodedDict)

        import os
        filePath = self.getFileName()
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory):
            os.makedirs(directory)

        text_file = open(filePath, "wb+")
        text_file.write(encryptedDict)
        text_file.close()

        logger.debug("Ini.save: " + str(self.dict))

    ############################################################################
    def set(self, key, value):
        if value is not None:
            value = str(value)
        self.dict[key] = value

    ############################################################################
    def get(self, key, defaultValue=None):

        if key not in self.dict:
            return defaultValue

        try:
            value = self.dict.get(key, None)
            if value is None:
                return None
            return str(value)
        except:
            return None

    ############################################################################
    def getInt(self, key, defaultValue=None):
        try:
            return int(self.get(key, defaultValue))
        except Exception:
            return -1
