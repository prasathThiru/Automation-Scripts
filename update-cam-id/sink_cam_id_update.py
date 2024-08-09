import json
from os import path
#instance1
f1 = open('/uncanny/sink/config/config_1.json')
path1 = "/uncanny/sink/client/client_1.json"

data1 = json.load(f1)
ExternalCameraId1 = data1['dashboard']['camId']
x1 = open(path1)
y1 = {"ExternalCameraId": ExternalCameraId1}
z1 = json.load(x1)
z1['extras'].update({"ExternalCameraId": ExternalCameraId1})
a1 = json.dumps(z1, indent=2)
print (a1)
with open(path1, "w") as outfile:
    outfile.write(a1)
f1.close()

#instance2
f2 = open('/uncanny/sink/config/config_2.json')
path2 = "/uncanny/sink/client/client_2.json"
data2 = json.load(f2)
ExternalCameraId2 = data2['dashboard']['camId']
x2 = open(path2)
y2 = {"ExternalCameraId": ExternalCameraId2}
z2 = json.load(x2)
z2['extras'].update({"ExternalCameraId": ExternalCameraId2})
a2 = json.dumps(z2, indent=2)
print (a2)
with open(path2, "w") as outfile:
    outfile.write(a2)
f2.close()

#instance3
f3 = open('/uncanny/sink/config/config_3.json')
path3 = "/uncanny/sink/client/client_3.json"
data3 = json.load(f3)
ExternalCameraId3 = data3['dashboard']['camId']
x3 = open(path3)
y3 = {"ExternalCameraId": ExternalCameraId3}
z3 = json.load(x3)
z3['extras'].update({"ExternalCameraId": ExternalCameraId3})
a3 = json.dumps(z3, indent=2)
print (a3)
with open(path3, "w") as outfile:
    outfile.write(a3)
f3.close()

#instance4
f4 = open('/uncanny/sink/config/config_4.json')
path4 = "/uncanny/sink/client/client_4.json"
data4 = json.load(f4)
ExternalCameraId4 = data4['dashboard']['camId']
x4 = open(path4)
y4 = {"ExternalCameraId": ExternalCameraId4}
z4 = json.load(x4)
z4['extras'].update({"ExternalCameraId": ExternalCameraId4})
a4 = json.dumps(z4, indent=2)
print (a4)
with open(path4, "w") as outfile:
    outfile.write(a4)
f4.close()
