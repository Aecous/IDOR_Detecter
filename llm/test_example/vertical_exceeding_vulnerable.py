
'''
    测试垂直越权,cookie不一样，返回结果一样

    Yes, there is vuln.
    Reason: The API reveals sensitive information, including the password, based on the userId parameter without checking if the requesting user is authorized to access that user's information. An attacker could manipulate the request and gain access to another user's credentials.
'''



source_request =\
'''
POST /api/user/info HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

userId=123
'''

source_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 123,
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password":"helloworld260@$"
    }
}
'''

modify_request = \
'''
POST /api/user/info HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMxMjM4OTAiLCJuYW1lIjoiVHJ1bXAiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

userId=123
'''

modify_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 123,
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password":"helloworld260@$"
    }
}
'''




