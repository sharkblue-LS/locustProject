from locust import HttpUser,task,constant,SequentialTaskSet
import re


#继承SequentialTaskSet的一个任务类，内部编排好任务的执行顺序
class TaskCase(SequentialTaskSet):
	
	#初始化
	def on_start(self):
		self.client.get('/')
		
	# @task装饰器说明下面是一个任务
	@task
	def open_blog(self):
		with self.client.get('/huanghaopeng/') as resp:
			if resp.status_code < 300:
				pattern = re.compile('<a href="(.*)" class="c_b_p_desc_readmore">')
				self.urlList = pattern.findall(resp.text)
			else:
				pass
			
	# @task装饰器说明下面是一个任务
	@task
	def open_links(self):
		#由于权重配置，无法确保open_links任务执行时，self.urlList包含文章链接列表
		for url in self.urlList:
			with self.client.get(url,name="open_links",catch_response=True) as resp:
				if resp.elapsed.total_seconds() > 3:
					resp.failure("Request took too long")
				else:
					resp.success()
					
	@task
	def search_page(self):
		with self.client.get('/',catch_response=True) as resp:
			if "test" in resp.text:
				resp.success()
			else:
				resp.failure(resp.text)
		
#继承HttpUser
class cnblogUser(HttpUser):
	tasks = [TaskCase]
	wait_time = constant(3)

