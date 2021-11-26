# Spotify Song Retriver App 
## Project1
## By Sai Tippana
 
### Problems faced during development

1. One of the first problems encountered was figuring out how to give and retrieve the right fields of interest from the Spotify API. This was new to me since I had never worked with json before, meaning I had to learn how to parse through the values and get more familiar with python dictionaries.

I looked at resources such as w3schools.com and learned more about how to use python dictionaries properly, and spent time exploring the json file since there were many layers to access the data which I had to know in order to process it properly. This revealed to me how to parse such large dictionaries and format the information using simple python logic to make it usable.

2. Another problem was with the genius API itself. This issue was a matter of not knowing what to pull from the data the API returns. Genius was more confusing as the API documentation gave even less information than the spotify API.

After some tedious trial and error I was able to figure it out, but then I found the lyricsgenius library for python which uses the same authentication and genius API but formats the data in a much cleaner way, so I switched to that for the rest of development. This provided me with a faster way to traverse the API's return value and get just the lyrics without having to parse through a large dictionary like the Spotify one mentioned above.

3. Lastly, the front end was a bit of a hassle. I've never done much HTML or CSS before, I've only ever focused on the backend and especially have never used flask. This provided the challenge of learning more CSS to style my page better and making sure it scales according to the size of the window, which took many tries to perfect. 

After practicing a lot with different attributes in CSS, and learning more of the jinja syntax, I was able to mostly fix my errors and work towards making a clean webpage. The problem with this was that it was time-inefficient to relaod my webpage after every change, especially when its tiny changes that are hard to notice.


### Known problems that stil exist

1. The first would be the the fact that some of the songs do not have Spotify preview links. This is not my fault, but I will think of a better way to handle the songs that have missing links. This means displaying a message or an alternative instead of just a blank, unplayable audio embed in the HTML.

2. Another is that for some rare songs, instead of the lyrics, the Genius API gets an associated song list, which I haven't been able to isolate and deal with. I would like to find when the API returns a song list instead of lyrics and display a different message saying the API couldn't fetch the lyrics.

3. One last thing, a minor issue but still bugs me, is that everytime the lyrics are fetched, the API includes a small tag at the end of the lyrics text. It's 2 words that likely indicate a hyperlink or some other function in the source of the lyrics, but it shows as plain text when retreived through the API, very small issue but nonetheless, will likely prove to be a tedious fix.

### Future Improvements

1. I'd like to add some more navigation features, including a details page aside from the main page and lyrics page. Maybe even a page where users can look at all the artist's top songs instead of just one. 

2. I'd like to fix the #3 issue mentioned above, despite how small the issue is.

3. I would like to add dynamically changing backgrounds, that follow suit with the album art. How? I'm not sure, but I'm sure there's a way to overlay it onto my current background which I can figure out later.

4. Add a feature where users can search for any artist, not just the ones I input.

## Cloning and using this repository

1. After cloning, you will need to get your own spotify ID, spotify client secret, and genius authentication token. Upon getting those, place them in a .env file in the main directory that you cloned this repository to. This will allow the program to read from that env file when accessing the data for authentication. 

2. To run locally, please install all the python libraries listed in requirements.txt. 

3. Turn off any web extensions that modify the front end of the browser, such as it's HTML/CSS values as those will interfere with the visuals of this web program.

4. If desired, the artists on rotation can be changed in the "accessories.py" file in the "artists" list. Remember to get the correct spotify artist ID.

### Link to heroku deloyment (site)

https://floating-thicket-58797.herokuapp.com/
