import tarfile
import hashlib
import subprocess

# tar = tarfile.open("newgopath.tar.gz", "w:gz")
# tar.add("/home/aaron/newgopath")
# tar.close()


tar_input = "/home/aaron/newgopath"
tar_output = "/home/aaron/test-subproc-4"

subprocess.check_call(['tar', '-cf', tar_output, tar_input])

# We need the sha of the unzipped and zipped tarball.
# So for performance, tar, sha, zip, sha.
sha = 'sha256:' + hashlib.sha256(open(tar_output).read()).hexdigest()

# We use gzip for performance instead of python's zip.
subprocess.check_call(['gzip', tar_output])

# aaron@aaron-Z87X-UD3H:~/sip-test$ time python subproc-test.py
# tar: Removing leading `/' from member names

# real    1m19.565s
# user    0m41.496s
# sys     0m1.716s
