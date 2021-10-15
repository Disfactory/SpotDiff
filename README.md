# SpotDiff

<div align="center">
  <img src="https://user-images.githubusercontent.com/4230968/136314041-d069957b-c42e-474f-8cef-f1ce541f44a8.png" width="400" />
</div><br>

English description:
- The SpotDiff project invites citizens to identify illegal industrial factories on the locations that are supposed to be used as farmland by comparing satellite images before and after May 20th, 2016.

繁體中文介紹：
- SpotDiff專案希望能讓鄉民比對 2016.5.20 前後衛星雲圖，去抓出農委會五萬筆資料中的疑似工廠位址上的建物是不是新增建物，可以集中火力去檢舉或是可以把台灣疑似工廠的地點掃一遍。

### Table of Content
- [Coding standards](#coding-standards)
- [Install PostgreSQL (administrator only)](#install-postgresql)
- [Setup back-end (administrator only)](#setup-back-end)
- [Setup development environment](#setup-dev-env)
- [Manipulate database](#manipulate-database)
- [Test cases](#test-cases)
- [Deploy back-end using uwsgi (administrator only)](#deploy-back-end-using-uwsgi)
- [API calls](#api-calls)

# <a name="coding-standards"></a>Coding standards
When contributing code for this repository, please follow the guidelines below:
### Language
- The primary language for this repository is set to English. Please use English when writing comments and docstrings in the code. The code should not contain languages that are other than English.
- The secondary language for this repository is set to Mandarin Chinese. It is OK to use Mandarin Chinese in git issues, pull requests, wiki pages, commit messages, and README files. However, English is encouraged.
### Git workflow
- Follow the [Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). The master branch preserves the development history with no broken code. When working on a system feature, create a separate feature branch.
- Always create a pull request before merging the feature branch into the main branch. Doing so helps keep track of the project history and manage git issues.
- NEVER perform git rebasing on public branches, which means that you should not run "git rebase [FEATURE-BRANCH]" while you are on a public branch (e.g., the main branch). Doing so will badly confuse other developers since rebasing rewrites the git history, and other people's works may be based on the public branch. Check [this tutorial](https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing) for details.
- NEVER push credentials to the repository, for example, database passwords or private keys for signing digital signatures (e.g., the user tokens).
- Request a code review when you are not sure if the feature branch can be safely merged into the main branch.
### Python package installation
- Make sure you are in the correct conda environment before installing packages. Otherwise, the packages will be installed to the server's general python environment, which can be problematic.
- Make sure the packages are in the [install_packages.sh](/back-end/install_packages.sh) script with version numbers, which makes it easy for others to install packages.
- Use the pip command first. Only use the conda command to install packages when the pip command does not work.
### Coding style
- Use the functional programming style (check [this Python document](https://docs.python.org/3/howto/functional.html) for the concept). It means that each function is self-contained and does NOT depend on a state that may change outside the function (e.g., global variables). Avoid using the object-oriented programming style unless necessary. In this way, we can accelerate the development progress while maintaining code reusability.
- Minimize the usage of global variables, unless necessary, such as system configuration variables. For each function, avoid modifying its input parameters. In this way, each function can be independent, which is good for debugging code and assigning coding tasks to a specific collaborator.
- Use a consistent coding style.
  - For Python, follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/), for example, putting two blank lines between functions, using the lower_snake_case naming convention for variable and function names. Please use double quote (not single quote) for strings.
  - For JavaScript, follow the [Idiomatic JavaScript style guide](https://github.com/rwaldron/idiomatic.js), for example, using lowerCamelCase naming convention for variable and function names. Please use double quote (not single quote) for strings.
- Document functions and script files using docstrings.
  - For Python, follow the [numpydoc style guide](https://numpydoc.readthedocs.io/en/latest/format.html). Here is an [example](https://numpydoc.readthedocs.io/en/latest/example.html#example). More detailed numpydoc style can be found on [LSST's docstrings guide](https://developer.lsst.io/python/numpydoc.html).
  - For JavaScript, follow the [JSDoc style guide](https://jsdoc.app/index.html)
- For naming files, never use white spaces.
  - For Python script files (and shell script files), use the lower_snake_case naming convention. Avoid using uppercase.
  - For JavaScript files, use the lower_snake_case naming convention. Avoid using uppercases.
- Always comment the code, which helps others read the code and reduce our pain in the future when debugging or adding new features.
- Write testing cases to make sure that functions work as expected.

# <a name="install-postgresql"></a>Install PostgreSQL (administrator only)
WARNING: this section is only for system administrators, not developers.

Install and start postgresql database (we will use version 13). This assumes that Ubuntu 18.04 LTS or Ubuntu 20.04 LTS is installed.
```sh
# For Ubuntu

# Get the signing key and import it
wget https://www.postgresql.org/media/keys/ACCC4CF8.asc
sudo apt-key add ACCC4CF8.asc

# Add the repository
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Fetch the metadata from the new repo
sudo apt-get update

# Install PostgreSQL 13
sudo apt-get install -y postgresql-13

# Start the service
sudo systemctl start postgresql

# Check postgresql status
sudo systemctl status postgresql

# Check postgresql log
sudo tail -100 /var/log/postgresql/postgresql-13-main.log
```
For Mac OS, I recommend installing postgresql by using [Homebrew](https://brew.sh/).
```sh
# For Mac OS

# Install PostgreSQL 13
brew install postgresql@13

# Start the service
brew services start postgresql
```
Enter the postgres shell.
```sh
# For Ubuntu
sudo -u postgres psql postgres

# For Mac OS
psql postgres
```
In the psql shell, create a project user, create a database for the user with a password, and check if the user and database exist. Replace the [DATABASE_PASSWORD] with the project's database password. IMPORTANT: do not forget the semicolon and the end of the commands.
```sh
# Set the password encryption method
SET password_encryption = 'scram-sha-256';
# Give the project user with a password
CREATE USER spotdiff PASSWORD '[DATABASE_PASSWORD]';

# Create databases for the project user
# For the staging server
CREATE DATABASE spotdiff_staging OWNER spotdiff;
# For the production server
CREATE DATABASE spotdiff_production OWNER spotdiff;
# For the test cases
CREATE DATABASE spotdiff_testing OWNER spotdiff;

# Check the list of user roles
SELECT rolname FROM pg_authid;

# Check the list of encrypted user passwords
SELECT rolpassword FROM pg_authid;

# Check if the user role exists
\du

# Check if the database exists
\l

# Exist the shell
\q
```
Edit the "pg_hba.conf" file to set the authentication methods to the ones that require encrypted passwords. This step is used to increase the security of the database on the Ubuntu server. You can skip this step if you are using Mac OS for development.
```sh
# For Ubuntu
sudo vim /etc/postgresql/13/main/pg_hba.conf
# Scroll to the end and relace all "peer" with "scram-sha-256", except those for the local connections
# Below are examples
local   all             postgres                                peer
local   all             all                                     peer
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256

# For Mac OS
vim /usr/local/var/postgres/pg_hba.conf
# Scroll to the end and relace all "trust" with "scram-sha-256", except those for the local connections
# Below are examples
local   all             all                                     trust
host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             ::1/128                 scram-sha-256
local   replication     all                                     trust
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```
If you want to delete a user or a database, enter the postgres shell and use the following:
```sh
# Delete the staging server database
DROP DATABASE spotdiff_staging;

# Delete the project user
DROP USER spotdiff;
```

# <a name="setup-back-end"></a>Setup back-end (administrator only)
WARNING: this section is only for system administrators, not developers.

Install conda for all users. This assumes that Ubuntu is installed. A detailed documentation is [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). First visit [here](https://conda.io/miniconda.html) to obtain the downloading path. The following script install conda for all users:
```sh
# For Ubuntu
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh
sudo sh Miniconda3-py38_4.9.2-Linux-x86_64.sh -b -p /opt/miniconda3
echo '' | sudo tee -a /etc/bash.bashrc
echo '# For miniconda3' | sudo tee -a /etc/bash.bashrc
echo 'export PATH="/opt/miniconda3/bin:$PATH"' | sudo tee -a /etc/bash.bashrc
echo '. /opt/miniconda3/etc/profile.d/conda.sh' | sudo tee -a /etc/bash.bashrc
source /etc/bash.bashrc
```
For Mac OS, I recommend installing conda by using [Homebrew](https://brew.sh/).
```sh
# For Mac OS
brew install --cask miniconda
echo 'export PATH="/usr/local/Caskroom/miniconda/base/bin:$PATH"' >> ~/.bash_profile
echo '. /usr/local/Caskroom/miniconda/base/etc/profile.d/conda.sh' >> ~/.bash_profile
source ~/.bash_profile
```
Clone this repository
```sh
git clone [PROJECT_REPOSITORY_URL] spotdiff
```
Set the permission of the folder (for Ubuntu server setup only, not Mac OS).
```sh
# Add a development group for the project
sudo addgroup spotdiff-dev

# Add yourself and collaborators to the group
sudo usermod -a -G spotdiff-dev $USER
sudo usermod -a -G spotdiff-dev [USER_NAME]

# Check the groups of a user
groups [USER_NAME]

# Check the group list
cat /etc/group

# Set permissions
sudo chown -R root spotdiff/
sudo chmod -R 775 spotdiff/
sudo chgrp -R spotdiff-dev spotdiff/
```
Create three text files to store the database urls in the "back-end/secret/" directory for the staging, production, and testing environments. For the url format, refer to [the flask-sqlalchemy documentation](http://flask-sqlalchemy.pocoo.org/2.3/config/#connection-uri-format). Replace [DATABASE_PASSWORD] with the database password. IMPORTANT: never push the database urls to the repository.
```sh
cd spotdiff/back-end/
mkdir secret
cd secret/
echo "postgresql://spotdiff:[DATABASE_PASSWORD]@localhost/spotdiff_staging" > db_url_staging
echo "postgresql://spotdiff:[DATABASE_PASSWORD]@localhost/spotdiff_production" > db_url_production
echo "postgresql://spotdiff:[DATABASE_PASSWORD]@localhost/spotdiff_testing" > db_url_testing
```
Create a private key for the server to encode the JSON Web Tokens for user login:
```sh
cd spotdiff/back-end/www/
python gen_key.py ../secret/private_key confirm
```

# <a name="setup-dev-env"></a>Setup development environment
Create conda environment and install packages. It is important to install pip first inside the newly created conda environment.
```sh
conda create -n spotdiff
conda activate spotdiff
conda install python=3.8
conda install pip
which pip # make sure this is the pip inside the conda environment
sh spotdiff/back-end/install_packages.sh
```
If the environment already exists and you want to remove it before installing packages, use the following:
```sh
conda deactivate
conda env remove -n spotdiff
```
Run the following to upgrade the database to the latest migration.
```sh
cd spotdiff/back-end/www/

# Upgrade the database to the latest migration
sh db.sh upgrade
```
If this is the first time that you set up the database, run the following to initialize the database migration. IMPORTANT: do NOT perform this step if the database migration folder exists on the repository. 
```sh
# Generate the migration directory
# IMPORTANT: do not perform this step if the database migration folder exists 
sh db.sh init

# Generate the migration script
# IMPORTANT: do not perform this step if the database migration folder exists 
sh db.sh migrate "initial migration"
```
Run server in the conda environment for development purpose.
```sh
sh development.sh
```
You can test the application using [http://localhost:5000/](http://localhost:5000/) or the following curl command.
```sh
curl localhost:5000
```

# <a name="manipulate-database"></a>Manipulate database
We use [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) to manage database migrations. The script "db.sh" enhances the workflow by adding the FLASK_APP environment. If you edit the database model and want to perform database migration, run the following:
```sh
cd spotdiff/back-end/www/

# Generate the migration script
sh db.sh migrate "[YOUR_MIGRATION_COMMIT_MESSAGE]"
```
Then, a new migration script will be generated under the "back-end/www/migrations/versions" folder. Make sure that you open the file and check if the code make sense. After that, run the following to upgrade the database to the latest migration:
```sh
# Upgrade the database to the latest migration
sh db.sh upgrade
```
If you want to downgrade the database to a previous state, run the following.
```sh
# Downgrade the database to the previous migration
sh db.sh downgrade
```

# <a name="test-cases"></a>Test cases
For the back-end, the test cases are stored in the "back-end/www/tests" folder and written using [Flask-Testing](https://pythonhosted.org/Flask-Testing/). Remember to write test cases for the model operations in the "back-end/www/models/model_operations" folder. Below shows how to run test cases:
```sh
cd spotdiff/back-end/www/tests
# Run all tests
python run_all_tests.py
# Run one test
python user_tests.py
```

# <a name="deploy-back-end-using-uwsgi"></a>Deploy back-end using uwsgi (administrator only)
WARNING: this section is only for system administrators, not developers.

Install [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) using conda.
```sh
conda activate spotdiff
conda install -c conda-forge uwsgi=2.0.19
```
Create a folder for server logging.
```sh
mkdir spotdiff/back-end/log/
```
Run the uwsgi staging server and check if it works.
```sh
cd spotdiff/back-end/www/
sh deploy_staging.sh
```
Check if the uwsgi staging server works.
```sh
curl localhost:8080
```
The staging server log is stored in the "back-end/log/uwsgi_staging.log" file. Refer to the "back-end/www/uwsgi_staging.ini" file for details. The documentation is on the [uwsgi website](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html). A custom log is stored in the "back-end/log/app.log" file.
```sh
# Keep printing the log files when updated
tail -f ../log/uwsgi_staging.log
tail -f ../log/app.log
```
Create a service on Ubuntu, so that the uwsgi server will start automatically after rebooting the system. Replace [PATH] with the path to the cloned repository. Replace [USERNAME] with your user name on Ubuntu.
```sh
sudo vim /etc/systemd/system/spotdiff-staging.service
# Add the following line to this file
[Unit]
Description=uWSGI instance to serve spotdiff
After=network.target

[Service]
User=[USERNAME]
Group=www-data
WorkingDirectory=/[PATH]/spotdiff/back-end/www
Environment="PATH=/home/[USERNAME]/.conda/envs/spotdiff/bin"
ExecStart=/home/[USERNAME]/.conda/envs/spotdiff/bin/uwsgi --ini uwsgi_staging.ini

[Install]
WantedBy=multi-user.target
```
Register the uwsgi staging server as a service on Ubuntu.
```sh
sudo systemctl enable spotdiff-staging
sudo systemctl start spotdiff-staging

# Check the status of the service
sudo systemctl status spotdiff-staging

# Restart the service
sudo systemctl restart spotdiff-staging

# Stop and disable the service
sudo systemctl stop spotdiff-staging
sudo systemctl disable spotdiff-staging
```
Check if the service work.
```sh
curl localhost:8080
```
The procedure of deploying the production server is the same as deploying the staging server (with differences in replacing the "staging" text with "production"). When the back-end code repository on the staging or production server is updated, run the following to restart the deployed service.
```sh
# Restart the uwsgi service
sudo systemctl restart spotdiff-staging
sudo systemctl restart spotdiff-production

# If error happend, check the uwsgi log files
tail -100 spotdiff/back-end/log/uwsgi_staging.log
tail -100 spotdiff/back-end/log/uwsgi_production.log

# Restart the apache service
sudo systemctl restart apache2
```

# <a name="api-calls"></a>API calls
The following code examples assusme that the root url is http://localhost:5000.
### Get the unique user token from the system
The server will return a user token in the form of JWT (JSON Web Token).
- Path:
  - **/user/**
- Available methods:
  - POST
- Required fields:
  - "client_id": the client ID provided by the front-end client
- Returned fields:
  - "user_token": user token provided by the back-end server
```JavaScript
// jQuery examples
$.ajax({
  url: "http://localhost:5000/user/",
  type: "POST",
  data: JSON.stringify({client_id: "uid_for_testing"}),
  contentType: "application/json",
  dataType: "json",
  success: function (data) {console.log(data)},
  error: function (xhr) {console.error(xhr)}
});
```
