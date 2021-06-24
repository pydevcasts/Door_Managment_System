# # import module
# import os

# # scan avaliable Wifi networks
# os.system('cmd /c "netsh wlan show networks"')

# # input Wifi name
# name_of_router = input('Enter Name/SSID of the Wifi Network you wish to connect to: ')

# # connect to the given wifi network
# os.system(f'''cmd /c "netsh wlan connect name={name_of_router}"''')

# print("If you're not yet connected, try connecting to a previously connected SSID again!")
# import module
import os

# function to establish a new connection
def createNewConnection(name, SSID, password):
	config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
	<name>"""+name+"""</name>
	<SSIDConfig>
		<SSID>
			<name>"""+SSID+"""</name>
		</SSID>
	</SSIDConfig>
	<connectionType>ESS</connectionType>
	<connectionMode>auto</connectionMode>
	<MSM>
		<security>
			<authEncryption>
				<authentication>WPA2PSK</authentication>
				<encryption>AES</encryption>
				<useOneX>false</useOneX>
			</authEncryption>
			<sharedKey>
				<keyType>passPhrase</keyType>
				<protected>false</protected>
				<keyMaterial>"""+password+"""</keyMaterial>
			</sharedKey>
		</security>
	</MSM>
</WLANProfile>"""
	command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
	with open(name+".xml", 'w') as file:
		file.write(config)
	os.system(command)

# function to connect to a network	
def connect(name, SSID):
	command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
	os.system(command)

# function to display avavilabe Wifi networks	
def displayAvailableNetworks():
	command = "netsh wlan show networks interface=Wi-Fi"
	os.system(command)


# display available netwroks
displayAvailableNetworks()

# input wifi name and password
name = input("Name of Wi-Fi: ")
password = input("Password: ")

# establish new connection
createNewConnection(name, name, password)

# connect to the wifi network
connect(name, name)
print("If you aren't connected to this network, try connecting with the correct password!")
