/*BoBoBo*/

#include "ngx_http_engine_module.h"

void *
ngx_http_engine_create_loc_conf(ngx_conf_t *cf)
{
	ngx_http_engine_conf_t *mycf = (ngx_http_engine_conf_t*) ngx_pcalloc(cf->pool, sizeof(ngx_http_engine_conf_t));
	if(!mycf) return NULL;

	mycf->engine_flag = NGX_CONF_UNSET;
	mycf->pin_app = (ngx_str_t)ngx_null_string;
	return mycf;
}

char *
ngx_http_engine_merge_loc_conf(ngx_conf_t *cf, void * parent, void *child)
{
	ngx_http_engine_conf_t * p = (ngx_http_engine_conf_t *)parent;
	ngx_http_engine_conf_t * c = (ngx_http_engine_conf_t *)child;
	ngx_conf_merge_value(p->engine_flag, c->engine_flag, 0);
	ngx_conf_merge_str_value((c->pin_app), (p->pin_app), NGX_HTTP_ENGINE_TEXT);
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
    u_char *path = ngx_pcalloc(r->pool, mycf->pin_app.len + 1);
    path[mycf->pin_app.len] = '\0';
    ngx_cpystrn(path, mycf->pin_app.data, mycf->pin_app.len + 1);
    char *pyfile = (char *)path;

    ngx_str_t response = ngx_null_string;
    char *init_res = py_initialize(pyfile, "engine");
    if(NULL == init_res){
        response = pin(r);
    }else{
        response.data = (u_char *)init_res;
        response.len = strlen(init_res);
    }

    py_finalize();

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


char *
ngx_http_engine_set_engine_flag(ngx_conf_t *cf, ngx_command_t *cmd, void *conf)
{
	ngx_http_core_loc_conf_t *clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);

	ngx_conf_post_t * post = NULL;
	ngx_str_t * value = NULL;
	ngx_int_t * np = (ngx_int_t *)((char *)conf+(cmd->offset));
	if(clcf == NULL)
		return "failed to get loc_conf";
	if(*np != NGX_CONF_UNSET)
		return "is duplicated";

	value = cf->args->elts;
	if(ngx_strncmp("on", value[1].data, value[1].len)==0) {
		clcf->handler = ngx_http_engine_handler;
		*np = 1;
	} else if(ngx_strncmp("off", value[1].data, value[1].len)==0) {
		clcf->handler = NULL;
		*np = 0;
	} else {
		return "invalid parameter";
	}
	post = (ngx_conf_post_t *)cmd->post;
	if(post)
		post->post_handler(cf, cmd->post, np);
	
	return NGX_CONF_OK;
}

static char *
ngx_http_engine_set_pin_app(ngx_conf_t * cf, ngx_command_t * cmd, void * conf)
{
	ngx_str_t * value;
	ngx_int_t nvalues;
	ngx_str_t * np = (ngx_str_t *)((char *)conf+(cmd->offset));
	if(np->data)
		return "is duplicated (chng)";
	nvalues = cf->args->nelts;
	value = cf->args->elts;
	if(nvalues < 2) {
        *np = default_text;
	} else {
		*np = value[1];
	}
	
	return NGX_CONF_OK;
}




