# Remote Server-Controlled Arm
## CS179J Project by Team 5

This project was created by Team 5 in the class of CS179J Spring 2020 at the University of California Riverside 
### What is this project.

This project is a robotic arm that is controlled using computer vision.  
An object detection client running tensorflow sends cartesian (x,y,z) coordinates as well as a string that represents whether the hand is open or closed.  This data is consistently sent and saved on a flask server.
The arm client will then pull the data using the Requests library for Python3 and convert the cartesian coordinates to cylindrical and control motors.

### Future Updates

Currently, there are some components of the project that are only for development purposes.  If this is to be released as an actual product, changes expected to be made are:

* Use HTTPS (encrypted) instead of HTTP for communication
* Use all stepper motors rather than the DC motor being used for up and down movement.
* Use subscription/signaling in the server communication to only send data when it's been updated.

More improvements/changes are discussed in the issues.

## License

This project is licensed under the MIT public license.
