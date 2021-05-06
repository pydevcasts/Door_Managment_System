from common.kernel.lsc.Hardware import *


class Validator:

    def validate(self, lsc):

        systemSerial = getSystemSerial()
        systemLsc = self.generate(systemSerial)
        if systemLsc == lsc:
            return True

        storageSerial = getStorageSerial()
        storageLsc = self.generate(storageSerial)
        # print(storageLsc)
        if storageLsc == lsc:
            return True

        serial1 = systemSerial + '-' + storageSerial
        lsc1 = self.generate(serial1)
        if lsc1 == lsc:
            return True

        serial2 = storageSerial + '-' + systemSerial
        lsc2 = self.generate(serial2)
        if lsc2 == lsc:
            return True

        return False

    def generate(self, identifier):
        z = 'q'
        x = 'a'
        c = 'z'
        v = 'w'
        b = 's'
        n = 'x'
        m = 'e'
        a = 'd'
        s = 'c'
        d = 'r'
        f = 'f'
        g = 'v'
        h = 't'
        j = 'g'
        k = 'b'
        l = 'y'
        q = 'h'
        w = 'n'
        e = 'u'
        r = 'j'
        t = 'm'
        y = 'i'
        u = 'k'
        i = 'o'
        o = 'l'
        p = 'p'

        a += b
        c = a + c
        d = c + d + d
        e = f + d + g + h
        i = j + k + e + l
        m = i + n + o + p
        q = r + s + r + m
        t = t + q + u + v
        w = t + x + y + z

        identifier = str(identifier) + w
        identifier = self.encrypt(identifier)

        return self.tokenize(identifier)

    ###############################################################################
    def encrypt(self, stringValue):
        if stringValue is None:
            return None

        stringValue = str(stringValue)

        import hashlib
        digest = hashlib.md5(stringValue.encode('utf-8')).hexdigest()
        return str(digest)

    ###############################################################################
    def tokenize(self, stringValue):
        if stringValue is None:
            return None

        stringValue = str(stringValue).upper()

        result = ''

        while len(result) < 40 and len(stringValue) > 3:
            result = result + '-' + stringValue[:4]
            stringValue = stringValue[4:]

        return result[1:]


######################################################
######################################################
######################################################

validator = Validator()
