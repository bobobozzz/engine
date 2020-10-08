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

    ngx_int_t rc = ngx_http_read_client_request_body(r, ngx_http_pin_body_handler);

    return NGX_DONE;
}

ngx_int_t 
ngx_http_engine_init(ngx_cycle_t *cycle)
{
    py_initialize("app.py", "engine");
}

ngx_int_t
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

    b->pos = (u_char*)r_body;
    b->last = b->pos + len;
    b->memory = 1;
    b->last_buf = 1;

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
    conf->py_content.len = 0;
    conf->py_content.data = NULL;
    return conf;
}

static char *
ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void *parent, void *child)
{
    ngx_http_engine_loc_conf_t *prev = parent;
    ngx_http_engine_loc_conf_t *conf = child;
    ngx_conf_merge_str_value(conf->py_content, prev->py_content, "");
    return NGX_CONF_OK;
}

