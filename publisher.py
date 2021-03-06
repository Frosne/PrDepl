def publish_queue(file_,path, host, port):

	print('File is put on the queue');
	import pika

	import sys

	ssl_option = {'certfile': '/home/anilam/client/cert.pem', 'keyfile': '/home/anilam/client/key.pem'}

	parameters = pika.ConnectionParameters(host=host, port=port);#
	#parameters = pika.ConnectionParameters(host=host, port=port,ssl = t, ssl_options = ssl_option);

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

	print("[X] Send task:" + file_);

	def callback(ch, method, properties, body):

    		print(" [x] Received response from worker:" + body)

		import os;

		file_ = open(path+'.backup','w');

		file_.write(body);
		file_.close();

		from shutil import copyfile

		copyfile(path+'.backup', path);

		os.remove(path+'.backup');	

    		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming();

	channel.basic_consume(callback,  queue='result')

	channel.start_consuming()



def publish():

	import time;

	import os;

	mypath = "/home/anilam/scripts/"

	while 1:				

		try:	

			from os import listdir

			from os.path import isfile, join

			filelist = [f for f in listdir(mypath) if isfile(join(mypath, f))]

			for f in filelist:

				if (f.split('.')[-1]  != 'result' and f.split('.')[-1]  != 'backup'):

					print('New File to work with : ' + f);

					filescr = mypath + f;

					file_ = open(filescr,'r');

					import fcntl;

					fcntl.flock(file_, fcntl.LOCK_EX | fcntl.LOCK_NB);

					text = file_.read();

					fcntl.flock(file_,fcntl.LOCK_UN);

					file_.close();

					os.remove(filescr);		
					publish_queue(text, filescr+'.result','10.0.0.1',5672);
					print('Execution finished');

							

		except:	

			print('Error occured, waiting');

			time.sleep(1);		

			continue;

	

publish();	