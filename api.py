"""Run this model in Python

> pip install azure-ai-inference
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential('1.'),
)
with open("prompt.txt", "r") as file:
    system_message = file.read()
    
response = client.complete(
    messages=[
        SystemMessage(system_message),
        UserMessage(
"""30000

I somehow have unrestricted access to all of the great pyramids of Egypt. 320-5768
Whoa. 5944-6520
No. 6600-6888
This is the coolest thing I've ever seen. 6944-8328
We'll be going into the tombs of ancient pharaohs, places that are literally illegal to enter because they're incredibly dangerous. 8384-15848
What if we fall? 15944-16808
Oh, yeah, you'll definitely die. 16864-17944
We'll even be swimming to a secret underground tomb beneath the pyramids. 17992-21784
Oh, my God. 21832-22424
We've only been granted 100 hours to explore, and we're gonna start right now. 22472-27944
Follow me, boys. 28032-29000
It's about to be fun. 29080-30216
This is so beautiful. 30288-31820
Someone 4500 years ago Put this rock right here. 31960-34868
Correct. 34924-35252
This pyramid dates back to about 4,500 years old. 35316-38996
The passageway we're in leads to what Egyptologists say is King Khufu's tomb. 39068-43604
The pharaoh who may have ordered the pyramids to be built. 43652-46372
Whoa. 46516-47316
Hey. 47508-48280
This room is called the Grand Gallery. 48780-51940
What percentage of this pyramid do you think we've seen so far? 52020-54484
We might never know the answer to that question. 54572-56804
That's the coolest way he could have answered that. 56972-58660
This next room was the king's final resting spot, as far as we believe. 58700-62148
Yeah. 62204-62532
Let's do it. 62596-63520
Whoa. 67000-67860
Holy crap, boys. 68440-69940
What is this? 70600-71820
4,600 years ago, this chamber may have contained the king's mummified body. 72440-77760
This is where the pharaoh was buried. 77880-79744
This is what we believe is the final resting place. 79872-83472
Believe? 83576-83936
How do we not know? 84008-84816
I think somewhere inside this pyramid there's another chamber that we have not found yet that might have the body of the king. 84888-93504
You know what in this video we're gonna find? 93552-95492
We will literally be exploring from hundreds of feet below the pyramids up to the highest point in the largest ancient pyramid on Earth. 95656-103708
Woo. 103804-104364
That was awesome. 104492-105980
Before we go explore the other giant pyramids, I want to show you guys base camp. 106140-109932
Yeah, this is nice. 110036-110956
We got a dinner table, some tents to sleep in, and yo. 110988-116556
Wow. 116748-117308
Okay. 117404-117980
We even brought lights so you could see the pyramids from camp. 118060-121244
That's got to be the most expensive nightlight that's ever existed. 121332-123920
This is the pyramid we're going to explore tomorrow. 124260-126220
I want to start at 5am Everyone get some sleep. 126300-129100
These pyramids were so technologically advanced for their time that some credit them to a pre Egyptian civilization, while some point to even crazier theories, like aliens. 129600-139016
But Egyptologists are sure that they were built by the first Egyptians as tombs for their kings. 139048-143912 
And by the end of this video, we're gonna find out which of these theories is true. 143976-147400
All right. 147480-147800
Boys, I hope you're ready to explore the next pyramid on our list. 147840-151016
The Pyramid of Khafre. 151088-152552
What is special about this monstrosity? 152616-155128
Well, this pyramid is how we learn how the casings of each pyramid look like. 155224-158872
This is how all looked like at some point. 158896-160916
That was right after the aliens built them. 160988-162628
No aliens. 162684-163828
Rami led us nearly 100ft below the Earth's surface, deep into Khafre's pyramid. 164004-169124
This is a place where hardly anyone in the modern world has ever been. 169172-172964
So to be honest, we had no idea what to expect going down here. 173052-177200
The ancient Egyptians had cardboard. 178140-180360
We believed that this was the burial chamber for King Khafre for the longest time. 180780-185140
And now they're using it to store stuff. 185260-187464
Well, they're restoring the pyramid, Jimmy. 187652-189568
They gotta use tools. 189584-190608
So that means there's a real burial chamber. 190704-192640
Yes. 192720-193072
Rami actually took us to the real resting place thought to have once held the body of King Khafre. 193136-198384
I see a big ceiling. 198432-199568
Whoa, dude, we're deep in this pyramid. 199664-201760
Here we are. 201840-202736
The final burial chamber of King Khephren. 202888-206224
No. 206352-206640
This is the coolest thing I've ever seen. 206680-208272
What the heck, bro? 208376-210592
What is this? 210696-211552
Wait, look at the date, the graffiti. 211656-214496
Right there is the guy who discovered this tomb. 214528-216464
He claims he discovered this tomb. 216592-218576
Yes. 218608-218864
This is where the Pharaoh was buried. 218912-220448
This is the final resting place for King Khafre. 220544-223392
Is it disrespectful to laying there? 223456-225168
I wouldn't worry about the disrespect so much as much as the curse. 225224-230096
What does the curse do to you? 230208-231740
Do you want to try? 232040-233260
No. 234120-234624
Alright, let's get out of here before we get cursed. 234712-236992
Oh my gosh. 237056-238176
That pyramid is insane. 238368-240240
The king's tomb didn't really answer many of our questions. 240320-243152
However, the portal to the underworld deep beneath the pyramids could have everything we were looking for. 243216-248324
This is the tomb of God Osiris, where very few humans have ever been. 248392-253052
What are we doing? 253156-254284
As you can imagine, the God of the underworld's tomb is pretty deep underground. 254372-258620
Oh, heck no. 258700-260040
It really just goes all the way down there. 260340-262680
After you, Carl. 263060-264156
Oh my gosh. 264268-265292
Oh my gosh. 265436-266560
Why is he walking down so nonchalant? 266900-269520
This is the entrance, Carl. 269940-271868
Yeah, to the God of the underworld. 271964-276240
This is a tall ladder. 277300-278620
It's actually really deep. 278700-280160
Oh yeah, you'll definitely die. 280880-282136
Yeah, this is getting pretty scary. 282168-286008
I don't like this anymore. 286184-287720
And if we weren't already scared enough, we then came across this 3,000 year old human. 287800-294152
Oh my God, why am I still holding this? 294336-296360
Dude, is this a part of the. 296400-297288
This is the skull, yeah. 297344-298344
Oh, my God. 298392-299240
When we go down there, we will be so far underground that there's a chance we pass out due to a lack of oxygen. 299320-304808
Correct. 304904-305688
Chandler is heading to Osiris resting place. 305864-308900
All right, here we go. 309640-311152
Oh, I'm in the water. 311256-312540
Whoa. 313240-314100
You can tell the air's pretty thin down here. 318600-321104
Wait, what is this? 321192-322016
This is a rock right here. 322088-322992
Is this a rock or a lid? 323016-324304
Right in the center of the room is the sarcophagus of God Osiris. 324432-328768
Right here is supposedly the gateway to the underworld. 328864-332032
Yeah. 332176-332832
So try to get in. 332976-334800
To the underworld. 334920-335840
Well, yeah. 335920-336672
Screw it. 336736-337104
Screw it, screw it, screw it, screw it. 337112-338700
Oh my God. 339240-339952
This sarcophagus is allegedly the portal to the underworld. 340016-343212
And virtually no humans have ever been here before. 343276-345996
How deep are you? 346068-346732
Oh, my God. 346756-347580
Why am I here? 347740-348540
Why? 348580-348876
I'm a YouTuber. 348948-349772
What are we. 349836-350444
Look all the way to that right corner up there. 350532-352908
That's a shaft that goes to nobody knows where. 352964-354940
Carl, get up in there. 354980-356236
I can go up there. 356388-357388
Jimmy, don't let him. 357444-358348
I'm so scared, bro. 358404-359612
Carl, that's not smart, dude. 359716-361756
I'm literally in a tunnel in ancient Egypt that nobody's ever been before. 361788-364924
No one is crazy enough. 365012-366460
Can you explain to us what's happening? 366580-368988
I'm in a turn in the cave and it's getting thinner, dude. 369084-373176
I'm literally like actually like actively kind of stuck in this thing. 373208-376900
Haro, you're making history. 378560-380232
I got like one inch of clearance, bro. 380416-383736
It's been longer than the safe limit for oxygen. 383888-387260
I'm ready. 389520-390328
So before we literally all die and see the underworld for ourselves, there's no gracefully doing this, is there? 390424-395640
We got out of there as quick as we could because I wanted to live long enough to explore the never before seen shafts of the great pyramid of Giza. 395680-402744
Where literally less people in modern better times have been than have gone to space. 402792-407120
Who wants to ride a camel with me? 410060-411620
Let's do it. 411660-412484
Pet him, pet him. 412572-413780
He doesn't want it. 413820-414708
Have you ever been bit by a camel? 414764-416292
Yes. 416356-416836
What? 416948-417364
Yeah. 417452-417812
Does it hurt? 417876-418500
Yes. 418580-419240
Oh, I told you. 419820-421412
Another big day of exploring ahead. 421516-423524
This is unbelievable. 423612-424772
Chandler, are you good? 424836-425716
Oh, no. 425788-427396
Bullet, bullet. 427548-428708
I can't. 428884-429716
Give me off the screen, bro. 429828-431360
Dude, it looks so good. 432300-434132
This is probably one of the coolest shots ever. 434316-435940
Me just right to camel by one of the great pyramids of Egypt, bro. 435980-438720
This is absolutely insane. 438760-440640
And now the director of the entire Giza Plateau is joining us for the third pyramid on our list, the pyramid of Menkaure. 440720-447920
If you look at the bottom, you'll still see some of the granite from 4,600 years ago remaining. 448000-452432  
Here's an illustration of what they think it used to look like. 452496-455340
Wow. 455800-456656
But now this is all that remains. 456848-458512
Almost 5,000 years later. 458576-460016
This is my friend Nolan. 460088-461360
Can we send him to go scout up there? 461440-463340
Yes. 464700-465480
I got permission to do something normally illegal. 466460-468788
Nolan, be careful. 468884-469860
Can you just, like, start yelling at Nolan? 469940-471716
He'll freak out. 471748-472356
You don't really get many opportunities to climb up here. 472428-474612
But I want to take it, bro. 474636-476160
Engine, engine, engine, engine. 476860-480852
Down. 480916-481284
Yes, Down. 481372-482212
All right, Nolan. 482316-482996
Not a bit. 483028-483332
You gotta come down. 483356-483940
Come on. 483980-484388
Yeah, I'm going down. 484444-485508
Engine. 485564-486164
Yallah. 486292-487028
Yella. 487124-487828
Hey, he's kidding. 487924-488756
Keep going. 488788-489140
He's kidding. 489180-490040
That was a joke. 490940-492004
Oh, my God. 492132-493108
Get me freaking out. 493204-494468
Oh, my God. 494524-495156
I thought I was gonna get arrest. 495188-496400
Lead the way, sir. 496840-498224
Let's do it. 498352-499360
Whoa, wait, wait. 499480-500608
Point the camera down there. 500624-501616
Why is it so dark? 501688-503056
You switch the light off. 503168-504816
Oh, okay. 504968-506224
That would explain it. 506352-507376
All right, lead the way. 507448-508384
The initial descent of the pyramid took us down a shaft over a hundred feet below the ground to the very first chamber in ancient Egyptian history to have decorative carving. 508472-517200
What is this a decoration of false doors? 517280-520336
We didn't have any decoration inside any pyramid from the false dynasty except this one. 520448-525968
So this was done four or five thousand years ago? 526024-528180
4,600 years. 528280-529836
Furthering our journey deeper into the pyramid. 529908-531964
The next shaft brought us to Menkaure's antechamber. 532012-535484
Whoa, bro. 535612-536988
So much history in here. 537044-538156
What's in that room? 538228-539036
I can't tell you. 539108-539916
Nothing there. 539988-540588
Have you been up there? 540644-541612
No. 541716-542316
How do you know nothing's up there? 542468-543580
Because I can see from here. 543620-544908
Oh, yeah. 545044-545804
You see? 545932-546524
It's just a tunnel. 546612-547356
Nothing there. 547388-547948
Okay. 548004-548316
Yeah. 548348-548508
You can see? 548524-548908
Yes. 548964-549580
Always be skeptical. 549740-550844
The pyramid of Menkaure, known for its complex passageways, had one final descending shaft that led to the burial chamber. 550892-557804
So this is the king chamber, and it has a vaulted ceiling to relieve the weight. 557852-562936
How did they know that 5,000 years ago? 563048-564760
If you can build a pyramid, you can build anything. 564800-567192
You can do anything. 567256-568232
You can do anything. 568296-569416
On our way out, I got to thinking, why is there three more pyramids outside next to this one? 569608-574840    
What are these, three mini pyramids? 574880-576440
Ming Kaora, he got three small pyramids for the queens, the wives. 576520-580040
So Ming Kaora had three wives, and these are their tombs? 580120-582984
Yes. 583032-583352
Nolan, come over here. 583416-584920
Oh, God. 585040-585848
If he can have three partners, you can at least find one. 585944-588876
It's a work in progress. 589028-590220
I did discover a mummy. 590300-591596
She's not asking for money. 591628-592764
She's always listening to you. 592852-594156
Never talk too much. 594228-595340
It's a good choice for you. 595460-596588
Can you just offer me a mummy? 596644-597804
Yes. 597852-598316
The things we do to find you, love. 598428-600028
Our time with Ashraf was coming to an end. 600084-601948
And before he left, I wanted to hear his take on this. 602004-604412
So aliens didn't build the pyramids? 604516-606124
Aliens? 606172-606636
Come on. 606668-606972
Don't break my heart. 606996-607884
We have 124 pyramids all over Egypt. 607972-611660
So each time I'm calling aliens. 611740-613516
Come build a pyramid for me. 613548-614652
Cannot be like this. 614676-615644
Egyptians were the builders. 615732-617852
3. 617916-618458
What? 618604-618958
Don't bring up aliens again. 619014-620046
You did. 620118-620558
Egyptians built it. 620614-621422
If you can build a pyramid, you can do anything. 621446-624318
Yeah. 624414-625006
Let's go. 625118-626010
And by anything, I guess that also meant a massive, half human, half lion mountain of a sculpture, which I'm sure is crawling with secrets. 626310-635294
And now we're at the Sphinx with Dr. 635342-637182
Zahi, the man who basically found everything here. 637246-639838
I read online that there's a temple buried beneath the Sphinx filled with gold, and I'm on a mission to find out who is right, Dr. 639894-646174
Zahay or all the conspiracy theories on the Internet. 646222-648366
Okay, Jimmy. 648398-649134
Yes, sir. 649182-649970
Whoa. 651810-652362
Is that an entrance? 652426-653290
Yes. 653370-653914
I cannot believe I'm entering the Sphinx. 654042-656042
I want to see if that temple's real. 656106-657670
I'm not sure I'm going to fit. 658130-659434
You will. 659482-660170
Whoa. 660290-660874
This is cool. 661002-661818
All right, let's see if there's any hidden gold. 661914-663750
Zahay, I just see an empty hole. 664130-666682
Then I need you to give a statement. 666746-668442
Right now. 668546-669510
I need a statement. 670290-671274
All right. 671362-671642
Zahi, there's nothing inside the Sphinx. 671666-673642
Jimmy, we're going to make history. 673706-675696
And what better way to make history than by leaving a message for the future. 675818-679636
How long do you think this paper will survive down here? 679708-682196
Thousands of years. 682348-683540
Really? 683660-684036
We'll dig it now with the letter, Can I bury this gold Swarm. 684108-687828
Perfect. 687924-688452
This is worth $10,000. 688516-689924
Really? 690052-690720
This is for the future, yo. 691180-693220
And I guess the Internet conspiracy theories are right, because the Sphinx definitely has gold in it now, thanks to the rarest swarm in the entire world. 693300-700404
Guys, I'm trusting you not to steal this gold. 700492-702772
At this point, I was starting to wonder what the other boys were doing until I heard this sound. 702876-707236 
Above. 707268-707512
Above me. 707556-708240
Zahay, do you hear some helicopters? 708360-710420
I can't believe we're doing this. 713000-714912
Somehow the boys convinced the Egyptian military and government to let them fly around in helicopters while Zahi And I were exploring the Sphinx. 715016-721840
This is an awesome day. 721920-723260
But the coolest part of this entire experience is yet to be seen. 725400-729328
When you take us to the top of the great pyramid, you're gonna show stuff on camera that you've never shown before. 729384-734016
Amazing things. 734088-734976
No spoilers, bro. 735048-736256
This video's gonna keep getting better as we go on. 736328-738368
And before we climb the top of the pyramid, we thought, what better way to look for more hidden secrets than in a place that almost no one gets to go? 738424-746236
Rami, where are we? 746308-747404
We are at the tomb of Emery, one of the places that is completely illegal for people to go in. 747492-754520   
That's why you're gonna unlock it before we go in. 754980-757276
It's extremely, extremely important not to touch these walls. 757348-762364
Do you hear me, Nolan? 762412-763484
Loud and clear. 763612-764188
You stay out here. 764244-764940
Just. 764980-765132
Maybe I will not touch actual walls. 765156-767486
Finger food. 767518-768046
A wall toucher. 768118-769150
Wall toucher. 769310-769966
Hey, butter fingers. 769998-771134
Oh. 771262-771710
Ready? 771790-772366
Yeah. 772478-772862"""),
    ],
    model="gpt-4o",
    temperature=0.8,
    top_p=0.1
)

print(response.choices[0].message.content)
