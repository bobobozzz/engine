/*BoBoBo*/

#include "py.h"

PyObject *load_py_script_dict;
PyObject *load_py_func;

char *
py_initialize(char *py_file, char *py_func)
{
    Py_Initialize();  
    if (!Py_IsInitialized()) {  
        return "Failed to init python vm.";  
    }

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('/var/engine/example')");

    PyObject *pName, *pModule, *pDict, *pFunc;
    pName =  PyUnicode_FromString(py_file);  
    pModule = PyImport_Import(pName);  
    if (!pModule) {  
        return "Failed to import python module";  
    }  
    pDict = PyModule_GetDict(pModule);  
    if (!pDict) {  
        return "Failed to get python module dict.";  
    } 

    load_py_script_dict = pDict;

    pFunc = PyDict_GetItemString(pDict, py_func);  
    if (!pFunc || !PyCallable_Check(pFunc)) {  
        return "Failed to get python function.";  
    }

    load_py_func = pFunc;
    return NULL;
}

void
py_finalize()
{
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
