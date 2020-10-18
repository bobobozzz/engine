/*BoBoBo*/

#include "engine_pin.h"

ngx_str_t
pin(ngx_http_request_t *r)
{
    PyObject *pin_request = assemble_dict(r);
    PyObject *pin_response = ex_py_file(pin_request);
    return assemble_response(r , pin_response);
}

PyObject *
assemble_dict(ngx_http_request_t *r)
{
    //TODO: get body str from request or url param

    PyObject *pArgsT = PyTuple_New(1);
    PyObject *pArgsD = PyDict_New();

    //TODO: assemble headers
    PyDict_SetItemString(pArgsD, "body", Py_BuildValue("s", "test pin"));

    PyTuple_SetItem(pArgsT, 0, pArgsD);
    return pArgsT;
}

ngx_str_t
assemble_response(ngx_http_request_t *r, PyObject *pin_response)
{
    //TODO: make response from dict
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_type.len = sizeof("text/plain") - 1;
    r->headers_out.content_type.data = (u_char*)"text/plain";

    ngx_str_t ns = ngx_string("hello");
    if(NULL != pin_response){
        char *ret_str;
        int len;
        PyArg_ParseTuple(pin_response, "si", &ret_str, &len);
        ns.len = len;
        ns.data = (u_char *)ret_str;
    }
    return ns;
}
