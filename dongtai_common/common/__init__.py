# loop base data return
def baseLoopResult(result_query):
    result = {}
    for item in result_query:
        ind = str(item["id"])
        del item["id"]
        result[ind] = item
    return result
