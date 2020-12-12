# Engine

[engine](https://github.com/bobobozzz/engine.git)
 - Embedded python for nginx-module and come with Pin which is a python functional web framework.

* To support developing web application using nginx in python;
* To use functional program paradim. 

## Now

* Nginx call python script embedly.
* Funcitonal web framework pin.
* Pin has a python embed http server to support develop mode.
* WSGI compliant.

## Todo

* Make it to be a complete project to support enterprise-level development.
* Support functional program well.

## Requirement

- Python 3.6+
- nginx-1.6.3+ 

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

## Usage

1.Add environment variable ENGINEPATH which is the path to search python app script file.

```
export ENGINEPATH=path/to/app
```

2.Configure nginx like the example below and start it:

```
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    default_type  application/octet-stream;

    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location /hello {
            engine on;
            engine_wsgi hello:app;
        }
    }
}
```

3.Request and get the response like this:

```sh
$ curl http://localhost/hello
Hello World!
```

docker(just an enviroment to run engine from code now):

```
cd /path/to/engine/docker
docker-compose up -d engine_compiler
```

## About a new Web Framework: Pin

It makes these things as follows work.

1. A web service interfact should be a funtion 
which param comes from http get/post paramters 
and return a text/json/html/binary value.

2. It`s process is direct and clear.

3. Could be replaced easily with WSGI.

## Version Rules 

N1.N2.N3[{a|b|rc}N][.dev][.postN]

 N1: Support Level

     N1 > 0: Support personal develop;
     N1 > 1: Support enterprise develop.

 N2: Big Functions

 N3: Fix bugs (1-Pass base test)

## Contributors

BoBoBo
