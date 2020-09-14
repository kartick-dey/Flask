from flask import Flask, jsonify
from controllers import user_controller
import logging as logger

logger.basicConfig(level=logger.DEBUG)
# logger.basicConfig(filename='app.log', filemode='a' ,level=logger.DEBUG, format='%(process)d - %(asctime)s -%(name)s - %(levelname)s - %(message)s')

appInstance = Flask(__name__)

if __name__ == "__main__":
    logger.debug("Starting the application")
    from api import *
    appInstance.run(debug=True)