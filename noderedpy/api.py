import requests

class NodeRedApi:
    def __init__(self, base_url):
        self.base_url = base_url

        r = requests.get(self.base_url + "/auth/login")
        self.need_auth = bool(r.json())
        if self.need_auth:
            print("Use get_auth_header to authenticate")
        self.mqtt_brokers = None
        self.influxdbs = None
        self.token_resp = {}
        self.auth_header = {}

    def authenticate(self, username: str, password: str):
        if self.need_auth:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = f'client_id=node-red-admin&grant_type=password&scope=*&username={username}&password={password}'
            r = requests.post(self.base_url + "/auth/token", headers=headers, data=data)
            self.token_resp = r.json()
            self.auth_header = {f"Authorization": f"Bearer {self.token_resp['access_token']}"}
        return

    def get_flows(self, flow_name):
            r = requests.get(self.base_url + "/flows", headers=self.auth_header)

            # get the id for a flow name
            flow_id = \
            [flow_obj for flow_obj in [obj for obj in r.json() if flow_name in obj.values()] if flow_obj["type"] == 'tab'][
                0]["id"]

            # get the flow as json
            r = requests.get(self.base_url + f"/flow/{flow_id}", headers=self.auth_header)
            return r.json()

    def get_mqtt_brokers(self):
        mqtt_brokers = []
        r = requests.get(self.base_url + "/flows", headers=self.auth_header)
        for node in r.json():
            if node['type'] == 'mqtt-broker':
                mqtt_brokers.append(node)
        self.mqtt_brokers = mqtt_brokers
        return

    def get_influxdbs(self):
        r = requests.get(self.base_url + "/flows", headers=self.auth_header)
        influxs = []
        for node in r.json():
            if node['type'] == 'influxdb':
                influxs.append(node)
        self.influxdbs = influxs
        return

    def revoke_token(self):
        header = {'Content-Type': 'application/x-www-form-urlencoded', **self.auth_header}
        data = f"token={self.token_resp['access_token']}"
        r = requests.post(self.base_url + "/auth/revoke", headers=header, data=data)
        return r.ok