# book_recommendations

## Index

* [Overview & Problem Statement](#Overview)
* [Data](#Data)
* [Metrics](#Metrics)
* [Algorithm](#Algorithm)
* [Evaluation](#Evaluation)
* [Setup](#Setup)
* [Recommender App](#WebApp)
* [Summary](#Summary)
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

### Current Implementation

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


<a href="https://www.codecogs.com/eqnedit.php?latex=Score[Book]&space;=&space;CosineSimilarity[book]_{max}&space;*&space;AuthorWeight[book,&space;Authors_{reader}]&space;*&space;RatingWeight_{smoothed}[book]&space;*&space;BookRatingWeight_{user}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Score[Book]&space;=&space;CosineSimilarity[book]_{max}&space;*&space;AuthorWeight[book,&space;Authors_{reader}]&space;*&space;RatingWeight_{smoothed}[book]&space;*&space;BookRatingWeight_{user}" title="Score[Book] = CosineSimilarity[book]_{max} * AuthorWeight[book, Authors_{reader}] * RatingWeight_{smoothed}[book] * BookRatingWeight_{user}" /></a>


```
    score[book] = book_similarity[book] \
                          * get_author_weight(book, read_authors) \
                          * get_ratings_weight(book) \
                          * get_user_book_weight(book, user_rating, max_similar_book)
```

### Top-K Recommendations

After the recommendation list is returned, Top-K recommendation further manipulates the rating to add more diversity 
to the list by punishing repeated authors.

* Recall that the score returned is already sorted.
* The Top-K algorithm goes through the sorted list and multiplying the score the inverted cardinality of the number of
  times the author is already seen in the list and insert it in the priority queue.

```
    priority = -1 * book_recommendations[book] * (1 / authors_cardinality[authors])
```
    
  Multiplication with -1 is implementation details in order to repurpose the heap to return max first.

## Evaluation

### Process

Currently implemented algorithm is the 3rd major iteration.

#### First Iteration

The first iteration had the least personalization aspect to the algorithm. The brief steps and considerations were:

* The cosine similarity between the books and the ratings of the recommended books.
* When recommendations were requested, the algorithm returns a sorted list of books in the descending order of similarity
  with the books read and liked by the reader.
* The final Top-K recommendations were then the top list sorted in descending order by average rating of the books.

The `hit-rate` achieved by the algorithm was `0.56`.

#### Second Iteration
 
The second iteration attempted to increase the personalization aspect by increasing the weights based on the genres read
by the readers. So the book will have a greater multiplying factor if it belongs to genre most read by the reader, so it
takes into consideration the cardinality of the genres with respect to the number of books read by the reader for each
genre.

This however did not result in better `hit rate`.

The Top-K recommendation methodology remained the same as iteration 1.

#### Third Iteration

This iteration removed the weight by cardinality introduced by the 2nd iteration and instead added two different factors
for personalization.

* Author's weight: If the book shares the author of the books the user had already liked, it will have a higher multiplying
  factor.
* User's rating weight: Instead of looking at the cardinality of the common genres for a book in consideration, the most similar book 
  from the reader's reviewed book is found and the weight returned is the reader's rating for that book.
  E.g. If the reader rated 'Blink' as `4.2` and another similar book is being scored for recommendation and it is the most similar 
  to this book `Blink`, then the weight returned would be `4.2`

Initially, the author's weight was doubled but by returning 3 when a shared author is found, I was able to see more of the same authors 
in the recommendation list. I thought this to be a qualitative improvement. Even though, if I already like an author, 
I would generally not need them to be recommended but it gives an assurance and I'm most definitely going to want to read
an author I like.

#### Results

The 3rd iteration of the algorithm produced the hit rate of `0.8`. That means of the test set passed to the algorithm, with
one liked book left out intentionally, 80% of the time, the recommendation engine recommended that book to the test reader.

The algorithm that only took into account genre similarity and the average rating of the book scored hit rate of `0.56`

The notebook 
[Recommendations.ipynb](https://github.com/ambreen2006/book_recommendations/blob/master/ML_Pipeline/Recommendations.ipynb)
is used for the algorithm evaluation.

From the qualitative standpoint, the Top-K method further re-orders the list while limiting the number of results to K by
discouraging already seen authors.

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

## Summary

`Written Words` provides book recommendation based on the content similarity by genres and other personalization
aspect of the books such as the authors of the books read by the reader.

The project evolved from a very basic cosine similarity between genres to adding more features such as authors and user's 
rating in consideration. The quantitative metric hit-rate improved from 0.56 to 0.80.

It's definitely not easy to evaluate qualitatively, I could add other factors such as whether the user comes back to
rate the recommended books, or ask specifically, what they think of recommendations.

Other metrics that can be added would be to gauge diversity of the content so the user is not just shown the most similar
but also somewhat different but relevant content.

### Limitations

* The dataset seems to have a lot of series data available, I believe I could either exclude books in series
or take into consideration what book the user had already read in series. The nature of the series are generally 
clustered in some variation of fiction genre. I could consolidate the dataset to consider recommending the series 
as opposed to individual books in the series. Unlike book-sellers, here we are hoping people to discover new books, if the reader has
already read and liked a book in series, obviously they'll seek out the next in series, there is no point in recommending
a book in series 4 or 5, if they had either read none or book 1 in the series. 

Either the reader hasn't started on the series and we recommend it or the user has started on the series
and so we suppress the recommendation.

* 'Fewer' option isn't useful right now, I could at least exclude the book if it was recommended.

### Improvements

* There is a lot more unstructured data available that is not being used in making recommendations. There is definitely
  potential for experimentation.

* I could use book based collaborative filtering for further diversifying the recommendations.


## References

* https://www.udacity.com/course/data-scientist-nanodegree--nd025
* https://www.manning.com/livevideo/building-recommender-systems-with-machine-learning-and-ai
* [goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k)