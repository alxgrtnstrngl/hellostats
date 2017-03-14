# README #
author: Alex G.S.

email: alxgrtnstrngl@gmail.com

### Hello API ###

Hellostats is a simple service that repeats "Hello NAME" when asked, gives the counts of what names it's been asked and can even report the loadavg of the server it's running on as a sign of that's server relative health.

* http://hostname/hello?name=<name>
  * this prints the name "Hello NAME"
  * it also submits the name to a local sqlite db for records
* http://hostname/counts
  * gives the counts of the names submitted in a simple list
* http://hostname/loadavg
  * reports the loadavg as a simplistic example of health reporting
* http://hostname/nodestats
  * reports the loadavg for nodes in the cluster and the overall average
  * each node is listed in the 'hosts.list' file by it's public ip-address

### Deployment ###

Deployment is done via an Ansible playbook.  This is organized into roles 'common', 'nginx' and 'hello'.  The 'common' role installs basic dependencies like python-devel.  The next two 'nginx' and 'hello' deploy the web server and the UWSGI based Hello app.

1. Add the hosts you would like to deploy to in the 'hosts' file, please use full public DNS hostnames.
2. Make sure your local SSH config is set to use the AWS EC2 pem file as the private key for these hosts.
3. Run the command listed below and everything should kick off promptly.
4. If there's a problem please contact the author directly.

```
#!shell
cd $GIT_REPO_DIR
ansible -v -i hosts site.yml

```

### Updating Code ###

To update the code and trigger a full Nginx and UWSGI reload please run the following.

```
#!shell
cd $GIT_REPO_DIR
ansible -v -i hosts reload.yml

```

### TODO ###

* Cluster Hello instances together so they know each other dynamically.
* Improve health reporting so it's more realistic and detailed.
* Report cluster health and provide overall stats.
