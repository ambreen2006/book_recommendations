# book_recommendations

* [Overview & Problem Statement](#Overview)
* [Data](#Data)
* [Metrics](#Metrics)
* [Algorithm](#Algorithm)
* [Evaluation](#Evaluation)
* [Setup](#Setup)
* [Recommender App](#WebApp)
* [Limitations and Improvements](#Limitations)

## Overview

`Written Words` is a book recommendation platform which uses a mix of content based similarity and 
user preferences to make recommendations. The collection at the time of this writing host 808 books.

The recommendations can be viewed with the accompanying app or the notebook provided.

App on free Heroku hosting can be accessed @ [https://writtenwords.herokuapp.com/](https://writtenwords.herokuapp.com/)

## Data

Data used for books is a mix of [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) and 
web scraping.

## Metrics

The algorithm is evaluated based on `hit rate`. 

<a href="https://www.codecogs.com/eqnedit.php?latex=HitRate&space;=&space;(&space;\sum_{i=0}^{len(test)}&space;Hit&space;)&space;/&space;len(test)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?HitRate&space;=&space;(&space;\sum_{i=0}^{len(test)}&space;Hit&space;)&space;/&space;len(test)" title="HitRate = ( \sum_{i=0}^{len(test)} Hit ) / len(test)" /></a>

A user's preferred books are partitioned such that one book is left out from the test set. The partitioned books
are then sent to the algorithm (without the left out book) and book recommendations are obtained.

If the left out book is present in the recommendation then a hit is considered. 

## Algorithm

1. Content similarity matrix is created based on the cosine similarity between the genre's of the books.
   This is done separately and ahead of time in 
   [ML_Pipeline/Content_Similarity.ipynb](https://github.com/ambreen2006/book_recommendations/blob/master/ML_Pipeline/Content_Similarity.ipynb)
   
   <a href="https://www.codecogs.com/eqnedit.php?latex=Similarity(A,&space;B)&space;=&space;\frac{A&space;.&space;B}{\|{A}\|&space;\|{B}\|}&space;=&space;\frac{\sum_{i=1}^nA_iB_i}{\sqrt{\sum_{i=1}^n{A_i}^2}\sqrt{\sum_{i=1}^n{B_i}^2}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Similarity(A,&space;B)&space;=&space;\frac{A&space;.&space;B}{\|{A}\|&space;\|{B}\|}&space;=&space;\frac{\sum_{i=1}^nA_iB_i}{\sqrt{\sum_{i=1}^n{A_i}^2}\sqrt{\sum_{i=1}^n{B_i}^2}}" title="Similarity(A, B) = \frac{A . B}{\|{A}\| \|{B}\|} = \frac{\sum_{i=1}^nA_iB_i}{\sqrt{\sum_{i=1}^n{A_i}^2}\sqrt{\sum_{i=1}^n{B_i}^2}}" /></a> 

2. Score for each book that the reader has not reviewed is calculated by taking following into account:

    1. The cosine similarity (as in 1)
    2. Smoothed rating value of the average rating of the book itself. Here, I'm bucketing the rating, such that a range
       of ratings within a bucket is considered the same. 
       
       Anything below 3 is considered of weight 1,
       anything above 4 is weight 3 and in between is weight 2.
    3. Weight consideration of whether the reader has read the author of that book before.
  
       If the book shares author with the books reviewed by reader then the weight returned is 3, otherwise 1.
 
    4. Weight consideration of how the user rated the most similar book they had read.
    
       This weight is the user rating of the book to which the book in consideration is most similar to with respect to its genre.

1 and 2 takes are content based while 3 and 4 provides personalization to the recommendation.

```
    score[book] = book_similarity[book] \
                          * get_author_weight(book, read_authors) \
                          * get_ratings_weight(book) \
                          * get_user_book_weight(book, user_rating, max_similar_book)
```
## Evaluation

This is the 3rd iteration of the algorithm with the hit rate of `0.8`. The algorithm that only took into
account genre similarity and the average rating of the book scored hit rate of `0.56`

The notebook 
[Recommendations.ipynb](https://github.com/ambreen2006/book_recommendations/blob/master/ML_Pipeline/Recommendations.ipynb)
is used for the algorithm evaluation.

## Setup

### Local setup

* Clone repository: `https://github.com/ambreen2006/book_recommendations`
* Install packages from `written_words_jupyter.txt`
* Run `jupyter notebook` from `book_recommendations` folder.
* Open `Data_Exploration.ipynb` for more information on the data itself.
* Open `ML_Pipeline/Recommendations.ipynb` for running the recommendation class locally.

### For adding new genres

* Pull the submodule specified in `.gitmodules`
* Add to the sqlite database `Data/books.db`

The database looks like this:

![](Screenshots/books_db.png)

* Run `ML_Pipeline/Content_Similarity.ipynb` to generate new matrix.

### Local Flask App Setup

* Install `postgres` locally
* Create database `written_words`
* Set the app config `app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pgpass@localhost/written_words'`
  by replacing the URI with the local URI in `Flask_App/main.py`
* Install packages from `Heroku_Setup/requirements.txt`
* Run from `book_recommendations` directory `python Flask_App/main.py`
* Note that you cannot login with Facebook if running locally, however, test user is available but shared.

### Heroku Setup

* Run `python Heroku_Setup/preprare.py '<destination>'` from `book_recommendations`
* Follow Heroku Setup
* Create a postgres database
* Update the `app.config`
* Push to the heroku git branch

## WebApp

### Written Words - Recommender App

[https://writtenwords.herokuapp.com/](https://writtenwords.herokuapp.com/)

* The main page has two options: login with Facebook or the test user. Test user is shared so, anyone 
making changes to the list would be persistent.

![](Screenshots/main_page.png)

* `Written Words` Logo/hyperlink takes you to the login page. At this time no logout facility is provided.
* `Search` page allows searching by author and book names. The search result contains 3-buttons for the user to
identify their preference or rating: Fewer like that book, Maybe, More like that book.
  
  The `Fewer` feature is for future addition. Right now it is not considered.
  The `More` button translate into rating value 5.
  The `Maybe` button translate into rating value 3.
  
 ![](Screenshots/search_page.png)
 
 * `Home` page shows the selection made by the user.
 
 ![](Screenshots/home_page.png)
 
 To remove the rating, double click on the selected rating. To change the rating, click on another.
 
 * `Recommendations` page shows recommendations. It also has 3 options available.

![](Screenshots/recommendation_page.png)

## Limitations

### Limitations & Improvements

* The dataset seems to have a lot of series data available, I believe I could either exclude series books
or take into consideration what book the user had already read in series.

* I could use book based collaborative filtering for further diversifying the recommendations.

* I could use the 'Fewer' option to exclude the book if it was recommended.