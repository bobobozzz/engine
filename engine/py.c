/*BoBoBo*/

#include <ngx_config.h>

void ex_content(ngx_str_t py_content) {
        if (!PYTHON) {
            PYTHON = std::move(std::make_shared<hi::pybind11_py>());
        }
        if (PYTHON) {
            PYTHON->set_req(&py_req);
            PYTHON->set_res(&py_res);
            if (py_content.len > 0) {
                PYTHON->call_content((char*)py_content.data);
            }
        }
    }

