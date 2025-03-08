# init 
打算用openai的API，目前openai的比较火，各大厂商应该都是能接入上的，后面换模型也方便一些

模型考虑：  

- 通义千问  
开源，但部署调用运行费劲
- chatgpt4omini  
还算便宜，但是有时候吞字
- 其他api
有的基本上能白嫖，或者说几块钱足够一直用，回头再说


`pip install openai`

使用这个库，脚本加上openai.api_base = url 就可以调用别的厂商的

# 使用LLM进行检测

LLM进行检测。

```
import LLM

source_request = \
'''
GET /api/v1/user/profile HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
'''
source_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 123,
        "username": "john_doe",
        "email": "john_doe@example.com"
    }
}

'''
modify_request = \
'''
GET /api/v1/user/profile HTTP/1.1
Host: example.com

'''
modify_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "data":{
    }
    "msg":"no auth"
}
'''
llm = LLM()
print(llm.check(source_request,source_response,modify_request,modify_response))

```

# LLMTest

测试test_example文件夹下的测试样例，在控制台输出结果

```
import LLMTest
test = LLMTest()
test.start()
```



# 实现过程

**判断一个接口，是否有未授权、平行越权、垂直越权：**

- 垂直越权：

  分别以admin的token和普通用户的token请求，看响应是否相同。

  如果是人工测，当然知道谁是admin，如果是llm就不知道，他只知道token不一样，不知道权限高低。

- 未授权：

  去掉token再请求，如果响应回来数据，就存在漏洞。

- 平行越权：

  拿同一个token，去修改某些参数比如orderId，读取到别的用户的数据，就是平行越权。

  但是如果是后台的接口，比如admin去管理所有的orders，这就是功能正常的。

  所以一个接口是不是后台接口，判定有没有洞的结果也不一样。



**一些要考虑的问题：**

- LLM判断authentication vulneribility的标准是什么？

  如果是人工测，看见响应回来一些不属于当前用户的数据，就是有洞，如果没有，大概率没洞。

  llm会考虑：

  - http状态码

    比如应该返回403或401而不是200

    ![1728877203126](imgs\1728877203126.jpg)

  - 提示信息

    如果没带token，响应应该有明确的信息，提示你没权限，比如no auth，才是合理的，别的就不合理，比如null，failed，或者空。

  - 接口是否返回密码明文等敏感信息。

    比如业务要求就要返回用户的敏感信息，姓名邮箱身份证密码明文什么的，测越权不考虑这些，但是llm会考虑。

- 对于一些接口，假如是管理员专用的，比如查看一个用户的详细信息，就必须带userId，orderId之类的。

  这种就不算平行越权。

- 修改无关权限的参数，造成的回显结果的不同，比如page和pageNum



**问题的解决方式：**

先给出authentication vulneribility的阐释，然后在的例子中继续消除别的因素的影响

```
Hello,I want you to help me check if some apis has authentication vulneribility.

An api is vulnerable in the following cases:
1. A low-permission user an access this api that is for high-permission users.
2. The api can be access successfully without authentication token.
3. Current user can retrieve other users's data by modifying specific params like id.

Before checking whether an api is vulnerable, you should assume 2 cases: The api is designed or not,for admin to manage the system,
because an api can be secure when it is designed for admin but vulnerable when not. 

Next I will give you some examples.
```

消除status code的影响

>request 1 of api 1
>
>GET /api/v1/background/info HTTP/1.1
>Host: example.com
>Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
>
>response body of request 1
>
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "data":{
>        "status":"on",
>        "password":"98y61283123oindcp",
>        "admin":"background_admin"
>    }
>    "msg":"ok"
>}
>
>request 2 of api 1
>
>GET /api/v1/background/info HTTP/1.1
>Host: example.com
>
>response of request 2
>
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "data":{
>    }
>    "msg":"no auth"
>}
>
>According to the requests and responses show above, the api return the result with data to the authenticated request and did not disclose any data to the unauthenticated request and show 'no auth' 
>Although the api still return the 200 status code, but the main point is wheather data is disclosed.So you don't need to take status code into consideration.
>So the api is secure.

然后，对于管理员接口，和平行越权的区分， 是这样处理的

>
>
>Let's see another example:
>
>request 1
>
>GET /api/v1/user/profile?id=81276417824 HTTP/1.1
>Host: example.com
>Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
>
>response body
>
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "user": {
>        "id": 81276417824,
>        "username": "john_doe",
>        "email": "john_doe@example.com"
>    }
>}
>
>
>request 2
>
>GET /api/v1/user/profile?id=81276417825 HTTP/1.1
>Host: example.com
>Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
>
>response
>
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "user": {
>        "id": 81276417825,
>        "username": "Trump",
>        "email": "Trump@example.com"
>    }
>}
>
>You can see that the api return specific result based on the modified param id and return other user's information
>So the api is vulnerable.
>However, If the api is designed for admin to manage the system,it works fine.So in this case it is secure though it's name "/api/v1/user/profile" does not imply it is for admin



如果token不一样，llm无法识别哪个是admin，哪个是普通用户，那就只能假设了。

>request: 
>
>POST /api/user/info HTTP/1.1
>Host: example.com
>Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
>
>userId=123
>
>response:
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "user": {
>        "id": 123,
>        "username": "john_doe",
>        "email": "john_doe@example.com",
>        "password":"helloworld260@$"
>    }
>}
>
>request:
>POST /api/user/info HTTP/1.1
>Host: example.com
>Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMxMjM4OTAiLCJuYW1lIjoiVHJ1bXAiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
>
>userId=123
>
>response: 
>HTTP/1.1 200 OK
>Content-Type: application/json
>
>{
>    "user": {
>        "id": 123,
>        "username": "john_doe",
>        "email": "john_doe@example.com",
>        "password":"helloworld260@$"
>    }
>}
>
>In this example, the 2 requests has different token. 
>We always assume the request 1's token is admin's and the other is normal user's.
>We also assume the api can be accessed by admin but not normal users.
>So in this case, the api return the same data to two token, means that it can be accessed by normal users.
>So it is vulnerable.
>Attention! Once you deal with requests with different tokens like this, you always make the above 2 assumptions

最后是检测完，该返回什么结果。

>If the api is sure to be vulnerable in given cases, you need to reply "Yes,vulnerable"
>If you are not sure, just reply "Not sure"
>
>After giving the above reply,you also need to give the reason in short words.

**总体思路：**

LLM初始化时，先依次读取下列文件夹内所有文件的内容，作为初始化prompt。

直接发送文件初始内容，文件名无要求。

- start-prompt 

  ```
  Hello,I want you to help me check if some apis has authentication vulneribility.
  
  An api is vulnerable in the following cases:
  1. A low-permission user an access this api that is for high-permission users.
  2. The api can be access successfully without authentication token.
  3. Current user can retrieve other users's data by modifying specific params like id.
  
  Before checking whether an api is vulnerable, you should assume 2 cases: The api is designed or not,for admin to manage the system,
  because an api can be secure when it is designed for admin but vulnerable when not. 
  
  Next I will give you some examples.
  
  ```

- vulnerable-example

  这里附带例子，告诉llm什么样的example是vulnerable的

- secure_example

  这里附带例子，告诉llm什么样的example是secure的

- end-prompt

  ```
  You need to pay attention to the following main points:
  1. whether the 2 requests' tokens are different.
  2. whether the 2 requests' params are different
  3. whether a request has token.
  
  Ok, please check the these apis and reply in 2 parts.
      Part 1. 
          Assume the api is designed for admin.
          If the api is sure to be vulnerable in given cases, you need to reply "Yes,vulnerable"
          If you are not sure, just reply "Not sure"
      Part 2. 
          Assume the api is not designed for admin.
          If the api is sure to be vulnerable in given cases, you need to reply "Yes,vulnerable"
          If you are not sure, just reply "Not sure"
  
  
  Attention! You cannot take wheather an api return sensitive user data such as password ,email or name into consideration,because we see it as business-needed.
  After giving the above reply,you also need to give the reason in short words.
  ```

  























