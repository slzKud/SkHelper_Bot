import requests,json,string,config
    #查询token
def ConohaCharge():
    header={"Accept":"application/json"}
    post_data='''{"auth":{"passwordCredentials":{"username":"'''+config.Conoha_Username+'''","password":"'''+config.Conoha_Password+'''"},"tenantId":"'''+config.Conoha_ID+'''"}}'''
    url="https://identity.tyo1.conoha.io/v2.0/tokens"
    r=requests.post(url,data=post_data,headers=header)
    r_json=json.loads(r.text)
    token=r_json['access']['token']['id']
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
    days=round(all/35,0)
    return("你的Conoha余额为"+str(all)+"日元，预计"+str(days)+"天内用完\n")

def CloudConeCharge():
    header={"App-Secret":config.CloudCone_Key,"Hash":config.CloudCone_Hash}
    url="https://api.cloudcone.com/api/v1/compute/"+config.CloudCone_id+"/info"
    r=requests.get(url,headers=header)
    r_json=json.loads(r.text)
    status=r_json['__data']['instances']['status']
    due=float(r_json['__data']['instances']['price']['due'])
    due=round(due,2)
    if status=="online":
        return("你的Cloudcone主机在线,本月花费约$"+str(due))
    else:
        return("你的Cloudcone主机现在不在线,赶紧续费去！")