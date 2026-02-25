from __future__ import annotations

import re
from typing import List, Tuple


def schedule_retries(requests_path: str, results_path: str, retry_delay_seconds: int) -> List[Tuple[int, str]]:
    # requests_log contains request_ids, and results_file contains the request id and status
    # if status == 429, must schedule a retry later
    # ex) requests file: 
    # 100 r1 /users, 105 r2 /login, 110 r1 /users
    # results file:
    # r1 429, r2 200, r3 429, invalid
    # retry_delay_seconds = 10
    # for r1 429 -> r1 is at time=100, so retry at 100+10
    # for r3 429, -> r3 not in requests file, so ignore
    # we essentially go through req file and for each request, map to its result in results file.
    # store tuple as (time retried, request id)
    
    # create map of results
    result_map = {}
    with open(results_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2 and parts[1].isdigit():
                result_map[parts[0]] = int(parts[1])
    
    result = []
    with open(requests_path, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].isdigit():
                curr_time = int(parts[0])
                request_id = parts[1]
                if request_id in result_map:
                    if result_map[request_id] == 429:
                        result.append(((curr_time+retry_delay_seconds), request_id))
    
    return result


def dedupe_latest_retry(requests_path: str, results_path: str, retry_delay_seconds: int) -> List[Tuple[int, str]]:
    retry_list = schedule_retries(requests_path, results_path, retry_delay_seconds)
    print(retry_list)
    retry_dict = {}
    for retry in retry_list:
        timestamp = retry[0]
        req_id = retry[1]
        if req_id not in retry_dict:
            retry_dict[req_id] = 0
        if timestamp > retry_dict[req_id]:
            retry_dict[req_id] = timestamp
    
    sorted_dict = sorted(retry_dict.items(), key= lambda x: (x[1], x[0]))
    result = []
    for req_id, timestamp in sorted_dict:
        result.append((timestamp, req_id))

    return result
