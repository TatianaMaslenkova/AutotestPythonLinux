import subprocess

result = subprocess.run("ls /etc", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
print(result.stdout)
print(result.returncode)
