# Rule-Based Poem Generator

## Introduction

This is a rule-based Chinese poem generator. 
Given some keywords provided by a user, we can generate both Song iambics and classical quatrains
that strictly conform to their format restrictions.

[learn.py](learn.py) is used to train the word model and to specify the tonal and rhyming constraints.
The word model will be generated in the ./model/ directory.

[test.py](test.py) is used to generate poems using the word model that has been trained. 

A command line argument should be provided as the path of the user input file,
which should contain format and content restrictions.

## Learning

    python learn.py <training_data_path>

![image](http://www-scf.usc.edu/~jiaqigu/544/learn.png)

## User Input File Format

Each line except the last one will be used as a guideline to generate a new poem.

The first word of a line is the format restrction of the poem, 
either the tune name of a Song iambic or the sentence length of a quatrain,
followed by a list of keywords which will restrict the content of the poem.
The keywords provided by a user must be those in the trained word model.
Words in each line should be split by spaces.

The last line should be string "END".

![image](http://www-scf.usc.edu/~jiaqigu/544/user_input.png)

## Let's generate some poems!

    python test.py <user_input_path>

![image](http://www-scf.usc.edu/~jiaqigu/544/test.png)
