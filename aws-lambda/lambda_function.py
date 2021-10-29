"""FlexVM API OPs"""
import logging
import json
import requests

FLEXVM_API_BASE_URI = "https://support.fortinet.com/ES/api/flexvm/v1/"
COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}
logging.getLogger().setLevel(logging.INFO)

def requests_post(resource_url, json_body, headers):
    """Requests Post"""
    logging.info("--> FlexVM API Request...")

    try:
        result = requests.post(resource_url, json=json_body, headers=headers)
        logging.info(result.content)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error

    return result.content


def get_token(username, password, client_id, grant_type):
    """Get Authentication Token"""
    logging.info("--> Retieving FlexVM API Token...")

    uri = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    body = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "grant_type": grant_type,
    }

    results = requests_post(uri, body, COMMON_HEADERS)
    return results


def programs_list(access_token):
    """Retrieve FlexVM Programs List"""
    logging.info("--> Retrieving FlexVM Programs...")

    uri = FLEXVM_API_BASE_URI + "programs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    results = requests_post(uri, "", headers)
    return results


def configs_create(access_token, program_serial_number, name, cpus, svc_package):
    """Create FlexVM Configuration"""
    logging.info("--> Create FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "programSerialNumber": program_serial_number,
        "name": name,
        "productTypeId": 1,
        "parameters": [{"id": 1, "value": cpus}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def configs_disable(access_token, config_id):
    """Disable FlexVM Configuration"""
    logging.info("--> Disable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/disable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_enable(access_token, config_id):
    """Enable FlexVM Configuration"""
    logging.info("--> Enable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/enable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_list(access_token, program_serial_number):
    """List FlexVM Configurations"""
    logging.info("--> List FlexVM Configurations...")

    uri = FLEXVM_API_BASE_URI + "configs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"programSerialNumber": program_serial_number}

    results = requests_post(uri, body, headers)
    return results


def configs_update(access_token, config_id, name, cpu, svc_package):
    """Update FlexVM Configuration"""
    logging.info("--> Update FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/update"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "id": config_id,
        "name": name,
        "parameters": [{"id": 1, "value": cpu}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def vms_create(access_token, config_id, count, description, end_date):
    """Create FlexVM Virtual Machines"""
    logging.info("--> Create FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "configId": config_id,
        "count": count,
        "description": description,
        "endDate": end_date,
    }

    results = requests_post(uri, body, headers)
    return results


def vms_list(access_token, config_id):
    """List FlexVM Virtual Machines"""
    logging.info("--> List FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"configId": config_id}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_config_id(access_token, config_id, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    logging.info("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"configId": config_id, "startDate": start_date, "endDate": end_date}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_serial_number(access_token, vm_serial_number, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    logging.info("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "serialNumber": vm_serial_number,
        "startDate": start_date,
        "endDate": end_date,
    }

    results = requests_post(uri, body, headers)
    return results


def vms_update(access_token, vm_serial_number, config_id, description, end_date):
    """Update FlexVM Virtual Machine"""
    logging.info("--> Update FlexVM Virtual Machine...")

    # Only Active Virtual Machines can be updated
    process_update = False
    vm_status = "Not Found"
    vm_list = json.loads(vms_list(access_token, config_id))
    if vm_list:
        logging.info("VM List:")
        logging.info(vm_list)
        for virtual_machine in vm_list["vms"]:
            if (
                virtual_machine["serialNumber"] == vm_serial_number
                and virtual_machine["status"] == "ACTIVE"
            ):
                process_update = True
                break
            if (
                virtual_machine["serialNumber"] == vm_serial_number
                and virtual_machine["status"] == "STOPPED"
            ):
                vm_status = virtual_machine["status"]
                break

    if process_update:
        uri = FLEXVM_API_BASE_URI + "vms/update"
        headers = COMMON_HEADERS.copy()
        headers["Authorization"] = f"Bearer {access_token}"

        body = {
            "serialNumber": vm_serial_number,
            "configId": config_id,
            "description": description,
            "endDate": end_date,
        }
        results = requests_post(uri, body, headers)
    else:
        results = {
            "error": "Cannot update VM: " + vm_serial_number,
            "configId": config_id,
            "status": vm_status,
        }

    return results


def vms_reactivate(access_token, vm_serial_number):
    """Reactivate FlexVM Virtual Machines"""
    logging.info("--> Reactivate FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/reactivate"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_stop(access_token, vm_serial_number):
    """Stop FlexVM Virtual Machines"""
    logging.info("--> Stop FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/stop"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_token(access_token, vm_serial_number):
    """Retrieve FlexVM Virtual Machines Token"""
    logging.info("--> Retrieve FlexVM Virtual Machines Token...")

    uri = FLEXVM_API_BASE_URI + "vms/token"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def lambda_handler(event, context):
    """Process FlexVM API Request"""

    logging.info("FlexVM OPs processing api request...")
    #logging.info("Received event: " + json.dumps(event, indent=2))

    process_request = False
    api_request_result = None
    flexvm_op = None

    if event["httpMethod"] == "POST":
        if event["body"]:
            req_body = json.loads(event["body"])
            logging.info("body: " + json.dumps(req_body, indent=2))

            if "flexvm_op" in req_body:
                flexvm_op = req_body["flexvm_op"]
                process_request = True
            else:
                api_request_result = "{'error': 'FlexVM Op is not specified'}"
        else:
            api_request_result = "{'error': 'FlexVM POST has no Body'}"
    else:
        api_request_result = (
            "{'error': 'FlexVM Unsupported method - " +
            event['httpMethod'] + "'}"
        )

    if process_request:

        if flexvm_op == "get_token":
            api_request_result = get_token(
                req_body["username"],
                req_body["password"],
                req_body["client_id"],
                req_body["grant_type"],
            )

        if flexvm_op == "programs_list":
            api_request_result = programs_list(req_body["access_token"])

        if flexvm_op == "configs_create":
            api_request_result = configs_create(
                req_body["access_token"],
                req_body["programSerialNumber"],
                req_body["name"],
                req_body["cpu"],
                req_body["svc_package"],
            )

        if flexvm_op == "configs_disable":
            api_request_result = configs_disable(
                req_body["access_token"], req_body["config_id"]
            )

        if flexvm_op == "configs_enable":
            api_request_result = configs_enable(
                req_body["access_token"], req_body["config_id"]
            )

        if flexvm_op == "configs_list":
            api_request_result = configs_list(
                req_body["access_token"], req_body["programSerialNumber"]
            )

        if flexvm_op == "configs_update":
            api_request_result = configs_update(
                req_body["access_token"],
                req_body["config_id"],
                req_body["name"],
                req_body["cpu"],
                req_body["svc_package"],
            )

        if flexvm_op == "vms_create":
            api_request_result = vms_create(
                req_body["access_token"],
                req_body["config_id"],
                req_body["count"],
                req_body["description"],
                req_body["end_date"],
            )

        if flexvm_op == "vms_list":
            api_request_result = vms_list(
                req_body["access_token"], req_body["config_id"]
            )

        if flexvm_op == "vms_points_by_config_id":
            api_request_result = vms_points_by_config_id(
                req_body["access_token"],
                req_body["config_id"],
                req_body["start_date"],
                req_body["end_date"],
            )

        if flexvm_op == "vms_points_by_serial_number":
            api_request_result = vms_points_by_serial_number(
                req_body["access_token"],
                req_body["vm_serial_number"],
                req_body["start_date"],
                req_body["end_date"],
            )

        if flexvm_op == "vms_update":
            api_request_result = vms_update(
                req_body["access_token"],
                req_body["vm_serial_number"],
                req_body["config_id"],
                req_body["description"],
                req_body["end_date"],
            )

        if flexvm_op == "vms_reactivate":
            api_request_result = vms_reactivate(
                req_body["access_token"], req_body["vm_serial_number"]
            )

        if flexvm_op == "vms_stop":
            api_request_result = vms_stop(
                req_body["access_token"], req_body["vm_serial_number"]
            )

        if flexvm_op == "vms_token":
            api_request_result = vms_token(
                req_body["access_token"], req_body["vm_serial_number"]
            )

    if isinstance(api_request_result, bytes):
        result = api_request_result.decode(encoding="UTF-8")
    else:
        result = api_request_result

    if api_request_result and process_request:
        logging.info(api_request_result)
        status_code = 200
    else:
        status_code = 400

    return {
        'statusCode': status_code,
        'headers': {"Content-type": "application/json"},
        'body': result
    }
