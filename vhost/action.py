#!/usr/bin/env python3

import os
import pwd
import grp

def check_server(name):
    return os.path.exists('/usr/sbin/apache2')

def check_availability(name):
    if not name:
        return False

    return not os.path.exists('/etc/apache2/sites-available/' + name + '.conf')

def check_arguments(args):
    errors = []

    if os.geteuid() != 0:
        errors.append('- you must have root privileges to run vhost')
 
    if not args.name:
        errors.append('- you must specify a host name using -n, --name options')

    if not check_server(args.server):
        errors.append(f'- {args.server} server is not installed')

    if not check_availability(args.name):
        errors.append(f'- host {args.name} is not available')

    try:
        pwd.getpwnam(args.user)
    except KeyError:
        errors.append(f'- user {args.user} does not exist')

    return errors

def create_host_directory(name, user):
    host_dir = f'/var/www/{name}'
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
        exit(f'Error: {host_dir} already exists')

def create_configuration_file(name):
    config = open(f'/etc/apache2/sites-available/{name}.conf', 'w+')

    # this could be better...
    content = f'''<VirtualHost *:80>
    ServerAdmin webmaster@{name}
    ServerName {name}
    ServerAlias www.{name}
    DocumentRoot /var/www/{name}/public_html

    <Directory /var/www/{name}/public_html>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
    </Directory>
                                                                                 
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
</Virtualhost>\n'''

    config.write(content)

def enable_host(name):
    src = f'/etc/apache2/sites-available/{name}.conf'
    dst = f'/etc/apache2/sites-enabled/{name}.conf'

    os.symlink(src, dst)

def create_host(args):
    errors = check_arguments(args)

    if errors:
        exit('Errors:\n' + '\n'.join(errors))

    create_host_directory(args.name, args.user)
    create_configuration_file(args.name)
    enable_host(args.name)

