Docker Virtual Environment
==========================
Run python/ipython in a docker container similar to python's virtualenv  (work in progress).

Installation
------------
To install

1. git clone https://github.com/joshloyal/dockerenv.git
2. add the following lines to your `.bashrc` or `.bash_profile`:
```
export PATH=/path/to/dockerenv/scripts:$PATH
source /path/to/dockerenv/scripts/dockerenvwrapper
```

Usage
-----
This library was designed with the [jupyter/docker-stacks](https://github.com/jupyter/docker-stacks) in mind.
To create a new dockerenv you must specify the docker tag as well as the workdir of the environment:
```
mkdockerenv denv --id jupyter/datascience-notebook --workdir /home/jovyan/work
```
You can then open up the dockerenv similar to virtualenvwrapper
```
workon denv
```
To deactivate the dockerenv simply type `deactivate`. When you run `python` or `ipython` in the docker environment
it will run in a docker container. This will mount your current working directory in container as well. In addition,
you can specificy an additional mount directory with the --data argument:
```
ipython --data /my/data/dir
python --data /my/data/dir
```

Finally you can start the container in daemon mode with `dockerenv-daemon`. This will run the container with port 8888 exposed.
Note that if you are running with docker-machine you will need to use the VMs ip instead of local host. This can be obtained with
`docker-machine ip <name-of-dm>`. The container will be removed when you deactivate the environment. You can also manually kill the
daemon container with the `killdockerenv` command.

To Do
-----
* Expand use beyond the bash shell
* Expose environmental variables to Docker.
