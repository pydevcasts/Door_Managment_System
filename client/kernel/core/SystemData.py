from client.kernel.core.Constants import Constants


class SystemData:
    
    # System Data ROM

    Steuerung = Constants.DEF_PRG  # Programmer

    User_Passwort = [
        Constants.DEF_UPW_0,  # Pos. 0 = Anzahl der Stellen
        Constants.DEF_UPW_1,  # Pos. 1 bis 6 = Passwort
        Constants.DEF_UPW_2,
        Constants.DEF_UPW_3,
        Constants.DEF_UPW_4,
        Constants.DEF_UPW_5,
        Constants.DEF_UPW_6
    ]

    Installer_Passwort = [
        Constants.DEF_IPW_0,  # Pos. 0 = Anzahl der Stellen
        Constants.DEF_IPW_1,  # Pos. 1 bis 6 = Passwort
        Constants.DEF_IPW_2,
        Constants.DEF_IPW_3,
        Constants.DEF_IPW_4,
        Constants.DEF_IPW_5,
        Constants.DEF_IPW_6
    ]

    Advanced_Passwort = [
        Constants.DEF_APW_0,  # Pos. 0 = Anzahl der Stellen
        Constants.DEF_APW_1,  # Pos. 1 bis 6 = Passwort
        Constants.DEF_APW_2,
        Constants.DEF_APW_3,
        Constants.DEF_APW_4,
        Constants.DEF_APW_5,
        Constants.DEF_APW_6
    ]

    User_Pass_wird_benutzt = Constants.DEF_User_Pass_Default

    Helligkeit = Constants.DEF_Helligkeit_Default

    def loadFromROM(self):
        self.uc_Steuerung = SystemData.Steuerung  #کنترل
        self.uc_User_Passwort = SystemData.User_Passwort[:]
        self.uc_Installer_Passwort = SystemData.Installer_Passwort[:]
        self.uc_Advanced_Passwort = SystemData.Advanced_Passwort[:]
        self.uc_User_Pass_wird_benutzt = SystemData.User_Pass_wird_benutzt
        self.uc_Helligkeit = SystemData.Helligkeit

    def __init__(self):
        self.currentState = Constants.RUHEN
        self.loadFromROM()


systemData = SystemData()
