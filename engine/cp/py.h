/*BoBoBo*/

#ifndef _CP_PY_H_INCLUDED_
#define _CP_PY_H_INCLUDED_

#include <Python.h>

int initialize();

void finalize();

void ex_py_content(char *py_content);

PyObject *ex_py_file(char *py_file, char *func_name, PyObject *pArgsT);

#endif /* _CP_PY_H_INCLUDED_ */
