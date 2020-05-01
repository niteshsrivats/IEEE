package RMHackathon.java;

import java.io.*;
import java.util.ArrayList;
import java.lang.Math;

public class Writer {

  public void writeCSV(String filename, double[][] data) throws  IOException, FileNotFoundException {
    PrintWriter pw = new PrintWriter(new File("dumbboi.csv"));
    StringBuilder sb = new StringBuilder();
    int m = data.length;
    int n = data[0].length;
    for(int i = 0; i < m; i++)
    {
        for(int j = 0; j < n; j++)
        {
            sb.append(data[i][j]);
            sb.append(',');
        }
        sb.append('\n');
    }
    pw.write(sb.toString());
    pw.close();
  }
}