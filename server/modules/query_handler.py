from logger import logger


def query_chain(chain,user_input:str):
    try:
        logger.debug(f"querying the chain with user input: {user_input}")
        result = chain({"query":user_input})
        response = {
            "response": result['result'],
            "source": [doc.metadata.get('source',"") for doc in result['source_documents']]
        }
        logger.debug(f"chain response: {response}")
        return response

    except Exception as e:
        logger.exception("Error on querying the chain")
        raise