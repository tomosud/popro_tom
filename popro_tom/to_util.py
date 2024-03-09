import asyncio
from bleak import BleakClient, BleakScanner
from main import run
import commands

from pywifi import PyWiFi, const, Profile

# Wi-Fi SSIDを読み取るためのキャラクタリスティックUUID
#WIFI_SSID_CHARACTERISTIC_UUID = "b5f90002-aa8d-11e3-9046-0002a5d5c51b"

#参考　https://gopro.github.io/OpenGoPro/ble/protocol/ble_setup.html
camera_info_chars = {"00002a00-0000-1000-8000-00805f9b34fb": {
	"name": "Camera ID"
},  # Camera ID
	commands.Characteristics.BatteryLevel: {
	"name": "Battery Level"
},  # Battery Level
	commands.Characteristics.SerialNumber: {
	"name": "Serial Number"
},  # Serial
	commands.Characteristics.FirmwareVersion: {
	"name": "Firmware Version"
},  # Firmware version
	"b5f90002-aa8d-11e3-9046-0002a5d5c51b": {
		"name": "WiFi SSID"
},  # SSID
	"b5f90003-aa8d-11e3-9046-0002a5d5c51b": {
		"name": "WiFi Password"
},  # WiFi AP Password
}

async def get_wifi_ssid(device_address,wifi=1):

    async with BleakClient(device_address) as client:
    
        if client.is_connected:
            print ("----Camera is connected")
        else:
            print ("----Camera is Not connected")
    
        #await client.connect()
        
        ssid = {}
        
        for service in client.services:
            for char in service.characteristics:
                if "read" in char.properties:
                    if char.uuid not in camera_info_chars:
                        continue
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        valueinutf = value.decode("utf-8")
                        
                        
                        if char.uuid == "00002a19-0000-1000-8000-00805f9b34fb":
                            valueinutf = str(ord(value)) + "%"
                        '''
                        caminfo.add_row([colored(camera_info_chars[char.uuid].get(
                            "name"), "cyan"), colored(valueinutf, "green")])
                        '''
                        print ([camera_info_chars[char.uuid].get("name"),valueinutf])
                        ssid[camera_info_chars[char.uuid].get("name")] = valueinutf
                    except Exception:
                        continue
                        
    if len(ssid.keys()) == 0:
        return None
    
    
    return ssid
                        
async def discover_gopro_cameras():
    devices = await BleakScanner.discover()
    filtered_gopro_cameras = [device for device in devices if device.name and "GoPro" in device.name]
    return filtered_gopro_cameras

async def command_send(command_to_run, device_address):
    await run(device_address, command_to_run)

async def do():
    gopro_cameras = await discover_gopro_cameras()
    if len(gopro_cameras) == 0:
        print('Not Found GoPro Camera')
        return
    
    for camera in gopro_cameras:
        print(f"Found GoPro Camera: {camera.name}, Address: {camera.address}")
    
    await ret_media(gopro_cameras)

async def ret_media(gopro_cameras):

    #

    for camera in gopro_cameras:
        print(f"--open wifi: {camera.name}, Address: {camera.address}")
        # WiFiをONにするコマンドを送信
        
        #print('Try to WiFi OFF!!')
        #await command_send('wifi off', camera.address)
        
        
        #connect_wifi('ODAGP777',ssid['WiFi Password'])
        
        print('Try to WiFi ON!! SSID:')
        await command_send('wifi on', camera.address)
        
        print('----get Info')
        # infoを取得
        ssid = await get_wifi_ssid(camera.address)
        
        #print(ssid)
        if ssid != None:
            print('Try to connect WiFi ',ssid['WiFi SSID'])
            
            connect_wifi(ssid['WiFi SSID'],ssid['WiFi Password'])


def connect_wifi(ssid, password):

    wifi = PyWiFi()  # Wi-Fiデバイスのインスタンスを作成
    ifaces = wifi.interfaces()[0]  # 最初の無線LANインターフェースを取得

    ifaces.disconnect()  # 既存の接続を切断
    profile = Profile()  # 新しいプロファイルを作成
    profile.ssid = ssid  # Wi-FiのSSIDを設定
    profile.auth = const.AUTH_ALG_OPEN  # 認証アルゴリズムを設定
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # キーマネジメントを設定
    profile.cipher = const.CIPHER_TYPE_CCMP  # 暗号タイプを設定
    profile.key = password  # Wi-Fiのパスワードを設定

    ifaces.remove_all_network_profiles()  # 既存のプロファイルをすべて削除
    tmp_profile = ifaces.add_network_profile(profile)  # 新しいプロファイルを追加

    ifaces.connect(tmp_profile)  # Wi-Fiに接続
    print(f"Connecting to {ssid}...")
    
    
    
if __name__ == "__main__":
    asyncio.run(do())
    
asyncio.run(do())