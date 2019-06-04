/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Biometric.Main;


import Biometric.Functions.WAVReader;
import Biometric.Utilities.AmplitudeList;
import Biometric.Utilities.Bank;
import Biometric.Utilities.FramesList;
import Biometric.Utilities.SpectrumsList;
import TestClasses.RSByte;
import TestClasses.SaveWave;
import org.apache.commons.math3.complex.Complex;

import Biometric.Functions.AudiotoByte;
import Biometric.Functions.DCT;
import Biometric.Functions.DTW;
import Biometric.AudioModifiers.Process;
import Biometric.AudioModifiers.RemoveSilence;
import Biometric.Utilities.Bank;
import Biometric.Utilities.FramesList;
import Biometric.Utilities.SpectrumsList;


import java.io.*;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.sound.sampled.*;


/**
 *
 * @author Patryk
 */
public class Record  {
   public static void main(String[] args)throws LineUnavailableException, InterruptedException, Exception{
        int samplingRate= 44100;

        //Register("Record1.wav");
      /* System.out.printf("\n" + "Natepne nagranie ");
=======
       /*Register("Record1.wav");
       System.out.printf("\n" + "Next record ");

       Register("Record2.wav");
       System.out.printf("\n" + "Next record ");
       Register("Record3.wav");*/
        DTW dtw= new DTW();
       byte[] data = null;

           final ByteArrayOutputStream baout = new ByteArrayOutputStream();
       WAVReader wr = new WAVReader();
       AudioInputStream as= wr.getAudioInputStream(new File("Ts.wav"));
           AudioSystem.write(as, AudioFileFormat.Type.WAVE, baout);
           as.close();
           baout.close();
           data = baout.toByteArray();
        Process test= new Process();
       AudiotoByte audio = new AudiotoByte();
       byte[] table = audio.readWAVAudioFileData("Ts.wav");
      // audio.BytetoString(table);

       double[] signal= test.BytetoDoubleArray(data);
       System.out.println("=======================");
       for (int i = 16 + 28; i < 1016 + 28; i+=2) {
           double samp = signal[i] + 256 * signal[i+1];
          // if (signal[i+1] >= 128) samp = -(signal[i] + 256 * (256 - signal[i+1]));
           if (signal[i+1] >= 128) samp = -(65536 - (signal[i] + 256 * signal[i+1]));
           samp = samp / 32768;
           System.out.println(samp);
       }
       SaveWave save= new SaveWave();
       AmplitudeList alist = new AmplitudeList();
       SpectrumsList slist = new SpectrumsList();


       // RSByte rs= new RSByte(table,44100);
       //byte rstable[]= rs.DetectSilence();

       //save.Save(table,"RS1.wav");

       //RemoveSilence remove= new RemoveSilence(test.BytetoDoubleArray(table),44100);
       //double [] tabledouble=remove.DetectSilence();
       FramesList flist = new FramesList();
       //audio.BytetoString(table);


       flist.Frames = test.SliceSignal(signal, 512,256);
       slist.Samples = test.PowerSpectrum(flist.Frames);



      /* System.out.printf("\n" + "Size of list: " + flist.Frames.size());

        alist.AList=test.ReturnAmplitude(slist.Samples);

            for(int i=0;i<alist.AList.get(0).length;++i)
            {
                System.out.println(alist.AList.get(0)[i]);
            }*/



       /*System.out.printf("\n" + "Suma DTW " + dtw.Compare(CaptureSound("Record1.wav"),CaptureSound("Record2.wav")));
       System.out.printf("\n" + "Suma DTW " + dtw.Compare(CaptureSound("Record1.wav"),CaptureSound("Record3.wav")));*/

      // System.out.printf("\n" + "Sum DTW 1st and 2nd sample " + dtw.Compare(CaptureSound("Record1.wav"),CaptureSound("Record2.wav")));
      // System.out.printf("\n" + "Sum DTW 2nd and 3rd sample " + dtw.Compare(CaptureSound("Record2.wav"),CaptureSound("Record3.wav")));
      // System.out.printf("\n" + "Sum DTW 1st and 3rd sample " + dtw.Compare(CaptureSound("Record1.wav"),CaptureSound("Record3.wav")));

      // System.out.printf("\n" + "Minimum " + dtw.GetMin(200,10,500));
       }







public static double[] CaptureSound(String file) {

    AudiotoByte audio = new AudiotoByte();
    SpectrumsList slist = new SpectrumsList();
    Process test = new Process();
    byte[] table = audio.readWAVAudioFileData(file);

   // RSByte rs= new RSByte(table,44100);
    //byte rstable[]= rs.DetectSilence();
    SaveWave save= new SaveWave();
    save.Save(table,"RS1.wav");

    RemoveSilence removeSilence = new RemoveSilence(test.BytetoDoubleArray(table),44100);


    //RemoveSilence remove= new RemoveSilence(test.BytetoDoubleArray(table),44100);
    double [] tabledouble= removeSilence.remove();
    FramesList flist = new FramesList();
    //audio.BytetoString(table);


    flist.Frames = test.SliceSignal(tabledouble, 512,256);
    slist.Samples = test.PowerSpectrum(flist.Frames);

    System.out.printf("\n" + "Size of list: " + flist.Frames.size());
    Bank bank = new Bank();
    double[] banks = test.ConvertFFTBin(bank.filters, 44100, slist.Samples);
    double[] logbank = test.LogEnergy(banks);
    DCT dct = new DCT();
    dct.transform(logbank);
//double[] dctrerult=dct.Transform(logbank);
    for (int i = 0; i < logbank.length; i++) {
      //  System.out.printf("\n" + "Power Spectrum: " + logbank[i]);


    }
    return logbank;
}

public static void Register(String file)throws LineUnavailableException, InterruptedException, Exception{
    AudioFormat format = new AudioFormat(44100, 16, 2, true, true);
    DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
    if(!AudioSystem.isLineSupported(info)){
        System.out.printf("Line is not supported");
    }
    TargetDataLine targetDataLine=(TargetDataLine)  AudioSystem.getLine(info);
    targetDataLine.open();
    System.out.printf("\n" +"Starting Recording");
    targetDataLine.start();
    Thread stopper = new Thread(new Runnable(){
        @Override
        public void run(){
            try {
                AudioInputStream audioStream = new AudioInputStream(targetDataLine);

                File wavFile= new File(file);
                try {
                    AudioSystem.write(audioStream, AudioFileFormat.Type.WAVE, wavFile);
                } catch (IOException ex) {
                    Logger.getLogger(Record.class.getName()).log(Level.SEVERE, null, ex);
                }

            } catch (Exception ex) {
                Logger.getLogger(Record.class.getName()).log(Level.SEVERE, null, ex);
            }
        }



    });

   stopper.start();

       Thread.sleep(5000);
       targetDataLine.stop();

       targetDataLine.close();


    System.out.printf("\n" +"Recording ended ");

   }


}
