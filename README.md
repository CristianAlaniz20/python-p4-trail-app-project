# Hiking Trails by City

This website was made for hiking enthusiasts. It allows users to search for hiking trails by entering a city name.

**Disclaimer: All trail and signup information you may see in the gifs below is for demonstration purposes only. It is not accurate!** 

## Usage

A user must make an account before getting access to the website features. Once logged in, a user can: 
* Search for hiking trails by typing in the name of a city
* Create their own review for a trail
* Read the reviews of a trail
* Save/Unsave a trail 
* Mark a trail as hiked/not hiked

A user can also view their account information which includes:
* Username
* Bio
* Account role
* List of saved trails
* list of hiked trails

A user also has the option of updating or deleting their account.

## Login / Signing Up

### Login

Logging is straightforward. Enter your credentials and click Log In.

### Signing Up

Only these fields are required to sign up:
* username
* password

The other fields are assigned a default value if left blank.

Additionally, all usernames are unique.

![Signup gif](gifs/Signup-ezgif.com-video-to-gif-converter.gif)

## Searching by City

Simply enter a city name, click search, and the results will be shown underneath.

If a city you entered is not in our database, you will be met with a message saying "Sorry, no trails were found!".

![Search by City gif](gifs/SearchForCity-ezgif.com-video-to-gif-converter.gif)

## Viewing Trail Page

After searching for a city and finding a trail that interests you, you can click the _View Trail Page_ button.

Doing so will allow you to:
1. View the trails information
2. Save the trail
3. Mark the trail as hiked
4. See a list of all the trail reviews
5. Create a review for the trail

![View Trail Page Image](images/ViewTrailPageSS.png)

## Creating a Review

To create a review press the _Create Review_ button. 

You will be redirected to a page. Once there, you can fill out the form and press the _Create Review_ button to create the review.

![Create Review gif](gifs/CreateReview-ezgif.com-video-to-gif-converter.gif)

## User Page

After clicking the _My Account_ button, you will be redirected to the user page. 

On this page you will be able to:
1. View your account information
2. Change account role
3. Update account information
4. Delete account
5. See a list of saved trails
6. See a list of hiked trails

![User Page Image](images/UserPageSS.png)

## Changing Account Role

This feature is exclusive to administrators.

## Updating Account Information

To update the account information:
1. click the _Update Account_ button
2. Enter your password to verify
3. Update the fields you wish to change
4. click _Update Account_

![Update User Account gif](gifs/UpdateAccount-ezgif.com-video-to-gif-converter.gif)

## Deleting Account

Deleting your account is straightforward. 

1. Click the _Delete Account_ button
2. Click the _YES_ button

![Delete Account gif](gifs/DeleteAccount-ezgif.com-video-to-gif-converter.gif)

## Introduction

Fork and clone this 

## Setup

### `server/`

The `server/` directory contains all of your backend code.

`app.py` is your Flask application. You'll want to use Flask to build a simple
API backend like we have in previous modules. You should use Flask-RESTful for
your routes. You should be familiar with `models.py` and `seed.py` by now, but
remember that you will need to use Flask-SQLAlchemy, Flask-Migrate, and
SQLAlchemy-Serializer instead of SQLAlchemy and Alembic in your models.

The project contains a default `Pipfile` with some basic dependencies. You may
adapt the `Pipfile` if there are additional dependencies you want to add for
your project.

To download the dependencies for the backend server, run:

```console
pipenv install
pipenv shell
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

Check that your server serves the default route `http://localhost:5555`. You
should see a web page with the heading "Project Server".

### `client/`

The `client/` directory contains all of your frontend code. The file
`package.json` has been configured with common React application dependencies,
include `react-router-dom`. The file also sets the `proxy` field to forward
requests to `"http://localhost:5555". Feel free to change this to another port-
just remember to configure your Flask app to use another port as well!

To download the dependencies for the frontend client, run:

```console
npm install --prefix client
```

You can run your React app on [`localhost:3000`](http://localhost:3000) by
running:

```sh
npm start --prefix client
```

Check that your the React client displays a default page
`http://localhost:3000`. You should see a web page with the heading "Project
Client".

## Generating Your Database

NOTE: The initial project directory structure does not contain the `instance` or
`migrations` folders. Change into the `server` directory:

```console
cd server
```

Then enter the commands to create the `instance` and `migrations` folders and
the database `app.db` file:

```
flask db init
flask db upgrade head
```

Type `tree -L 2` within the `server` folder to confirm the new directory
structure:

```console
.
├── app.py
├── config.py
├── instance
│   └── app.db
├── migrations
│   ├── README
│   ├── __pycache__
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── models.py
└── seed.py
```

Edit `models.py` and start creating your models. Import your models as needed in
other modules, i.e. `from models import ...`.

Remember to regularly run
`flask db revision --autogenerate -m'<descriptive message>'`, replacing
`<descriptive message>` with an appropriate message, and `flask db upgrade head`
to track your modifications to the database and create checkpoints in case you
ever need to roll those modifications back.

> **Tip: It's always a good idea to start with an empty revision! This allows
> you to roll all the way back while still holding onto your database. You can
> create this empty revision with `flask db revision -m'Create DB'`.**

If you want to seed your database, now would be a great time to write out your
`seed.py` script and run it to generate some test data. Faker has been included
in the Pipfile if you'd like to use that library.

---

## Updating Your README.md

`README.md` is a Markdown file that describes your project. These files can be
used in many different ways- you may have noticed that we use them to generate
entire Canvas lessons- but they're most commonly used as homepages for online
Git repositories. **When you develop something that you want other people to
use, you need to have a README.**

Markdown is not a language that we cover in Flatiron's Software Engineering
curriculum, but it's not a particularly difficult language to learn (if you've
ever left a comment on Reddit, you might already know the basics). Refer to the
cheat sheet in this lesson's resources for a basic guide to Markdown.

### What Goes into a README?

This README should serve as a template for your own- go through the important
files in your project and describe what they do. Each file that you edit (you
can ignore your migration files) should get at least a paragraph. Each function
should get a small blurb.

You should descibe your application first, and with a good level of detail. The
rest should be ordered by importance to the user. (Probably routes next, then
models.)

Screenshots and links to resources that you used throughout are also useful to
users and collaborators, but a little more syntactically complicated. Only add
these in if you're feeling comfortable with Markdown.

---

## Conclusion

A lot of work goes into a full-stack application, but it all relies on concepts
that you've practiced thoroughly throughout this phase. Hopefully this template
and guide will get you off to a good start with your Phase 4 Project.

Happy coding!

---

## Resources

- [Setting up a respository - Atlassian](https://www.atlassian.com/git/tutorials/setting-up-a-repository)
- [Create a repo- GitHub Docs](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Python Circular Imports - StackAbuse](https://stackabuse.com/python-circular-imports/)
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
