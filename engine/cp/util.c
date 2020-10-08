/*BoBoBo*/

#include "util.h"

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
