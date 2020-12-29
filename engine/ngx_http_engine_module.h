/*BoBoBo*/

#ifndef _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_
#define _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_


#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <nginx.h>
#include "engine_pin.h"


static void * ngx_http_engine_create_loc_conf(ngx_conf_t *cf);
static char * ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void * parent, void *child);

static char * ngx_http_engine_set_engine_app(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);

static ngx_int_t ngx_http_engine_handler(ngx_http_request_t *r);


typedef struct {
    ngx_str_t engine_app;
} ngx_http_engine_conf_t;


#endif /* _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_ */
