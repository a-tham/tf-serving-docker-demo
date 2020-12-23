#### Introduction
This is a demo of setting up and running TF Serving with Docker. 
As I had some trouble at the start of this project, I decided to document and create a 
README file to serve as simple starting instructions for me to follow.
Hopefully this helps beginners starting out and need a simple concise tutorial.  

The model folders are empty placeholders, these are the folders where you should be placing your TF SavedModels into.  
See below Model directory structure diagram for further info.

##### Install Docker
Head to the following link and choose the correct OS installer:  
https://docs.docker.com/desktop/

##### Check Docker version
run: docker -v  
(Docker version 19.03.13, build 4484c46d9d)

##### Build requirements.txt
Populate requirements.txt file with packages needed

##### Build Docker image
1. cd into folder containing Dockerfile  
2. run: docker build . -t {your own image name}

##### Check Docker image
run: docker images   
(Your own image name above should be listed)

##### Run Docker image
- Port 8500 exposed for gRPC
- Port 8501 exposed for the REST API
- 'Models' folder should contain sub-folders containing each SavedModel.pb. This is to aid serving multiple models
- Version numbers for each model strictly needs to be numerical. By default, the server will serve the version with the largest version number.
- A config file (models.config) is used to tell TF Serving on the multiple models configuration.
- --model_config_file_poll_wait_seconds can be used to instruct the server to check for any new config file at --model_config_file path 

The Model directory structure needs to be:
```
/models
│
└───models.config
│
└───model_1
│   └───001
│       │   assets
│       │   variables
│       └── savedmodel.pb
│   
└───model_2
│    └───001
│        │   assets
│        │   variables
│        └── savedmodel.pb
│
...
```


##### Starting Docker container
Current folders to mount:   
models  
test

Current ports exposed:
8501 (TF Serving)
5000 (for server purposes)

docker run -p 8501:8501 -p 5000:5000 --mount type=bind,source={path/to/models},target=/models --mount type=bind,source={path/to/test},target=/test -t {your image name} --model_config_file=/ models/models.config --model_config_file_poll_wait_seconds=300

##### Access terminal in Docker container
local terminal:
docker exec -it {container id}   

Commands can be run off the container's terminal once the above has been run.

##### Installing packages
pip is available.  
Current requirements.txt file is at \test , add to file for more packages  
Will need to run 'pip install -r requirements.txt' each time a container is killed and run again, but this can be incorporated into the Dockerfile when packages are more or less settled on.

 ##### Inference
Indicate which model is to be used for inference when request is sent to TF server by using its model name as specified in the models.config file.

The TF serving call would be something similar to:  
url = 'http://{IP address of server}:8501/v1/models/{}:predict'.format(model_name)'

##### Commonly used Docker commands:
Check running Docker containers: docker ps  
Check available images: docker images  
Kill a running container: docker kill {container id} *use docker ps to find container id, not image name

##### For Windows Users on EC2
Nested virtualization isn't working on AWS EC2's VM AMIs, and one of the often mentioned solution
is to use Metal instances, however, this is a very expensive workaround. 


















