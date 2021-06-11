
(localy) scp backend/.env varveler@161.35.179.4:~/realedge/backend

(localy) scp devops/docker/db/.env varveler@161.35.179.4:~/realedge/devops/docker/db

(localy) scp devops/docker/rabbit/.env varveler@161.35.179.4:~/realedge/devops/docker/rabbit

#(localy) scp devops/docker/backups/.env varveler@161.35.179.4:~/realedge/devops/docker/backups

#(localy) scp devops/docker/backups/pgenv.sh varveler@161.35.179.4:~/realedge/devops/docker/backups

mkdir ~/realedge/devops/docker/rabbit




docker-compose -f docker-compose.yml -f production.yml up -d
sudo curl -L https://github.com/docker/compose/releases/download/1.28.6/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
ls -la /usr/local/bin/docker-compose
