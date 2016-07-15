from flask import Flask
from boto.s3.connection import S3Connection
import os
import logging, logging.config


app = Flask(__name__)
logging.config.fileConfig('conf/logging.conf')

access_key = os.environ['BROWSER_S3_ACCESS_KEY']
secret_key = os.environ['BROWSER_S3_SECRET_KEY']
bucket = os.environ['BROWSER_S3_BUCKET']
endpoint = os.environ['BROWSER_S3_ENDPOINT']
region_host = os.environ['BROWSER_S3_REGION']

@app.route('/', methods=['GET'])
def browse():
    logging.info("start browse")
    message = ""
    try:
        # conn = S3Connection(access_key,
        #     secret_key, host=region_host)
        # logging.info("conn: " + str(conn))
        # bucket_conn = conn.get_bucket(bucket)
        # logging.debug("bucket_conn: " + str(bucket_conn))

        conn = S3Connection(access_key,
            secret_key)
        logging.info("conn: " + str(conn))
        bucket_conn = conn.get_bucket(bucket, validate=False)
        logging.debug("bucket_conn: " + str(bucket_conn))

        logging.debug("")
        logging.debug("---------------")
        for key in bucket_conn.list():
            name = key.name
            modified = key.last_modified
            url = key.generate_url(expires_in=0, query_auth=False, force_http=True)
            x = '<p><a href="' + url + '">' + name + '</a></p>'
            message = message + x
            logging.debug("")
            logging.debug("name: " + name)
            logging.debug("modified: " + modified)
            logging.debug("url: " + url)
        logging.debug("")       
        logging.debug("---------------")
        logging.debug("")       

        logging.info("browse success")
    except Exception, e:
        message = "Error"
        logging.info("browse fail: " + str(e))
    return message


if __name__== "__main__":

    logging.debug("s3_bucket: " + bucket)
    logging.debug("s3_endpoint: " + endpoint)   
    logging.debug("access_key: " + access_key)
    logging.debug("secret_key: " + secret_key)  
    logging.debug("region_host: " + region_host)  
    if not (access_key or secret_key or bucket or endpoint):
        logging.info("Missing environment variables")
    else:
        app.run(host='0.0.0.0', port=80)