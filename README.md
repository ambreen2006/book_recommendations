# book_recommendations

## Index

* [Overview & Problem Statement](#Overview)
* [Data](#Data)
* [Metrics](#Metrics)
* [Algorithm](#Algorithm)
* [Evaluation](#Evaluation)
* [Setup](#Setup)
* [Recommender App](#WebApp)
* [Limitations and Improvements](#Limitations)
* [References](#References)

## Overview

### Problem Statement 

This project is my submission for the [Udacity Data Scientist NanoDegree Program](https://www.udacity.com/course/data-scientist-nanodegree--nd025). The most important reason
why I chose to work on a book recommender system is that I'm a passionate reader and although there are several
solutions out there, the inherent nature of recommendation's viability being dependent on a person's idiosyncrasies, 
opens up this area to creative solutions from plethora of different approaches and point of views.

If you are buying a commodity product such as for example a shampoo, it might probably be logical to think that 
perhaps, you may also be interested in the conditioner. Or if you buy a cat's toy, then you might also be interested in
cat food, but I think that there will be less variability in your interest in buying what is recommended and or available.
Books unlike those kind of products span from a necessity or educational to entertainment and beyond. It is I believe a 
hard problem to figure out what you might want at a given point in time, because your mood to read something may change
from one point in time to another. When you are not looking for something specific, 
say for example a textbook or already have a book in your mind, then it is hard to know what you might be most likely
to purchase and there is always this struggle of recommendations being made to you for the purpose of selling the product,
such as the latest release of a book in the genre you've purchased before but a book released say for example few years
back may still be the perfect read for you but may not serve a business's purpose. 

### Objective

With, `Written Words` you can discover books similar to what you had read before and liked and not just only from that genre and hence allows gentle 
exploration of new content. The recommender system uses a mix of content based similarity and user preferences to make recommendations. 
I expect the project to become much more feature rich in the future allowing people to discover interesting books with 
consideration to their liking as well as the quality of the contents.

The collection at the time of this writing host 808 books.

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


## References

* https://www.udacity.com/course/data-scientist-nanodegree--nd025
* https://www.manning.com/livevideo/building-recommender-systems-with-machine-learning-and-ai
*  [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k)