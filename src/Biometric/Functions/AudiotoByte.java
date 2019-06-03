/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Biometric.Functions;

import java.io.ByteArrayOutputStream;
import java.io.File;
import javax.sound.sampled.*;


/**
 *
 * @author Patryk
 */
public class AudiotoByte {
    
     public byte[] readWAVAudioFileData(final String filePath)
  {
    byte[] data = null;
    try
    {
      final ByteArrayOutputStream baout = new ByteArrayOutputStream();
      final AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(filePath));

      AudioSystem.write(audioInputStream, AudioFileFormat.Type.WAVE, baout);
      audioInputStream.close();
      baout.close();
      data = baout.toByteArray();
    }
    catch (Exception e)
    {
      e.printStackTrace();
    }

    return CutHeader(data);
  }
     public void BytetoString(byte[] a){
     for(int i=0;i<a.length;i++){
         System.out.printf("byte number: "+i+" "+(a[i] & 0xFF)+"\n");
         
     }
     }
     public byte[] CutHeader(byte[] source)
     {
         byte[] result=new byte[source.length-44];
         int i;
         int j=0;
         for(i=45;i<source.length;++i)
         {

             result[j]=source[i];
             ++j;
         }
         return result;
     }
}
