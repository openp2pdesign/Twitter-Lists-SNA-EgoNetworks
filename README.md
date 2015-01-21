# Twitter-Lists-SNA-EgoNetwork
A python script for analysing social networks on Twitter through Ego Networks of lists of accounts

## Description
There are two scripts:

- **twitter-lists-egonetworks.py**: ask you for a Twitter username, from which you can select multiple lists. The script will then analyze the connections (followers/following) among all the accounts in the lists, and save the results as a .gexf file.
- **data_anonymization.py**: loads a .gexf file and save an anonymized version. 

## Requisites

```
pip install networkx
```
```
pip install twitter
```

## Instructions

- **twitter-lists-egonetworks.py**: Create a Twitter App [here](https://apps.twitter.com/app/new). Edit the file and add the details of the app, and run the script with:
```
python twitter-lists-egonetworks.py
```
- **data_anonymization.py**: Edit the file and add the filename for the .gexf input and output files, and run the script with:
```
python data_anonymization.py
```

## License
[GPL v.3.0](http://www.gnu.org/licenses/gpl.html)

