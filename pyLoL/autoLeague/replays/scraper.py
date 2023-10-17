"""Scrapes observations from a replay file by replaying a match using
the League game client and storing the observations in a json file."""

import os
import time
import json
import subprocess
import base64
import requests
import pyautogui
import pydirectinput

class ReplayScraper(object):
    """League of Legends replay scraper class.
    
    This class handles executing the League of Legends client in
    replay mode and the scraping application in the correct order.
    Args:
        game_dir: League of Legends game directory.
        replay_dir: League of Legends *.rofl replay directory.
        dataset_dir: JSON replay files output directory.
        replay_speed: League of Legends client replay speed multiplier.
        scraper_path: Directory of the scraper program.
    """
    def __init__(self,
            game_dir,
            replay_dir,
            dataset_dir,
            scraper_dir,
            replay_speed=8,
            region="KR"):
        self.game_dir = game_dir
        self.replay_dir = replay_dir
        self.dataset_dir = dataset_dir
        self.scraper_dir = scraper_dir
        self.replay_speed = replay_speed
        self.region = region

    def run_client(self, replay_path, gameId, start, end, speed, paused , team):
        args = [
            str(os.path.join(self.game_dir, "League of Legends.exe")),
            replay_path,
            "-SkipRads",
            "-SkipBuild",
            "-EnableLNP",
            "-UseNewX3D=1",
            "-UseNewX3DFramebuffers=1"]
        #print('run lol client:', args)
        subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.game_dir)
        
        '''
        post_running : 리플레이 시작시간, 배속, 일시중지 여부 post 요청 진행 여부, 클라이언트가 리플레이를 돌리기 전까지 계속 요청.
        리플레이 돌리고 post 성공하면 False 로 변환.
        '''
        #리플레이 진영 시야 선택을 위한 단축키선택
        key = None

        if team == "Red":
            key = 'f2'
        elif team == "Blue":
            key = 'f1'  
        else:
            key = 'f'
        post_running = True 

        # 리플레이 실행 호출 횟수 임계값, post 가 POST_COUNT_THRESH 이상이 되어도 리플레이 실행이 안되면 다음으로 넘어감
        POST_COUNT_THRESH = 3
        post_count = 0
        while post_running:
            
            try:
                time.sleep(1)
                req = requests.post(
                        'https://127.0.0.1:2999/replay/playback',
                        headers={
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        data = json.dumps({
                            "paused": paused,
                            "seeking" : False,   
                            "time": start - 5,
                            "speed": speed
                        }),
                        verify=False
                    )
                #req = requests.get('https://127.0.0.1:2999/replay/playback' , verify = False)
                if req.status_code == 200:
                    #print("상태코드 : ",req.status_code , "응답 : ",req)
                    post_running = False
            except:
                time.sleep(2)
                # 리플레이 실행 호출 횟수, 예외 날때마다 1 추가
                post_count = post_count + 1

                # 탈출 조건 : 이정도로 요청을 보냈는데도 리플레이 실행이 안되면, 다음 경기 리플레이 실행
                if post_count >= POST_COUNT_THRESH:
                    return None
                
                pass
        
        
        

        '''
        replay_running : 리플레이가 실행중인가에 대한 불린 ; 클라이언트가 end 시각까지만 실행하도록
        capture_count : 리플레이 하나 당 캡쳐하는 이미지 갯수 (또는 캡쳐중인 이미지의 현재 리플레이에서 인덱스)
        '''     

        # Directory 
        directory = gameId
        # Parent Directory path 
        parent_dir = "C:/Users/김성윤/Desktop/pyLoL/"
        # Path 
        path = os.path.join(parent_dir, directory)  
        
        try:
            os.mkdir(path)
        except:
            pass

        path = os.path.join(path,team)
        # Create the directory 
        os.mkdir(path)

        #Show Team's Info Window 
        pydirectinput.keyDown('p')
        time.sleep(0.25)
        pydirectinput.keyUp('p')

        #Show Blue Team's Vision   ( RedTeam : f2 , All : f3)
        pydirectinput.press(key)
        # pydirectinput.press(key)

        replay_running = True 
     
        capture_count = 0  
        while replay_running:
            try:
                requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
                timestamp = requests.get('https://127.0.0.1:2999/replay/playback', verify=False).json()['time']    

                if  end <= timestamp <= end + 22:
                    print(f"리플레이 정상 정지, 요청 종료 시각 : {end}s , 실제 종료 시각{timestamp}s")
                    replay_running  = False
                else:
                    fore = pyautogui.getActiveWindow()
                    # 가운데 팀 정보창 스크린샷
                    # pyautogui.screenshot(rf'C:\Users\김성윤\Desktop\pyLoL\{gameId}\{team}\{capture_count}_team.png', region=(fore.size[0]-2650, fore.size[1]-450, 1500, 450))
                    # 가운데 팀 정보창 중 KDA / 제압골드 / CS 스크린샷
                    # pyautogui.screenshot(rf'C:\Users\김성윤\Desktop\pyLoL\{gameId}\{team}\{capture_count}_team_kda.png', region=(fore.size[0]-2650 + 50*8, fore.size[1]-450, 1500 -8*50 -9*50, 450))
                    # 미니맵 스크린샷
                    pyautogui.screenshot(rf'C:\Users\김성윤\Desktop\pyLoL\{gameId}\{team}\{capture_count}_minimap.png', region=(fore.size[0]-870, fore.size[1]-870, 840, 840))
                    # 전체 스크린샷
                    # pyautogui.screenshot(rf'C:\Users\김성윤\Desktop\pyLoL\{gameId}\{team}\{capture_count}.png', region=(fore.size[0]-3840, fore.size[1]-2160, 3840, 2160))
                    #print(fore.title , fore.size)
                    capture_count = capture_count + 1
                    time.sleep(0.1)
                   
            except:
                pass
        
        time.sleep(1)
        #클라이언트 종료           
        os.system("taskkill /f /im \"League of Legends.exe\"")       
        time.sleep(1)

        
    def get_replay_dir(self):
        return self.replay_dir