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

def submit(path):
	import os;
	address = "10.0.0.1";
	username = "dante1";
	password = "123";
	keyaddress = "";	
	pathfromput = generate_file(path);
	print(pathfromput);
	import paramiko
	import time;
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	while 1:	
		try:
			ssh.connect(address, username=username,  password=password)
			break;
		except: 
			print("Connection failed");
			time.sleep(10);
	print("Connection established");
	sftp = ssh.open_sftp()
	print("FTP established");
	pathtoput = os.path.expanduser('~');
	pathtoput = pathtoput + '/'+ pathfromput.split('/')[-1]
	print(pathtoput);
	while 1:
		try:	
			sftp.put(pathfromput, pathtoput);
			break;
		except:
			print("Error during putting the file");	
	sftp.close();
	ssh.close();
	get(pathtoput+'.result');
	
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
	while 1:
		try:
			ssh.connect(address,username=username,  password=password);
			break;
		except:
			print('Connection failed');
			time.sleep(10);
	sftp = ssh.open_sftp();
	while 1:
		try:
			filestat=sftp.stat(path)		
			try:	
				nametosave = os.path.expanduser('~')+'/'+path.split('/')[-1]
				sftp.get(path, nametosave)
				break;
			except:
				time.sleep(10);
		except:	
			#file is not appeared
			time.sleep(10);
			print('Sleeping, waiting for '+ path);	
	f = open(nametosave,'r');
	text = f.read();
	print text; 
submit('/home/anilam/123');