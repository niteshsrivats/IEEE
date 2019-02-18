//reading csv file into 2 D array

#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

int main()
{
    double data[12][10];
    int rows = 0;
    std::ifstream file("Test2.csv"); //csv file from which values have to be retrieved

    string line;
    while (getline( file, line,'\n'))
    {
        ++rows;
        int row = rows - 1;
        std::stringstream iss(line);
        for (int col = 0; col < 8; ++col)
        {
            std::string val;
            std::getline(iss, val, ',');
            if ( !iss.good() )
                break;
            std::stringstream convertor(val);
            convertor >> data[row][col];
        }
        data[row][8] = 0;
    }

    // Write Code Here

    std::ofstream outfile("ans.csv"); //csv file from which values have to be retrieved
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < 9; ++j)
            outfile << data[i][j] << ",";
        outfile << "\n";
    }
    return 0;
}
