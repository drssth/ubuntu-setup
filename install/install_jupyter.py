import os, os.path
import time
import json

from runcmd import load_content, run_command


service_txt = '''[Unit]
Description=Jupyterhub
After=syslog.target network.target

[Service]
User=root
Environment="PATH=/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin{}"
ExecStart={} -f /etc/jupyterhub/jupyterhub_config.py

[Install]
WantedBy=multi-user.target
'''

    
def install_jupyter():    
    
    try:
        import jupyterhub
        print('jupyterhub', jupyterhub.__version__)

    except:
        print('==> install jupyterhub...')
        
        cmd = 'sudo apt-get update'
        run_command(cmd.split())
        cmd = 'sudo apt-get upgrade -y'
        run_command(cmd.split())
        cmd = 'sudo apt-get autoremove'
        run_command(cmd.split())

        pkgs = 'npm nodejs'.split()
    
        for pkg in pkgs:
            cmd = ['sudo', 'apt-get', 'install', pkg, '-y']
            run_command(cmd)
            
        cmd = 'sudo npm install -g configurable-http-proxy'
        run_command(cmd.split())
    
        cmd = 'sudo pip3 install -U pip'
        run_command(cmd.split())

        pkgs = 'ipykernel jupyter jupyterlab jupyterhub'.split()
        for pkg in pkgs:
            cmd = ['sudo', 'pip3', 'install', '-U', pkg]
            run_command(cmd)

    conf = '/etc/jupyterhub/jupyterhub_config.py'
    if os.path.exists(conf):
        print('juputerhub conf exists')
    else:
        fn = 'jupyterhub_config.py'
        cmd = 'sudo rm '+fn
        run_command(cmd.split())

        cmd = 'jupyterhub --generate-config'
        run_command(cmd.split())
        time.sleep(1)
        
        content = ''
        with open(fn, 'r') as f:
            content = f.read()
        
        content = content.replace("#c.JupyterHub.default_url = ''", "c.Spawner.default_url = '/lab'") 
        os.makedirs(os.path.dirname(conf), exist_ok=True)
        with open(conf, 'w') as f:
            content = f.write(content)
        
        fn = 'jupyterhub_config.py'
        cmd = 'sudo rm '+fn
        run_command(cmd.split())
        
    service = '/etc/systemd/system/jupyterhub.service'
    if os.path.exists(service):
        print('juputerhub service exists')
    else:
        cmd = "which jupyterhub"
        jupyter_path = run_command(cmd.split())
        jupyter_parent = os.path.dirname(jupyter_path)
        service_content = service_txt.format(':'+jupyter_parent, jupyter_path)
        # create service file
        with open(service, 'w') as f:
            f.write(service_content)
            
    cmd = "sudo systemctl daemon-reload"
    run_command(cmd.split())
    cmd = "sudo systemctl start jupyterhub"
    run_command(cmd.split())
    cmd = "sudo systemctl status jupyterhub --no-pager"
    run_command(cmd.split())
    cmd = "sudo systemctl enable jupyterhub"
    run_command(cmd.split())
    
    

                
        
        
    
