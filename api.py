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
2 clips of 45 seconds
All rise. 240-1160
United States v. 1320-2568
Raymond Reddington, CR 183656. 2624-6648
Magistrate Judge Roberta Wilkins now presiding. 6784-9224
Morning, you, honor. 9352-10152
Assistant U.S. 10216-10888
attorney Michael Cima for the United States. 10944-13112
Jerome Lonergan from the Office of the Federal Public Defender for the accused waived reading of the rights and charges, but not the rights thereunder. 13216-21080
So waived. 21160-21720
Your Honor, given the defendant's history, the government asked that he be remanded. 21800-25016
Yeah, I'm gonna calendar this for a month from today. 25048-27688
A month from today would be just perfect, you, Honor. 27824-29848
Thank you. 29864-30668
Your Honor, may I be heard? 30864-32868
I don't recommend it. 33044-34132
Mr. 34156-34356
Reddington, you have an attorney. 34388-35812
I strongly suggest you let him do the talking. 35876-38244
And I would, you, Honor. 38372-39604
No question. 39652-40164
But given how quickly things are proceeding, I get the distinct impression that Jerry here has a bus to catch. 40252-45940
I'm sorry, are we moving too fast for you, Mr. 46020-48532
Reddington? 48596-49480
I'm just saying there are important matters to discuss. 49820-53796
Such as? 53948-54772
Well, for starters. 54876-56164
Your Honor hasn't really considered the issue of Bailey. 56212-60260
Sir, you have been a federal fugitive for nearly three decades. 60910-66054
The FBI's number one most wanted. 66182-68678
You are the textbook definition of a flight risk and a danger to the community. 68774-73894
Now, let me be clear. 73982-75190
Even if you were prepared to submit every last dollar in circulation on the planet, I still wouldn't grant you bail. 75310-82150
Ever. 82310-83010
Okay. 84110-84790
I, for one, feel better knowing it was considered. 84870-87554
Anything else? 87702-88810
I'm afraid so. 88970-90470
May we approach? 92850-93990
Carefully. 94770-95870
You hang here, Jerry. 97890-99386
This will only take a sec. 99418-100950
Look at my face, Mr. 108130-109322
Reddington. 109386-109962
I'm not amused. 110026-110986
And I assure you, neither am I. 111098-112986
But? 113058-113356
But the fact remains, the prosecution has intentionally failed to inform the court of a critical factor in this case. 113418-120104
That is my immunity agreement with the federal government. 120272-127880
An agreement that expressly covers the charges before you and protects me from overzealous beavers like Mr. 128000-136072
Seema and his bosses. 136136-137672
Good Lord. 137816-138920
Your confidential informant, Mr. 139000-141752
Seema. 141816-142700
If there's an agreement I have, I haven't seen any evidence to prove it. 143200-147556
That's hardly a denial, Mr. 147708-150644
Reddington. 150692-151716
Is there anything you can offer this court to support the existence of an immunity agreement? 151908-156680
Assistant Director Harold Cooper of the FBI is here. 160140-163508
He may be able to shed some light on the matter. 163564-165840
Assistant Director Cooper, step up, please, sir. 166860-172130
Mr. 177990-178462
Cooper, I'm going to ask you this once and only once. 178526-181598
To your knowledge, is there currently an immunity agreement in place with this defendant? 181734-185870
Yes or no? 185950-186970
Yes. 190630-191410
Chambers. 193910-194590
All of you. 194670-195198
Now. 195254-195850
You talk. 201940-203320
I run a task force. 204020-205600
Officially, it doesn't exist. 206020-207740
Its purpose is to arrest high priority targets using intelligence obtained from Mr. 207900-212124
Reddington. 212172-212748
So main justice made a deal with the devil himself. 212844-215836
Shouldn't judges at least pretend to be impartial? 216028-219356
Your Honor, as I said, if such a deal exists. 219468-222300
Oh, it exists. 222380-223436
Harold and I have been at this for over five years now. 223548-226700
Of course, some of the people who originally approved it are either dead or have moved on, leaving Director Cooper to deal with that cover their asses crowd, who, by the way, are perfectly happy to milk this cow all the way to the slaughterhouse. 226820-240024
I'm sure the first question they asked in response to my arrest was whether I could still continue to be an effective asset while locked up in jail. 240152-247224
Am I right, Harold? 247272-248440
Mr. 248600-248984
Cooper, you tell your superiors at Main justice that I just ordered a hearing on the scope of the agreement, and I want a copy of it on my desk today. 249032-255736
I can't rule on a contract I haven't seen. 255808-257736
Understood. 257808-258552
Good. 258696-259380
We'll reconvene in the morning. 259930-261586
Mr. 261738-262114
Reddington, you have an attorney sitting out there who has no idea what he's gotten into. 262162-266242
I suggest you fill him in. 266346-268050
Actually, I don't think that'll be necessary. 268170-270466
Why's that? 270578-271634
Because after careful consideration of the circumstances, I feel it more prudent to represent myself. 271802-278450
"""),
    ],
    temperature=1,
    top_p=1,
    model=model
)

print(response.choices[0].message.content)

