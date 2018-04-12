# Vhost

Simple tool to help developers start new projects and setup apache virtual hosts


## Getting started
There is an extra step to install **vhost**, you must log in as root before
install.

### Prerequisites
Python version greater than 3

### Installing
```
$ su -
$ pip3 install vhost
$ exit
```

Now you can use **vhost** with ```sudo```

### Usage
Currently, ```vhost``` only supports **Apache** and was tested using
**Debian**. Support for **Nginx** and other features are going to be
added in next releases.

#### Add a new virtual host
```
$ sudo vhost -n your_hostname.localhost -u your_user
```

where your_hostname and your_user are up to you.

#### Finding help
```
$ vhost --help
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details