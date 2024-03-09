import requests
import time

# 送信先のURL
url = 'http://192.168.1.4:810'

'''


https://www.toolsforgopro.com/cameratools_server

上記の制御を行うTool

'''

def command(data):
    # JSONデータをPOSTリクエストで送信
    response = requests.post(url, json=data)
    # レスポンスデータをJSON形式で返す
    return response.json()
    
def ret_info(cmd='getAllCameras'):
    # 辞書としてデータを渡す
    data = command({'command': cmd})
    
    for o in data.keys():
        print(o, ':', data[o])
    
    return data
    
'''
cameras : [{'connection_state': 'connected', 'name': 'GoPro 3084'}]
command : getAllCameras
status_code : 0
'''

def ret_all_cam_info():

    d = ret_info(cmd='getAllCameras')
    
    cameras = []
    
    for o in d['cameras']:
    
        cameras.append(o['name'])
        
    print ('find caeras -- ',cameras,'\n\n')
    
    #Get the camera status
    '''
    {
	"command": "cameraStatus",
	"cameras": ["GP123456"]
    }
    '''
    data = {'command': 'cameraStatus'}
    data['cameras'] = cameras
    
    r = command(data)
    
    
    #for o in r.keys():
    #    print(o, ':', r[o])
        
    return r
        
#
'''
The status code can be 0 (ok), 
-3 (camera with the given name was not found),
 or -5 (camera is not connected).     
{
	"command": "connectToCameraWiFiAsync",
	"camera": "GP123456"
}
 
''' 
def wifi():
    #try to connect 1st camera 
    

    #list of dict
    r = ret_all_cam_info()
    
    #print(r)
    
    for o in r['cameras']:
        
        camname = o['name']
        sdata = {}
        sdata['command'] = 'sendCameraCommand'
        sdata['cameras'] = [camname]
        for on in o.keys():
            print('---',on, ':',o[on])     
        
        print ('disableWiFi')
        sdata['cameraCommand'] = 'disableWiFi'
        command(sdata)
        time.sleep(5) 
        
        print ('enableWiFi')
        sdata['cameraCommand'] = 'enableWiFi'
        command(sdata)
        time.sleep(5) 
        
        #connected bluetooth_status
        if o['bluetooth_status'] != 'connected':
        
            print ('try to conect BLE-----')
            

            sdata['cameraCommand'] = 'connectToCamera'
            
            r = command(sdata)
            
            print (r)
            
            
            
            '''
            {
                "command": "sendCameraCommand",
                "cameras": ["GP123456"],
                "cameraCommand": "connectToCamera"
            }
            '''
        
        ###########
        
        print ('try to connect WiFi:',camname)
        
        data = {'command':'connectToCameraWiFiAsync'}
        data['camera'] = camname
        
        r = command(data)
        
        print(r)
        
        return r
    