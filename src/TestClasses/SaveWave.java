package TestClasses;




import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SaveWave {


    public SaveWave() {


    }
    public void Save (byte[] source,String file)
    {


        AudioInputStream stream = new AudioInputStream(
                new ByteArrayInputStream(source),
                new AudioFormat(44100, 16, 2, true, true),
                source.length
        );
        File wavFile= new File(file);
        try {
            AudioSystem.write(stream, AudioFileFormat.Type.WAVE, wavFile);
        } catch (IOException ex) {

        }


    }
}
