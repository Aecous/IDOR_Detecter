
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
    "data":
        {    "user": {
            "id": 123,
            "username": "john_doe",
            "email": "john_doe@example.com",
            "password":"helloworld260@$"
        }
    },
    "msg":"success"

}
'''

modify_request = \
'''
POST /api/user/info HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

userId=124
'''

modify_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "data":null,
    "msg":"failed"
}
'''




