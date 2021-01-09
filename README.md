# inMyCab!

## Table of contents
* [General information](#general-information)
* [Technologies](#technologies)
* [Features](#features)
* [Illustrations](#illustrations)
* [Status](#status)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license)

## General information

dansMonCab! is a tiny chatbot that provides the user with information (description, map, latest news) about a point of interest (e.g. a public place, a monument...).

Intended for French users, the language communication of dansMonCab! is French.

Feel free to [play](http://198.50.131.242/) with it! And be kind with Serge, our taxi driver, who sometimes will need you to spell again...

## Technologies

The application is programmed in Python 3.8 and relies on the framework [Flask 1.1.2](http://flask.palletsprojects.com/en/1.1.x/).

You can use the package manager pip to install all the required libraries.

```bash
pip3 install -r requirements.txt
```
***Do not forget to set you own environment variables and store them in .env file !***

## Features

The user enters a simple destination (e.g. "Musée du Louvre" and the app returns a clickable map and a short presentation extracted from [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) as well as the latest news provided by [NewsAPI](https://newsapi.org/s/france-news-api).

## Status

This project is in progress.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

* Initial work: Stephanie BLANCHET, Data Application Programmer.

## License

This project is licensed under the MIT License - see [MIT](https://choosealicense.com/licenses/mit/) for details.
