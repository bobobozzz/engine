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
    string change_dir = "sys.path.append('../scripts')";
    PyRun_SimpleString(change_dir.c_str());

    PyObject *pName, *pModule;
    pName =  PyUnicode_FromString(py_file);
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
