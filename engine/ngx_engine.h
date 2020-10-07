/*BoBoBo*/

#ifndef _NGX_ENGINE_H_INCLUDED_
#define _NGX_ENGINE_H_INCLUDED_

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

#include "cp/py.h"
#include "cp/util.h"

static char *ngx_http_engine(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
static void *ngx_http_engine_create_loc_conf(ngx_conf_t *cf);
static char *ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child);
static ngx_int_t ngx_http_engine_handler(ngx_http_request_t *r);

typedef struct {
    ngx_str_t  py_content;
} ngx_http_engine_loc_conf_t;

ngx_command_t ngx_http_engine_commands[] = {
    {
        ngx_string("engine_py_content"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_http_engine,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_engine_loc_conf_t, py_content),
        NULL
    },
    ngx_null_command
};

static ngx_http_module_t ngx_http_engine_module_ctx = {
    NULL, /* preconfiguration */
    NULL, /* postconfiguration */
    NULL, /* create main configuration */
    NULL, /* init main configuration */

    NULL, /* create server configuration */
    NULL, /* merge server configuration */

    ngx_http_engine_create_loc_conf, /* create location configuration */
    ngx_http_engine_merge_loc_conf /* merge location configuration */
};

ngx_module_t  ngx_http_engine_module = {
    NGX_MODULE_V1,
    &ngx_http_engine_module_ctx,             /* module context */
    ngx_http_engine_commands,                /* module directives */
    NGX_HTTP_MODULE,                       /* module type */
    NULL,                                  /* init master */
    NULL,                                  /* init module */
    NULL,                                  /* init process */
    NULL,                                  /* init thread */
    NULL,                                  /* exit thread */
    NULL,                                  /* exit process */
    NULL,                                  /* exit master */
    NGX_MODULE_V1_PADDING
};

#endif /* _NGX_ENGINE_H_INCLUDED_ */
