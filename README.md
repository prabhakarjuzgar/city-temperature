# city temperature
By default APPLICATION_CONFIG is set to development. This implies config/development.yml settings will be used.

# 1) Build the docker image
$> ./manage.py compose build app

# 2) Bring up the server
$> ./manage.py compose up -d

# 3) Initialize the database if it is the very first time
$> ./manage.py create-initial-db

$> python -m flask db migrate -m "Initial version"

$> python -m flask db upgrade

# Testing - 
$> ./manage.py test
