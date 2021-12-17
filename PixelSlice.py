import cv2
import numpy as np
import random
import os
import time
from threading import Thread


CANNY_THRESH_1 = 30
CANNY_THRESH_2 = 50

low_ir = np.array([100,0,80],np.uint8) # Define lower threshold for ir images to get hand
up_ir = np.array([200, 150, 255],np.uint8) # Define uper threshold for ir images to get hand
low_rgb = np.array([0,40,100],np.uint8)
up_rgb = np.array([205, 200, 255],np.uint8)


cam = cv2.VideoCapture(0)
images_dir = 'fruits_images_bg_rm/'
fruits_list = os.listdir(images_dir)
resol = (480,480)
fruit_w = 80

def rnd():
    return(random.randint(0,10))
fruits_lst = []
fruits_names = []
r, im = cam.read()
im = im[0:480,80:560]
prf = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

players = [1,2]
p1_score = 0
p2_score = 0
c_plr = players[0]

started = False
missed = 0

def play_sound():
    os.system('omxplayer -o local /home/pi/Desktop/Project_directory/sound.mp3')

while True:
    re,im = cam.read()
    if re:
        im = cv2.flip(im,1)
        im = im[0:480,80:560]
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        skin = cv2.inRange(hsv, low_rgb,up_rgb) # Extracting hand in the range of upper and lower threshold values that are defined above
        skin = cv2.dilate(skin, None,iterations=2) # Image closing
        skin = cv2.erode(skin, None,iterations=4)
        
        img = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        
        im = cv2.absdiff(img,prf)
        re,thr = cv2.threshold(im,40,255,cv2.THRESH_BINARY)
        thr = cv2.erode(thr,None,iterations = 2)
        thr = cv2.dilate(thr,None,iterations = 14)

        thr = cv2.bitwise_and(skin,thr,mask = skin)
        im = cv2.merge([thr,thr,thr])
        
        
        contours, hierarchy = cv2.findContours(thr,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        new_contours = []
        cens = [(frt['pos'][0]+40,frt['pos'][1]+40) for frt in fruits_lst]
        removed = False
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            c_area = cv2.contourArea(cnt)
            #print(c_area)
            if int(c_area) in range(5000,45000):
                if started:
                    for cen in cens:
                        if cen in cnt:
                            th1 = Thread(target=play_sound,args=())
                            th1.start()
                            if c_plr == 1:
                                p1_score+=1
                            else:
                                p2_score+=1
                            if True:#try:
                                print(len(fruits_lst), len(fruits_names))
                                fruits_names.remove(fruits_lst[cens.index(cen)]['name'])
                                fruits_lst.remove(fruits_lst[cens.index(cen)])
                                removed = True
                            else:#except:
                                aaa=0
                            break
                    if removed:
                        break
                new_contours.append(cnt)
        cv2.drawContours(im, new_contours,-1,(50,255,50),-1)
        #cv2.imshow('mask',mask)
        print(p1_score,p2_score,missed,c_plr)
        #final = 
        prf = img
        if started:
            if len(fruits_lst)<random.randint(0,2):
                name = fruits_list[rnd()]
                px = random.randint(0,resol[0]-fruit_w)
                if px > int(resol[0]/2):
                    difx = -random.randint(1,2)
                else:
                    difx = random.randint(2,3)
                dify = random.randint(20,25)
                fruits_lst.append({'name':name,'im':cv2.imread(images_dir+name),'pos':[px,resol[1]-fruit_w],'dif':[difx,dify],'range':random.randint(int(0.1*resol[1]),int(0.5*resol[1])),'up':1})
                fruits_names.append(name)
            for fruit in fruits_lst:
                #print(fruit['range'],fruit['pos'][1])
                try:
                    im[fruit['pos'][1]:fruit['pos'][1]+fruit_w,fruit['pos'][0]:fruit['pos'][0]+fruit_w] = fruit['im']
                    if fruit['pos'][1]<fruit['range']:
                        fruit['up']=0
                        
                    if fruit['up']==1:
                        fruit['pos'][1]-=fruit['dif'][1]
                        
                    else:
                        fruit['pos'][1]+=int(0.7*fruit['dif'][1])
                    fruit['pos'][0]+=fruit['dif'][0]
                    fruits_lst[fruits_lst.index(fruit)] = fruit
                except:
                    if True:#try:
                        print(len(fruits_lst), len(fruits_names))
                        if fruit['name'] in fruits_names:
                            #fruits_lst.remove(fruits_lst[fruits_lst.index(fruit)])
                            fruits_lst.remove(fruits_lst[fruits_names.index(fruit['name'])])
                            fruits_names.remove(fruit['name'])
                            missed+=1
                    else:#except:
                        aaa=0
            if c_plr == 1:
                score_show = str(p1_score)
                cv2.rectangle(im, (200,5), (280,55), (100,200,50), -1)
                cv2.putText(im,'P 1',(210,30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,255,255), 2, cv2.LINE_AA)
            else:
                score_show = str(p2_score)
                cv2.rectangle(im, (200,5), (280,55), (100,200,50), -1)
                cv2.putText(im,'P 2',(210,30), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.rectangle(im, (5,5), (105,55), (100,200,50), -1)
            cv2.putText(im,score_show,(10,30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.rectangle(im, (5,420), (105,475), (100,200,50), -1)
            cv2.putText(im,str(missed),(10,445), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255,255,255), 2, cv2.LINE_AA)
            
            if missed > 2:
                if c_plr == 1:
                    print('changing')
                    c_plr = 2
                    missed = 0
                    fruits_lst = []
                    fruits_names = []
                    for j in range(10):
                        im = cv2.resize(im,(1020,1020))
                        cv2.imshow('im',im)
                        time.sleep(0.1)
                        key = cv2.waitKey(27)
                        if key == ord('q'):
                            break
                else:
                    if p1_score>p2_score:
                        text1 = 'Winner'
                        text2 = 'P-1'
                    else:
                        text1 = 'Winner'
                        text2 = 'P-2'
                    p1_score = 0
                    p2_score = 0
                    c_plr = 1
                    missed = 0
                    fruits_lst = []
                    fruits_names = []
                    for j in range(100):
                        if j == 0:
                            cv2.rectangle(im, (80,80), (400,400), (100,200,50), -1)
                            cv2.putText(im,text1,(100,170), cv2.FONT_HERSHEY_SIMPLEX,
                                        2.5, (200,200,200), 5, cv2.LINE_AA)
                            cv2.putText(im,text2,(150,300), cv2.FONT_HERSHEY_SIMPLEX,
                                        2.5, (200,200,200), 6, cv2.LINE_AA)
                        im = cv2.resize(im,(1020,1020))
                        cv2.imshow('im',im)
                        time.sleep(0.1)
                        key = cv2.waitKey(27)
                        if key == ord('q'):
                            break
                started = False
                
        else:
            print('d')
            cv2.rectangle(im, (350,10), (460,60), (100,200,50), -1)
            cv2.putText(im,'Start',(360,40), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255,255,255), 1, cv2.LINE_AA)
            print(len(new_contours))
            if len(new_contours):
                for cnt in new_contours:
                    hcnt = cv2.convexHull(cnt)
                    if (400,30) in hcnt:
                        th1 = Thread(target=play_sound,args=())
                        th1.start()
                        started = True
                        break
        #time.sleep(0.01)
        im = cv2.resize(im,(1020,1020))
        cv2.imshow('im',im)
    key = cv2.waitKey(27)
    if key == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()

