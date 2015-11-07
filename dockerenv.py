import os
import shutil
import argparse

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='/tmp/dockerenv.log',
                    filemode='w')

logger = logging.getLogger('docker_env')

def build_ipython_script(docker_id, workdir):
    with open('ipython.template', 'r') as ipy:
        IPYTHON_SH = ipy.read()
        return IPYTHON_SH.format(docker_id=docker_id, workdir=workdir)

def build_python_script(docker_id, workdir):
    with open('python.template', 'r') as py:
        PYTHON_SH = py.read()
        return PYTHON_SH.format(docker_id=docker_id, workdir=workdir)

def dockerenv_dir():
    return os.environ['HOME'] + '/.dockerenv'

def make_dockerenv_dir():
    """ create the docker environment directory if it does not exist """
    mkdir(dockerenv_dir())

def mkdir(path):
    """ check if an directory exists and make if it does not """
    if not os.path.exists(path):
        logger.info('Creating %s', path)
        os.makedirs(path)
    else:
        logger.info('Directory %s already exists', path)

def copyfile(src, dest):
    if not os.path.exists(src):
        logger.warn('Cannot find file %s', src)
        return
    if os.path.exists(dest):
        logger.debug('File %s already exists', dest)
        return
    if not os.path.exists(os.path.dirname(dest)):
        logger.info('Creating parent directories for %s', os.path.dirname(dest))
        os.makedirs(os.path.dirname(dest))
    logger.info('Copying to %s', dest)
    shutil.copy2(src, dest)

def make_executable(fn):
    """ taken from virtualenv package """
    oldmode = os.stat(fn).st_mode & 0xFFF # 0o7777
    newmode = (oldmode | 0x16D) & 0xFFF # o555, 0o7777
    os.chmod(fn, newmode)
    logger.info('Changed mode of {} to {}'.format(fn, oct(newmode)))

def make_new_env(name, docker_id, workdir):
    envir_dir = dockerenv_dir() + '/{}'.format(name)
    bin_dir =  envir_dir + '/bin'
    mkdir(envir_dir)
    mkdir(bin_dir)
    with open(bin_dir+'/python', 'wr') as f:
        PYTHON_SH = build_python_script(docker_id, workdir)
        f.write(PYTHON_SH)

    with open(bin_dir+'/ipython', 'wr') as f:
        IPYTHON_SH = build_ipython_script(docker_id, workdir)
        f.write(IPYTHON_SH)

    make_executable(bin_dir+'/python')
    make_executable(bin_dir+'/ipython')

def main():
    parser = argparse.ArgumentParser(description='Setup docker environment')
    parser.add_argument('name',
                        help='Name of docker environemnt')
    parser.add_argument('--id',
                        dest='docker_id',
                        help='Docker id of docker container to use to setup the environemnt')
    parser.add_argument('--workdir',
                        dest='workdir',
                        help='Docker WORKDIR where any additional data directories will be mounted')

    args = parser.parse_args()
    make_dockerenv_dir()

    make_new_env(args.name, args.docker_id, args.workdir)

if __name__ == '__main__':
    main()
