/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Biometric.AudioModifiers;

import java.util.*;
import org.apache.commons.math3.complex.Complex;
import org.apache.commons.math3.transform.DftNormalization;
import org.apache.commons.math3.transform.FastFourierTransformer;
import org.apache.commons.math3.transform.TransformType;

/**
 *
 * @author Patryk
 */
public class Process {

    public List<double[]> SliceSignal(double[] a, int framesize,int hopsize) {
       
      
        List<double[]> Samples = new ArrayList<double[]>();
        double x[] = new double[framesize];

        for (int i = 0; i < a.length; i += hopsize) {
            int k=0;

            

            for (int j = i; j < i+framesize ; j++) {
                if (j < a.length) {
                    x[k] = a[j];
                   // System.out.printf("\n"+"Dodane obiekty "+ x[k]);
                   

                } else {
                    x[k] = 0;
                   //System.out.printf("\n"+"Poza a tablica "+ x[k]);
                }
                 k++;
                
            }
            Samples.add(x);

            //System.out.printf("\n"+"Element added: "+i);
            //Arrays.fill(x, 0);

        }

        return Samples;
    }
    public List<Complex[]> PowerSpectrum(List<double[]> frames){

        for(int i=0;i<frames.get(0).length;++i)
        {
            System.out.println(frames.get(0)[i]);
        }
        FastFourierTransformer fft = new FastFourierTransformer(DftNormalization.STANDARD);
        Complex result[] ;
        List<Complex[]> spectrum = new ArrayList<Complex[]>();
        
        for(double[] frame: frames){
            result= fft.transform(frame, TransformType.FORWARD);
            spectrum.add(result);
    
    
    }
        return spectrum;

    
    
    }

    public List<double[]> ReturnAmplitude(List<Complex[]> list)
    {
        List<double[]> result= new ArrayList<>();
        int i;
        double [] amplitide;
        for(Complex[] com :list)
        {
            amplitide=new double[com.length];
            for(i=0;i<com.length;++i)
            {
                amplitide[i]=Math.sqrt(Math.pow(com[i].getImaginary(),2)+Math.pow(com[i].getReal(),2));
            }
            result.add(amplitide);
        }
        return result;
    }
    public double[] ConvertFFTBin(double[] bank,double sampleRate,List<Complex[]> list){
    double[] FFTBin= new double[bank.length];
        for(int i=0;i<bank.length;i++)
        {
            for(Complex[] com :list){
                FFTBin[i]+=Math.floor((com.length+1)*bank[i]/sampleRate);

            }
        }


    return FFTBin;
    }


    public double[] LogEnergy(double[] bank){
        double[] table= new double[bank.length];

        for(int i=0;i<bank.length;i++){

            table[i]=Math.log(bank[i]);
        }

        return table;
    }

    
    public double HztoMel(double hz){
    
    return 2595*Math.log10(1+hz/700);
    }
    
    public double MeltoHz(double mel){
    
    return 700*(Math.pow(10,mel/2595.0)-1);
    }

    public double[] BytetoDoubleArray(byte[]a)
    {
        double[]result= new double[a.length];
        for(int i=0;i<a.length;i++)
        {
            result[i]=a[i]&0xFF;
        }

        return result;
    }

}
