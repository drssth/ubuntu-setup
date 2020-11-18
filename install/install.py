import os, os.path, sys
import argparse

from runcmd import load_content

import install_base
import install_jupyter
import install_app

def main():
    settings = load_content('settings.txt')
    
    if 'base' in settings:
        install_base.install_base()
    
    if 'apache' in settings:
        install_base.setup_apache()
        
    if 'docker' in settings:
        install_base.setup_docker()
        
    if 'jupyter' in settings:
        install_jupyter.install_jupyter()
        
    if 'redis' in settings:
        install_app.install_redis()
        
    if 'pypis' in settings or 'requirements' in settings:
        install_app.install_pypi_pkgs()
        
    if 'vscode' in settings:
        install_app.install_vscode()

    if 'pyenv' in settings:
        install_app.install_pyenv()
    
        
        
if __name__ == '__main__':
    main()
        