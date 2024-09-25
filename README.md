# Password Manager
This project is a relatively simple command line password manager. Websites, usernames, and their associated passwords are stored within a SQL database. These entries can be access, edited, or removed all through the command line and their respective arguments. Before any of that can be done, the master password and key for decryption must be provided to ensure the user is supposed to have access. For each entry in the database there can only be one username and password combination per URL. This allows for an easier time removing, updating, and verifying entries. If there are multiple entries in the database with the same URL, any updates/removals will be applied to both of them. Perhaps in a future version there will be implementation for multiple accounts on one URL. Each password is randomly generated then encrypted and only then is it added to the database. The encrypted passwords are only decrypted when queried through this password manager. Below are more details on certain aspects of the project I may want to revisit.

### Password Encryption
Passwords are created using a random sequence of 20 characters, numbers, and special characters. The function that creates the random sequence insures there are at least 3 digits, 1 lowercase, and 1 uppercase letter in each generated password. This password is then encrypted using the master key (stored in *super_secret.py*) and then inputted into the database. The database contains no non-encrypted passwords which means the only way to access the raw passwords is through this password manager. When a entry is queried, the encrypted password is decrypted and then printed to the terminal. Both the encryption and decryption process uses the *Fernet* class from the cryptography package. The encrypted passwords stored in the database are actually fernet tokens which can only be decrypted using the master key.

#### Vulnerabilities
A primary vulnerability from this project is that the master key is stored in raw text in the *super_secret.py* file. If a attacker were to gain access to this file then all of the passwords could be decrypted with ease. A similar vulnerability comes from the fact that the master key must be pasted to the terminal in order to gain access to the password manager. This acts as another layer of protection encase your password is stolen however that is another instance where the master key can be leaked. The master password and salt are also stored in the *super_secret.py* file which makes that file the Achilles heel of security. Since this is for practice the file will be included in the repo but IT SHOULD NEVER ACTUALLY BE ADDED. I am unsure if there is a better way to store these key values which should be looked into in the next project.

### docker-compose.yaml file
Docker Compose is a tool for defining and running multi-container applications. The docker-compose.yaml file is the configuration file for the infrastructure of this project. Since the config file contains the username and password for the database, it shouldn't be included in project repositories. However, this project is just for practice in SQL, docker, and development in general the password is *password01* and the username is default so I will be leaving the file for future reference. The same goes for the database.ini file which contains the same info for connecting to the database. The two packages being used for this project are the PostgreSQL package for database usage and the Adminer package which provides a web UI for manipulating the database. The docker compose documentation can be found at this URL: https://docs.docker.com/compose/.

#### PostgreSQL
This password manager uses the open source relational database system called PostgreSQL. This system is great for this project as it is free and open source however it does require some setup on the host computer or through a docker container for the database to function. The system has primarily SQL support/usage for the bulk of the database interaction with client interfaces in C and python for ease of implementation. The C client interface is called *libpq* and the python is a wrapper for *libpq* called *psycopg2*. The documentation can be found at this URL: https://www.postgresql.org/docs/.

#### Adminer
Adminer is a docker package for database management written in PHP, consisting of a single file for easy deployment to the target server. It provides a web UI for interacting and manipulating the PostgreSQL database along with other SQL databases like MySQL, MongoDB, etc. It allows for easy table and value manipulation with the UI and has capabilities to execute individual SQL commands through the interface. The documentation can be found at this URL: https://www.adminer.org/.

### Useful Commands from this Project
* newgrp docker
  - Ensures the docker group is running properly and will not require sudo to run
* docker ps -a
  - Lists all containers, including non-running ones
* docker rm *container_id*
  - Removes a docker container at the given container id
  - *docker rm -fv $(docker ps -aq)* will remove all containers
* docker start *container_id*
  - Starts a docker container with the given id
* docker run -d --name *DB_Name* -p 5432:5432 -e POSTGRES_PASSWORD=*yourpassword* postgres
    - Starts a new PostgreSQL docker container in CL
    - Found that using the compose file causes less problems
* docker exec -it *DB_Name* psql -U postgres   
  - Connect to the psql interface of the PostgreSQL docker container
* sudo lsof -i -P -n | grep *port_number*
  - List what program is using a certain port number
  - Follow up with *sudo kill "process_id"* to clear up the port
