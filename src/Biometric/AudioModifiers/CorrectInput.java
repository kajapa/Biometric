package Biometric.AudioModifiers;

import java.util.ArrayList;
import java.util.List;

public class CorrectInput {
    public double [] input;

    public CorrectInput(double[] input) {
        this.input = input;
    }

    public double [] ReturnCorrectInput()
    {
        List<Double> temp= new ArrayList<Double>();

        int len = input.length;

        for (int i = 44; i < len; i+=2) {
            double samp = input[i] + 256 * input[i+1];
            // if (signal[i+1] >= 128) samp = -(signal[i] + 256 * (256 - signal[i+1]));
            if (input[i+1] >= 128) samp = -(65536 - (input[i] + 256 * input[i+1]));
            samp = samp / 32768;
           temp.add(samp);
        }

        double[] result = temp.stream().mapToDouble(Double::doubleValue).toArray();

        return result;

    }
}
