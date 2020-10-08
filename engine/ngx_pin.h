/*BoBoBo*/

#ifndef _NGX_PIN_H_INCLUDED_
#define _NGX_PIN_H_INCLUDED_

#include <Python.h>
#include <ngx_http.h>
#include <ngx_http_request.h>

#include "cp/py.h"
#include "cp/util.h"

void pin(ngx_http_request_t *r);
PyObject *assemble_dict(ngx_http_request_t *r);
void assemble_response(ngx_http_request_t *r, PyObject *pin_response);

#endif /* _NGX_PIN_H_INCLUDED_ */
