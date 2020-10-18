/*BoBoBo*/

#ifndef _ENGINE_PIN_H_INCLUDED_
#define _ENGINE_PIN_H_INCLUDED_

#include <Python.h>
#include <ngx_http.h>
#include <ngx_http_request.h>

#include "cp/py.h"
#include "cp/util.h"

ngx_str_t pin(ngx_http_request_t *r);
PyObject *assemble_dict(ngx_http_request_t *r);
ngx_str_t assemble_response(ngx_http_request_t *r, PyObject *pin_response);

#endif /* _ENGINE_PIN_H_INCLUDED_ */
