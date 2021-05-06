from os import listdir
from os.path import isfile, join

from Globals import ini


class Language:

    ############################################################################
    def __init__(self):

        self.langMap = None
        self.default = 'en'

        self.listeners = []

        self.current = None
        try:
            self.current = ini.getLanguage()
        except:
            pass

        if self.current is None:
            self.english()

    ############################################################################
    def getDefault(self, key, *params):
        if self.langMap is None:
            self.load()

        try:
            return self.read(self.default, key, *params)
        except:
            pass

        return key

    ############################################################################
    def get(self, key, *params):
        if self.langMap is None:
            self.load()

        try:
            return self.read(self.current, key, *params)
        except:
            pass

        return self.getDefault(key, *params)

    ############################################################################
    def read(self, lang, key, *params):
        result = self.langMap[lang][key].strip()
        paramNo = len(params)
        for i in range(0, paramNo):
            result = result.replace("{" + str(i) + "}", str(params[i]))
        return result

    ############################################################################
    def load(self):

        self.langMap = {}

        path = './lang'
        postfix = ".properties"

        fileNames = [f for f in listdir(path) if isfile(join(path, f)) and f.lower().endswith(postfix)]

        for fileName in fileNames:

            lang = "unknown"
            try:
                lang = fileName[:-(len(postfix))]

                d = {}
                import io
                with io.open(join(path, fileName), encoding='utf-8') as f:
                    for line in f:
                        try:
                            key, value = line.split('=')
                            if len(str(value).strip()) > 0 :
                                d[key.strip()] = str(value)
                        except:
                            pass
                self.langMap[lang] = d

            except:
                print("the language file not loaded: " + lang)

    ############################################################################
    def register(self, listener):
        self.listeners.append(listener)

    ############################################################################
    def notify(self):
        for listener in self.listeners:
            listener.setTranslations()

    ############################################################################
    def english(self):
        self.setCurrent('en')

    ############################################################################
    def spanish(self):
        self.setCurrent('es')

    ############################################################################
    def german(self):
        self.setCurrent('de')

    ############################################################################
    def persian(self):
        self.setCurrent('fa')

    ############################################################################
    def setCurrent(self, lang):
        if lang == self.current:
            return
        self.current = lang
        self.notify()

        try:
            ini.setLanguage(lang)
            ini.save()
        except:
            pass
