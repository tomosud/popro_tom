import requests

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
    
    for o in r.keys():
        print(o, ':', r[o])
        
def wifi():
    #try to connect 1st camera 
    
    '''
    {
	"command": "connectToCameraWiFiAsync",
	"camera": "GP123456"
    }
    '''
    #list of dict
    r = ret_all_cam_info()
    
    camname = r[0]['name']
    
    print ('try to connect :',camname)
    