#启动命令：
启动单项任务  
locust -f locustfiles/web.py --web-host=127.0.0.1  
分布式运行  
locust -f locustfiles/web.py --master  
locust -f locustfiles/web.py --slave --master-host=主机ip 
