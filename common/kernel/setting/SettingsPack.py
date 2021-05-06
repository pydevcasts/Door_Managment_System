class SettingsPack:

    ################################################################################
    def __init__(self, titleKey):
        self.titleKey = titleKey
        self.settingList = []

    ################################################################################
    def __len__(self):
        return len(self.settingList)

    ################################################################################
    def getTitle(self):
        from Lang import lget
        return lget(self.titleKey)

    ################################################################################
    def add(self, setting):
        if setting is None:
            return None
        self.settingList.append(setting)
        return setting

    ################################################################################
    def find(self, code):
        for setting in self.settingList:
            found = setting.find(code)
            if found is not None:
                return found
        return None

    ################################################################################
    def getPureSettingsList(self):
        result = []
        for setting in self.settingList:
            result.extend(setting.getPureSettingsList())
        return result
