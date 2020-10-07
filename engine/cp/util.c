/*BoBoBo*/

#include "util.h"

PyObject *
assemble_dict(ngx_http_request_t *r)
{
    PyObject *pArgsT = PyTuple_New(1);
    PyObject *pArgsD = PyDict_New();

    //TODO: assemble headers
    PyDict_SetItemString(pArgsD, "body", Py_BuildValue("s", "value"));

    PyTuple_SetItem(pArgsT, 0, pArgsD);
    return pArgsT;
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
