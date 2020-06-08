from doc import zhenzismsclient as smsclient
import random


# 生成四位数的随机验证码
code = ''
for num in range(1, 5):
    code = code + str(random.randint(0,9))
print(code)
AppId=105115;AppSecret='c30cd79b-3b98-4230-9370-ca00fc0b2954'
# 将AppId和AppSecret复制粘贴过来
client = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com', AppId,AppSecret )
# 第一个参数为发送号码，第二个参数为发送的验证码内容
params = {'message':'您的验证码为:%s,您的木木'%code, 'number':'18866812508'};
result = client.send(params);
# 注意result为str类型，并不是字典
print(result)

