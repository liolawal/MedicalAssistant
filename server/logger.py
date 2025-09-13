import logging

def setup_logger(name="MedicalAssisstant"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] ----[%(message)s]")
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)


    return logger

logger = setup_logger()
logger.info("RAG process started")
logger.debug("Debugging information")
logger.error("An error occurred")
logger.critical("Critical issue")