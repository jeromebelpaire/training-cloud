
# Creating a webapp with Azure Container Services


Small project running a small webapp with a classification model with Docker, on Azure.

This project can be used as a base for other Docker/Azure Container Service applications

## Setup

The following setup starts from scratch, you might want to skip steps:

1. Install git and checkout the https://github.com/Agilytic/training-cloud.git

### Install Python (Optional*)
\* Everything will run in Docker, so it is not strictly needed, but if you want to test things outside docker it can be useful.

2. Install [anaconda]/[miniconda] python version 3.6+
3. Change working directory the project root directory
4. Create the self contained conda environment. Open anaconda prompt and go to the project root directory and enter the command:

    `conda create --name training_cloud python=3.6`
5. Activate the environment:

    `activate training_cloud`
6. Install the required packages through:

    `pip install -r requirements.txt`

### Construct docker image locally

7. Install [Docker Toolbox] (The official docker version only runs on Windows Professional)

8. Launch Docker toolbox through the command line:

    `docker-machine start default`

9. Build docker image locally (The name 'training_cloud' and the version '1.0' can be changed):

    `docker build --tag training_cloud:1.0 .`

10. Test out the docker image locally:

    launch container: `docker run -p 5555:80 training_cloud:1.0`
    
    get docker toolbox ip by typing: `docker-machine ls`

    then go to: `<dockertoolbox ip>:5555`

    get list of running docker containters: `docker ps`

    stop the container by: `docker stop <container id>` 

### Setup Azure

11. Install the [azure command line]

    
12. Create a ressource group, in this example it will be named MyRessourceGroup, but this can be changed:

    `az group create --name MyRessourceGroup --location "West Europe"`

### Publish on Azure Container Registries

13. Create a container (the name 'trainingcloudACR' can be changed) :

    `az acr create --name trainingcloudACR --resource-group MyRessourceGroup --sku Basic --admin-enabled true`

14. Get azure credentials:

    `az acr credential show --name trainingcloudACR`

    The output reveals two passwords along with the user name, both passwords can be used.

15. Login in azure container registry (docker needs to be running for this):

    `docker login trainingcloudACR.azurecr.io --username trainingcloudACR`

16. Tag your local image for the Azure Container Registry:

    `docker tag training_cloud:1.0 trainingcloudACR.azurecr.io/training_cloud:1.0`

17. Push the image to the registry:

    `docker push trainingcloudACR.azurecr.io/training_cloud:1.0`

### Launch on Azure Container Instances

18. Launch the container, change the DNS if you want:

    `az container create --resource-group MyRessourceGroup --name training-cloud --image trainingcloudACR.azurecr.io/training_cloud:1.0 --ports 80 --ip-address Public --dns-name-label my-training-cloud-site`

    This will ask you the username and password from step 14.

    Within a few seconds, you should get a response from the Azure CLI indicating that the deployment has completed.

19. Check the status, dns and the ip-adress with:

    `az container show --resource-group MyRessourceGroup --name training-cloud --query "{FQDN:ipAddress.fqdn, IP:ipAddress.ip,ProvisioningState:provisioningState}" --out table`

20. Try out the API through:

    http://my-training-cloud-site.westeurope.azurecontainer.io/

### Clean up

21. To clean up:

    `az group delete --name MyRessourceGroup`

22. Stop docker-machine

    `docker-machine stop default`

## Pro's and con's of Docker and Azure Container Services

### Pro's
- With a Dockerfile compatibility issues are almost none!
- You can easily redeploy on azure with more or less computing power to meet your demand
- You can easily deploy multiple containers if your task can be fragmented into smaller pieces
- No need to manage servers

### Con's
- Docker takes a bit of technical setup to get started
- Docker does not take away all security concerns
- Persistent storage on Docker is not not straightforward
- Azure Container Services does not apply autoscaling by default

## File Structure

```
├── .gitignore               <- Files that should be ignored by git. Add seperate .gitignore files in sub folders if 
│                               needed
├── App                      <- Code for Flask app serving
│
├── README.md                <- The top-level README for developers using this project.
│
├── Data                     <- Data files for the project
│
├── Documentation            <- Documentation
│
├── Models                   <- Trained models
│
├── Scripts                  <- All scripts
│
├── Utils                    <- Reusable pyhton code
│
├── Dockerfile               <- Blueprint for the docker image
│
└── requirements.txt         <- Essential packages for the project
```

## Contacts
* Author: Jerome Belpaire
* Agilytic team: Jerome Belpaire
* Client: Agilytic

## References
* https://docs.microsoft.com/en-us/azure/app-service/containers/tutorial-custom-docker-image
* https://docs.microsoft.com/en-us/azure/container-instances/container-instances-quickstart

[//]: #
   [anaconda]: <https://www.continuum.io/downloads>
   [miniconda]: <https://docs.conda.io/en/latest/miniconda.html>
   [Docker Toolbox]: <https://docs.docker.com/toolbox/toolbox_install_windows/>
   [azure command line]: <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest>