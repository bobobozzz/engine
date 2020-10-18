/*BoBoBo*/

#ifndef _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_
#define _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <nginx.h>

#include "engine_pin.h"
#include "cp/py.h"

#ifndef offsetof
#define offsetof(type, field) (size_t)(&(((type *)0)->field))
#endif

#ifndef NGX_HTTP_ENGINE_TEXT
#define NGX_HTTP_ENGINE_TEXT "app.py"
#endif

ngx_str_t default_text = ngx_string(NGX_HTTP_ENGINE_TEXT);

static void * ngx_http_engine_create_loc_conf(ngx_conf_t *cf);
static char * ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void * parent, void *child);

static ngx_int_t ngx_http_engine_handler(ngx_http_request_t *r);

static char * ngx_http_engine_set_engine_flag(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
static char * ngx_http_engine_set_pin_app(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);

typedef struct {
    ngx_flag_t engine_flag;
    ngx_str_t pin_app;
} ngx_http_engine_conf_t;

ngx_command_t ngx_http_engine_commands[] = {
    {
        ngx_string("engine"),
        NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF | NGX_CONF_FLAG,
        ngx_http_engine_set_engine_flag,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_engine_conf_t, engine_flag),
        NULL
    },
    {
        ngx_string("engine_pin_app"),
        NGX_HTTP_SRV_CONF | NGX_HTTP_LOC_CONF | NGX_HTTP_LMT_CONF | NGX_CONF_ANY,
        ngx_http_engine_set_pin_app,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_engine_conf_t, pin_app),
        NULL
    },
    ngx_null_command
};

ngx_http_module_t ngx_http_engine_module_ctx = {
    /*called before resolving the configuration file */
    NULL,    /* ngx_int_t (*preconfiguration)(ngx_conf_t *cf) */
    /*called after resolving the configuration file */
    NULL,    /* ngx_int_t (*postconfiguration)(ngx_conf_t *cf) */

    /*create a conf struct for grobal configuration */
    NULL,    /* void * (*create_main_conf)(ngx_conf_t * cf)*/
    /*initialize the main conf struct */
    NULL,    /* char * (*init_main_conf)(ngx_conf_t * cf)*/

    NULL,    /* void * (*create_srv_conf)(ngx_conf_t * cf)*/
    NULL,    /* char * (*merge_srv_conf)(ngx_conf_t * cf, void * prev, void * conf)*/

    ngx_http_engine_create_loc_conf, /*create location configuration*/
    ngx_http_engine_merge_loc_conf, /*merge location configuration: enables the same conf apears in different blocks*/
};

ngx_module_t ngx_http_engine_module = {
    NGX_MODULE_V1, /*0,0,0,0,0,0,1 (version=1 as the default) reserved variables*/
    &ngx_http_engine_module_ctx,
    ngx_http_engine_commands,    /* array with only one ngx_command_t*/
    NGX_HTTP_MODULE,
    NULL,    /*init_master: not used*/
    NULL,    /*init_module*/
    NULL,    /*init_process*/
    NULL,    /*init_thread: not support*/
    NULL,    /*exit_thread: not support*/
    NULL,    /*exit_process*/
    NULL,    /*exit_master*/
    NGX_MODULE_V1_PADDING /*0,0,0,0,0,0,0,0, eight reserved variables*/
};

#endif /* _NGX_HTTP_ENGINE_MODULE_H_INCLUDED_ */
