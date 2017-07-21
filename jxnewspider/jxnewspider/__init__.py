from twisted.python import log
import logging

logging.basicConfig(level=logging.ERROR, filemode='w', filename='log.txt',format='%(asctime)s %(levelname)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
observer = log.PythonLoggingObserver()
observer.start()