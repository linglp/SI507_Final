ReadMe File
#####Overview: 
Data source: Yelp fusion and New York Times
Data base: Final_Proj (Three tables: SearchYelp, Stories, Location) 
Data Presentation: 
-A bar graph that shows the max and min of rating
-A bar graph that shows the show the name of places that have a higher rating than 4.0
-A map that shows all the places that you search
-A map that shows the location of the place you picked before

#####Usage 
####The program allows the user to search and store data. But to pass the uniitest, user has to follow the following step
##Q1: What places do you want to search for? Example: Chicago/Detroit/Ann Arbor
A: Enter "Chicago"
##Q2: What term do you want to search? (Example: food, restaurant, Starbucks)
A: Enter "food"
##Q3: What pricing level do you wish to see? (You can pick from 1-4. 1 is the least expensive, and 4 is the most expensive)
A: Enter "4"
##Q4:How many results do you want to see? Please enter an integer from 1-50.
A: Enter 50 
##Q5: Want to know more about the location of a place? Please enter an integer. Do not enter an integer out of the range!
A: Enter 4
##Q6: Do you want to see top stories of the term you search? Press 'Y' to continue
A: Enter Y 
##Q7: We have Four graph options. Please pick one!
A: User has to enter integer like this: 1,2,3,4 to see all graphs
(Please remember to seperate your search by ",")

####Data processing: 
The program has three types of data processing
<1> It could find out places that have rating greater than 4.0
<2> It could find out the best and the worst rating within your search

####Note
<1>Yelp could search a broader category than New York Times. Thus, if the term you pick in question1 is not "food", "automobiles", "books", "business" or "fashion", the program won't show you top stories about that topic in New York Times
<2>You can't receive more than 50 results from Yelp Fusion (Please refer to this document: https://www.yelp.com/developers/documentation/v3/business_search)
