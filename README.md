### 20170914更新内容：
更新内容&功能：
1. 按要求重新设计表结构：  
用户表：用户名 密码 邮箱 业务线(多对多)  
  主机表：主机名 ip port 类型 环境(一对多) 硬件 业务线(一对多)  
环境：名称  
业务线：名称
2. 登录&注册(Ajax+Form实现)
业务线管理：修改，删除(Ajax+Form实现)，增加(Form实现)
用户管理：修改，删除(Ajax+Form实现)，增加(Form实现)
主机管理：修改，删除(Ajax+Form实现)，增加(Form实现)
3. 分页&搜索：
三个页面实现分页和搜索功能(按名称)
4. 登录：  
admin(密码:admin)
user01,user02,user03,user04,user05,user06(密码均为123)
5. 操作：  
 只有admin用户可以更改主机所属业务线,用户所管理业务线；
其他用户只能更改主机除业务线其他字段，用户邮箱字段。

存在问题：
1. 更新资产，用户信息，一对多，多对多字段仅显示id，需刷新页面
2. 未实现功能：  
业务线创建、删除功能；  
批量删除功能；











### 20170909更新内容：
1. 分页器改用自定义Page类实现(/utils/pagination.py)
2. 登录密码md5加密校验
3. 调整登录seisson

### 20170903关于Bms_demo:
1. runserver后登陆http://127.0.0.1:8080/bms/login/  
  提供3个账号：  
    - 账号：admin  密码：admin 可以查看所有主机信息条目，可以对主机管理员进行更改  
    - 账号：Dylan  密码：123 可以查看管理员为Dylan的主机条目，不可对主机条目的管理员进行更改，添加主机条目默认属于Dylan用户  
    - 账号：Elaine 密码：123 可以查看管理员为Elaine的主机条目，不可对主机条目的管理员进行更改,添加主机条目默认属于Elaine用户
2. 进入http://127.0.0.1:8080/bms/index/可进行如下操作：  
  a. 创建资产：创建一条资产，默认属于当前登录用户(后续只能通过登录admin账号更改)  
  b. 更新：更新主机条目的信息(只有admin才能更改主机条目的"管理员"项)  
  c. 删除：删除一条主机信息(需要选中主机信息前的checkbox)  
  d. 批量删除  
  e. 注销登录：注销当前用户，返回http://127.0.0.1:8080/bms/login/页面
3. 分页：点击相应页码得到相应页数的数据
4. 搜索：在Search for..输入关键字(仅限主机名)筛选相应主机
5. Ajax实现异步请求：主机信息更新，删除功能实现异步请求


