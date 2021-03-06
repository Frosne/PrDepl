def docker(script):

	try:

		print("Docker is running");

		import docker

		cli = docker.Client(base_url='unix://var/run/docker.sock', version = '1.9', timeout = 100)

		container = cli.create_container(image='i686/ubuntu', 	command=script)

		id = container.get('Id')

		cli.start(container = id)

		response = cli.logs(container = id);
		print(response);
		while response is '':
			container = cli.create_container(image='i686/ubuntu', 	command=script)

			id = container.get('Id')

			cli.start(container = id)

			response = cli.logs(container = id);
		print(response);
	except:

		return ('Execution failed');

	return response;





def worker():

	print("[X] Worker is started");

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

	

	def callback(ch, method, properties, body):

		print(" [x] Received %r" % body)

		result = docker(body);

		channel.basic_publish(exchange='',

                      routing_key='result',

                      body=result)

		ch.basic_ack(delivery_tag = method.delivery_tag)



	channel.basic_qos(prefetch_count=1)

	channel.basic_consume(callback,

                      queue='task_queue')



	channel.start_consuming()

worker();