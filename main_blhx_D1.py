import os
import time
import cv2
import threading


class leidian:
    def __init__(self):
        # 1个模拟器
        # 必须与实际情况匹配，否则报错
        self.nameList = ['' for i in range(1)]

    def m_connect(self, name):
        """
        连接模拟器
        :param name:模拟器的serialNo
        :return:NULL
        """
        cmd = 'adb connect %s' % name
        try:
            os.system(cmd)
        except:
            print('---------------------------connect %s fail' % name)
            exit(1)

    def m_tap(self, x, y, name):
        """
        屏幕点击
        :param x:x坐标
        :param y:y坐标
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s ' + name + ' shell input tap %s %s' % (x, y)
        try:
            os.system(cmd)
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 点击 %s %s' % (name, x, y))
        except:
            print('---------------------------click fail' + name)
            exit(1)
        print(cmd)

    def m_swipe(self, x1, y1, x2, y2, duration, name):
        """
        屏幕滑动
        :param x1:起始x坐标
        :param y1:起始y坐标
        :param x2:终止x坐标
        :param y2:终止y坐标
        :param duration:持续时间
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s ' + name + ' shell input swipe %s %s %s %s %s' % (x1, y1, x2, y2, duration)
        try:
            os.system(cmd)
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 滑动 %s %s %s %s' % (
                      name, x1, y1, x2, y2))
        except:
            print('---------------------------swipe fail' + name)
            exit(1)
        print(cmd)

    def m_text(self, s, name):
        """
        屏幕输入
        :param s:输入文本内容
        :param name:模拟器的serialNo
        :return:
        """
        cmd = 'adb -s ' + name + ' shell input text %s' % s
        try:
            os.system(cmd)
            print(
                '---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 输入 %s ' % (
                    name, s))
        except:
            print('---------------------------text fail' + name)
            exit(1)
        print(cmd)

    def m_screencap(self, name):
        """
        屏幕截屏
        :param name:模拟器的serialNo
        :return:
        """
        path = os.path.abspath('.') + '\\' + name + 'screenshot.png'
        try:
            os.system('adb -s ' + name + ' shell screencap /data/' + name + 'screen.png')
        except:
            print('---------------------------%s screencap fail' % name)
            exit(1)

        try:
            os.system('adb -s ' + name + ' pull /data/' + name + 'screen.png %s' % path)
        except:
            print('---------------------------%s pull screencap fail' % name)
            exit(1)

    def getSerialNo(self):
        """
        获取模拟器的serialNo
        :return:
        """
        cmd = 'adb devices'
        try:
            os.system(cmd)
        except:
            print('---------------------------get serial number fail')
            exit(1)
        r = os.popen(cmd)
        r.readline()
        i = 0
        for line in r.readlines():
            name = line.split()
            if len(name) > 0:
                self.nameList[i] = name[0]
                i += 1

    def image2position(self, name, imagepath, m=0):
        leidian.m_screencap(self, name)
        templatetimg = cv2.imread(imagepath, 0)  # 模板图像
        # if (templatetimg.empty()):
        #     print('open template image fail!')
        #     exit(1)
        screenshot = cv2.imread(os.path.abspath('.') + '\\' + name + 'screenshot.png', 0)  # 屏幕截图
        # if (screenshot.empty()):
        #     print('open screenshot fail!')
        #     exit(1)

        methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
        image_x, image_y = templatetimg.shape[:2]
        result = cv2.matchTemplate(screenshot, templatetimg, methods[m])
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(imagepath, max_val)
        if max_val > 0.7:
            center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
            print(center[0], center[1])
            return center
        else:
            return False

    def recognize(self, name, ipath, t, templatename='模板图像'):
        """
        识别函数
        :param name: 模拟器serialNo
        :param ipath: 模板图像路径
        :param t: 循环次数
        :param templatename: 模板图像名称，用于输出
        :return: cen
        """
        print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 开始识别 %s ' % (
            name, templatename))
        cen = False
        ts = 0
        while (not cen):
            print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                time.localtime()) + ' %s 循环识别 %s ' % (
                      name, templatename))
            ts += 1
            if (ts == t):
                print('---------------------------' + name + ' fail to recognize :' + templatename)
                break
            cen = leidian.image2position(self, name, ipath)
        print('---------------------------' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' %s 识别结束 %s ' % (
            name, templatename))
        return cen

    def autoD1(self, name):
        if name == '':
            print('---------------------------emulator name error')
            exit(1)

        print('---------------------------开始一次D1')

        # mD1.png
        ipath = os.path.abspath('.') + '\mal_script\images\mD1.png'
        cen = leidian.recognize(self, name, ipath, 15, 'D1')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        # mImmediateStart.png
        ipath = os.path.abspath('.') + '\mal_script\images\mImmediateStart.png'
        cen = leidian.recognize(self, name, ipath, 15, '立即前往')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        # mCollate.png
        ipath = os.path.abspath('.') + '\mal_script\images\mCollate.png'
        cen = leidian.recognize(self, name, ipath, 5, '整理')
        if cen:
            leidian.m_tap(self, cen[0], cen[1], name)

            # mRetire.png
            ipath = os.path.abspath('.') + '\mal_script\images\mRetire.png'
            cen = leidian.recognize(self, name, ipath, 15, '一键退役')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mInform.png
            ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
            cen = leidian.recognize(self, name, ipath, 15, '信息')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mGetitems.png
            ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
            cen = leidian.recognize(self, name, ipath, 15, '获得道具')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mInform.png
            ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
            cen = leidian.recognize(self, name, ipath, 15, '信息')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mMaterials.png
            ipath = os.path.abspath('.') + '\mal_script\images\mMaterials.png'
            cen = leidian.recognize(self, name, ipath, 15, '材料')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mGetitems.png
            ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
            cen = leidian.recognize(self, name, ipath, 15, '获得道具')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mCancel.png
            ipath = os.path.abspath('.') + '\mal_script\images\mCancel.png'
            cen = leidian.recognize(self, name, ipath, 15, '取消')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mD1.png
            ipath = os.path.abspath('.') + '\mal_script\images\mD1.png'
            cen = leidian.recognize(self, name, ipath, 15, 'D1')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mImmediateStart.png
            ipath = os.path.abspath('.') + '\mal_script\images\mImmediateStart.png'
            cen = leidian.recognize(self, name, ipath, 15, '立即前往')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

        # mFleetselect.png
        ipath = os.path.abspath('.') + '\mal_script\images\mImmediateStart.png'
        cen = leidian.recognize(self, name, ipath, 15, '舰队选择')
        if not cen:
            exit(1)

        # mImmediateStart.png
        ipath = os.path.abspath('.') + '\mal_script\images\mImmediateStart.png'
        cen = leidian.recognize(self, name, ipath, 15, '立即前往')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        # elite * 2
        elitePosition = [[740, 635], [927, 700], [745.5, 846]]
        for i in range(3):
            print('---------------------------wait 10s for refresh')
            time.sleep(10)
            leidian.m_tap(self, elitePosition[i][0], elitePosition[i][1], name)

            print('---------------------------wait 2s for moving')
            time.sleep(2)  # 移动时长
            # mCollate.png
            ipath = os.path.abspath('.') + '\mal_script\images\mCollate.png'
            cen = leidian.recognize(self, name, ipath, 5, '整理')
            if cen:
                leidian.m_tap(self, cen[0], cen[1], name)

                # mRetire.png
                ipath = os.path.abspath('.') + '\mal_script\images\mRetire.png'
                cen = leidian.recognize(self, name, ipath, 15, '一键退役')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mInform.png
                ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
                cen = leidian.recognize(self, name, ipath, 15, '信息')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mGetitems.png
                ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
                cen = leidian.recognize(self, name, ipath, 15, '获得道具')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mInform.png
                ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
                cen = leidian.recognize(self, name, ipath, 15, '信息')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mMaterials.png
                ipath = os.path.abspath('.') + '\mal_script\images\mMaterials.png'
                cen = leidian.recognize(self, name, ipath, 15, '材料')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mGetitems.png
                ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
                cen = leidian.recognize(self, name, ipath, 15, '获得道具')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mCancel.png
                ipath = os.path.abspath('.') + '\mal_script\images\mCancel.png'
                cen = leidian.recognize(self, name, ipath, 15, '取消')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mOffensive.png
                ipath = os.path.abspath('.') + '\mal_script\images\mOffensive.png'
                cen = leidian.recognize(self, name, ipath, 15, '迎击')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

            # mOffensive.png
            ipath = os.path.abspath('.') + '\mal_script\images\mOffensive.png'
            cen = leidian.recognize(self, name, ipath, 5, '迎击')
            if not cen:
                print('---------------------------wait 60s for weigh anchor')
                time.sleep(60)  # 战斗时长

                # mContinue.png
                ipath = os.path.abspath('.') + '\mal_script\images\mContinue.png'
                cen = leidian.recognize(self, name, ipath, 15, '点击继续')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mGetitems.png
                ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
                cen = leidian.recognize(self, name, ipath, 15, '获得道具')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                for j in range(4):
                    leidian.m_tap(self, 1000, 250, name)  # 获得紫金

                # mConfirm_gold.png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm_gold.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定（金色）')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

        # enemy * 3
        for i in range(3):
            print('---------------------------wait 10s for a refresh')
            time.sleep(10)
            # mEnemy1.png
            ipath1 = os.path.abspath('.') + '\mal_script\images\mEnemy1.png'
            cen1 = leidian.recognize(self, name, ipath1, 5, '敌舰1：主力舰队')

            # mEnemy2.png
            ipath2 = os.path.abspath('.') + '\mal_script\images\mEnemy2.png'
            cen2 = leidian.recognize(self, name, ipath2, 5, '敌舰2：航空舰队')

            # mEnemy3.png
            ipath3 = os.path.abspath('.') + '\mal_script\images\mEnemy3.png'
            cen3 = leidian.recognize(self, name, ipath3, 5, '敌舰3：侦查舰队')

            if cen1:
                leidian.m_tap(self, cen1[0], cen1[1], name)
            elif cen2:
                leidian.m_tap(self, cen2[0], cen2[1], name)
            elif cen3:
                leidian.m_tap(self, cen3[0], cen3[1], name)
            else:
                print('---------------------------fail to recognize enemy: %s' % i)
                exit(1)

            print('---------------------------wait 2s for moving')
            time.sleep(2)  # 移动时长
            # mCollate.png
            ipath = os.path.abspath('.') + '\mal_script\images\mCollate.png'
            cen = leidian.recognize(self, name, ipath, 5, '整理')
            if cen:
                leidian.m_tap(self, cen[0], cen[1], name)

                # mRetire.png
                ipath = os.path.abspath('.') + '\mal_script\images\mRetire.png'
                cen = leidian.recognize(self, name, ipath, 15, '一键退役')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mInform.png
                ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
                cen = leidian.recognize(self, name, ipath, 15, '信息')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mGetitems.png
                ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
                cen = leidian.recognize(self, name, ipath, 15, '获得道具')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mInform.png
                ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
                cen = leidian.recognize(self, name, ipath, 15, '信息')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mMaterials.png
                ipath = os.path.abspath('.') + '\mal_script\images\mMaterials.png'
                cen = leidian.recognize(self, name, ipath, 15, '材料')
                if not cen:
                    exit(1)

                # mConfirm .png
                ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
                cen = leidian.recognize(self, name, ipath, 15, '确定')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mGetitems.png
                ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
                cen = leidian.recognize(self, name, ipath, 15, '获得道具')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mCancel.png
                ipath = os.path.abspath('.') + '\mal_script\images\mCancel.png'
                cen = leidian.recognize(self, name, ipath, 15, '取消')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

                # mOffensive.png
                ipath = os.path.abspath('.') + '\mal_script\images\mOffensive.png'
                cen = leidian.recognize(self, name, ipath, 15, '迎击')
                if not cen:
                    exit(1)
                leidian.m_tap(self, cen[0], cen[1], name)

            print('---------------------------wait 60s for weigh anchor')
            time.sleep(60)  # 战斗时长

            # mContinue.png
            ipath = os.path.abspath('.') + '\mal_script\images\mContinue.png'
            cen = leidian.recognize(self, name, ipath, 15, '点击继续')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mGetitems.png
            ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
            cen = leidian.recognize(self, name, ipath, 15, '获得道具')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            for j in range(4):
                leidian.m_tap(self, 1000, 250, name)  # 获得紫金

            # mConfirm_gold.png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm_gold.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定（金色）')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

        print('---------------------------wait 5s for refresh')
        time.sleep(5)
        # mSwitchover.png
        ipath = os.path.abspath('.') + '\mal_script\images\mSwitchover.png'
        cen = leidian.recognize(self, name, ipath, 15, '切换')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        # mRichelieu.png
        ipath = os.path.abspath('.') + '\mal_script\images\mRichelieu.png'
        cen = leidian.recognize(self, name, ipath, 15, '黎塞留')
        if not cen:
            exit(1)

        leidian.m_swipe(self, 1000, 250, 500, 250, 2000, name)  # 2000ms = 2s

        # mStone.png
        ipath = os.path.abspath('.') + '\mal_script\images\mStone.png'
        cen = leidian.recognize(self, name, ipath, 15, '石头')
        if not cen:
            exit(1)

        bossPositon = [[605, cen[1]], [800, cen[1]]]

        print('---------------------------wait 2s for refresh')
        time.sleep(2)
        leidian.m_tap(self, bossPositon[0][0], bossPositon[0][1], name)

        print('---------------------------wait 10s for moving')
        time.sleep(10)
        leidian.m_tap(self, bossPositon[1][0], bossPositon[1][1], name)

        print('---------------------------wait 10s for moving')
        time.sleep(10)
        # mCollate.png
        ipath = os.path.abspath('.') + '\mal_script\images\mCollate.png'
        cen = leidian.recognize(self, name, ipath, 5, '整理')
        if cen:
            leidian.m_tap(self, cen[0], cen[1], name)

            # mRetire.png
            ipath = os.path.abspath('.') + '\mal_script\images\mRetire.png'
            cen = leidian.recognize(self, name, ipath, 15, '一键退役')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mInform.png
            ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
            cen = leidian.recognize(self, name, ipath, 15, '信息')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mGetitems.png
            ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
            cen = leidian.recognize(self, name, ipath, 15, '获得道具')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mInform.png
            ipath = os.path.abspath('.') + '\mal_script\images\mInform.png'
            cen = leidian.recognize(self, name, ipath, 15, '信息')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mMaterials.png
            ipath = os.path.abspath('.') + '\mal_script\images\mMaterials.png'
            cen = leidian.recognize(self, name, ipath, 15, '材料')
            if not cen:
                exit(1)

            # mConfirm .png
            ipath = os.path.abspath('.') + '\mal_script\images\mConfirm.png'
            cen = leidian.recognize(self, name, ipath, 15, '确定')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mGetitems.png
            ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
            cen = leidian.recognize(self, name, ipath, 15, '获得道具')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mCancel.png
            ipath = os.path.abspath('.') + '\mal_script\images\mCancel.png'
            cen = leidian.recognize(self, name, ipath, 15, '取消')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

            # mOffensive.png
            ipath = os.path.abspath('.') + '\mal_script\images\mOffensive.png'
            cen = leidian.recognize(self, name, ipath, 15, '迎击')
            if not cen:
                exit(1)
            leidian.m_tap(self, cen[0], cen[1], name)

        print('---------------------------wait 120s for weigh anchor')
        time.sleep(120)  # 战斗时长

        # mContinue.png
        ipath = os.path.abspath('.') + '\mal_script\images\mContinue.png'
        cen = leidian.recognize(self, name, ipath, 15, '点击继续')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        # mGetitems.png
        ipath = os.path.abspath('.') + '\mal_script\images\mGetitems.png'
        cen = leidian.recognize(self, name, ipath, 15, '获得道具')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        for j in range(4):
            leidian.m_tap(self, 1000, 250, name)  # 获得紫金

        # mConfirm_gold.png
        ipath = os.path.abspath('.') + '\mal_script\images\mConfirm_gold.png'
        cen = leidian.recognize(self, name, ipath, 15, '确定（金色）')
        if not cen:
            exit(1)
        leidian.m_tap(self, cen[0], cen[1], name)

        print('---------------------------一次D1结束')


if __name__ == '__main__':
    ld = leidian()
    ld.getSerialNo()

    while True:
        t_start = time.process_time()
        ld.autoD1(ld.nameList[0])
        t_end = time.process_time()
        t_process = t_end - t_start
        print('---------------------------一次D1用时: %s' % t_process)
