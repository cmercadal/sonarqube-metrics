# Running Python App and Sonarqube in docker containers: 

This python app will connect to your Sonarqube instance and retrieve metrics on different projects. Output is an excel file

## 1. Create a Network to connect both python app and Sonarqube instance

```sh
docker network create sq-pyapp-network
```

## 2. Run your sonarqube instance
```sh
docker run -d --name sonarqube --network sq-pyapp-network -p 9000:9000 sonarqube:lts
```

Now you'll have your Sonarqube instance running. You can mount a volume or send apps build information to this instance.

## 3. Build and run python app

```sh
docker build -t py-app-image .
docker run -d --name python_app --network sq-pyapp-network -e SONAR_URL="http://localhost:9000" -e SONAR_TOKEN="<
your_sonar_token>" py-app-image
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

### Other useful commands

#Base64
```sh
echo -n “some-string” | base64
```
```sh
echo -n “some-string” | base64 --decode
```

## Kubernetes manifest

Repository also have kubernetes manifest files to deploy a postgres database, the sonarqube instance and the application. I run it with minikube and port forwarding (docker desktop and mac)

```sh
kubectl port-forward svc/sonarqube-svc 9000:9000
```