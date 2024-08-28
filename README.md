# UGAHacks-sponsor-Emailer

Email automation for cold emails

# How to use

You need a google cloud application client secret with Gmail api enabled.
in the data folder, there should be a file called check.csv that contains entries of previously-emailed people.
When running clean.py, you should have your new entries in a file called new.csv. After clean.py runs, you get a file called batch.csv.

main.py will take you to a google auth page, and afterwards it will loop through the batch.csv file email each at 5 second intervals.
