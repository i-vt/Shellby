#!/bin/bash

# Update package information
echo "Updating package information..."
sudo apt-get update -y

# Install MySQL server
echo "Installing MySQL server..."
sudo apt-get install mysql-server -y

# Start MySQL service
echo "Starting MySQL service..."
sudo systemctl start mysql

# Enable MySQL service to start on boot
echo "Enabling MySQL service to start on boot..."
sudo systemctl enable mysql

# Generate a random password for MySQL root user
MYSQL_ROOT_PASSWORD=$(openssl rand -base64 12)

# Store the generated password in a file
echo "Storing MySQL root password in './mysql_root_password.txt'..."
echo "$MYSQL_ROOT_PASSWORD" > ./mysql_root_password.txt
chmod 600 ./mysql_root_password.txt

# Secure MySQL installation
echo "Securing MySQL installation..."

# Set MySQL root password
echo "Setting MySQL root password..."
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY '$MYSQL_ROOT_PASSWORD';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Run the MySQL secure installation script
echo "Running the MySQL secure installation script..."
SECURE_MYSQL=$(expect -c "
set timeout 10
spawn sudo mysql_secure_installation
expect \"Enter password for user root:\"
send \"$MYSQL_ROOT_PASSWORD\r\"
expect \"Would you like to setup VALIDATE PASSWORD plugin?\"
send \"n\r\"
expect \"Change the password for root ?\"
send \"n\r\"
expect \"Remove anonymous users?\"
send \"y\r\"
expect \"Disallow root login remotely?\"
send \"y\r\"
expect \"Remove test database and access to it?\"
send \"y\r\"
expect \"Reload privilege tables now?\"
send \"y\r\"
expect eof
")

echo "$SECURE_MYSQL"

# Display completion message
echo "MySQL installation and basic security setup are complete."
echo "MySQL root password is stored in './mysql_root_password.txt'."
