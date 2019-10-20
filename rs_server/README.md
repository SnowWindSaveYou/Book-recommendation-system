# Book-recommendation-system

## Dependences
```
flask
flask_sqlalchemy
pytorch
numpy
```

## Prepare data
to deploy this system must first to setup mysql.
and the data is from: `https://www.kaggle.com/zygmunt/goodbooks-10k`
you can download it by `kaggle datasets download -d zygmunt/goodbooks-10k`

After enable mysql must first create dataset`bookrs`
then run the file: `PrepareDataset.ipynb` or `setup_sql.py`

## Start application
after setup the environment and sql, you can start application by runing `app.py` file, this is a web server based on python flask.