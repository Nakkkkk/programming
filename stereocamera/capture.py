# -*- coding: utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt


def main():
    # カメラのキャプチャ
    cap1 = cv2.VideoCapture(1)
    cap2 = cv2.VideoCapture(0)

    im1ele = cap1.read()[1]
    hight = im1ele.shape[0]
    width = im1ele.shape[1]
    hexp = int(hight*1.1)
    wexp = int(width*1.1)

    im2log = cap2.read()[1]
    h = im2log.shape[0]
    w = im2log.shape[1]

    hcut = int((hexp - h)/2)
    wcut = int((wexp - w)/2)

    im1ele = cv2.resize(im1ele,(wexp,hexp))
    im1eleexpcut = im1ele[hcut:h+hcut,wcut:w+wcut]

    print "ele(h,w) = " + str(hight) + " , " + str(width)
    print "log(h,w) = " + str(h) + " , " + str(w)
    print "eleexp(h,w) = " + str(hexp) + " , " + str(wexp)
    print "eleexpcut(h,w) = " + str(im1eleexpcut.shape[0]) + " , " + str(im1eleexpcut.shape[1])
    print "hcut = " + str(hcut) + " ,wcut = " + str(wcut)

    while(1):
        im1 = cap1.read()[1]        # カメラ1のフレーム取得
        im2 = cap2.read()[1]        # カメラ2のフレーム取得

        im1 = cv2.resize(im1,(wexp,hexp))
        im1 = im1[hcut:h+hcut,wcut:w+wcut]
        im2 = im2[0:h,0:w]
        
        cv2.imshow("Left",im1)
        cv2.imshow("Right",im2)
        im1_g = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2_g = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        img_left = cv2.GaussianBlur(cv2.equalizeHist(im1_g), (3,3), 0)
	img_right = cv2.GaussianBlur(cv2.equalizeHist(im2_g) ,(3,3), 0)
	window_size = 1
	stereo = cv2.StereoSGBM(
	    minDisparity = 0,           # 視差の下限
	    numDisparities = 32,        # 最大の上限
	    SADWindowSize = window_size,# SADの窓サイズ
 	    uniquenessRatio = 2,        # パーセント単位で表現されるマージン
	    speckleWindowSize = 2,      # 視差領域の最大サイズ
	    speckleRange = 16,          # それぞれの連結成分における最大視差値
	    disp12MaxDiff = 2,          # left-right 視差チェックにおけて許容される最大の差
	    P1 = 8*3*window_size**2,    # 視差のなめらかさを制御するパラメータ1
	    P2 = 32*3*window_size**2,   # 視差のなめらかさを制御するパラメータ2
	    fullDP = True               # 完全な2パス動的計画法を使うならTrue
	)
        disp = 
        disp = stereo.compute(img_left, img_right).astype(np.int16)
	disp = cv2.normalize(disp, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
	cv2.imshow("disp", disp)
        ''' 
        stereo = cv2.StereoBM_create(numDisparities=16, blockSize=21)
        im1_g = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2_g = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        disparity = stereo.compute(im1_g,im2_g)
       # disparity = stereo.compute(im1,im2)
        plt.imshow(disparity,"gray")
       # plt.imshow("stereo",disparity)
        plt.show()
        '''
        # キーが押されたらループから抜ける
        if cv2.waitKey(10) > 0:
            cap1.release()
            cap2.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
