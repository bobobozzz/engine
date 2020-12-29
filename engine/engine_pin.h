/*BoBoBo*/

#ifndef _ENGINE_PIN_H_INCLUDED_
#define _ENGINE_PIN_H_INCLUDED_

#include <Python.h>
#include <ngx_http.h>
#include <ngx_http_request.h>

char *get_str(PyObject *pyObject, char *key);
void ex_py_content(char *py_content);

char *engine_app_initialize(char *py_path, char *py_file, char *py_func);
void engine_app_finalize();
PyObject *engine_app_ex(PyObject *pArgsT);

ngx_str_t pin(ngx_http_request_t *r);
PyObject *assemble_dict(ngx_http_request_t *r);
ngx_str_t assemble_response(ngx_http_request_t *r, PyObject *pin_response);

#endif /* _ENGINE_PIN_H_INCLUDED_ */
