import commands
import os


def ssh_exec(cmd, *hosts):
    for host in hosts:
        remote_cmd = "ssh {host} {cmd}".format(host=host, cmd=cmd)
        print("run command {cmd} on {host}".format(host=host, cmd=cmd))
        (status, output) = commands.getstatusoutput(remote_cmd)
        if status != 0:
            raise Exception("run command error")
        print(output)


def ssh_copy(src, dest, *hosts):
    if os.path.isdir(src):
        prefix = "scp -r "
    else:
        prefix = "scp "
    for host in hosts:
        remote_cmd = prefix + "{src} {host}:{dest}".format(src=src, host=host, dest=dest)
        print(remote_cmd)
        (status, output) = commands.getstatusoutput(remote_cmd)
        if status != 0:
            raise Exception("run command error")
        print(output)


if __name__ == '__main__':
    ssh_copy("docker_util.py", "/tmp", "localhost")
