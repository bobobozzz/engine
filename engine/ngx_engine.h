/*
 * PROGRAMER: BoBoBo
 * EMAIL: bobobonet@163.com
 */

static char *ngx_http_engine_conf_init(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);

ngx_command_t ngx_http_engine_commands[] = {
    {
        ngx_string("engine_py"),
        NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF | NGX_CONF_TAKE1,
        ngx_http_engine_conf_init,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_hi_loc_conf_t, python_script),
        NULL
    },
    {
        ngx_string("engine_py"),
        NGX_HTTP_LOC_CONF | NGX_HTTP_LIF_CONF | NGX_CONF_TAKE1,
        ngx_http_engine_conf_init,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_hi_loc_conf_t, python_content),
        NULL
    }
}

