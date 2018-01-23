
import pika
import config
import json
import traceback


class QSystem(object):

	def __init__(self, address='localhost'):
		self.address = address

	def get_channel(self):
		params = pika.URLParameters(self.address)
		params.socket_timeout = 5
		connection = pika.BlockingConnection(params)
		channel = connection.channel()
		return channel



class Scheduler(object):
	
	instance = None

	def __new__(cls, *args, **kwargs):
		if not cls.instance:
			cls.instance = object.__new__(cls, *args, **kwargs)
			
		return cls.instance

	def setUp(self, q_system):
		self.channel = q_system.get_channel()

	@staticmethod
	def get_instance(q_system):
		scheduler = Scheduler()
		scheduler.setUp(q_system)
		return scheduler

	@staticmethod
	def add(task_name, data):
		self = Scheduler.get_instance(QSystem(config.RABBIT_MQ_URL))
		self.channel.queue_declare(config.Q_INFO[task_name]['Q_NAME'], durable=True)
		self.channel.basic_publish(exchange='', routing_key=config.Q_INFO[task_name]['Q_NAME'], body=json.dumps(data))


	@staticmethod
	def recieve(task_name, callback):
		self = Scheduler.get_instance(QSystem(config.RABBIT_MQ_URL))
		self.channel.queue_declare(config.Q_INFO[task_name]['Q_NAME'], durable=True)
		self.channel.basic_consume(callback, queue=config.Q_INFO[task_name]['Q_NAME'], no_ack=False)
		try:
			self.channel.start_consuming()
		except Exception as e:
			print(traceback.format_exc())

