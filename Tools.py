#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests,json,string,config,re,os
    #查询token
def GetConohaToken():
    header={"Accept":"application/json"}
    post_data='''{"auth":{"passwordCredentials":{"username":"'''+config.Conoha_Username+'''","password":"'''+config.Conoha_Password+'''"},"tenantId":"'''+config.Conoha_ID+'''"}}'''
    url="https://identity.tyo1.conoha.io/v2.0/tokens"
    r=requests.post(url,data=post_data,headers=header)
    r_json=json.loads(r.text)
    token=r_json['access']['token']['id']
    return token

def GetConohaCharge():
    token=GetConohaToken()
    #查询总费用
    header={"Accept":"application/json","X-Auth-Token":token}
    url="https://account.tyo1.conoha.io/v1/"+config.Conoha_ID+"/payment-summary"
    r=requests.get(url,headers=header)
    r_json=json.loads(r.text)
    total=int(r_json["payment_summary"]["total_deposit_amount"])
    #查询订单花费
    url="https://account.tyo1.conoha.io/v1/"+config.Conoha_ID+"/billing-invoices?limit=1"
    r=requests.get(url,headers=header)
    r_json=json.loads(r.text)
    for r1 in r_json["billing_invoices"]:
        paid=int(r1["bill_plus_tax"])
    all=total-paid
    return all

def GetConohaStatus():
    token=GetConohaToken()
    header={"Accept":"application/json","X-Auth-Token":token}
    url="https://account.tyo1.conoha.io/v1/"+config.Conoha_ID+"/order-items"
    r=requests.get(url,headers=header)
    r_json=json.loads(r.text)
    for r1 in r_json["order_items"]:
        if r1['service_name']=="VPS":
            return r1['item_status']
    
def ConohaCharge():
    all=GetConohaCharge()
    days=round(all/35,0)
    return("你的Conoha余额为"+str(all)+"日元，预计"+str(days)+"天内用完\n")
def GetCloudConeInfo():
    header={"App-Secret":config.CloudCone_Key,"Hash":config.CloudCone_Hash}
    url="https://api.cloudcone.com/api/v1/compute/"+config.CloudCone_id+"/info"
    r=requests.get(url,headers=header)
    r_json=json.loads(r.text)
    status=r_json['__data']['instances']['status']
    due=float(r_json['__data']['instances']['price']['due'])
    due=round(due,2)
    m={"due":due,"status":status}
    return m

def CloudConeCharge():
    m=GetCloudConeInfo()
    if m["status"]=="online":
        return("你的Cloudcone主机在线,本月花费约$"+str(m["due"]))
    else:
        return("你的Cloudcone主机现在不在线,赶紧续费去！")

def ip_or_domain(str):
    ip_regex=r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'
    domain_regex=r'^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$'
    i=re.match(ip_regex,str)
    d=re.match(domain_regex,str)
    if i!=None:
        m={"Code":1,"match":i.group(0)}
    elif d!=None:
        m={"Code":2,"match":d.group(0)}
    else:
        m={"Code":-1,"match":''}
    return m

def domain_to_ip(domain):
    ip_regex=r'((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))'
    if ip_or_domain(domain)['Code']==2:
        command_i="dig "+domain+" +short"
        p=os.popen(command_i)
        t=p.read()
        if t=="":
            return 'error'
        else:
            print(t)
            i=re.search(ip_regex,t)
            if i!=None:
                return i.group(0)
            else:
                return 'error'
    else:
        return 'error'

def find_ip(ip):
    if ip_or_domain(ip)['Code']==1:
        url="curl ip.cn/?ip="+ip
        p=os.popen(url)
        r=p.read()
        r=r.replace('\n','')
        m={"Code":1,"Text":r}
    elif ip_or_domain(ip)['Code']==2:
        real_ip=domain_to_ip(ip)
        if real_ip=='error':
            m={"Code":-1,"Text":"Error"}
            return m
        url="curl ip.cn/?ip="+real_ip
        p=os.popen(url)
        r=p.read()
        r=r.replace('\n','')
        m={"Code":1,"Real_IP":real_ip,"Text":r}
    else:
        m={"Code":-1,"Text":"Error"}
    print(m)
    return m

def send_to_admin(msg):
    import telegram
    if config.Proxy_URL!="":
        B=telegram.Bot(config.Bot_Token,request=telegram.utils.request.Request(proxy_url=config.Proxy_URL))
    else:
        B=telegram.Bot(config.Bot_Token)
    B.send_message(chat_id=config.Master_ID, text=msg)

