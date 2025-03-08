source_request =\
'''
GET /api/v1/user/profile?id=81276417824 HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
'''

source_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 81276417824,
        "username": "john_doe",
        "email": "john_doe@example.com"
    }
}
'''

modify_request = \
'''
GET /api/v1/user/profile?id=81276417825 HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

'''

modify_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "user": {
        "id": 81276417825,
        "username": "Trump",
        "email": "Trump@example.com"
    }
}
'''




