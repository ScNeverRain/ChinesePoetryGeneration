# ChinesePoetryGeneration
# Introduction
learn.py is to learn the traning data and pingze constrains, it will produce some data models under ./model/ folder

test.py will generate the poem using these models prodeuced by the learn.py. It will take a user input file as a parameter, this input file contains the poem title and keywords. 

# learn
python learn.py YOUR_TRAINING_DATA
![image](http://www-scf.usc.edu/~jiaqigu/544/learn.png)

# user input file format
Every line will generate a poem, the first word is the poem title(what kind of poem should be generated), then is a list of keywords
The last line is the "END" string

![image](http://www-scf.usc.edu/~jiaqigu/544/user_input.png)

# Let's generate some poems
python test.py USER_INPUT_FILE

![image](http://www-scf.usc.edu/~jiaqigu/544/test.png)
