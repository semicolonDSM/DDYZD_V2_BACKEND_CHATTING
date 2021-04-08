echo "docker down"
sudo docker stop flask_chatting

echo "remove docker container"
sudo docker rm flask_chatting

echo "remove docker image"
sudo docker rmi flask_chatting

echo "restart flask_chatting"
cd /home/semicolon/DDYZD
sudo docker-compose up -d --build flask_chatting
