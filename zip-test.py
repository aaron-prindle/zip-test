import zlib
import time
import subprocess

with file('testing.in', 'w+') as f:
	test = 'hello how are you today?' * 10000000
	f.write(test)

# First, let's zlib
start = -time.time()
with file('testing.in.Z', 'w+') as outf:
	with file('testing.in') as inf:
		outf.write(zlib.compress(inf.read()))

start += time.time()
print 'zlib: %fs' % start

# Now the subprocess
start = -time.time()
r = subprocess.check_call(['gzip', '-f', 'testing.in'])
start += time.time()
print 'gzip: %fs' % start
