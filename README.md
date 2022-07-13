# README for homelessness_uk repo

Analysis of UK Homelessness 

Part of my personal "Ignorance reduction" series. This series is about understanding the issues that are so commonly spoken about in the media, but rarely I take the effort to look through the raw data. Ideally, if the media or politicians say something is "really bad" I want to know, how bad in reality, are the underselling it or is the issue less priority than other issues and theyre using it as a stunt for publicity.

Goal: to understand the extent of homelessness in the uk. How widespread, any specific regions, potential influencing factors.






# README for Base Python Docker  

Builds ubuntu docker container, installing pip requirements for python and running jupyter notebook in your local browser.

Maps this repo folder into Docker so you can create and save notebooks and then git push outside of docker afterwards.

# Setup:

### Build and start container  
`bash go.sh`

### Stop container 
`bash stop.sh`  
(OR: `docker stop base_python`)
note: each time you run `bash go.sh`, it will stop the container that is currently running, so be careful if you havent saved changes in notebooks.

### Remove all stopped containers
`docker container rm $(docker ps -aq)`

## Optional:requirements.txt
You can change the packages in requirements.txt
After you run the container, it's recommended to do a pip freeze on the package versions, so this build will hold for future. Python version should be included too ideally.


## Version details
- python3.10 currently in ubuntu 22.04)  
- Works on Apple Silicon.  
- Updated June2022

## Author
George Goldberg
