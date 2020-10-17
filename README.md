# Engine

[engine](https://github.com/bobobozzz/engine.git)
 - Embedded python for nginx-module and come with Pin which is a python functional web framework.

* To support developing web application using nginx in python;
* To use functional program paradim. 

## Now

* Nginx call python script embedly.
* Funcitonal web framework pin.
* Pin has a python embed http server to support develop mode.

## Todo

* Make it to be a complete project to support enterprise-level development.
* Support WSGI.
* Support functional program well.

## Requirement

- Python 3.6+
- nginx-1.6.3+ 

test:

- cunit-2.1-3

## Installation

```sh
$ git clone https://github.com/bobobozzz/engine.git

$ wget 'http://nginx.org/download/nginx-1.19.3.tar.gz'
$ tar -zxvf nginx-1.19.3.tar.gz
$ cd nginx-1.19.3

$ ./configure --user=www --group=www \
      --prefix=/path/to/nginx \
      --add-module=/path/to/engine/engine \
      --with-ld-opt="`python3.6-config --ldflags`"

$ make
$ make install
```

## Useage

configure nginx:

```
user www www;
worker_processes  4;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location * {
            engine /path/to/engine/example/hello/hello/app.py;
        }
    }
}
```

execute:

```sh
$ curl http://localhost/engine_example/hello
{"err_code": 0, "err_msg": "", "data": {"content": "Hello Engine!"}}
```

docker(just an enviroment to run engine from code now):

```
cd /path/to/engine/docker
docker-compose up -d engine_compiler
```

## Version Rules 

N1.N2.N3

 N1: Support Level

     N1 > 0: Support personal develop;
     N1 > 1: Support enterprise develop.

 N2: Big Functions

 N3: Fix bugs

## Contributors

BoBoBo
