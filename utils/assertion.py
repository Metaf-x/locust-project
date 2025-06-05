from config.config import logger

def check_http_response(response, param_to_check) -> bool:
    result=None

    try:
        assert param_to_check in response.text

    except AssertionError as err:
        response.failure(f"Assertion error: text pattern {param_to_check} was not found in response body")
        logger.warn(f"Assertion error: text pattern {param_to_check} was not found in response body")
        result=False

    else:
        result=True

    finally:
        return result
