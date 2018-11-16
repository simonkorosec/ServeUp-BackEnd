# ServeUp-BackEnd

#### Setup local Postgres database

Install Postgres locally:  
Tutorial: https://devcenter.heroku.com/articles/heroku-postgresql#local-setup

Install Heroku CLI:  
Tutorial: https://devcenter.heroku.com/articles/heroku-cli#download-and-install

To pull and create a local copy of the database:  
**heroku pg:pull postgresql-opaque-40940 serveuplocaldb --app serveup-backend**  

To push to the database:  
1. step: Reset the database before pushing  
**heroku pg:reset postgresql-opaque-40940 --app serveup-backend --confirm serveup-backend**

2. step: Push to heroku data store  
**heroku pg:push serveuplocaldb postgresql-opaque-40940 --app serveup-backend**  

#### Setup Django environment in PyCharm

Build the PyCharm project from Github directly using 
"Check out from Version Control" option when choosing 
a project.

**Important:** Set up Virtualenv inside project, if Pycharm
doesn't do it by default.

1. Install virtualenv globally using: **pip install virutalenv**
2. https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html

After a successful install, navigate into PyCharm terminal
and run command: **pip install -r requirements.txt**  
which will install all necessary dependencies for the project.

Verify by running the server (SHIFT + F10 or Control + R for Mac)

###### Adding new dependencies

All new dependencies should be added to the *requirements.txt* file, 
otherwise the build on Heroku will fail. This can be achieved by either
adding them manually or using command: **pipreqs [options] \<path>**

Tutorial for pipreqs: https://github.com/bndr/pipreqs



