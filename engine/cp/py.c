/*BoBoBo*/

#include "py.h"

int
initialize()
{
    Py_Initialize();  
    if (!Py_IsInitialized()) {  
        return -1;  
    }
    return 0;
}

void
finalize()
{
    Py_Finalize();  
}

void
ex_py_content(char *py_content)
{
    PyRun_SimpleString(py_content);
}

PyObject *
ex_py_file(char *py_file, char *func_name, PyObject *pArgsT)
{
    PyObject *pName,*pModule,*pDict,*pFunc,*pArgs;  
  
    pName =  PyUnicode_FromString(py_file);  
    pModule = PyImport_Import(pName);  
    if (!pModule) {  
        return NULL;  
    }  
    pDict = PyModule_GetDict(pModule);  
    if (!pDict) {  
        return NULL;  
    }  
  
    pFunc = PyDict_GetItemString(pDict, func_name);  
    if (!pFunc || !PyCallable_Check(pFunc)) {  
        return NULL;  
     }  

    PyObject *pReturn = PyEval_CallObject(pFunc, pArgsT);

    Py_DECREF(pName);  
    Py_DECREF(pArgs);  
    Py_DECREF(pModule);  

    return pReturn;
}
