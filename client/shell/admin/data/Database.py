import json
import traceback

from pyDes import *
""" یک پیاده سازی پایتون خالص از الگوریتم های رمزنگاری DES و TRIPLE DES."""
from Globals import logger


######################################################################################################
######################################################################################################
class DataEncoder(json.JSONEncoder):

    def default(self, list):
        l = []
        l.extend(list)
        return l


######################################################################################################
######################################################################################################
class DataDecoder(json.JSONDecoder):

    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.loadList)

    def loadList(self, l):
        return l


######################################################################################################
######################################################################################################
class Database:

    ###############################################################################################
    def __init__(self):
        self.encryptor = des("DESCRYPT", CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        self.decoder = DataDecoder()
        self.load()

    ###############################################################################################
    def getFileName(self):
        return "cache/profiles.bin"

    ###############################################################################################
    def load(self):
        self.list = []

        try:
            with open(self.getFileName()) as f:
                self.list = self.decoder.decode(f.readlines()[0])
                logger.debug("Database.load: " + str(self.list))
        except Exception as e:
            logger.exception(traceback.format_exc())
            self.list = []

    ###############################################################################################
    def getProfiles(self):
        return self.list

    ###############################################################################################
    def save(self):
        encodedList = json.dumps(self.list, cls=DataEncoder)

        text_file = open(self.getFileName(), "w")
        text_file.write(encodedList)
        text_file.close()

        logger.debug("Database.save: " + str(self.list))

    ###############################################################################################
    def get(self, profileName):

        for p in self.list:
            if profileName == p.get("name", None):
                return p

        return None

    ###############################################################################################
    def add(self, profile, counter=2):
        name = profile.get("name", None)
        if name is None:
            return None

        if self.get(name) is not None:
            profile[name] = name + "(" + str(counter) + ")"
            return self.add(profile, counter + 1)

        self.list.append(profile)
        self.save()

        return profile["name"]

    ###############################################################################################
    def update(self, profile):
        name = profile.get("name", None)
        if name is None:
            return None

        for p in self.list:
            if name == p.get("name", None):
                p.clear()
                p.update(profile)
                self.save()
                return p["name"]

        return self.add(profile)

    ###############################################################################################
    def delete(self, profileName):
        if profileName is None:
            return None

        for i in range(0, len(self.list)):
            if profileName == self.list[i].get("name", None):
                temp = self.list[: i] + self.list[i + 1:]
                self.list = temp
                self.save()
                return True

        return False


###############################################################################################
###############################################################################################
###############################################################################################
database = Database()
