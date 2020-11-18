import os, os.path
import json
import getpass
from runcmd import load_content, run_command


def setup_docker():
    run_command('sudo apt-get update'.split())
    
    pkgs = '''install
        apt-transport-https
        ca-certificates
        curl
        gnupg-agent
        software-properties-common'''.split()

    for pkg in pkgs:
        cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
        run_command(cmd)
        
    cmds = [
        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -',
        'sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) \
          stable"',
        'sudo apt-get update',
        'sudo apt-get install docker.io -y',
        ]
    for cmd in cmds:
        run_command(cmd.split())
        
    cmd = 'sudo service docker start'
    run_command(cmd.split())
        
    homedir = os.path.expanduser("~")
    username = os.path.basename(homedir)
    cmd = 'sudo usermod -aG docker '+ username
    run_command(cmd.split())

    dockersetting = {}
    if os.path.exists('docker.json'):
        with open('docker.json', 'r') as f:
            dockersetting = json.load(f)

    if os.path.exists('/etc/docker/daemon.json'):
        cmd = 'sudo cp /etc/docker/daemon.json /etc/docker/daemon-bk.json'
        run_command(cmd.split())
            
        deamon = {}
        with open('/etc/docker/daemon.json', 'r') as f:
            deamon = json.load(f)
        
        for k in dockersetting:
            if k not in deamon:
                deamon[k] = dockersetting[k]
            
        if 'data-root' in deamon:
            dataroot = deamon['data-root']
            if username not in dataroot:
                deamon['data-root'] = '/home/{}/docker/data'.format(username)
                dataroot = deamon['data-root']
            print('docker data root = {}'.format(dataroot))
            if not os.path.exists(dataroot):
                os.makedirs(dataroot)

        with open('/etc/docker/daemon.json', 'w') as f:
            json.dump(deamon, f, sort_keys=True, indent=4)
        
        cmd = 'sudo service docker restart'
        run_command(cmd.split())
    
    
    pkgs = 'python3-pip libffi-dev python3-openssl'.split()

    for pkg in pkgs:
        cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
        run_command(cmd)

    pkgs = 'docker-compose'.split()
    for pkg in pkgs:
        cmd = ['sudo', 'pip3', 'install', '-U', pkg]
        run_command(cmd)
    
    
    
def setup_apache():
    cmd = 'sudo systemctl start apache2.service'
    run_command(cmd.split())
    cmd = 'sudo systemctl restart apache2.service'
    run_command(cmd.split())
    
    os.makedirs('/var/www/html/test', exist_ok=True)
    
    cmd = 'sudo chmod 777 -R /var/www/html'
    run_command(cmd.split())
    
    with open('/var/www/html/test.html', 'w') as f:
        f.write('Hello! Welcome to apache2! it works. ;)\n\n')

    with open('/var/www/html/test/test.html', 'w') as f:
        f.write('Hello! Welcome to apache2! it works. ;)\n\n')
    
    
    
    
def install_base():
    pkgs = load_content('apt.txt')
    
    cmd = 'sudo apt-get update'
    run_command(cmd.split())
    cmd = 'sudo apt-get upgrade -y'
    run_command(cmd.split())
    cmd = 'sudo apt-get autoremove'
    run_command(cmd.split())
    
    for pkg in pkgs:
        cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
        run_command(cmd)
    
    homedir = os.path.expanduser("~")
    username = os.path.basename(homedir)
    
    cmd = 'sudo chmod 777 -R /home/{}/.cache'.format(username)
    run_command(cmd.split())
        
    


    
