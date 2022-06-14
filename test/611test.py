import docker
dockerclient = docker.DockerClient(base_url='unix:///var/run/docker.sock')
for dp in dockerclient.containers.list():
    print(dp)
    print(db.images)
    print(type(dp))
