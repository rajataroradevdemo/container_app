Welcome to the Containers World

This is a 3 Tier App which is based on MongoDB, Flex API in Python and Frontend designed using ReactJS

Step By Step Guide for End to End Application Run

Network create
docker network create tutorialapp

Volume Create
docker volume create --name mongodb_data

Setup MongoDB Database Container 

docker run  -e 'MONGO_INITDB_ROOT_USERNAME=admin' \
			-e 'MONGO_INITDB_ROOT_PASSWORD=password' \
			-e 'MONGO_INITDB_DATABASE=tutorialsdb' \
			-e 'MONGODB_DATA_DIR=/data/db' \
			--network tutorialapp \
			-p 27017:27017 \
			-v mongodb_data:/data/db \
			-d mongo:7

Setup API layer

Build Docker image for API, go to backend folder and run

docker build -t api .

Run API Container (Provide Private IP of Docker EC2 Machine)

Step Missing #Run gunicorn server for production mode
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]



docker run -e 'MONGODB_HOST=172.31.23.115' \
		   -e 'MONGODB_USERNAME=admin' \
		   -e 'MONGODB_PASSWORD=password' \
		   -p 5000:5000 --network tutorialapp \
		   -d api


Build and Run FrontEnd Image and Container

docker build -f Dockerfile.dev -t tutorialui .

Run FrontEnd Container (Provide Public IP of EC2 Machine for API)

docker run -d -e REACT_APP_API_URL=13.127.174.232 -p 8081:8081 tutorialui

