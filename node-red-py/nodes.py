import random


def create_id():
    """
    Creates a 16 digit hex random number
    """
    # js from node red code: (1+Math.random()*4294967295).toString(16).replace('.', '')
    return hex(random.randint(1, 16 ** 16))[2:]


class Flow:
    def __init__(self, label):
        self.id = create_id()
        self.label = label
        self.disabled = False
        self.info = ""
        self.env = []
        self.nodes = []

    def add_node(self, Node):
        self.nodes.append(Node)

    def json(self):
        nodes = [node.json() for node in self.nodes]
        flow_d = vars(self).copy()
        flow_d['nodes'] = nodes
        return flow_d


class Node:
    def __init__(self, name: str, flow: Flow):
        self.flow = flow
        self.id = create_id()
        self.z = flow.id  # The flow, or subflow, the node is a member of
        self.name = name

        # random position
        self.x = random.randint(0, 1920)
        self.y = random.randint(0, 1080)

        self.wires = []

        self.flow.add_node(self)


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def json(self):
        d = vars(self).copy()
        del d['flow']
        return d


# class MqttbrokerNode(Node):
#     def __init__(self, name, broker, port, usetls):
#         self.id = create_id()
#         self.type = "mqtt-broker",
#         self.name = name #"bem.eco"
#         self.broker = broker #"bem.eco",
#         self.port= port #"43660",
#         self.tls = "2f43073528146e9d"
#         self.clientid = ""
#         self.autoConnect = True
#         self.usetls = usetls
#         self.protocolVersion = 5
#         self.keepalive = 60
#         self.cleansession= True,
#         self.birthTopic= ""
#         self.birthQos= "0"
#         self.birthRetain= False
#         self.birthPayload= ""
#         self.birthMsg= {}
#         self.closeTopic= ""
#         self.closeQos= "0"
#         self.closeRetain= False
#         self.closePayload= ""
#         self.closeMsg= {}
#         self.willTopic= ""
#         self.willQos= "0",
#         self.willRetain= "False"
#         self.willPayload= ""
#         self.willMsg= {}
#         self.userProps= ""
#         self.sessionExpiry= ""

# class InfluxNode(Node):
#     def __init__(self, name, hostname, port):
#         self.id = create_id()
#         self.type = "influxdb"
#         self.hostname = hostname #127.0.0.1"
#         self.port = port #"8086"
#         self.protocol = "http"
#         self.database = "database"
#         self.name= name # "wg1nsbrk"
#         self.usetls = False
#         warn("tls")
#         self.tls = "2f43073528146e9d"
#         self.influxdbVersion = 2.0
#         self.url = "http://localhost:8086"
#         self.rejectUnauthorized= True

class MqttinNode(Node):
    def __init__(self, mqttbroker_id, name: str, flow: Flow, topic: str, qos: int):
        super().__init__(name, flow, )
        self.type = 'mqtt in'
        self.topic = topic
        self.qos = qos
        self.datatype = 'auto-detect'
        self.broker = mqttbroker_id
        self.nl = False
        self.rap = True
        self.rh = 0
        self.inputs = 0
        self.wires = [[]]


class DebugNode(Node):
    def __init__(self, name: str, flow: Flow, active: bool = False):
        super().__init__(name, flow, )
        self.type = "debug"
        self.active = active
        self.tosidebar = True
        self.console = False
        self.tostatus = False
        self.complete = False
        self.statusVal = ""
        self.statusType = "auto"


class InfluxdbOutNode(Node):
    def __init__(self, influxnode_id: int, name: str, flow: Flow, influx_bucket: str, influx_measurement: str):
        super().__init__(name, flow, )
        self.type = 'influxdb out'

        self.influxdb = influxnode_id
        self.measurement = influx_measurement
        self.name = f'{influx_bucket}/{self.measurement}'
        self.repcision = ""
        self.retentionPolicy = ""
        self.database = "database"
        self.precisionV18FluxV20 = 'ms'
        self.retentionPolicyV18Flux = ''
        self.org = "BEM"
        self.bucket = influx_bucket


class ChangeNode(Node):
    def __init__(self, name: str,
                 flow: Flow,
                 to_payload: str):
        super().__init__(name, flow)
        self.type = 'change'
        self.rules = [{'t': 'set',
                       'p': 'payload',
                       'pt': 'msg',
                       'to': f'payload.{to_payload}',  # e.g.  'payload.ATCff9430', or payload.ENERGY
                       'tot': 'msg'}],
        self.action = ''
        self.property = ""
        # self.from = "" # TODO self.from funktioniert nicht
        self.to = ""
        self.reg = False
        self.wires = [[]]


class SwitchNode(Node):
    def __init__(self, name: str,
                 flow: Flow, ):
        super().__init__(name, flow)
        self.type = "switch"
        self.property = "payload"
        self.propertyType = "msg"
        self.rules = [{'t': 'istype', 'v': 'undefined', 'vt': 'undefined'},
                      {'t': 'istype', 'v': 'object', 'vt': 'object'}],
        self.checkall = True  # was 'true'
        self.repair = False  # was False
        self.outputs = 2
        self.wires = [[] for _ in range(self.outputs)]


def connect_nodes(node1: Node, node2: Node, node1_output=0, node2_output=0, pos=None):
    # wire_id = create_id()
    if isinstance(node1, MqttinNode) or isinstance(node1, ChangeNode):
        node1.wires[0].append(node2.id)

    elif isinstance(node1, SwitchNode):
        node1.wires[node1_output].append(node2.id)
    else:
        node1.wires.append(node2.id)

    #     if isinstance(node2, SwitchNode):
    #         node2.wires[node2_output].append(node1.id)
    #     else:
    #         node2.wires.append(node1.id)
    x_offset = 300
    y_offset = 75
    if pos == "right":
        node2.x = node1.x + x_offset
        node2.y = node1.y
    elif pos == "top-right":
        node2.x = node1.x + x_offset
        node2.y = node1.y - y_offset
    elif pos == "bottom-right":
        node2.x = node1.x + x_offset
        node2.y = node1.y + y_offset



