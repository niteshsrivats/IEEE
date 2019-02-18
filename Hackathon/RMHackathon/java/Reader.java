package RMHackathon.java;

import java.io.*;
import java.util.ArrayList;
import java.lang.Math;

public class Reader {
  
  public double[][] readCSV(String filename) throws IOException, FileNotFoundException {
    
    ArrayList<ArrayList<Double>> matrix = new ArrayList<ArrayList<Double>>();
    String line = "";
    BufferedReader br = new BufferedReader(new FileReader(filename));
    while ((line = br.readLine()) != null)
    {
        String[] eachval = line.split(",");
        ArrayList<Double> doubleValues = new ArrayList<Double>();
        //each row of csv file stored as array of Double objects
        for (int i = 0; i <eachval.length; i++)
             doubleValues.add(Double.valueOf(eachval[i]));
        matrix.add(doubleValues);
        //putting all rows together to create 2D matrix
    }

    int m=matrix.size(),n=matrix.get(0).size();
    double data[][] = new double [m][n];
    //putting Double objects into 2D array of double type to reproduce entire csv file in the array
    for(int i = 0; i < m; i++)
        for(int j = 0; j < n; j++)
            data[i][j]= matrix.get(i).get(j);
    br.close();
    // Dataset for java is given as a csv file

    return data;

  }
}