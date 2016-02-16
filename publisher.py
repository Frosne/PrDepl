def lock(path):
	import fcntl
	x = open('path', 'w+')
	fcntl.flock(x, fcntl.LOCK_EX | fcntl.LOCK_NB)
	return x;

def unlock(x):
	import fcntl
	fcntl.flock(x, fcntl.LOCK_UN);

def publish_queue(host, port, file_):
	host = 'localhost';
	import pika
	import sys
	#ssl_option = {'certfile': '/home/anilam/client/cert.pem', 'keyfile': '/home/anilam/client/key.pem'}
	parameters = pika.ConnectionParameters(host=host, port=port);#
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
	channel.confirm_delivery();

	channel.queue_declare(queue='task_queue', durable=True)
	channel.queue_declare(queue='result', durable = True);
		

	channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=file_,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
	def callback(ch, method, properties, body):
    		print(" [x] Received response %r" % body)
    		ch.basic_ack(delivery_tag = method.delivery_tag)

	channel.basic_consume(callback,  queue='result')
	channel.start_consuming()

def unlock(x):
	import fcntl
	fcntl.flock(x, fcntl.LOCK_UN);

def publish_queue(file_):
	print('queue');
	host = 'localhost';	
	port = 5672
	import pika
	import sys
	#ssl_option = {'certfile': '/home/anilam/client/cert.pem', 'keyfile': '/home/anilam/client/key.pem'}
	parameters = pika.ConnectionParameters(host=host, port=port);#
	connection = pika.BlockingConnection(parameters)

	channel = connection.channel()
	channel.confirm_delivery();

	channel.queue_declare(queue='task_queue', durable=True)
	channel.queue_declare(queue='result', durable = True);
		

	channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=file_,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
	print("[X] Send " + file_);
	def callback(ch, method, properties, body):
    		print(" [x] Received response %r" % body)
		
    		ch.basic_ack(delivery_tag = method.delivery_tag)
	channel.basic_consume(callback,  queue='result')
	channel.start_consuming()

def publish():
	import time;
	import os;
	from threading import Thread
	mypath = "/home/anilam/scripts/"
	while 1:				
		try:
			from os import listdir
			from os.path import isfile, join
			filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
			for f in filelist:
				if (f.split('.')[-1]  != 'backup'):
					import uuid
					import os
					from shutil import copyfile
					x =  mypath+f+'.'+'backup';
					filescr = mypath + f;
					copyfile(filescr, x);			
					file_ = open(filescr);
					text = file_.read();
					desc = lock(filescr);
					file_.close();
					unlock(desc);
					os.remove(filescr);							
					host = 'localhost';
					port = 5672;
					thread = Thread(target = publish_queue, args = (text, ))
					thread.start()
					
		except:	
			print('Waiting file to appear');
			time.sleep(1);		
			continue;
	
publish();	