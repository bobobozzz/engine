/*BoBoBo*/

#include "ngx_pin.h"

void
pin(ngx_http_request_t *r)
{
    PyObject *pin_request = assemble_dict(r);
    PyObject *pin_response = ex_py_file(pin_request);
    assemble_response(r , pin_response);
}

PyObject *
assemble_dict(ngx_http_request_t *r)
{
    //TODO: get body str from request or url param
    char *r_body = "test";

    PyObject *pArgsT = PyTuple_New(1);
    PyObject *pArgsD = PyDict_New();

    //TODO: assemble headers
    PyDict_SetItemString(pArgsD, "body", Py_BuildValue("s", r_body));

    PyTuple_SetItem(pArgsT, 0, pArgsD);
    return pArgsT;
}

void
assemble_response(ngx_http_request_t *r, PyObject *pin_response)
{
    //TODO: make response from dict
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_type.len = sizeof("text/plain") - 1;
    r->headers_out.content_type.data = (u_char*)"text/plain";
}
