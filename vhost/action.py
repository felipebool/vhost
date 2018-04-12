#!/usr/bin/env python3

import os
import pwd
import grp

def check_server(name):
    return os.path.exists('/usr/sbin/apache2')

def check_availability(name):
    if not name:
        return False

    config_file = '/etc/apache2/sites-available/{}.conf'.format(name)
    return not os.path.exists(config_file)

def check_arguments(args):
    errors = []

    if os.geteuid() != 0:
        errors.append('- you must have root privileges to run vhost')
 
    if not args.name:
        errors.append('- you must specify a host name using -n, --name options')

    if not check_server(args.server):
        errors.append('- {} server is not installed'.format(args.server))

    if not check_availability(args.name):
        errors.append('- host {} is not available'.format(args.server))

    try:
        pwd.getpwnam(args.user)
    except KeyError:
        errors.append('- user {} does not exist'.format(args.user))

    return errors

def create_host_directory(name, user):
    host_dir = '/var/www/{}'.format(name)
    document_root = host_dir + '/public_html'

    try:
        os.mkdir(host_dir)
        os.mkdir(document_root)

        os.chmod(host_dir, 0o755)
        os.chmod(document_root, 0o775)

        uid = pwd.getpwnam(user).pw_uid
        gid = grp.getgrnam(user).gr_gid

        os.chown(document_root, uid, gid)
    except FileExistsError:
        exit('Error: {} already exists'.format(host_dir))

def create_configuration_file(name):
    config_file = '/etc/apache2/sites-available/{}.conf'.format(name)
    config = open(config_file, 'w+')

    # this could be better...
    content = '''<VirtualHost *:80>
    ServerAdmin webmaster@{}
    ServerName {}
    ServerAlias www.{}
    DocumentRoot /var/www/{}/public_html

    <Directory /var/www/{}/public_html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
    </Directory>
                                                                                 
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</Virtualhost>\n'''.format(name, name, name, name, name)

    config.write(content)

def enable_host(name):
    src = '/etc/apache2/sites-available/{}.conf'.format(name)
    dst = '/etc/apache2/sites-enabled/{}.conf'.format(name)

    os.symlink(src, dst)

def create_host(args):
    errors = check_arguments(args)

    if errors:
        exit('Errors:\n' + '\n'.join(errors))

    create_host_directory(args.name, args.user)
    create_configuration_file(args.name)
    enable_host(args.name)

