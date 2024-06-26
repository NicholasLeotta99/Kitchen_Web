# Digital Kitchen Manager

This application allows users to manage their kitchen through an interactive webpage. Users can view all pantry items and recipes in a recipe book. Pantry items can be added, updated, and deleted.

## Features

- Monitor pantry items
- Collect recipes

## Setup

1. Clone the repository
2. Run the container using `docker-compose up`
    i. The application will be available at `http://localhost:5000`
    ii. To run the container in detached mode, use `docker-compose up -d`
3. To stop the container, use `docker-compose down`
   
## Database

The application uses two SQLite databases: `pantry.db` for pantry items and `recipe.db` for recipes. The databases are managed using Flask-SQLAlchemy.

## Templates

The application uses Flask's templating engine to render HTML pages. The main templates are `open_pantry.html` for displaying pantry items and `recipe_book.html` for displaying recipes.

## Styles

The application uses CSS for styling. The styles are defined in `styles.css`.

## Ignored Files

The `data` directory is ignored by Git. This directory contains the SQLite database files.