from __future__ import annotations

from typing import Dict, List, Tuple


def compute_error_rate(filepath: str) -> Dict[str, float]:
    """
    Compute error rate per service from a log file.

    See README for line format and invalid-line rules.
    Must stream the file line-by-line.

    So we know:
    - formatting is timestamp service status
    - need to read in per line
    """
    error_dict = {} # 0 -> total req, 1 -> total error
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and parts[2].isnumeric() and parts[1] != "":
                service = parts[1].strip()
                status = int(parts[2].strip())
                if service not in error_dict:
                    error_dict[service] = [0, 0]
                error_dict[service][0] += 1
                if status >= 500:
                    error_dict[service][1] += 1
    for service, nums in error_dict.items():
        error_dict[service] = round((nums[1]/nums[0]), 4)
    return error_dict


def services_by_error_rate(filepath: str) -> List[Tuple[str, float]]:
    """
    Follow-up: returns (service, error_rate) sorted by:
    - error_rate desc
    - total_requests desc
    - service asc
    """
    error_dict = {} # 0 -> total req, 1 -> total error
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and parts[2].isnumeric() and parts[1] != "":
                service = parts[1].strip()
                status = int(parts[2].strip())
                if service not in error_dict:
                    error_dict[service] = [0, 0]
                error_dict[service][0] += 1
                if status >= 500:
                    error_dict[service][1] += 1
    error_dict = sorted(error_dict.items(), key=lambda x : (-round(x[1][1]/x[1][0], 4), -x[1][0], x[0]))
    result = []
    for item in error_dict:
        result.append((item[0], round((item[1][1]/item[1][0]), 4)))

    return result

