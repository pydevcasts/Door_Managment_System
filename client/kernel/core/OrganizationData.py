from client.kernel.core.Constants import Constants


class OrganizationData:
    # Organization Data ROM
    Steuerungstype = [
        Constants.SW_Type_0,
        Constants.SW_Type_1,
        Constants.SW_Type_2,
        Constants.SW_Type_3,
        Constants.SW_Type_4
    ]  # Hersteller- Nr etc

    SW_Version = [  # SW - Version
        ord('V'),
        ord('0') + Constants.SW_Stand_1,
        ord('.'),
        ord('0') + Constants.SW_Stand_2,
        ord('0') + Constants.SW_Stand_3,
        ord('H'),
        ord('T')
    ]  # Beispiel V1.00a6

    Seriennummer = [0x09, 0x99, 0x99, 0x99, 0x99, 0x99]  # Beispiel 27443829103 BCD Codiert

    Dummy_Org = 0xA5  # Nur Dummy Byte

    def loadFromROM(self):
        self.uc_Steuerungstype = OrganizationData.Steuerungstype[:]
        self.uc_SW_Version = OrganizationData.SW_Version[:]
        self.uc_Seriennummer = OrganizationData.Seriennummer[:]
        self.dummy_Org = OrganizationData.Dummy_Org

    def __init__(self):
        self.checksum = 0
        self.loadFromROM()
        # self.uc_Steuerungstype = [0,0,0,0,0] # Hersteller- Nr etc
        # self.uc_SW_Version = [0,0,0,0,0,0,0] # Beispiel V1.00a6
        # self.uc_Seriennummer = [0,0,0,0,0,0]    # Beispiel 27443829103 BCD Codiert
        # self.dummy_Org = 0 # Nur Dummy Byte
        # self.checksum  = 0 # Checksumme


organizationData = OrganizationData()
