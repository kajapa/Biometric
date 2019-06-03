package TestClasses;

public class RSByte {

    private      byte [] inputaudio;
    private    byte [] outputaudio;
    private  int samplingRate;
    private  int firstSamples;
    private int samplePerFrame;

    public RSByte(byte[] inputaudio, int samplingRate)
    {
        this.inputaudio = inputaudio;
        this.samplingRate = samplingRate;
        samplePerFrame = this.samplingRate / 1000;
        firstSamples = samplePerFrame * 200;
    }

    public byte [] DetectSilence()
    {
        byte[] sound = new byte [inputaudio.length];
        double sum=0;
        double sd =0.0;
        double m=0;
        System.out.printf("\n" +"dlugosc tablicy"+inputaudio.length);
        System.out.printf("\n" +"FirstSamples"+firstSamples);
        for(int i=0;i<firstSamples;i++)
        {
            sum+=inputaudio[i];

        }
        m=sum/firstSamples;
        sum=0;
        for(int i=0;i<firstSamples;i++)
        {
            sum+=Math.pow((inputaudio[i]-m),2);
        }

        sd= Math.sqrt(sum/firstSamples);
        for(int i=0;i<inputaudio.length;i++)
        {
            if((Math.abs(inputaudio[i])-m)/sd>0.3)
            {
                sound[i]=1;

            }
            else
            {
                sound[i]=0;
            }
        }

        int frameCount=1;
        int usefulFramesCount=1;
        int count_sound=0;
        int count_nosound=0;
        int [] soundFrame= new int[inputaudio.length/samplePerFrame];
        int loopCount=inputaudio.length-(inputaudio.length%samplePerFrame);
        for(int i =0;i<loopCount;i+=samplePerFrame)
        {
            count_sound=0;
            count_nosound=0;
            for(int j=0;j<i+samplePerFrame;j++)
            {
                if(sound[i]==1)
                {
                    count_sound++;

                }
                else
                {
                    count_nosound++;
                }
            }

            if(count_sound>count_nosound)
            {
                usefulFramesCount++;
                soundFrame[frameCount++]=1;
            }
            else
            {
                soundFrame[frameCount++]=0;
            }

        }
        outputaudio= new byte[usefulFramesCount*samplePerFrame];
        int k =0;
        for(int i=0;i<frameCount;i++)
        {
            if(soundFrame[i]==1)
            {
                for(int j=i*samplePerFrame;j<i*samplePerFrame+samplePerFrame;j++)
                {
                    outputaudio[k++]=inputaudio[j];
                }
            }
        }


        return outputaudio;
    }
}
