# Suffix Analyzer

## Brief

* Create a web application for analyzing word suffixes. It will take a suffix as an input, then retrieve a list of words that end with that suffix, along with their definitions. All of the definitions should be stored in a database such that the definition of any given word is never retrieved more than once.

* Lists of suffixes can be retrieved by querying “words ending in X” to the Wolfram Alpha API. Definitions of words can be retrieved by querying “define X”. The first definition given by the API is sufficient.
e.g., the query “words ending in gry” will give you a list of the words “angry, anhungry, hangry, hungry, unangry”, which you'd then retrieve the definitions of.
The interface should have a text input field for the suffix, and the output should pour in asynchronously as an unordered list.

* The format of the output should just be <word>: <definition>
e.g., angry: feeling or showing anger

* App ids for querying the Wolfram Alpha API can be acquired here: https://developer.wolframalpha.com/portal/signin.html

* Feel free to use whatever tools you'd prefer, but be prepared to defend your reason for using them. When you're finished, send us a link to the source repository with instructions for how to get it running.

## Setup

### Installing Tools

This project is built on the Python Flask framework.

```
sudo pip install virtualenv
cd <project>
virtualenv venv
. venv/bin/activate
pip install Flask
history
```

