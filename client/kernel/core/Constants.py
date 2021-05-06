#!/usr/bin/python
# -*- coding: utf-8 -*-


class Constants:

    # ==============================================================================
    # Definitionen für die Funktion der Steuerung

    DEF_STAND_ALONE = 0
    DEF_FRW_MASTER = 1
    DEF_FRW_SLAVE = 2
    DEF_PRG = 3
    DEF_NOTHING = 99

    SW_OFF = 0  # AUS-Schalten !!!
    SW_ON = 10  # EIN-Schalten
    BLINK_SLOW = 20  # langsames blinken
    BLINK_NORMAL = 30  # normales blinken
    BLINK_QUICK = 40  # schnelles blinken

    # ==============================================================================

    # Definitionen für User Passwort  Default- Stellung
    DEF_UPW_0 = 4  # Anzahl der Stellen: 4
    DEF_UPW_1 = '0'  # Passwort
    DEF_UPW_2 = '0'  # Passwort
    DEF_UPW_3 = '0'  # Passwort
    DEF_UPW_4 = '0'  # Passwort
    DEF_UPW_5 = '0'  # Passwort
    DEF_UPW_6 = '0'  # Passwort

    DEF_User_Pass_Default = SW_OFF  # USer PAsswort- Benutzung ist AUS

    # Definitionen für Installer Passwort  Default- Stellung
    DEF_IPW_0 = 4  # Anzahl der Stellen: 4
    DEF_IPW_1 = '0'  # Passwort
    DEF_IPW_2 = '0'  # Passwort
    DEF_IPW_3 = '4'  # Passwort
    DEF_IPW_4 = '9'  # Passwort
    DEF_IPW_5 = '0'  # Passwort
    DEF_IPW_6 = '0'  # Passwort

    # Definitionen für Advanced Passwort  Default- Stellung

    DEF_APW_0 = 4  # Anzahl der Stellen: 4
    DEF_APW_1 = '3'  # Passwort
    DEF_APW_2 = '3'  # Passwort
    DEF_APW_3 = '4'  # Passwort
    DEF_APW_4 = '1'  # Passwort
    DEF_APW_5 = '0'  # Passwort
    DEF_APW_6 = '0'  # Passwort

    # Definitionen für Hintertür: Global Passwort  Default- Stellung

    DEF_HPW_0 = 4  # Anzahl der Stellen: 4
    DEF_HPW_1 = '3'  # Passwort
    DEF_HPW_2 = '0'  # Passwort
    DEF_HPW_3 = '2'  # Passwort
    DEF_HPW_4 = '2'  # Passwort
    DEF_HPW_5 = '0'  # Passwort
    DEF_HPW_6 = '0'  # Passwort

    # ==============================================================================
    # Definitionen für HElligkeit der LEDs Default- Stellung

    DEF_Helligkeit_Default = 2  # = x 10%,   0,10,20,30,...90,100%

    #  *****   Software Stand Festlegung HIER !!!!!  *****
    #  *****   SW=  Version: V SW_Stand_1 . SW_Stand_2  SW_Stand_3  *****
    SW_Stand_1 = 1
    SW_Stand_2 = 0
    SW_Stand_3 = 5

    SW_Type_0 = ord('3')  # Steuerungs- Nr // Hersteller-Nr: 0=Deutschtec,1=Holux,2=EAD,3=Bocamo,4=Hörmann
    SW_Type_1 = ord('0')  # Steuerungs- Nr
    SW_Type_2 = ord('0')  # Steuerungs- Nr
    SW_Type_3 = ord('0')  # Steuerungs- Nr
    SW_Type_4 = ord(' ')  # Steuerungs- Nr, Zusatz, z.B. F = Fast

    # Machine States - Automatenzustände

    POWERUP = 0  # Der Zustand nach dem Einschalten
    RUHEN = 10  # Warten   # Rest
    ZEIGE_SW_STAND_E_PRG = 20  # Warten
    EINGABE_PASSWORT = 30  #
    ENTER_PASSWORD = 31
    EINGABE_PASSWORT_A = 32
    ENTER_NEW_PASSWORD = 33
    WRONG_PASSWORT = 34

    TUER_STATUS = 40  #
    MENUE_AUSWAHL = 50

    MENUE_PASSWORTE = 60
    MENUE_USER_PASSWORTE = 61
    MENUE_INST_PASSWORTE = 62
    MENUE_ADV_PASSWORTE = 63

    MENUE_SETTING = 70
    MENUE_OPEN_SPEED = 71
    MENUE_CLOSE_SPEED = 72
    MENUE_OPEN_TIME = 73
    MENUE_PARTIAL_WIDTH = 74
    MENUE_MAX_OPEN_POINT = 75
    MENUE_REMOTE_OPEN_TIME = 76
    MENUE_INITIAL_SETUP = 77

    MENUE_NEUES_DING = 78

    MENUE_SENSOR_SETTING = 80
    MENUE_RADAR_SETTING = 81

    MENUE_LED_BACKLIGHT = 82
    MENUE_SHOW_ERRORS = 83
    MENUE_SHOW_SW_VERSIONS = 84
    MENUE_SHOW_ERRORS_IN_MAIN_MENUE = 85
    MENUE_SHOW_SERIAL = 86

    MENUE_ADV_SETTING = 100
    MENUE_TIME_TO_PUSH_INTO_STOPPER = 101
    MENUE_MOTOR_DIR = 102
    MENUE_REVERS_SENSITIVITY = 103
    MENU_TIME_AUTORESET_ERRORS = 104
    MENU_RUN_ON_BAT = 105
    MENUE_ADV_SET_BRAND_NAME = 106
    MENUE_RAMPS = 107
    MENUE_BATTERY_VOLTAGE_LIMIT = 108
    MENUE_MOTOR_VALUES = 109

    MENUE_RAMPS_OPEN_DELTA1 = 110
    MENUE_RAMPS_OPEN_DELTA2 = 111
    MENUE_RAMPS_OPEN_V2 = 112
    MENUE_RAMPS_OPEN_P2 = 113
    MENUE_RAMPS_OPEN_P3 = 114
    MENUE_RAMPS_CLOSE_DELTA1 = 115
    MENUE_RAMPS_CLOSE_DELTA2 = 116
    MENUE_RAMPS_CLOSE_V2 = 117
    MENUE_RAMPS_CLOSE_P2 = 118
    MENUE_RAMPS_CLOSE_P3 = 119

    MENUE_FACTORY_RESET = 120
    MENUE_SAVE_AS_DEFAULT = 121
    MENUE_LOAD_FROM_DEFAULT = 122
    MENUE_MANUFACTURER_SETTINGS = 123
    MENUE_CHANGE_SERIAL = 124
    MENUE_ACCEL_MOTION_PROFILES = 125
    MENUE_CLOSE_RAMPS = 126
    MENUE_OPEN_RAMPS = 127
    MENUE_DECCEL_MOTION_PROFILES = 128
    MENUE_LOCKTYPE = 129

    MENUE_PULLY_SIZE = 130
    MENUE_GEARBOX_REDUCTION = 131
    MENUE_ENCODER_PULSES = 132
    MENUE_MOTOR_VOLTAGE = 133
    MENUE_GLOBAL_MIN_SPEED = 134

    MENUE_BEHAVIOUR = 150
    MENUE_POSCONTROLCLOSEONEWAY = 151
    MENUE_POSCONTROLOPENPARTIAL = 152
    MENUE_POSCONTROLOPENFULLOPEN = 153
    MENUE_AFTERAUTOREV_OPENDIR = 154
    MENUE_AFTERAUTOREV_CLOSEDIR = 155
    MENUE_ONEWAYTRAFFIC = 156
    MENUE_HIGHTRAFFICVAL = 157
    MENUE_HIGHTRAFFICBEHAVIOUR = 158
    MENUE_TWOWAYTRAFFIC = 159
    MENUE_LOCKCHECK = 160
    MENUE_MINPWM = 161
    MENUE_OPENBYFORCE = 162

    MENUE_INPUT_FUNCTIONS = 170
    MENUE_INPUT_ESC = 171
    MENUE_INPUT_STOP = 172
    MENUE_INPUT_REMOTE = 173

    FEHLERANZEIGEN = 200  # Fehleranzeigen
    WERKS_RESET = 210  # Steuerung zurücksetzten auf Werkskonfiguration, Tordaten löschen !
    STATISTIK_LESEN = 220  # Auslesen der im EEPROM gespeicherten Statistik-Daten mit Display
    PRUEFEN = 230  # Prüfen mittels Kommando- Interpreter im Prüffeld

    # typedefs for state mashine

    state_close = 0
    state_open = 1
    state_stopAndWait = 2
    state_driveToOpen = 3
    state_driveToClose = 4
    state_reverseOpen = 5
    state_reverseClose = 6
    state_locked = 7
    state_doLock = 8
    state_doUnlock = 9
    state_startup = 10
    state_referenceDrive = 11
    state_learning = 12
    state_securityStop = 13
    state_systemReset = 14
