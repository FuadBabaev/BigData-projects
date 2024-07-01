#!/opt/conda/envs/dsenv/bin/python

import sys, os
import logging
from joblib import load
import pandas as pd

sys.path.append('.')
from model import fields

numeric_features = ["if"+str(i) for i in range(1,14)]
categorical_features = ["cf"+str(i) for i in range(1,27)]

#
# Init the logger
#
logging.basicConfig(level=logging.DEBUG)
logging.info("CURRENT_DIR {}".format(os.getcwd()))
logging.info("SCRIPT CALLED AS {}".format(sys.argv[0]))
logging.info("ARGS {}".format(sys.argv[1:]))

#load the model
model = load("2a.joblib")

#fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
#num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

#read and infere
fields.remove('label')
read_opts=dict(
        sep='\t', names=fields, index_col=0, header=None,
        iterator=True, chunksize=100, na_values=['', 'NULL', '\\N']
)

for df in pd.read_csv(sys.stdin, **read_opts):
    df[numeric_features] = df[numeric_features].fillna(-1)
    df[categorical_features] = df[categorical_features].fillna("missing")
    pred = model.predict(df)
    out = zip(df.index, pred)
    print("\n".join(["{0}\t{1}".format(*i) for i in out]))