import pexpect
import time


def connect():
	print 'trying to connect, press side button'
	tool.sendline('connect')	
	tool.expect('Connection successful')
	print 'connection successful'


	
bluetooth_adr = "00:24:e4:1d:7c:42"
tool = pexpect.spawn('gatttool -b ' + bluetooth_adr + ' --interactive')
if tool.expect('\[LE\]>') == 0: 
	print 'device found'

connect()
d = "Characteristic value/descriptor: "
tool.read_nonblocking(1000)
tool.sendline('char-read-hnd ' + '0x000' + hex(1)[-1])
tool.expect(d)

file = open("pulse_dumps/pulse_"+ time.strftime("%m-%d-%H%M%S", time.localtime()) + ".ang", "w")

for i in range(1, 14):
	if i == 10: continue
	tool.sendline('char-read-hnd ' + '0x000' + hex(i + 1)[-1])
	tool.expect(d)
	file.write(str(i) + ": " + tool.before[:tool.before.find("\n")])
file.close()