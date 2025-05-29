import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        SystemMessage("""You are a viral segment identifier, where you are given a transcript and you find short video sections from the video engagement, viewer retention, and virality on platforms such as youtube shorts and instagram reels. The sections you choose should be on a same topic of interest, as well as have a coherent storyline where any issues brought up should have meaningful closure at the end. What is extremely important is a sustained section, be it a sustained interesting conversation on a certain topic or a cool scene with a sustained mini plot/narrative. Do not just pick a scene. Pick a sustained mini story with setting rising action climax and resolution. 
You should output a python format list of your selected scenes, with each scene being a tuple of its start and end time. DO NOT CUT OFF SENTENCES, ROUND UP FOR END TIMES NEVER DOWN.
The transcript will be given to you with sentence level start and end timestamps that are in milliseconds. You will be given a set amount of milliseconds and you should aim to choose sections which are approximately the given clip duration (given by your end time-start time for the final tuple). If instead you are given "Auto" you have the flexibility to choose segments of any length between 15 to 90 seconds you deem necessary to achieve a coherent, engaging scene. If a scene is way beyond the given duration scope do not include it.

As an example, this would be ONE good scene to choose:
The one requirement Alan had today about this episode was that we would all get dressed up in French Renaissance outfits. 15896-17000  
So right now he thinks we're all individually getting dressed up, but little does he know, he's actually the only one getting dressed up today. 17905-23997  
Do we feel bad? 24141-25287  
No. 25491-26085  
We're gonna see what it looks like first. 26185-27185  
I feel bad. 27245-28197  
Has he got full makeup on? 28381-29893  
Yes. 29949-30469  
What if he doesn't react at all? 30597-32401  
Dude, look at us. 32653-33893  
What if he just thinks this is the most normal? 34029-38185  
You look great. 42825-43965  
Thank God. 48025-48849  
Dude, look at your face. 48897-51713  
Have you seen your face? 51769-53165  
You look great, Alan. 53705-54865  
Oh, my gosh, you're blushing, mate. 54945-57841  
You're blushing. 57873-58785  
Is that the kid who wears a school uniform on mufti Day? 58945-61725  
Like auditioning for Les Miserables? 62265-64065

It is a complete section of the video that talks about Alan being pranked with a start of explaining the prank and resolution of the prank being played out fully. It is also engaging as it's fresh and funny.
For this scene you would put (15896, 64065)

Your job is to find multiple of these scenes and output them in a python list. Quality over quantity. Always finish sentences and storylines over trying to match exactly the given time. Importantly, do not cut off sentences.

Example Output:
[
    (0, 25120),
    (15896, 64065),
    (103350, 126500),
    (243500, 360800)
]"""),
        UserMessage("""
2 clips of 40 seconds
Sam. 240-14800
Chip, what makes you think that I'm gonna let the whitest man that I have ever seen interview for our firm? 30710-36630
Because I have an appointment. 38150-39510
Thanks. 43190-43750
You can do this. 67890-68530
Kid, what is wrong with you? 87650-89390
You look like you're 11 years old. 89390-90830
I was late to puberty. 91150-92590
Okay. 93390-94030
Thank you. 96190-96830
I respect Burrito. 98750-123920
Come on. 124160-124800
Uh, excuse me. 125520-126560
I was thinking about going for a swim. 127120-128600
Are the pool facilities here nice? 128600-130319
Of course, sir. 130720-131600
It's the Chilton Hotel. 131600-132880
Best in the city. 132960-133920
Why is the pool closed? 135600-137000
And do you have the time? 137000-138240
It's ten o' clock. 138800-142560
Thanks. 143840-144320
I saw your gun. 149190-149950
Oh, you think that's him? 149950-151030
Match his description. 156870-157910
But he didn't go in the room. 158310-159310
It's 10. 159310-159750
Exactly. 159750-160150
He's just walking by. 160150-161030
Go after him. 164950-165710
Stay in the radio. 165710-166550
Rick Sorkin. 189730-190690
Rick Sorkin. 191730-193090
Rick Sorkin. 196610-197730
Excuse me, Mr. 198690-199650
Sorkin, you are five minutes late. 199650-201490
Is there a reason why I should let you in? 201490-203330
Look, I'm just trying to ditch the cops, okay? 205490-207890
I don't really care if you let me in. 207970-209080
Internet. 209230-209710
Mr. 218590-218990
Spectre will be right with you. 218990-220190
What Can I get you anything? 221470-223270
A coffee or bottle of water. 223270-224990
Hi. 229550-230030
Rick Sorkin. 230270-231150
Harvey Spectre. 231150-231870
Nice to meet you. 231870-232670
Should you have a seat here? 232750-233790
Whoa, what's this? 235260-236860
Can I help you? 244540-245500
No. 247260-247660
Excuse me, Mr. 255100-256220
Tate? 256220-256620
Who are you? 256700-257420
My name is Lewis Slit. 257420-258540
I work for Pearson Hardman. 258540-259820
I have some information that I think will lead you to the conclusion that you're better served at Pearson, with me as your lead counsel. 260140-265820
I'm listening. 267640-268360
How the hell did you know they were the police? 271560-273720
I read this novel in elementary school. 274280-276440
Cops are staking out a hotel. 277560-279080
One of them dresses as a bellhop, the other is a man in a suit, and it was the exact same thing. 279080-283560
You read a novel in elementary school? 283640-286200
What? 287000-287280
I like to read. 287280-288040
And why'd you ask them what time it was? 289320-290920
Throw them off. 291400-292200
What kind of drug dealer asks a cop what time it is when he's got a briefcase full of pot? 293000-296680
Right? 296680-297080
We should hire you. 297560-298600
Jesus. 299480-299920
I'd give you the 25 grand as a signing bonus. 299920-302520
I'll take it. 303000-303800
Unfortunately, we only hire from Harvard. 304920-307240
And you not only did not go to Harvard Law School, you haven't even gone to any law school. 307320-313000
What if I told you that I consume knowledge like no one you've ever met and I've actually passed the bar? 313720-318040
I'd say you're full of crap. 319090-320210
That's a Barbie Legal handbook right there, Right? 321890-323890
Open it up. 325010-325730
Read me something. 325730-326370
Anything. 326850-327410
Civil liability associated with agency is based on several factors, including the deviation of the agent from his path, the reasonable inference of agency on behalf of the plaintiff, and the nature of the damages themselves. 332850-344770      
How did you know that? 346330-347290
I learned it when I studied for the bar. 347610-351050
Okay, hotshot, fire up this laptop. 353130-356890
I'm gonna show you what a Harvard attorney can do. 358490-362490
Pick a topic. 363130-364090
Stock option backdating. 365930-367290
Although backdating options is legal, violations arise related to disclosures under IRC section 409A. 367450-374810
You forgot about Sarbanes Oxley. 376040-377640
The statute of limitations render Sarbanes oxley moot post 2007. 377880-381720
Well, not if you can find actions to cover up the violation as established in the 6th Circuit, May 2008. 381880-387400
That's impressive, but you're sitting at a computer playing hearts. 388760-394520
Sorry. 396440-396920
If you want to beat me, you're gonna have to do it at something else. 396920-399320
How can you know all that? 400120-401400
I told you, I like to read. 401690-402970
And once I read something, I understand it. 403370-405730
And once I understand it, I never forget it. 405730-409130
Why take the bar? 409850-410730
"""),
    ],
    temperature=1,
    top_p=1,
    model=model
)

print(response.choices[0].message.content)

