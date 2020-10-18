/*BoBoBo*/

#ifndef _CP_PY_H_INCLUDED_
#define _CP_PY_H_INCLUDED_

#include <Python.h>

char *py_initialize(char *py_file, char *py_func);
void py_finalize();
void ex_py_content(char *py_content);
PyObject *ex_py_file(PyObject *pArgsT);

#endif /* _CP_PY_H_INCLUDED_ */
