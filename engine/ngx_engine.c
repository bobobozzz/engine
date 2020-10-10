/*BoBoBo*/

#include "ngx_engine.h"

static char *
ngx_http_engine(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
    ngx_http_core_loc_conf_t  *clcf;
    clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
    clcf->handler = ngx_http_engine_handler;
    ngx_conf_set_str_slot(cf,cmd,conf);
    return NGX_CONF_OK;
}

static ngx_int_t
ngx_http_engine_handler(ngx_http_request_t *r)
{
    if(!(r->method & (NGX_HTTP_HEAD|NGX_HTTP_GET|NGX_HTTP_POST))) {
        return NGX_HTTP_NOT_ALLOWED;
    }

    ngx_http_read_client_request_body(r, ngx_http_pin_body_handler);

    return NGX_DONE;
}

static ngx_int_t 
ngx_http_engine_init(ngx_cycle_t *cycle)
{
    ngx_http_engine_loc_conf_t *emf = ngx_http_cycle_get_module_main_conf(cycle, ngx_http_engine_module);
    

    u_char *path = ngx_pcalloc(cycle->pool, emf->py_file.len + 1);
    path[emf->py_file.len] = '\0';
    ngx_cpystrn(path, emf->py_file.data, emf->py_file.len);
    char *pyfile = (char *)path;
    py_initialize(pyfile, "engine");
    return NGX_OK;
}

static void
ngx_http_engine_exit(ngx_cycle_t *cycle)
{
    py_finalize();
}

static void
ngx_http_pin_body_handler(ngx_http_request_t *r)
{
    pin(r);

    ngx_buf_t *b;
    ngx_chain_t out;

    b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));
    if (b == NULL) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0, "ngx_pcalloc return null");
        return;
    }

    /*
    b->pos = (u_char*)r_body;
    b->last = b->pos + len;
    b->memory = 1;
    b->last_buf = 1;
    */

    out.buf = b;
    out.next = NULL;
    
    ngx_http_send_header(r);
    ngx_http_output_filter(r, &out);
}

static void *
ngx_http_engine_create_loc_conf(ngx_conf_t *cf)
{
    ngx_http_engine_loc_conf_t  *conf;
    conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_engine_loc_conf_t));
    if (conf == NULL) {
        return NGX_CONF_ERROR;
    }
    conf->py_file.len = 0;
    conf->py_file.data = NULL;
    return conf;
}

static char *
ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child)
{
    ngx_http_engine_loc_conf_t *prev = parent;
    ngx_http_engine_loc_conf_t *conf = child;
    ngx_conf_merge_str_value(conf->py_file, prev->py_file, "");
    return NGX_CONF_OK;
}

