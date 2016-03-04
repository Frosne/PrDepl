import crypt
import pwd
import os
def createUser(name, username, password):
	counter = 0;
	_username = username;
	flag = 0;
	while 1:	
		try: 
			if flag == 1:
				break;
			pwd.getpwnam(_username)
			_username = username + str(counter);			
			counter = counter+1;
		except KeyError:
			flag = 1;
	encPass = crypt.crypt(password,"22");
	print('useradd '+_username+' -p ' + encPass + ' -d ' + '/home/'+_username +'/'+ ' -m ');
	return os.system('useradd '+_username+' -p ' + encPass + ' -d ' + '/home/'+_username +'/'+ ' -m ');

#createUser('dante', 'dante', '123');