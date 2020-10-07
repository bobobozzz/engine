/*BoBoBo*/

#ifndef _CP_UTIL_H_INCLUDED_
#define _CP_UTIL_H_INCLUDED_

#include <Python.h>
#include <ngx_http.h>
#include <ngx_http_request.h>

PyObject *assemble_dict(ngx_http_request_t *r);

char *get_str(PyObject *pyObject, char *key);

#endif /* _CP_UTIL_H_INCLUDED_ */
