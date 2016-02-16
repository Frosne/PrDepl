def generate_file(path):
	import uuid
	import os
	from shutil import copyfile
	if os.path.exists(path):
		x =  path+str(uuid.uuid1());
		copyfile(path, x)
	else :
		print('File not found');
	return x;

def lock(path):
	import fcntl
	x = open('path', 'w+')
	fcntl.flock(x, fcntl.LOCK_EX | fcntl.LOCK_NB)

def unlock(path, x):
	import fcntl
	fcntl.flock(x, fcntl.LOCK_UN);

def submit(path):
	import os;
	address = "10.0.0.1";
	username = "dante1";
	password = "123";
	keyaddress = "";	
	pathfromput = generate_file(path);
	print(pathfromput);
	import paramiko
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(address, username=username,  password=password)
	print("Connection established");
	sftp = ssh.open_sftp()
	print("FTP established");
	pathtoput = os.path.expanduser('~');
	#lock(pathtoput)
	pathtoput = pathtoput + '/'+ pathfromput.split('/')[-1]
	print(pathtoput);
	sftp.put(pathfromput, pathtoput);
	sftp.close();
	ssh.close();
	get(pathtoput+'result');
	
def get(path):
	print("Waiting for result");
	address = "10.0.0.1";
	username = "dante1";
	password = "123";
	import paramiko;
	import os;
	import time;
	ssh = paramiko.SSHClient();
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(address,username=username,  password=password);
	sftp = ssh.open_sftp();
	while 1:
		print('1');
		try:
			filestat=sftp.stat(path)		
			try:	
				lock(path);
				#print('TRY'+ os.path.expanduser('~')+'/'+path.split('/')[-1]);
				sftp.get(path, os.path.expanduser('~')+'/'+path.split('/')[-1])
				#print("FTP");
				break;
			except:
				time.sleep(10);
		except:	
			time.sleep(10);
			print('Sleeping, waiting for '+ path);
			continue;

	
	f = open(os.path.expanduser('~')+'/'+path.split('/')[-1],'r');
	text = f.read();
	print text; 
submit('/home/anilam/script');