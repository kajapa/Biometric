/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Biometric;

import java.io.ByteArrayOutputStream;
import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.LineUnavailableException;
import javax.sound.sampled.SourceDataLine;
import javax.sound.sampled.TargetDataLine;

/**
 *
 * @author Patryk
 */
public class TestMain {

    /*

    public static void main() {
        AudioFormat format = new AudioFormat(AudioFormat.Encoding.PCM_SIGNED, 44100, 16, 2, 4, 44100, false);
        try {
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
            final SourceDataLine sourceLine = (SourceDataLine) AudioSystem.getLine(info);
            sourceLine.open();

            info = new DataLine.Info(TargetDataLine.class, format);
            final TargetDataLine targetLine = (TargetDataLine) AudioSystem.getLine(info);
            targetLine.open();
            final ByteArrayOutputStream out= new ByteArrayOutputStream();
            Thread sourceThread = new Thread() {
                @Override
                public void run() {
                    sourceLine.start();
                    while (true) {
                        sourceLine.write(out.toByteArray(), 0, out.size());
                    }
                }
            };
            
            Thread targetThread = new Thread() {
                @Override
                
                public void run() {
                    targetLine.start();
                    byte[] data=new byte[targetLine.getBufferSize()/5];
                    int readbytes;
                    while (true) {
                        readbytes= targetLine.read(data, 0, data.length);
                        out.write(data, 0, readbytes);
                        
                    }
                }
            };
            
            targetThread.start();
            System.out.println("Record Start....");,
            Thread.sleep(5000);
            targetLine.stop();
            targetLine.close();
            System.out.println("Record Stop....");
            System.out.println("Starting Playback....");
            sourceThread.start();
            Thread.sleep(5000);
            sourceLine.stop();
            sourceLine.close();
            System.out.println("End Playback....");
        } catch (LineUnavailableException lue) {
            lue.printStackTrace();
        }
        catch(InterruptedException ie){ie.printStackTrace();}
    }*/

}
