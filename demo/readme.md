# 测试demo
采用flask + vue开发


安装依赖启动
```
python3 -m pip install -r requirements.txt
python3 app.py
```




## 漏洞接口
### /api/editpasswd
存在越权修改密码
### /api/shop/product/detail
存在越权查看订单
### /api/shop/order/delete
存在越权删除订单