// BoBoBo


#include "test_engine_pin.h"
#include <string.h>
#include <stdlib.h>


void TestStrCat(CuTest *tc) {
    char* actual = NULL;
    char* s1 = strdup("a");
    char* s2 = strdup("b");
    char* s3 = strdup("c");
    strcatn(&actual, s1, s2, s3, NULL);
    char* expected = "abc";
    CuAssertStrEquals(tc, expected, actual);
}


CuSuite* CommonTestSuite() {
    CuSuite* suite = CuSuiteNew();
    SUITE_ADD_TEST(suite, TestStrCat);
    return suite;
}
