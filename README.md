This is a research Pan and I have done, which potential could be the topic for our master thesis.
But for now, it serves as our group project for Introduction to Digital Humanities, and DIP705.
**********************************
The research is:
•	To Understand Public Opinions in China
•	To find the Gap between Public Sentiment and Government Narratives
•	And to further analyze the mechanism of this gap: 
1.	Is it that the government is incapable of understanding the public needs, or is this gap between public opinion and government narrative intentionally neglected the public sentiment?
2.	And if it is intentional, does this intentional behavior actually show the priorities of the government, or potential concerns.
**********************************
About the webcrawler:

The webcrawler for Zhihu answers is named 01_Zhihu_Answer_SpiderV2.py
It has 3 files used in package named packages:
1_ The utils.py is responsible for converting the timestamp, gender of the users and clean the contents(removing duplicated texts and illegal characters and etc)
2_ The spider.py is used for scraping the data from Zhihu posts.
3_ The helper.py is used for getting the additional names for csv file and the directory.

When using the webcrawler, you need to first find Zhihu question ID
For example, this is a question in Zhihu containing 7 posts: https://www.zhihu.com/question/587848376 The question ID is the number at the end of the url, which is 587848376
After running the main program, you would need to input the question ID on the terminal. 
And then do what it asks, follow the instruction, input the directory you want the file to be stored, and the additional name for the file (which is in the formate of "知乎回答_question_id_additional_name")
The file would be stored as a CSV file to the directory you wish or the current directory.

And one more thing, make sure to use "utf-8-sig" instead of any other endocding format.
**********************************
The results:
The results are catigorized and put in seperate folders under Topic. 
You can check the result directly from the Jupyter Notebook.
The code is done with the help of ChatGPT, so the variable naming could be a little bit messy.
I'll refactor them when I have the time, but so far, they get the job done.
**********************************
I'll keep updating the results.
