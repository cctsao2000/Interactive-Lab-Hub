# Chatterboxes
**Amber Tsao (ct649), Aris Huang (th625), Julia Lin (jtl236), Sherri Lin (yl3658), Wayne Cheng (cc2796), Ifeng Wu (iw84)**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

**Please note:** connect the webcam/speaker/microphone while the pi is *off*. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Setup 

*DO NOT* forget to work on your virtual environment! 

Run the setup script
```chmod u+x setup.sh && sudo ./setup.sh  ```

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the directory is a folder called `speech-scripts` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/speech-scripts $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files `.sh` by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/speech-scripts $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech
```
You can test the commands by running
```
echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? 
Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

[**GoogleTTS_myname.sh**](speech-scripts/GoogleTTS_myname.sh)

```
#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say "Hi Amber, how are you doing today?"
```

---
Bonus:
[Piper](https://github.com/rhasspy/piper) is another fast neural based text to speech package for raspberry pi which can be installed easily through python with:
```
pip install piper-tts
```
and used from the command line. Running the command below the first time will download the model, concurrent runs will be faster. 
```
echo 'Welcome to the world of speech synthesis!' | piper \
  --model en_US-lessac-medium \
  --output_file welcome.wav
```
Check the file that was created by running `aplay welcome.wav`. Many more languages are supported and audio can be streamed dirctly to an audio output, rather than into an file by:

```
echo 'This sentence is spoken first. This sentence is synthesized while the first sentence is spoken.' | \
  piper --model en_US-lessac-medium --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -
```
  
### Speech to Text

Next setup speech to text. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 
```
pip install vosk
pip install sounddevice
```

Test if vosk works by transcribing text:

```
vosk-transcriber -i recorded_mono.wav -o test.txt
```

You can use vosk with the microphone by running 
```
python test_microphone.py -m en
```

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

[**own_sh.sh**](speech-scripts/own_sh.sh)
```
#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say "Please tell me your zip code"
python speech-scripts/speech2num.py -m en
```

[**speech2num.py**](speech-scripts/speech2num.py)  
```
text2num_dict = {'zero':'0', 'one':'1', 'two':'2', 'three':'3', 'four':'4', 
                 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
def text2num(num_list):
    result = ""
    for n in num_list:
        try:
            result += text2num_dict[n]
        except KeyError:
            continue
    return result

...

while True:
  data = q.get()
  if rec.AcceptWaveform(data):
      speech_detected = json.loads(rec.Result())
      if list(speech_detected.keys())[0] == 'text':
          print(text2num(speech_detected['text'].split()))
  if dump_fn is not None:
      dump_fn.write(data)
```  
**Video**

https://github.com/cctsao2000/Interactive-Lab-Hub/assets/60999245/c18b854e-594e-49f1-ab8a-6d5ddc93f042



### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

![](https://hackmd.io/_uploads/rJ3Qf6skp.jpg)  
![](https://hackmd.io/_uploads/BkGtWTjya.jpg)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*

![](https://hackmd.io/_uploads/Syfbw3oJp.png)

[Link to Script](https://docs.google.com/document/d/1HKsMSRjF0ELpIccWbYSJYWkbKBNw8_C8tZTLe8Lkzl0/edit)

### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

 [Dialogue Acting Video](https://drive.google.com/file/d/1oRaEOPZ7_Oj229C0Medrwhu07qhtvb_0/view?usp=sharing)
 
\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

In the first take of the video (due to blooper), we realized that when we asked the user to indicate whether they want to eat breakfast, lunch, or dinner, we realized that instead of simply stating one choice, the user will answer in complete sentences. Therefore, we may have to think about how to process and handle user's speech if the user did not respond in the format that we anticipated. This seems to be a recurring problem, so we need to think about how we can change the way we structure the question to make the users respond as intended. Lastly, we realize that sometimes the user will respond even before we finish listing out all of our choices from our questions. So, that might be something that we could consider (i.e.  only allow the users to respond AFTER the robot finished asking the question).

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...

Timing: For timing, we have to think about what would happen if the users did not speak for a long time. How would the system handle long pause or silence.

Misunderstanding: It is highly plausible that the device might not be able to catch all the word precisely, but in the case if the device cannot decipher the user's speech, we should then be able to re-prompt the user to say their speech again.

2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?

We may consider to incorporate camera as inputs in addition to speech. If we are trying to detect user's emotion, using computer vision via the camera, we can also evaluate people's state of emotion when they're inquiring the device with food recommendation. For instance, if the user seems to be angry or sad, we may want to offer more comfort food options for the users to pick from. Additionally, if the user seems confused or puzzled by the prompt, we can initiate the device to re-ask the prompt.

3. Make a new storyboard, diagram and/or script based on these reflections.

Storyboard:

![](https://hackmd.io/_uploads/Sk2zQpuxa.jpg)

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*
1) Run the speech.py file, make sure to pip install gTTS and OpenA first. 
2) To initate a conversation, say 'hey'. This is similar to how people normally summon Siri.
3) The user can try to say something rude or aggressive to the system. Ex. speech: "Can you shut up?"
4) The system will respond, "To make it more polite from (original speech), you can (system suggested speech)."

Storyboard:  
![](https://hackmd.io/_uploads/HyKMBTOgT.jpg)

*Include videos or screen captures of both the system and the controller.*

Videos:  

https://github.com/cctsao2000/Interactive-Lab-Hub/assets/60999245/fd85d695-298d-4a3f-9459-299b209cc3e0



## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Participants: Joanne Chen and Yichen

Answer the following:

### What worked well about the system and what didn't?

To make sure our idea is brand new, we integrated the latest tool OpenAI API into our design. The ability to transform speech from impolite to polite was our central focus, which worked really well. One part that could've been done better is that more functions could be added. Our current design only contains one function, that is to reframe words into a more polite way. One of our test user mentioned that the use case of the system is a little unclear. Potentially in the future, we can explore more functionalities. 

### What worked well about the controller and what didn't?

The controller used in this design is OpenAI API. By sending the speech detected from the webcam as the request input then ouput the response of the reframed speech. Both Joanne and Yichen thought the stength of our design is that we built our system on top of one of the most powerful tools nowadays, so that our design can tackle different queries and always provide an response. However, Joanne also mentioned that this could also be a double-edge sword, if the server-side of OpenAI has broken down then this controller will not be able to work.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

We used the OpenAI API to build an autonomous system. The most challenging part is to decide the prompt to create a smooth interaction. For example, there are cases that chatGPT is not able to revise users' sentences but instead reply the users. This may be solved by adding a clearer prompt to the system.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

How data could be collected:
- We could gather data on user feedback and use it to improve the quality of responses.
- Gather more data from users and calculate the average length of questions, then based on the result, adjust the default listening time to improve overall user experience.

Other sensing modalities to capture: 
- Emotional Tone (like IBM Watson “Tone Analyzer”)
    - Positivity/negativity of the question asked

- Facial Expression
    - Detect user's emotion state by using camera to further analyze how the system can address the user
- Extend of the Volume (dB)
