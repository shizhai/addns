import json
from fastapi import FastAPI
import utils

app = FastAPI()
aliyun = utils.AlirunUtilsWrap("LTAI5tBDViMBvzC62NbhYRzu", "bAOS1feSOxnGApNAMsB3HtT4mgRJOR")

@app.get("/", description="this is root director to request")
def read_root():
    return {"Hello": "World"}

@app.get("/domain/list")
def read_domain_item(target: str | None = None, limit: int = 10):
    if not target:
        return {"error": "target is required"}
    # return {"target": target, "limit": limit}
    domains = aliyun.aliyun_get_domain_records(domain=target)
    match_record = ["recordid", "type", "rr", "value"]
    response = {}
    domains = domains.to_map()
    # print(domains['Record'])
    for item in domains['Record']:
        rsp = {}
        for field in item:
            if str(field).lower() in match_record:
                rsp[field] = item[field]
        response[item["RecordId"]] = rsp

    return response

@app.get("/public/ip")
def read_public_ip():
    ip = aliyun.retrieve_public_ip()
    return {"ip": ip}

@app.post("/domain/{domain_id}")
def read_user(domain_id: int):
    return {"user_id": ""}