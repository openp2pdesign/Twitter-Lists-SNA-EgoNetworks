# Twitter-Lists-SNA-EgoNetworks
Python scripts for analysing social networks on Twitter through Ego Networks of accounts on lists or searched by keywords

<a href="http://dx.doi.org/10.5281/zenodo.18209"><img src="https://zenodo.org/badge/doi/10.5281/zenodo.18209.svg" alt="10.5281/zenodo.18209"></a>

## Description
There are three scripts:

- **twitter-lists-egonetworks.py**: ask you for a Twitter username, from which you can select multiple lists. The script will then analyse the connections (followers/following) among all the accounts in the lists, and save the results as a .gexf file.
- **twitter-search-egonetworks.py**: indicate the keywords to be searched in the *keyword* variable. The script will then search for users on Twitter with those keywords and then analyse the connections (followers/following) among all the accounts, and save the results as a .gexf file.
- **data_anonymization.py**: loads a .gexf file and save an anonymized version.

## Requisites

```
pip install networkx
```
```
pip install twitter
```

## Instructions

- **twitter-lists-egonetworks.py** / **twitter-search-egonetworks.py**: Create a Twitter App [here](https://apps.twitter.com/app/new). Edit the file and add the details of the app, and run the script with:
```
python twitter-lists-egonetworks.py
```
or
```
python twitter-search-egonetworks.py
```

- **data_anonymization.py**: Edit the file and add the filename for the .gexf input and output files, and run the script with:
```
python data_anonymization.py
```

## License
[GPL v.3.0](http://www.gnu.org/licenses/gpl.html)
