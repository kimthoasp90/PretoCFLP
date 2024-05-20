DBLP Publications Records and ACM Metadata for SIGWEB Conferences
Published: 29 March 2016| Version 1 | DOI: 10.17632/dn5d8fbkb9.1
Contributors:
Swati Agarwal,
,
Description

The dataset ”DBLP-SIGWEB.zip” is derived from September 17, 2015 snapshot of dblp bibliography database. It contains all publications and authors records (available in dblp data) of 8 ACM SIGWEB conferences (HT, DL, DocEng, WebSci, CIKM, WSDM, UMAP, SIGIR): 
The dataset also contains the authors, chairs, affiliations and additional metadata information of conferences that are published in ACM digital library.

dblp-sigweb.sql file creates 14 tables in mysql. Followings are the list and description of all attributes and tables used in the dataset. Same attributes used in different tables are listed only once.

1. Table- papers
dblp_key- unique id of each publication in dblp database
crossref- unique id of each conference in dblp database
doi- unique doi url to publisher page
paper_id- unique id of each article in acm digital library (DL)
cite_count- number of citations for each article calculated for the papers published in acm DL
pages- number of pages for each article in conference proceedings
conf_id- unique id of each conference in acm DL
funding- funding source information of article. NULL- if no funcding source available

2. Table- paper_authors
author_id- unique id of an author in acm DL
affiliation- affiliation information of author for associated article

3. Table- concepts
concept- concepts in an article- tagged by ACM

4. Table- author_tags
author_tag- Keywords/tags provided by authors

5. cited_by
paper_id- acm DL id of article A to be cited
cite_id- unique id of article that has cited article A

6. paper_references
refer_id- unique id of the articles (published in sigweb conferences) cited in article A.

7. Table- conferences
dblp_key- unique id of each conference in dblp database
year- year of the conference
publisher- publisher name of each conference (ACM, Springer, IEEE etc.)
title- full name of the conference proceeding
doi- unique doi url to the conference publisher page

8. Table- general_chairs, program_chairs, editors
author_id- unique id of author (as general chair, program chair or editor of conference conf_id)
affiliation- affiliation of author

9. authors_affiliation_history, colleagues
author_id- unique id of author A in ACM DL
position- index of affiliation- starts from 0
affiliation- lists all affiliations of an author
colleague_id- lists acm IDs of all authors publishing papers in ACM co-authored with A.

11. authors_info
author_name- full name of author acquired from ACM publisher page
year_first- year of first article publication in ACM
year_last- year of recent article publication in ACM
pub_count- total number of publciations in ACM DL
cite_count- total number of citations mentioned in ACM publciations
avg_cite- average number of citation in ACM publications

12. affiliations_info
affiliation- name of the affiliation
affiliation_type- type of affiliatioin (Industry, Academic Institution)
city, state, country- geographical location of affiliation
lat, lng- geocodes (latitude and longitude) of affiliation

Files 5.74 MB
Steps to reproduce

Commands to import data in MySQL

mysql -u root -p; \\log-in to mysql
enter your password 
create database sigweb; \\create a new schema
use dblp; \\change the database
source filename.sql; \\import sql file
