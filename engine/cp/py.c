/*BoBoBo*/

#include "py.h"

int
py_initialize(char *py_file, char *py_func)
{
    Py_Initialize();  
    if (!Py_IsInitialized()) {  
        return -1;  
    }

    PyObject *pName, *pModule, *pDict, *pFunc;
    pName =  PyUnicode_FromString(py_file);  
    pModule = PyImport_Import(pName);  
    if (!pModule) {  
        return -1;  
    }  
    pDict = PyModule_GetDict(pModule);  
    if (!pDict) {  
        return -1;  
    } 

    load_py_script_dict = pDict;

    pFunc = PyDict_GetItemString(pDict, py_func);  
    if (!pFunc || !PyCallable_Check(pFunc)) {  
        return -1;  
    }

    load_py_func = pFunc;
    return 0;
}

void
py_finalize()
{
    Py_DECREF(load_py_script_dict);  
    Py_DECREF(load_py_func);  
    Py_Finalize();  
}

void
ex_py_content(char *py_content)
{
    PyRun_SimpleString(py_content);
}

PyObject *
ex_py_file(PyObject *pArgsT)
{
    PyObject *pFunc = load_py_func;
    if (!pFunc || !PyCallable_Check(pFunc)) {  
        return NULL;  
     }  

    return PyEval_CallObject(pFunc, pArgsT);
}
