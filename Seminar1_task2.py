import subprocess

res = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding="utf-8")
if res.returncode == 0:
    result = res.stdout.split("\n")
    if "VERSION_CODENAME=jammy" in result and "VERSION='22.04.1 LTS (Jammy Jellyfish)'" in result:
        print("SUCCESS")
    else:
        print("FAIL")


