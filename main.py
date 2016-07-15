from flask import Flask
import boto
import boto.s3.connection
import os
logging.config.fileConfig('conf/logging.conf')

access_key = os.environ['BROWSER_S3_ACCESS_KEY']
secret_key = os.environ['BROWSER_S3_SECRET_KEY']
bucket = os.environ['BROWSER_S3_BUCKET']
endpoint = os.environ['BROWSER_S3_ENDPOINT']

if __name__== "__main__":

    logging.debug("s3_bucket: " + bucket)
    logging.debug("s3_endpoint: " + endpoint)   
    if not (access_key or secret_key or bucket or endpoint):
        logging.info("Missing environment variables")
    else:
        app.run('0.0.0.0')

@app.route('/', methods=['GET'])
def browse():
    logging.info("start browse")
    try:

        bucket_name = s3_bucket
        conn = boto.connect_s3(access_key,
            secret_key)
        bucket_conn = conn.get_bucket(bucket)

        logging.debug("")
        logging.debug("---------------")
        for key in bucket_conn.list():
            name = key.name
            modified = key.last_modified
            url = key.generate_url(expires_in=0, query_auth=False, force_http=True)
            print "{name}\t{modified}\t{url}".format(
                name = name,
                modified = modified,
                url = url
            )
            logging.debug("")
            logging.debug("name: " + name)
            logging.debug("modified: " + modified)
            logging.debug("url: " + url)
        logging.debug("")       
        logging.debug("---------------")
        logging.debug("")       

        message = 'Success
        logging.info("browse success")
    except Exception, e:
        message = "Error"
        logging.info("browse fail")
    return message