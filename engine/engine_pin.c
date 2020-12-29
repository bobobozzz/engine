/*BoBoBo*/

#include "engine_pin.h"


ngx_str_t
pin(ngx_http_request_t *r)
{
    PyObject *pin_request = assemble_dict(r);
    PyObject *pin_response = engine_app_ex(pin_request);
    return assemble_response(r , pin_response);
}

PyObject *
assemble_dict(ngx_http_request_t *r)
{
    PyObject *pArgsT = PyTuple_New(1);
    PyObject *pArgsD = PyDict_New();

    PyDict_SetItemString(pArgsD, "QUERY_STRING", Py_BuildValue("s", "test pin"));

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

    ngx_str_t ns = ngx_string("NULL");
    if(NULL != pin_response){
        PyObject *pContent = PyDict_GetItemString(pin_response, "content");
        char *content;
        PyArg_Parse(pContent, "s", &content);
        ns.len = strlen(content);
        ns.data = (u_char *)content;
    }
    return ns;
}


PyObject *pyo_engine_app_py;
PyObject *pyo_engine_app;

char *
engine_app_initialize(char *py_path, char *py_file, char *py_func)
{
    Py_Initialize();
    if (!Py_IsInitialized()) {
        return "Failed to init python vm.";
    }

    PyRun_SimpleString("import sys");

    char *syspath_stmt = NULL;
    strcatn(&syspath_stmt, "sys.path.append('", py_path ,"')", NULL);
    PyRun_SimpleString(syspath_stmt);

    PyObject *pName, *pModule;
    pName = PyUnicode_FromString(py_file);
    pModule = PyImport_Import(pName);
    if (!pModule) {
        return "Failed to import python module";
    }
    pyo_engine_app_py = PyModule_GetDict(pModule);
    if (!pyo_engine_app_py) {
        return "Failed to get python module dict.";
    }

    pyo_engine_app = PyDict_GetItemString(pyo_engine_app_py, py_func);
    if (!pyo_engine_app || !PyCallable_Check(pyo_engine_app)) {
        return "Failed to get python function.";
    }
    return NULL;
}


void
engine_app_finalize()
{
    Py_Finalize();
}


void
ex_py_content(char *py_content)
{
    PyRun_SimpleString(py_content);
}


PyObject *
engine_app_ex(PyObject *pArgsT)
{
    if (!pyo_engine_app || !PyCallable_Check(pyo_engine_app)) {
        PyObject *pDict = PyDict_New();
        PyDict_SetItemString(pDict, "content", Py_BuildValue("s", "ERROR"));
        return pDict;
    }
    return PyEval_CallObject(pyo_engine_app, pArgsT);
}


char *
get_str(PyObject *pyObj, char *key)
{
    if (pyObj == NULL) {
      return NULL;
    }
    PyObject *pValue = PyDict_GetItemString(pyObj, key);
    char *value = NULL;
    PyArg_Parse(pValue, "s", value);
    return value;
}


size_t 
strcatn(char **dst_out, ...)
{
    size_t len = 0, len_sub;
    va_list argp;
    char *src;
    char *dst = NULL, *dst_p;

    *dst_out = NULL;

    va_start(argp, dst_out);
    for (;;) {
        if ((src = va_arg(argp, char *)) == NULL) break;
        len += strlen(src);
    }
    va_end(argp);

    if (len == 0) return 0;

    dst = (char *)malloc(sizeof(char) * (len + 1));
    if (dst == NULL) return -1;
    dst_p = dst;

    va_start(argp, dst_out);
    for (;;) {
        if ((src = va_arg(argp, char *)) == NULL) break;
        len_sub = strlen(src);
        memcpy(dst_p, src, len_sub);
        dst_p += len_sub;
    }

    va_end(argp);
    *dst_p = '\0';

    *dst_out = dst;

    return len;
}
