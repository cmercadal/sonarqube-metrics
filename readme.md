# Running Python App and Sonarqube in docker containers: w

## 1. Create a Network to connect both

```sh
docker network create sq-pyapp-network
```

## 2. Run your sonarqube instance
```sh
docker run -d --name sonarqube --network sq-pyapp-network -p 9000:9000 sonarqube:lts
```

Now you'll have your Sonarqube instance running. You can mount a volume or send apps buildinformation to this instance.

## 3. Build and run python app

```sh
docker build -t py-app-image .
docker run -d --name python_app --network sq-pyapp-network -e SONAR_URL="http://localhost:9000" -e SONAR_TOKEN="squ_b790b77538172fce1d53b6e2d093af8293aa3851" py-app-image
```

## 4. Check the logs

The container will run and exit, but you can check info retrieved in logs:

```sh
docker logs python_app
```

## 5. Store data

If you haven't mounted a volume, you can copy the output file to your local:

```sh
docker cp python_app:/app/output.xlsx .
```