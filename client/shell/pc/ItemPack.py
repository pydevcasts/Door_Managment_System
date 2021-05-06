from Lang import DOOR_STATUS, PASSWORDS, SETTINGS, ADVANCED_SETTINGS, CONFIGURATIONS
from client.shell.pc.ui.AdvancedSettingsPanel import advancedSettingsPanel
from client.shell.pc.ui.CListWidgetItem import CListWidgetItem
from client.shell.pc.ui.ConfigPanel import configPanel
from client.shell.pc.ui.DoorStatusPanel import doorStatusPanel
from client.shell.pc.ui.PasswordsPanel import passwordsPanel
from client.shell.pc.ui.SettingsPanel import settingsPanel
from common.kernel.SysArgument import sysArgument


class ItemPack:

    def __init__(self, titleKey, imageFilePrefix, ItemPanel):
        self.titleKey = titleKey
        self.listWidgetItem = CListWidgetItem(titleKey, imageFilePrefix)
        self.ItemPanel = ItemPanel

    def select(self):
        self.listWidgetItem.select()

    def unselect(self):
        self.listWidgetItem.deselect()


# Items
doorStatusPack = ItemPack(DOOR_STATUS, "images/door", doorStatusPanel)
passwordsPack = ItemPack(PASSWORDS, "images/passwords", passwordsPanel)
settingsPack = ItemPack(SETTINGS, "images/settings", settingsPanel)
advancedSettingsPack = ItemPack(ADVANCED_SETTINGS, "images/advancedsettings", advancedSettingsPanel)
configPack = ItemPack(CONFIGURATIONS, "images/configurations", configPanel)

items = [doorStatusPack, passwordsPack, settingsPack, advancedSettingsPack]

if sysArgument.exists("ConfigPanel"):
    items.append(configPack)
