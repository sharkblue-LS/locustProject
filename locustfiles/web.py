from locust import HttpUser,task,constant,SequentialTaskSet,TaskSet
import re


# #继承SequentialTaskSet的一个任务类，内部编排好任务的执行顺序
# class TaskCase(SequentialTaskSet):
#
# 	#初始化
# 	def on_start(self):
# 		self.client.get('/')
#
# 	# @task装饰器说明下面是一个任务
# 	@task
# 	def open_blog(self):
# 		with self.client.get('/huanghaopeng/') as resp:
# 			if resp.status_code < 300:
# 				pattern = re.compile('<a href="(.*)" class="c_b_p_desc_readmore">')
# 				self.urlList = pattern.findall(resp.text)
# 			else:
# 				pass
#
# 	# @task装饰器说明下面是一个任务
# 	@task
# 	def open_links(self):
# 		#由于权重配置，无法确保open_links任务执行时，self.urlList包含文章链接列表
# 		for url in self.urlList:
# 			with self.client.get(url,name="open_links",catch_response=True) as resp:
# 				if resp.elapsed.total_seconds() > 3:
# 					resp.failure("Request took too long")
# 				else:
# 					resp.success()
#
# 	@task
# 	def search_page(self):
# 		with self.client.get('/',catch_response=True) as resp:
# 			if "test" in resp.text:
# 				resp.success()
# 			else:
# 				resp.failure(resp.text)
#
# #继承HttpUser
# class cnblogUser(HttpUser):
# 	tasks = [TaskCase]
# 	wait_time = constant(3)

#循环取数据，数据可重复使用
# class UserBehavior(TaskSet):
# 	def on_start(self):
# 		self.index = 0
#
# 	@task
# 	def test_visit(self):
# 		url = self.user.share_data[self.index]
# 		print('visit url:%s'%url)
# 		self.index = (self.index + 1)%len(self.user.share_data)
# 		print(self.index)
# 		self.client.get(url)
#
# class WebsiteUser(HttpUser):
# 	host = 'https://debugtalk.com'
# 	tasks = [UserBehavior]
# 	share_data = ['url1', 'url2', 'url3', 'url4', 'url5']
# 	min_wait = 1000
# 	max_wait = 3000

#保证并发测试数据唯一性，不循环取数据
import queue

class UserBehavior(TaskSet):
	
	@task
	def test_register(self):
		try:
			data = self.user.user_data_queue.get()
		except queue.Empty:
			print('account data run out,test ended.')
			exit(0)
			
		print('register with user:{},pwd:{}'.format(data['username'],data['password']))
		payload = {'username':data['username'],'password':data['password']}
		
		self.client.post('/register',data=payload)
		
class WebsiteUser(HttpUser):
	host = 'https://debugtalk.com'
	tasks = [UserBehavior]
	
	user_data_queue = queue.Queue()
	for index in range(10):
		data = {'username':'test%04d'%index,
		        'password':'pwd%04d'%index,
		        'email':'test%04d@debugtalk.test'%index,
		        'phone':'186%08d'%index}
		user_data_queue.put_nowait(data)
		
	min_wait = 1000
	max_wait = 3000
	

