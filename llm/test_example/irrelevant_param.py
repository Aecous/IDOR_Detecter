
'''
    修改无关权限的参数，比如一页显示几条记录，造成的回显结果不一样
'''


source_request =\
'''
GET /api/school/list/page=1&pageNum=10 HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
'''

source_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
    "school": {
        "id": 81276417824,
        "name": "清华大学",
    },
    "school": {
        "id": 81276417824,
        "name": "北京大学",
    },
    "school": {
        "id": 81276417824,
        "name": "哈佛大学",
    },
    "school": {
        "id": 81276417824,
        "name": "剑桥大学",
    },
    "school": {
        "id": 81276417824,
        "name": "广州大学",
    },
    "school": {
        "id": 81276417824,
        "name": "南京大学",
    },
    "school": {
        "id": 81276417824,
        "name": "浙江大学",
    },
}
'''

modify_request = \
'''
GET /api/school/list/page=1&pageNum=0 HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
'''

modify_response = \
'''
HTTP/1.1 200 OK
Content-Type: application/json

{
}
'''




