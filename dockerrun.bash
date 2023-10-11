df -h /freespace/local
#if /freespace/local has less than 15GB, use another machine
 
# WARNING: we may remove files from /freespace between semesters.
# Because this setup uses /freespace/local, this setup is only
# effective on machine you setup this docker.
# Note: /freespace/local is a local filesystem, therefore
# its content is only available locally.

# make a directory for docker on a local file system
mkdir -p /freespace/local/$USER/docker

# link it to where docker expects it to be
mkdir -p ~/.local/share
ln -s /freespace/local/$USER/docker ~/.local/share
sudo /usr/libexec/addsubusers.py
# if the previous command fails, contact help@cs.rutgers.edu
# the system you're usin isn't properly set up

# create the network config file
mkdir -p ~/.config/docker
cp /etc/docker/daemon.json ~/.config/docker/daemon.json

### up to here should only be done once
### below here has to be done every time you login

# the curl command will print two export commands. do them
export PATH="$HOME/bin:$PATH"
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

# put those two export commands in .bashrc if you are
# going to do this a lot

# you must do the follow command again every time
# you login.
systemctl --user start docker
# verify that docker started with no errors
# systemctl --user status docker
docker pull gcr.io/deepmind-environments/dm_memorytasks:v1.0.1
docker run --rm -p 10000:10000/tcp gcr.io/deepmind-environments/dm_memorytasks:v1.0.1