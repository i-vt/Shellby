#!/bin/bash

# Test script for MySQL deployment and security setup

# Load the MySQL root password from the file
MYSQL_ROOT_PASSWORD=$(cat ./mysql_root_password.txt)

# Check if MySQL is installed
echo "Checking if MySQL is installed..."
if ! command -v mysql &> /dev/null; then
    echo "MySQL is not installed. Please run the deployment script first."
    exit 1
else
    echo "MySQL is installed."
fi

# Check MySQL service status
echo "Checking MySQL service status..."
if sudo systemctl is-active --quiet mysql; then
    echo "MySQL service is running."
else
    echo "MySQL service is not running. Please start the MySQL service."
    exit 1
fi

# Attempt to connect to MySQL with the root password
echo "Testing MySQL root login..."
mysql_output=$(mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES;" 2>&1)
if [[ $? -eq 0 ]]; then
    echo "Successfully connected to MySQL as root."
else
    echo "Failed to connect to MySQL as root. Error:"
    echo "$mysql_output"
    exit 1
fi

# Check if remote root login is disabled
echo "Checking if remote root login is disabled..."
remote_login_status=$(mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT Host FROM mysql.user WHERE User='root';" | grep -v Host)
if [[ $remote_login_status == "localhost" ]]; then
    echo "Remote root login is disabled."
else
    echo "Remote root login is not properly configured. Current hosts:"
    echo "$remote_login_status"
    exit 1
fi

# Check if anonymous users have been removed
echo "Checking if anonymous users have been removed..."
anonymous_users=$(mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT User FROM mysql.user WHERE User='';")
if [[ -z $anonymous_users ]]; then
    echo "Anonymous users have been removed."
else
    echo "Anonymous users are still present. Users:"
    echo "$anonymous_users"
    exit 1
fi

# Check if test database has been removed
echo "Checking if the test database has been removed..."
test_db=$(mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SHOW DATABASES LIKE 'test';")
if [[ -z $test_db ]]; then
    echo "Test database has been removed."
else
    echo "Test database is still present. Databases:"
    echo "$test_db"
    exit 1
fi

# Success message
echo "All checks passed. MySQL is installed and secured properly."
