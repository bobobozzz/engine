/*BoBoBo*/

#include "ngx_http_engine_module.h"

#ifndef offsetof
#define offsetof(type, field) (size_t)(&(((type *)0)->field))
#endif


ngx_command_t ngx_http_engine_commands[] = {
    {
        ngx_string("engine_app"),
        NGX_HTTP_LOC_CONF | NGX_CONF_ANY,
        ngx_http_engine_set_engine_app,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_engine_conf_t, engine_app),
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


void *
ngx_http_engine_create_loc_conf(ngx_conf_t *cf)
{
	ngx_http_engine_conf_t *mycf = (ngx_http_engine_conf_t*) ngx_pcalloc(cf->pool, sizeof(ngx_http_engine_conf_t));
	if(!mycf) return NULL;

	mycf->engine_app = (ngx_str_t)ngx_null_string;
	return mycf;
}


char *
ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void * parent, void *child)
{
	ngx_http_engine_conf_t * p = (ngx_http_engine_conf_t *)parent;
	ngx_http_engine_conf_t * c = (ngx_http_engine_conf_t *)child;
	ngx_conf_merge_str_value((c->engine_app), (p->engine_app), "");
	return NGX_CONF_OK;
}


ngx_int_t
ngx_http_engine_handler(ngx_http_request_t *r)
{
	ngx_http_engine_conf_t * mycf;
	//return 405 if method is not GET, POST or HEAD
	if (!(r->method & (NGX_HTTP_GET | NGX_HTTP_POST | NGX_HTTP_HEAD)))
		return NGX_HTTP_NOT_ALLOWED;

	//discard the request body
	ngx_int_t rc = ngx_http_discard_request_body(r);
	if (rc != NGX_OK)
		return rc;
	
	mycf = (ngx_http_engine_conf_t *)ngx_http_get_module_loc_conf(r, ngx_http_engine_module);
	if(mycf==0)
		return NGX_HTTP_INTERNAL_SERVER_ERROR;
	
	ngx_str_t type = ngx_string("text/plain");

    //app
    u_char *path = ngx_pcalloc(r->pool, mycf->engine_app.len + 1);
    path[mycf->engine_app.len] = '\0';
    ngx_cpystrn(path, mycf->engine_app.data, mycf->engine_app.len + 1);
    char *pyfile = (char *)path;

    ngx_str_t response = ngx_null_string;
    char *init_res = engine_app_initialize(pyfile, "engine");
    if(NULL == init_res){
        response = pin(r);
    }else{
        response.data = (u_char *)init_res;
        response.len = strlen(init_res);
    }

    engine_app_finalize();

	r->headers_out.status = NGX_HTTP_OK;
	r->headers_out.content_length_n = response.len;
	r->headers_out.content_type = type;

	rc = ngx_http_send_header(r);
	if(rc == NGX_ERROR || rc > NGX_OK || r->header_only)
		return rc;
	ngx_buf_t *b = ngx_create_temp_buf(r->pool, response.len);
	if(b == NULL)
		return NGX_HTTP_INTERNAL_SERVER_ERROR;
	
	ngx_memcpy(b->pos, response.data, response.len);
	b->last = b->pos + response.len;
	b->last_buf = 1;


	ngx_chain_t out;
	out.buf = b;
	out.next = NULL;

	return ngx_http_output_filter(r, &out);
}


static char *
ngx_http_engine_set_engine_app(ngx_conf_t * cf, ngx_command_t * cmd, void * conf)
{
	ngx_http_core_loc_conf_t *clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
	if(NULL == clcf)
        return NGX_CONF_ERROR;
    clcf->handler = ngx_http_engine_handler;
	
	ngx_str_t * np = (ngx_str_t *)((char *)conf+(cmd->offset));
	if(np->data)
        return NGX_CONF_ERROR;

	//ngx_int_t nvalues = cf->args->nelts;
	//ngx_str_t * value = cf->args->elts;
    //*np = value[1];
	
	return NGX_CONF_OK;
}
