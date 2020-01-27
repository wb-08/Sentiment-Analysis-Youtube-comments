
Sentiment-Analysis-Youtube-comments 
============================================

This repository helps you analyze comments for any russian YouTube video.

Highlights of our annotation policy:
-------------------------------
1.negative and positive sentiment classes cover both implicit and explicit sentiment, 
both for expressing emotion and attitudes;

2.neutral class: unmarked for sentiment;

3.speech act class: social media posts often include formulaic greetings, thank-you posts and congratulatory posts, 
which may or may not express the actual sentiment of the sender;

4.skip class: for unclear cases, noisy posts, content that was likely not created by the users themselves
(poems, lyrics, jokes etc.).

Dependencies
--------------------

+ Python3.6+
+ requests
+ lxml
+ cssselect
+ linux
+ https://github.com/bureaucratic-labs/dostoevsky


Usage
-----------
Run circular_diargram.py.Then enter the video id:

![изображение](https://user-images.githubusercontent.com/42088646/73200387-b9911d00-4147-11ea-8d01-b48053979fcf.png)


Then the files should appear:

- diagram.png
- negative.txt
- neutral.txt
- positive.txt
- skip.txt
- speech.txt
