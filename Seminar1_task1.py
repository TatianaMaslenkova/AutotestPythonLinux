import subprocess

res = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
if "jammy" in res.stdout and "22.04" in res.stdout and res.returncode == 0:
    print("SUCCESS")
else:
    print("FAIL")
