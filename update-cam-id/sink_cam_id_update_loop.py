import json
from os import path
#instance1
for instance in range(1, 3):
    config_file_name = "/uncanny/sink/config/config_{}.json".format(instance)
    f1 = open(config_file_name)
    client_file_name = "/uncanny/sink/client/client_{}.json".format(instance)
    config_json = json.load(f1)
    cam_id = config_json['dashboard']['camId']
    x1 = open(client_file_name)
    y1 = {"cam_id": cam_id}
    z1 = json.load(x1)
    z1['extras'].update({"cam_id": cam_id})
    a1 = json.dumps(z1, indent=2)
    print (a1)
    with open(client_file_name, "w") as outfile:
        outfile.write(a1)
    f1.close()

# #instance4
# f4 = open('/uncanny/sink/config/config_4.json')
# path4 = "/uncanny/sink/client/client_4.json"
# data4 = json.load(f4)
# ExternalCameraId4 = data4['dashboard']['camId']
# x4 = open(path4)
# y4 = {"ExternalCameraId": ExternalCameraId4}
# z4 = json.load(x4)
# z4['extras'].update({"ExternalCameraId": ExternalCameraId4})
# a4 = json.dumps(z4, indent=2)
# print (a4)
# with open(path4, "w") as outfile:
#     outfile.write(a4)
# f4.close()
