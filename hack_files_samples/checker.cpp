#include "testlib.h"
#include <sstream>
#include <string>
#include <vector>

using namespace std;

bool compareWords(string a, string b)
{
    vector<string> va, vb;
    stringstream sa;

    sa << a;
    string cur;
    while (sa >> cur)
        va.push_back(cur);

    stringstream sb;
    sb << b;
    while (sb >> cur)
        vb.push_back(cur);

    return (va == vb);
}

int main(int argc, char *argv[])
{
    setName("compare files as sequence of tokens in lines");
    registerTestlibCmd(argc, argv);

    while (!ans.eof())
    {
        string judge = ans.readString();
        if (judge == "" && ans.eof())
        {
            break;
        }
        string player = ouf.readString();
        if (judge != player)
        {
            quitf(_wa, "wrong");
        }
    }

    quitf(_ok, "ok");
}
