// BoBoBo


#include "test_engine_pin.h"
#include <string.h>


char* StrToUpper(char* str) {
    return str;
}


void TestStrCat(CuTest *tc) {
    char* input = strdup("hello world");
    char* actual = StrToUpper(input);
    char* expected = "HELLO WORLD";
    CuAssertStrEquals(tc, expected, actual);
}


CuSuite* CommonTestSuite() {
    CuSuite* suite = CuSuiteNew();
    SUITE_ADD_TEST(suite, TestStrCat);
    return suite;
}
