# -*- Blueprint setup -*-
from os import environ as env
from packaging.version import parse
from sanic import Blueprint
from sanic.response import json

from utils.SiteHelper import JailbreakMap as jMap
from utils.SiteHelper import DeviceMapPG as dMap
from utils.SiteHelper import DeviceMapPGNamed as aMap
from utils.SiteHelper import MinVersionMap as minMap
from utils.SiteHelper import MaxVersionMap as maxMap

APIBP = Blueprint("APIBP", version="v1")
valid_tokens = [t for t in env.get("VALID_TOKENS").split("\n")]


# -*- Helper -*-
async def get_parsed_device(device):
    rv = [k for k, v in aMap.items() if device in v]
    return rv[-1]


# -*- Routes -*-
@APIBP.route('/pls/<device>/<iosv>')
async def home2(request, device, iosv):
    _token = request.headers.get('Authorization')
    if _token == None:
        return json({"status": -1})
    else:
        if _token in valid_tokens:
            dev = await get_parsed_device(device)
            if dev == None:
                return json({"status": 1})
            if parse(minMap.get(device)) <= parse(iosv) <= parse(maxMap.get(device)):
                map_supported = [x for x in jMap if (parse(x.get('minIOS')) <= parse(iosv) <= parse(x.get('maxIOS'))) \
                                 and (dMap.index(x.get('minProc')) <= dMap.index(dev) <= dMap.index(x.get('maxProc')))]
                return json(
                    {
                        "status": 0,
                        "jelbreks": map_supported
                    }
                )
            else:
                return json(
                    {
                        "status": 2,
                        "minIOS": minMap.get(device),
                        "maxiOS": maxMap.get(device)
                    }
                )
        else:
            return json({"status": -1})
