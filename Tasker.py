#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import Tools,config,sys, getopt

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("error")
        exit()
    op=sys.argv[1]
    task_name=sys.argv[2]
    if op=="-t":
        if task_name=="say_hello":
            Tools.send_to_admin("您好,这是一条测试信息")
        elif task_name=="status":
            Tools.send_to_admin("我状态很好")
        elif task_name=="check_conoha":
            Charge_C=Tools.GetConohaCharge()
            Status_C=Tools.GetConohaStatus()
            if(Charge_C<=config.Conoha_Warning_Charge):
               Tools.send_to_admin("你的Conoha账户余额已经小于70日元,请尽快续费!")
            elif Status_C!="Active" :
                Tools.send_to_admin("你的Conoha服务器已经停止运行,请尽快补清欠费!")
        elif task_name=="check_cloudcone":
            M=Tools.GetCloudConeInfo()
            if M["status"]!="online":
                Tools.send_to_admin("你的CloudCone账户已经停机,请尽快缴费!")
        elif task_name=="check_server":
            pass
        else:
            print("Error")
            exit()
    else:
        print("Error")
        exit()


