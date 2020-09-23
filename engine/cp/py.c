/*BoBoBo*/

#include "py.h"

static void ex_content(ngx_str_t py_content) {
    Py_Initialize();
    PyRun_SimpleString("print(\"Hello World\")");
    Py_Finalize();
    system("PAUSE");
}
