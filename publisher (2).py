def lock(path):
	import fcntl
	x = open('path', 'w+')
	fcntl.flock(x, fcntl.LOCK_EX | fcntl.LOCK_NB)
	return x;

def unlock(x):
	import fcntl
	fcntl.flock(x, fcntl.LOCK_UN);

def publish_queue(file_, filename):
	print('queue');
	host = 'localhost';	
	port = 5672
	import pika
	import sys
	import os;
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
		#print(" [x] Received %r" % body)
		ch.basic_ack(delivery_tag = method.delivery_tag)
		connection.close();				
    		print(" [x] Received response")	
		fo = open(filename, "wb+")
		fo.write(body);			
    		#ch.basic_ack(delivery_tag = method.delivery_tag)
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
				if (f.split('.')[-1]  != 'backup' and f.split('.')[-1]  != 'result'):
					import uuid
					import os
					from shutil import copyfile
					x =  mypath+f+'.'+'backup';
					filescr = mypath + f;
					print(filescr + x);
					copyfile(filescr, x);			
					file_ = open(filescr);
					text = file_.read();
					print(text);
					desc = lock(filescr);
					file_.close();
					unlock(desc);
					os.remove(filescr);							
					host = 'localhost';
					port = 5672;
					#thread = Thread(target = publish_queue, args = (text,filescr+'result', ))
					#thread.start()	
					print(text + "    " + filescr+"."+'result');
					publish_queue(text,filescr+"."+'result');
					
		except:	
			print('Waiting file to appear');
			time.sleep(1);		
			continue;
	
publish();	