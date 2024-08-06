#!/bin/bash

# Function to install Apache2
install_apache2() {
    echo "Installing Apache2..."
    sudo apt update
    sudo apt install -y apache2
}

# Function to enable necessary Apache2 modules
enable_apache2_modules() {
    echo "Enabling essential Apache2 modules..."
    sudo a2enmod rewrite
    sudo a2enmod headers
    sudo a2enmod ssl
}

# Function to configure UFW firewall
configure_firewall() {
    echo "Configuring UFW firewall..."
    sudo ufw allow 'Apache Full'
    sudo ufw delete allow 'Apache'
    sudo ufw --force enable
}

# Function to obtain and install SSL certificate using Certbot
setup_https() {
    echo "Installing Certbot and obtaining SSL certificate..."
    sudo apt install -y certbot python3-certbot-apache
    sudo certbot --apache
    echo "Setting up automatic SSL renewal..."
    echo "0 3 * * * /usr/bin/certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null
}

# Function to harden Apache2 configuration
harden_apache2() {
    echo "Hardening Apache2 configuration..."

    # Disable server signature
    sudo sed -i 's/ServerTokens OS/ServerTokens Prod/' /etc/apache2/conf-available/security.conf
    sudo sed -i 's/ServerSignature On/ServerSignature Off/' /etc/apache2/conf-available/security.conf

    # Disable directory listing
    sudo sed -i 's/Options Indexes FollowSymLinks/Options FollowSymLinks/' /etc/apache2/apache2.conf

    # Add security headers
    echo "Adding security headers..."
    sudo bash -c 'cat > /etc/apache2/conf-available/security-headers.conf <<EOF
<IfModule mod_headers.c>
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set X-Content-Type-Options "nosniff"
    Header always set Referrer-Policy "no-referrer-when-downgrade"
    Header always set Content-Security-Policy "default-src '\''self'\''; script-src '\''self'\''; object-src '\''none'\''; style-src '\''self'\'' '\''unsafe-inline'\''; img-src '\''self'\'' data:;"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
</IfModule>
EOF'

    sudo a2enconf security-headers
}

# Function to set file permissions and ownership
set_permissions() {
    echo "Setting file permissions and ownership..."
    sudo chown -R www-data:www-data /var/www/html
    sudo find /var/www/html -type d -exec chmod 755 {} \;
    sudo find /var/www/html -type f -exec chmod 644 {} \;
}

# Function to configure logging and monitoring
configure_logging() {
    echo "Configuring logging..."
    sudo bash -c 'cat > /etc/logrotate.d/apache2 <<EOF
/var/log/apache2/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 640 root adm
    sharedscripts
    postrotate
        if /etc/init.d/apache2 status > /dev/null ; then \\
            /etc/init.d/apache2 reload > /dev/null; \\
        fi;
    endscript
}
EOF'
}

# Function to restart Apache2
restart_apache2() {
    echo "Restarting Apache2 to apply changes..."
    sudo systemctl restart apache2
}

# Main function to orchestrate the deployment and securing process
main() {
    install_apache2
    enable_apache2_modules
    configure_firewall
    setup_https
    harden_apache2
    set_permissions
    configure_logging
    restart_apache2
    echo "Apache2 deployment and security configuration complete!"
}

# Execute the main function
main

