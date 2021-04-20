

# [BazBlog](http://ex-blogg.herokuapp.com)
    A mini-blog application written with python's flask framework
    
### HOW TO RUN ON LOCAL MACHINE(windows)
- clone this repository
- run the following codes on the command line;
    - python -m venv venv/
    - pip install -r requirements.txt
    - set FLASK_APP=bazblog
    - flask init-db to initialize the database
    
- **flask run** or **python bazblog** on the command line to run the app.


### HOW TO RUN TEST
- pytest
- coverage run -m pytest
- coverage report
- coverage html

*This is a tutorial from flask official tutorial (flaskr)*
