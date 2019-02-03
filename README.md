# YouTube Music RESTful API
### Flask-RestPlus & SQLAlchemy
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php) [![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

A simple RESTful API connected with YouTube API.

## Motivation
This is meant to be a hands-on learning project for anyone who wants to understand how RESTful API's works and their potential.

## Screenshots


## Features
- Saves the music videos information in a relational database.
- Retrieves the last 50 YouTube **music** videos that you liked.
- Add and delete videos.

## Prerequisites

For gathering the videos from the auto-generated liked music list from YouTube, you'll need a `client_id.json` file with the credentials from Google.

To get the file:
1. Use this [wizard](https://console.developers.google.com/flows/enableapi?apiid=youtube) to create or select a project in the Google Developers Console and automatically turn on the API. Click **Continue**, then **Go to credentials**.
2. On the **Add credentials to your project page**, click the **Cancel** button.
3. At the top of the page, select the **OAuth consent screen** tab. Select an **Email address**, enter a **Product name** if not already set, and click the **Save** button.
4. Select the **Credentials** tab, click the Create credentials button and select **OAuth client ID**.
5. Select the application type **Web application** and enter the name "YouTube Data API". Under **Authorized redirect URIs**, add `http://localhost:8090/oauth2callback`, which is the default redirect URL used in the code.
You can specify a different redirect URI. If you do, then you may also need to change the sample code to launch the web server at an address other than `http://localhost:8090` and/or to specify a callback endpoint other than `oauth2callback`.
6. Click the **Create** button.
7. Click the download icon (Download JSON) button to the right of the client ID.
8. Move the downloaded file `client_id.json` to your working directory.

**Note**: The program works without this prerequisite.

## Installation

This project uses `Pipenv` for managing the dependencies.
1. `$ pip install pipenv`
2. In the project directory install the dependencies and create the environment `$ pipenv install`
3. To activate the project's virtualenv, run `$ pipenv shell`. Alternatively, run a command inside the virtualenv with `$ pipenv run`.

## How to use?

1. In the environment shell or using `$ pipenv run`, run `$ python app.py`
Immediately after, the Flask local server located in `http://localhost:8090/` will start:
```
bash
$ pipenv run python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://localhost:8090/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```
2. 

## Contribute
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/chmbrs/)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

Feedbacks, questions, critics, ideas, etc. are extremely welcome.

## References

- [Pipenv](https://pipenv.readthedocs.io/en/latest/basics/) - Pipenv basic usage
- [YouTube API](https://developers.google.com/youtube/v3/docs/playlistItems/list#usage) - Playlist Items usage
- [YouTube Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python) - Python Quickstart
- [Flask-RestPlus](https://flask-restplus.readthedocs.io/en/stable/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

## Credits

- [Pipenv Guide](https://realpython.com/pipenv-guide/)
- [Pretty Printed](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ) -  Awesome Tutorials on Flask
- [Well structured Rest APIs](https://medium.com/ki-labs-engineering/designing-well-structured-rest-apis-with-flask-restplus-part-1-7e96f2da8850) - Excellent Medium Post
- [Flask RestPlus Server](https://github.com/frol/flask-restplus-server-example) - Nice Example

## License: MIT
Copyright (c) 2019 Juan José Chambers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

MIT © [Juan José Chambers](https://github.com/chmbrs/)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/chmbrs/)
