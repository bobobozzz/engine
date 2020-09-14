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
    ngx_int_t rc;
    ngx_buf_t *b;
    ngx_chain_t out;
    ngx_http_engine_loc_conf_t *elcf;
    elcf = ngx_http_get_module_loc_conf(r, ngx_http_engine_module);
    if(!(r->method & (NGX_HTTP_HEAD|NGX_HTTP_GET|NGX_HTTP_POST)))
    {
        return NGX_HTTP_NOT_ALLOWED;
    }
    r->headers_out.content_type.len = sizeof("text/html") - 1;
    r->headers_out.content_type.data = (u_char *) "text/html";
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = elcf->py_content.len;
    if(r->method == NGX_HTTP_HEAD)
    {
        rc = ngx_http_send_header(r);
        if(rc != NGX_OK)
        {
            return rc;
        }
    }
    b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));
    if(b == NULL)
    {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0, "Failed to allocate response buffer.");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    out.buf = b;
    out.next = NULL;
    b->pos = elcf->py_content.data;
    b->last = elcf->py_content.data + (elcf->py_content.len);
    b->memory = 1;
    b->last_buf = 1;
    rc = ngx_http_send_header(r);
    if(rc != NGX_OK)
    {
        return rc;
    }
    return ngx_http_output_filter(r, &out);
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

