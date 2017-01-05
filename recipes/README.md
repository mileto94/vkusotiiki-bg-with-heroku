# vkusotiiki_bg

##Installation

### Notes:
1. Install python first - version 3.5.2

2. Install pip for python3.5.2: `sudo apt-get install python3.5-pip`

3. Install virtualenv: `pip3.5 install virtualenv`

4. Install additional dependencies: `sudo apt-get install python3-dev libmysqlclient-dev`

5. Install mysql server: `sudo apt-get install mysql-server`

6. Create virtualenv next to 'README.md' file: `virtualenv -p /usr/bin/python3.5 vkusotiiki_env`

7. Enter into the virtualenv: `source vkusotiiki_env/bin/activate`

8. Install all dependencies inside the virtualenv: `pip install -r requirements.txt`

You're done :)