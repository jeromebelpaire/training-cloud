
# Training-cloud Docker

Small project running a small webapp with a classification model with Docker, on Azure.

## Setup

The following setup starts from scratch, you might want to skip steps:

1. Install git and checkout the https://github.com/Agilytic/training-cloud.git
2. Install [anaconda]/miniconda python version 3.6+
3. Change working directory the project root directory
4. Create the self contained conda environment. Open anaconda prompt and go to the project root directory and enter the command:

    `conda env create --name training_cloud python=3.6`
5. Activate the environment:

    `activate training_cloud`
5. Install the required packages through:

    `pip install -r requirements.txt`

6. Install Docker Toolbox (The official docker version only runs on Windows Professional)

7. Launch Docker toolbox through the command line:

    `docker-machine start default`

8. Build docker image locally (THe name 'training_cloud' and the version '1.0' can be changed):

    `docker build --tag training_cloud:1.0 .`

9. Test out the docker image locally:

    `docker run -p 80:5555 training_cloud:1.0`
    
    then go to:
    http://localhost:80

8. Install the azure command line

    
9. Create a ressource group, in this example it will be named Jerome, but this can be changed:

    `az group create --name Jerome --location "West Europe"`

10. Create a container (the name 'trainingcloudACR' can be changed) :

    `az acr create --name trainingcloudACR --resource-group Jerome --sku Basic --admin-enabled true`

11. Get azure credentials:

    `az acr credential show --name trainingcloudACR`

    The output reveals two passwords along with the user name, both passwords can be used.

12. Login in azure container registry:

    `docker login trainingcloudACR.azurecr.io --username trainingcloudACR`

13. Tag your local image for the Azure Container Registry:

    `docker tag training_cloud:1.0 trainingcloudACR.azurecr.io/training_cloud:1.0`

14. Push the image to the registry:

    `docker push trainingcloudACR.azurecr.io/training_cloud:1.0`

15. Launch the container:

    `az container create --resource-group Jerome --name training-cloud --image trainingcloudACR.azurecr.io/training_cloud:1.0 --ports 80 --ip-address Public`

    Within a few seconds, you should get a response from the Azure CLI indicating that the deployment has completed.

16. Check the status and the ip-adress with:

    `az container show --resource-group Jerome --name training-cloud --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" --out table`

17. Try out the API through:

    `<ip-adress from previous step>:80`

18. To clean up:

    `az group delete --name Jerome`

## File Structure

```
├── .gitignore               <- Files that should be ignored by git. Add seperate .gitignore files in sub folders if 
│                               needed
├── App                      <- Code for Flask app serving
│
├── README.md                <- The top-level README for developers using this project.│
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
