import os, os.path, json

from runcmd import load_content, run_command


    
def install_vscode():    

    fn = 'code_1.50.1-1602600906_amd64.deb'
    if os.path.exists(fn):
        print('vscode installed')
    else:
        # install
        pkgs = 'wget'.split()
        for pkg in pkgs:
            cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
            run_command(cmd)

        cmd = 'wget https://az764295.vo.msecnd.net/stable/d2e414d9e4239a252d1ab117bd7067f125afd80a/code_1.50.1-1602600906_amd64.deb'
        run_command(cmd.split())
    cmd = 'sudo dpkg -i ' + fn
    run_command(cmd.split())
    cmd = 'rm ' + fn
    run_command(cmd.split())
    
    
    
def install_redis():    
    pkgs = 'redis-server openssl'.split()
    for pkg in pkgs:
        cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
        run_command(cmd)

    cmd = 'sudo systemctl enable redis-server.service'
    run_command(cmd.split())
    cmd = 'sudo systemctl restart redis-server.service'
    run_command(cmd.split())
    
    pkgs = 'redis'.split()
    for pkg in pkgs:
        cmd = ['sudo', 'pip3', 'install', '-U', pkg]
        run_command(cmd)

        

def install_pypi_pkgs():
    
    pkgs = load_content('requirements.txt')
    
    for pkg in pkgs:
        cmd = ['sudo', 'pip3', 'install', '-U', pkg]
        run_command(cmd)


def install_pyenv():
    cmd = 'curl https://pyenv.run | bash'
    run_command(cmd.split())
    
    home = os.path.expanduser('~')
    bashrc = os.path.join(home, '.bashrc')
    if os.path.exists(bashrc):
        with open(bashrc, 'a+') as f:
            f.write('\n\n')
            f.write('export PATH="$HOME/.pyenv/bin:$PATH"')
            f.write('\n')
            f.write('eval "$(pyenv init -)"')
            f.write('\n')
            f.write('eval "$(pyenv virtualenv-init -)"')
            f.write('\n')
    