import tarfile
import hashlib
import subprocess
import zlib
import cStringIO
import gzip

def deflate(filename, outfile=None, level=6):
	f = open(filename)
	data = f.read()
	f.close()

	compress = zlib.compressobj(
		level,                # level: 0-9
		zlib.DEFLATED,        # method: must be DEFLATED
		-zlib.MAX_WBITS,      # window size in bits:
		                      #   -15..-8: negate, suppress header
		                      #   8..15: normal
		                      #   16..30: subtract 16, gzip header
		zlib.DEF_MEM_LEVEL,   # mem level: 1..8/9
		0                     # strategy:
		                      #   0 = Z_DEFAULT_STRATEGY
		                      #   1 = Z_FILTERED
		                      #   2 = Z_HUFFMAN_ONLY
		                      #   3 = Z_RLE
		                      #   4 = Z_FIXED
	)
	deflated = compress.compress(data)
	deflated += compress.flush()

	if outfile != None:
		f = open(outfile, 'w')
		f.write(deflated)
		f.close()

	return deflated

# tar = tarfile.open("newgopath.tar.gz", "w:gz")
# tar.add("/home/aaron/newgopath")
# tar.close()


tar_input = "/home/aaron/newgopath"
tar_output = "/home/aaron/test-native-7"

# subprocess.check_call(['tar' '-cf', tar_output, tar_input])
tar = tarfile.open(tar_output, "wr")
tar.add(tar_input)

# We need the sha of the unzipped and zipped tarball.
# So for performance, tar, sha, zip, sha.
sha = 'sha256:' + hashlib.sha256(open(tar_output).read()).hexdigest()

# We use gzip for performance instead of python's zip.
# subprocess.check_call(['gzip', tar_output])
# real    0m51.968s
# user    0m43.040s
# sys     0m1.996s
# with file("output6.tar.gz", 'w+') as outf:
# 	with file(tar_output) as inf:
# 		outf.write(zlib.compress(inf.read()))

gz = cStringIO.StringIO()
with gzip.GzipFile(fileobj=gz, mode='w', compresslevel=1) as f:
	f.write(tar.read())
print gz.getvalue(), sha
tar.close

# deflate(tar_output, "output8.tar.gz", 6)
# real    0m55.894s
# user    0m42.840s
# sys     0m1.924s

# tar = tarfile.open("output7.tar.gz", "w:gz")
# tar.add(tar_output)
# tar.close()
# real    3m35.094s
# user    2m23.264s
# sys     0m2.572s

# aaron@aaron-Z87X-UD3H:~/sip-test$ time python native-test.py

# real    0m45.895s
# user    0m42.768s
# sys     0m1.908s
