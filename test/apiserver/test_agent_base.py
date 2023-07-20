######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_register
# @created     : 星期四 12月 09, 2021 19:25:14 CST
#
# @description :
######################################################################


import gzip
import json

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, RequestsClient

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.server import IastServer
from dongtai_common.models.user import User
from dongtai_protocol.decrypter import parse_data

REGISTER_JSON = {
    "serverPath": "/Users/erzhuangniu/workspace/vul/SecExample",
    "containerVersion": "9.0.46.0",
    "pid": "1416",
    "language": "JAVA",
    "serverPort": "0",
    "version": "v1.1.3",
    "network": '[{"isAddress":"1","ip":"172.22.22.11","name":"enp0s8"},{"isAddress":"1","ip":"10.0.2.15","name":"enp0s3"}]',
    "serverEnv": "e2phdmEucnVudGltZS5uYW1lPU9wZW5KREsgUnVudGltZSBFbnZpcm9ubWVudCwgc3ByaW5nLm91dHB1dC5hbnNpLmVuYWJsZWQ9YWx3YXlzLCBwcm9qZWN0Lm5hbWU9U3ByaW5nU2VjLCBzdW4uYm9vdC5saWJyYXJ5LnBhdGg9L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIsIGphdmEudm0udmVyc2lvbj0yNS4zMTItYjA3LCBnb3BoZXJQcm94eVNldD1mYWxzZSwgamF2YS52bS52ZW5kb3I9QW1hem9uLmNvbSBJbmMuLCBqYXZhLnZlbmRvci51cmw9aHR0cHM6Ly9hd3MuYW1hem9uLmNvbS9jb3JyZXR0by8sIHBhdGguc2VwYXJhdG9yPTosIHByb2plY3QudmVyc2lvbj0xMjA5MDEsIGphdmEudm0ubmFtZT1PcGVuSkRLIDY0LUJpdCBTZXJ2ZXIgVk0sIGZpbGUuZW5jb2RpbmcucGtnPXN1bi5pbywgdXNlci5jb3VudHJ5PUNOLCBzdW4uamF2YS5sYXVuY2hlcj1TVU5fU1RBTkRBUkQsIHN1bi5vcy5wYXRjaC5sZXZlbD11bmtub3duLCBqYXZhLnZtLnNwZWNpZmljYXRpb24ubmFtZT1KYXZhIFZpcnR1YWwgTWFjaGluZSBTcGVjaWZpY2F0aW9uLCB1c2VyLmRpcj0vVXNlcnMvZXJ6aHVhbmduaXUvd29ya3NwYWNlL3Z1bC9TZWNFeGFtcGxlLCBqYXZhLnJ1bnRpbWUudmVyc2lvbj0xLjguMF8zMTItYjA3LCBqYXZhLmF3dC5ncmFwaGljc2Vudj1zdW4uYXd0LkNHcmFwaGljc0Vudmlyb25tZW50LCBqYXZhLmVuZG9yc2VkLmRpcnM9L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZW5kb3JzZWQsIG9zLmFyY2g9eDg2XzY0LCBqYXZhLmlvLnRtcGRpcj0vdmFyL2ZvbGRlcnMveHkveHl4NTZoM3MyOXo2Mzc2Z3ZrMzI2MjFoMDAwMGduL1QvLCBsaW5lLnNlcGFyYXRvcj0KLCBqYXZhLnZtLnNwZWNpZmljYXRpb24udmVuZG9yPU9yYWNsZSBDb3Jwb3JhdGlvbiwgb3MubmFtZT1NYWMgT1MgWCwgc3VuLmpudS5lbmNvZGluZz1VVEYtOCwgamF2YS5saWJyYXJ5LnBhdGg9L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9FeHRlbnNpb25zOi9MaWJyYXJ5L0phdmEvRXh0ZW5zaW9uczovTmV0d29yay9MaWJyYXJ5L0phdmEvRXh0ZW5zaW9uczovU3lzdGVtL0xpYnJhcnkvSmF2YS9FeHRlbnNpb25zOi91c3IvbGliL2phdmE6Liwgc3ByaW5nLmpteC5lbmFibGVkPXRydWUsIGphdmEuc3BlY2lmaWNhdGlvbi5uYW1lPUphdmEgUGxhdGZvcm0gQVBJIFNwZWNpZmljYXRpb24sIGphdmEuY2xhc3MudmVyc2lvbj01Mi4wLCBzdW4ubWFuYWdlbWVudC5jb21waWxlcj1Ib3RTcG90IDY0LUJpdCBUaWVyZWQgQ29tcGlsZXJzLCBzcHJpbmcubGl2ZUJlYW5zVmlldy5tYmVhbkRvbWFpbj0sIG9zLnZlcnNpb249MTEuNCwgdXNlci5ob21lPS9Vc2Vycy9lcnpodWFuZ25pdSwgc3VuLm5ldC5odHRwLmFsbG93UmVzdHJpY3RlZEhlYWRlcnM9dHJ1ZSwgdXNlci50aW1lem9uZT0sIGphdmEuYXd0LnByaW50ZXJqb2I9c3VuLmx3YXd0Lm1hY29zeC5DUHJpbnRlckpvYiwgZmlsZS5lbmNvZGluZz1VVEYtOCwgamF2YS5zcGVjaWZpY2F0aW9uLnZlcnNpb249MS44LCBqYXZhLmNsYXNzLnBhdGg9L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvY2hhcnNldHMuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9qcmUvbGliL2V4dC9jbGRyZGF0YS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L2Ruc25zLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9leHQvamFjY2Vzcy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L2pmeHJ0LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9leHQvbG9jYWxlZGF0YS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L25hc2hvcm4uamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9qcmUvbGliL2V4dC9zdW5lYy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L3N1bmpjZV9wcm92aWRlci5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L3N1bnBrY3MxMS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0L3ppcGZzLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9qY2UuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9qcmUvbGliL2pmci5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvamZ4c3d0LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9qc3NlLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9tYW5hZ2VtZW50LWFnZW50LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9yZXNvdXJjZXMuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9qcmUvbGliL3J0LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvbGliL2FudC1qYXZhZnguamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9saWIvZHQuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS9MaWJyYXJ5L0phdmEvSmF2YVZpcnR1YWxNYWNoaW5lcy9jb3JyZXR0by0xLjguMF8zMTIvQ29udGVudHMvSG9tZS9saWIvamF2YWZ4LW14LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvbGliL2pjb25zb2xlLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvbGliL3BhY2thZ2VyLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvbGliL3NhLWpkaS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2xpYi90b29scy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L3dvcmtzcGFjZS92dWwvU2VjRXhhbXBsZS90YXJnZXQvY2xhc3NlczovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9ib290L3NwcmluZy1ib290LXN0YXJ0ZXItdGh5bWVsZWFmLzIuNS4wL3NwcmluZy1ib290LXN0YXJ0ZXItdGh5bWVsZWFmLTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9ib290L3NwcmluZy1ib290LXN0YXJ0ZXIvMi41LjAvc3ByaW5nLWJvb3Qtc3RhcnRlci0yLjUuMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvYm9vdC9zcHJpbmctYm9vdC1zdGFydGVyLWxvZ2dpbmcvMi41LjAvc3ByaW5nLWJvb3Qtc3RhcnRlci1sb2dnaW5nLTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvY2gvcW9zL2xvZ2JhY2svbG9nYmFjay1jbGFzc2ljLzEuMi4zL2xvZ2JhY2stY2xhc3NpYy0xLjIuMy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NoL3Fvcy9sb2diYWNrL2xvZ2JhY2stY29yZS8xLjIuMy9sb2diYWNrLWNvcmUtMS4yLjMuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvYXBhY2hlL2xvZ2dpbmcvbG9nNGovbG9nNGotdG8tc2xmNGovMi4xNC4xL2xvZzRqLXRvLXNsZjRqLTIuMTQuMS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9hcGFjaGUvbG9nZ2luZy9sb2c0ai9sb2c0ai1hcGkvMi4xNC4xL2xvZzRqLWFwaS0yLjE0LjEuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc2xmNGovanVsLXRvLXNsZjRqLzEuNy4zMC9qdWwtdG8tc2xmNGotMS43LjMwLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvamFrYXJ0YS9hbm5vdGF0aW9uL2pha2FydGEuYW5ub3RhdGlvbi1hcGkvMS4zLjUvamFrYXJ0YS5hbm5vdGF0aW9uLWFwaS0xLjMuNS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy95YW1sL3NuYWtleWFtbC8xLjI4L3NuYWtleWFtbC0xLjI4LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3RoeW1lbGVhZi90aHltZWxlYWYtc3ByaW5nNS8zLjAuMTIuUkVMRUFTRS90aHltZWxlYWYtc3ByaW5nNS0zLjAuMTIuUkVMRUFTRS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy90aHltZWxlYWYvdGh5bWVsZWFmLzMuMC4xMi5SRUxFQVNFL3RoeW1lbGVhZi0zLjAuMTIuUkVMRUFTRS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9hdHRvcGFyc2VyL2F0dG9wYXJzZXIvMi4wLjUuUkVMRUFTRS9hdHRvcGFyc2VyLTIuMC41LlJFTEVBU0UuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvdW5iZXNjYXBlL3VuYmVzY2FwZS8xLjEuNi5SRUxFQVNFL3VuYmVzY2FwZS0xLjEuNi5SRUxFQVNFLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NsZjRqL3NsZjRqLWFwaS8xLjcuMzAvc2xmNGotYXBpLTEuNy4zMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy90aHltZWxlYWYvZXh0cmFzL3RoeW1lbGVhZi1leHRyYXMtamF2YTh0aW1lLzMuMC40LlJFTEVBU0UvdGh5bWVsZWFmLWV4dHJhcy1qYXZhOHRpbWUtMy4wLjQuUkVMRUFTRS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvYm9vdC9zcHJpbmctYm9vdC1zdGFydGVyLXdlYi8yLjUuMC9zcHJpbmctYm9vdC1zdGFydGVyLXdlYi0yLjUuMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvYm9vdC9zcHJpbmctYm9vdC1zdGFydGVyLWpzb24vMi41LjAvc3ByaW5nLWJvb3Qtc3RhcnRlci1qc29uLTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvY29tL2Zhc3RlcnhtbC9qYWNrc29uL2NvcmUvamFja3Nvbi1kYXRhYmluZC8yLjEyLjMvamFja3Nvbi1kYXRhYmluZC0yLjEyLjMuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9jb20vZmFzdGVyeG1sL2phY2tzb24vY29yZS9qYWNrc29uLWFubm90YXRpb25zLzIuMTIuMy9qYWNrc29uLWFubm90YXRpb25zLTIuMTIuMy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9mYXN0ZXJ4bWwvamFja3Nvbi9jb3JlL2phY2tzb24tY29yZS8yLjEyLjMvamFja3Nvbi1jb3JlLTIuMTIuMy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9mYXN0ZXJ4bWwvamFja3Nvbi9kYXRhdHlwZS9qYWNrc29uLWRhdGF0eXBlLWpkazgvMi4xMi4zL2phY2tzb24tZGF0YXR5cGUtamRrOC0yLjEyLjMuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9jb20vZmFzdGVyeG1sL2phY2tzb24vZGF0YXR5cGUvamFja3Nvbi1kYXRhdHlwZS1qc3IzMTAvMi4xMi4zL2phY2tzb24tZGF0YXR5cGUtanNyMzEwLTIuMTIuMy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9mYXN0ZXJ4bWwvamFja3Nvbi9tb2R1bGUvamFja3Nvbi1tb2R1bGUtcGFyYW1ldGVyLW5hbWVzLzIuMTIuMy9qYWNrc29uLW1vZHVsZS1wYXJhbWV0ZXItbmFtZXMtMi4xMi4zLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9ib290L3NwcmluZy1ib290LXN0YXJ0ZXItdG9tY2F0LzIuNS4wL3NwcmluZy1ib290LXN0YXJ0ZXItdG9tY2F0LTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL2FwYWNoZS90b21jYXQvZW1iZWQvdG9tY2F0LWVtYmVkLWNvcmUvOS4wLjQ2L3RvbWNhdC1lbWJlZC1jb3JlLTkuMC40Ni5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9hcGFjaGUvdG9tY2F0L2VtYmVkL3RvbWNhdC1lbWJlZC1lbC85LjAuNDYvdG9tY2F0LWVtYmVkLWVsLTkuMC40Ni5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9hcGFjaGUvdG9tY2F0L2VtYmVkL3RvbWNhdC1lbWJlZC13ZWJzb2NrZXQvOS4wLjQ2L3RvbWNhdC1lbWJlZC13ZWJzb2NrZXQtOS4wLjQ2LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9zcHJpbmctd2ViLzUuMy43L3NwcmluZy13ZWItNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL3NwcmluZy1iZWFucy81LjMuNy9zcHJpbmctYmVhbnMtNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL3NwcmluZy13ZWJtdmMvNS4zLjcvc3ByaW5nLXdlYm12Yy01LjMuNy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvc3ByaW5nLWFvcC81LjMuNy9zcHJpbmctYW9wLTUuMy43LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9zcHJpbmctY29udGV4dC81LjMuNy9zcHJpbmctY29udGV4dC01LjMuNy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvc3ByaW5nLWV4cHJlc3Npb24vNS4zLjcvc3ByaW5nLWV4cHJlc3Npb24tNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL2Jvb3Qvc3ByaW5nLWJvb3QtZGV2dG9vbHMvMi41LjAvc3ByaW5nLWJvb3QtZGV2dG9vbHMtMi41LjAuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL2Jvb3Qvc3ByaW5nLWJvb3QvMi41LjAvc3ByaW5nLWJvb3QtMi41LjAuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL2Jvb3Qvc3ByaW5nLWJvb3QtYXV0b2NvbmZpZ3VyZS8yLjUuMC9zcHJpbmctYm9vdC1hdXRvY29uZmlndXJlLTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL215YmF0aXMvc3ByaW5nL2Jvb3QvbXliYXRpcy1zcHJpbmctYm9vdC1zdGFydGVyLzEuMy4wL215YmF0aXMtc3ByaW5nLWJvb3Qtc3RhcnRlci0xLjMuMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvYm9vdC9zcHJpbmctYm9vdC1zdGFydGVyLWpkYmMvMi41LjAvc3ByaW5nLWJvb3Qtc3RhcnRlci1qZGJjLTIuNS4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvY29tL3pheHhlci9IaWthcmlDUC80LjAuMy9IaWthcmlDUC00LjAuMy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L29yZy9zcHJpbmdmcmFtZXdvcmsvc3ByaW5nLWpkYmMvNS4zLjcvc3ByaW5nLWpkYmMtNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL3NwcmluZy10eC81LjMuNy9zcHJpbmctdHgtNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvbXliYXRpcy9zcHJpbmcvYm9vdC9teWJhdGlzLXNwcmluZy1ib290LWF1dG9jb25maWd1cmUvMS4zLjAvbXliYXRpcy1zcHJpbmctYm9vdC1hdXRvY29uZmlndXJlLTEuMy4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL215YmF0aXMvbXliYXRpcy8zLjQuNC9teWJhdGlzLTMuNC40LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL215YmF0aXMvbXliYXRpcy1zcHJpbmcvMS4zLjEvbXliYXRpcy1zcHJpbmctMS4zLjEuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9teXNxbC9teXNxbC1jb25uZWN0b3ItamF2YS81LjEuMzEvbXlzcWwtY29ubmVjdG9yLWphdmEtNS4xLjMxLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3Byb2plY3Rsb21ib2svbG9tYm9rLzEuMTguMjAvbG9tYm9rLTEuMTguMjAuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9jb20vZ2l0aHViL3BhZ2VoZWxwZXIvcGFnZWhlbHBlci1zcHJpbmctYm9vdC1zdGFydGVyLzEuMy4wL3BhZ2VoZWxwZXItc3ByaW5nLWJvb3Qtc3RhcnRlci0xLjMuMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9naXRodWIvcGFnZWhlbHBlci9wYWdlaGVscGVyLXNwcmluZy1ib290LWF1dG9jb25maWd1cmUvMS4zLjAvcGFnZWhlbHBlci1zcHJpbmctYm9vdC1hdXRvY29uZmlndXJlLTEuMy4wLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvY29tL2dpdGh1Yi9wYWdlaGVscGVyL3BhZ2VoZWxwZXIvNS4yLjAvcGFnZWhlbHBlci01LjIuMC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9naXRodWIvanNxbHBhcnNlci9qc3FscGFyc2VyLzMuMi9qc3FscGFyc2VyLTMuMi5qYXI6L1VzZXJzL2Vyemh1YW5nbml1Ly5tMi9yZXBvc2l0b3J5L2NvbS9hbGliYWJhL2Zhc3Rqc29uLzEuMi4yNC9mYXN0anNvbi0xLjIuMjQuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS8ubTIvcmVwb3NpdG9yeS9vcmcvc3ByaW5nZnJhbWV3b3JrL3NwcmluZy1jb3JlLzUuMy43L3NwcmluZy1jb3JlLTUuMy43LmphcjovVXNlcnMvZXJ6aHVhbmduaXUvLm0yL3JlcG9zaXRvcnkvb3JnL3NwcmluZ2ZyYW1ld29yay9zcHJpbmctamNsLzUuMy43L3NwcmluZy1qY2wtNS4zLjcuamFyOi9Vc2Vycy9lcnpodWFuZ25pdS93b3Jrc3BhY2UvbmFnZW50L0RvbmdUYWktYWdlbnQtamF2YS9yZWxlYXNlL2lhc3QtYWdlbnQuamFyOi9BcHBsaWNhdGlvbnMvSW50ZWxsaUogSURFQS5hcHAvQ29udGVudHMvbGliL2lkZWFfcnQuamFyLCB1c2VyLm5hbWU9ZXJ6aHVhbmduaXUsIGNvbS5zdW4ubWFuYWdlbWVudC5qbXhyZW1vdGU9LCBqYXZhLnZtLnNwZWNpZmljYXRpb24udmVyc2lvbj0xLjgsIHN1bi5qYXZhLmNvbW1hbmQ9Y29tLnN1eXUuc2VjZXhhbXBsZS5TZWNleGFtcGxlQXBwbGljYXRpb24sIGphdmEuaG9tZT0vVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlLCBzdW4uYXJjaC5kYXRhLm1vZGVsPTY0LCB1c2VyLmxhbmd1YWdlPXpoLCBqYXZhLnNwZWNpZmljYXRpb24udmVuZG9yPU9yYWNsZSBDb3Jwb3JhdGlvbiwgYXd0LnRvb2xraXQ9c3VuLmx3YXd0Lm1hY29zeC5MV0NUb29sa2l0LCBqYXZhLnZtLmluZm89bWl4ZWQgbW9kZSwgamF2YS52ZXJzaW9uPTEuOC4wXzMxMiwgamF2YS5leHQuZGlycz0vVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0V4dGVuc2lvbnM6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvZXh0Oi9MaWJyYXJ5L0phdmEvRXh0ZW5zaW9uczovTmV0d29yay9MaWJyYXJ5L0phdmEvRXh0ZW5zaW9uczovU3lzdGVtL0xpYnJhcnkvSmF2YS9FeHRlbnNpb25zOi91c3IvbGliL2phdmEsIHN1bi5ib290LmNsYXNzLnBhdGg9L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvcmVzb3VyY2VzLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9ydC5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvc3VucnNhc2lnbi5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvanNzZS5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvamNlLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2xpYi9jaGFyc2V0cy5qYXI6L1VzZXJzL2Vyemh1YW5nbml1L0xpYnJhcnkvSmF2YS9KYXZhVmlydHVhbE1hY2hpbmVzL2NvcnJldHRvLTEuOC4wXzMxMi9Db250ZW50cy9Ib21lL2pyZS9saWIvamZyLmphcjovVXNlcnMvZXJ6aHVhbmduaXUvTGlicmFyeS9KYXZhL0phdmFWaXJ0dWFsTWFjaGluZXMvY29ycmV0dG8tMS44LjBfMzEyL0NvbnRlbnRzL0hvbWUvanJlL2NsYXNzZXMsIGphdmEudmVuZG9yPUFtYXpvbi5jb20gSW5jLiwgc3ByaW5nLmFwcGxpY2F0aW9uLmFkbWluLmVuYWJsZWQ9dHJ1ZSwgZmlsZS5zZXBhcmF0b3I9LywgamF2YS52ZW5kb3IudXJsLmJ1Zz1odHRwczovL2dpdGh1Yi5jb20vY29ycmV0dG8vY29ycmV0dG8tOC9pc3N1ZXMvLCBpYXN0LnNlcnZlci5tb2RlPWxvY2FsLCBzdW4uaW8udW5pY29kZS5lbmNvZGluZz1Vbmljb2RlQmlnLCBzdW4uY3B1LmVuZGlhbj1saXR0bGUsIHN1bi5jcHUuaXNhbGlzdD19",
    "hostname": "localhost",
    "serverAddr": "",
    "containerName": "Apache Tomcat/9.0.46",
    "name": "Mac OS X-localhost-v1.1.3-java.action.github.com12313",
    "projectName": "SpringSec",
    "projectVersion": "120901",
    "autoCreateProject": 0,
}

METHODPOOL_JSON = {
    "detail": {
        "reqHeader": "c2VjLWZldGNoLW1vZGU6bmF2aWdhdGUKcmVmZXJlcjpodHRwOi8vbG9jYWxob3N0OjgwODAvCnNlYy1mZXRjaC1zaXRlOnNhbWUtb3JpZ2luCmFjY2VwdC1sYW5ndWFnZTp6aC1DTix6aDtxPTAuOQpjb29raWU6SWRlYS1mMmYwZDM1Nj1iN2I3MWM3Yi1kNWIzLTQzZWEtYWRiZC00OTJhMWM0ODE5ODc7IElkZWEtZjJmMGQzNTc9ZjY3NzQyYzEtYzZhNC00YTY2LTkwYmYtY2E3NGU5YzY4OThiCmR0LXRyYWNlaWQ6NzFhODRlYzlmNDhkNDJjYjk3NDkwMWVjOWNhNGI4MDAuMzQyMy4zNjg2LjAKc2VjLWZldGNoLXVzZXI6PzEKYWNjZXB0OnRleHQvaHRtbCxhcHBsaWNhdGlvbi94aHRtbCt4bWwsYXBwbGljYXRpb24veG1sO3E9MC45LGltYWdlL2F2aWYsaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOQpzZWMtY2gtdWE6IiBOb3QgQTtCcmFuZCI7dj0iOTkiLCAiQ2hyb21pdW0iO3Y9Ijk2IiwgIkdvb2dsZSBDaHJvbWUiO3Y9Ijk2IgpzZWMtY2gtdWEtbW9iaWxlOj8wCnNlYy1jaC11YS1wbGF0Zm9ybToibWFjT1MiCmhvc3Q6bG9jYWxob3N0OjgwODAKdXBncmFkZS1pbnNlY3VyZS1yZXF1ZXN0czoxCmNvbm5lY3Rpb246a2VlcC1hbGl2ZQphY2NlcHQtZW5jb2Rpbmc6Z3ppcCwgZGVmbGF0ZSwgYnIKdXNlci1hZ2VudDpNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV83KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTYuMC40NjY0LjkzIFNhZmFyaS81MzcuMzYKc2VjLWZldGNoLWRlc3Q6ZG9jdW1lbnQK",
        "agentId": 3423,
        "scheme": "http",
        "method": "GET",
        "contextPath": "",
        "pool": [
            {
                "invokeId": 1174,
                "interfaces": [],
                "targetHash": [490291580],
                "targetValues": "org.apache.tomcat.util.http.ValuesEnumerator@1d39417c",
                "signature": "org.apache.catalina.connector.Request.getHeaders",
                "originClassName": "org.apache.catalina.connector.Request",
                "sourceValues": "accept-language",
                "methodName": "getHeaders",
                "className": "javax.servlet.http.HttpServletRequest",
                "source": True,
                "callerLineNumber": 3424,
                "callerClass": "org.apache.catalina.connector.Request",
                "args": "",
                "callerMethod": "parseLocales",
                "sourceHash": [],
                "retClassName": "",
            },
            {
                "invokeId": 1175,
                "interfaces": [],
                "targetHash": [419874307],
                "targetValues": "zh-CN,zh;q=0.9",
                "signature": "org.apache.tomcat.util.http.ValuesEnumerator.nextElement",
                "originClassName": "org.apache.tomcat.util.http.ValuesEnumerator",
                "sourceValues": "org.apache.tomcat.util.http.ValuesEnumerator@1d39417c",
                "methodName": "nextElement",
                "className": "java.util.Enumeration",
                "source": False,
                "callerLineNumber": 3427,
                "callerClass": "org.apache.catalina.connector.Request",
                "args": "",
                "callerMethod": "parseLocales",
                "sourceHash": [490291580],
                "retClassName": "",
            },
            {
                "invokeId": 1176,
                "interfaces": [],
                "targetHash": [1543785287],
                "targetValues": "java.io.StringReader@5c044b47",
                "signature": "java.io.StringReader.<init>",
                "originClassName": "java.io.StringReader",
                "sourceValues": "zh-CN,zh;q=0.9",
                "methodName": "<init>",
                "className": "java.io.StringReader",
                "source": False,
                "callerLineNumber": 3451,
                "callerClass": "org.apache.catalina.connector.Request",
                "args": "",
                "callerMethod": "parseLocalesHeader",
                "sourceHash": [419874307],
                "retClassName": "",
            },
            {
                "invokeId": 1177,
                "interfaces": [],
                "targetHash": [1628901220],
                "targetValues": "cn.huoxian.iast.api.RequestWrapper@61170f64",
                "signature": "org.springframework.web.method.support.HandlerMethodArgumentResolverComposite.resolveArgument",
                "originClassName": "org.springframework.web.method.support.HandlerMethodArgumentResolverComposite",
                "sourceValues": 'method \'vuln1\' parameter 0 ModelAndViewContainer: reference to view with name \'cors/cors\'; default model {name={"敏感信息账号": "suyu", "敏感信息手机": "13888888888","敏感信息qq": "10010", "敏感信息身份证": "321222222222222222", "敏感信息地址": "网商路699号阿里巴巴园区"}} ServletWebRequest: uri=/cors1;client=0:0:0:0:0:0:0:1 org.springframework.web.servlet.mvc.method.annotation.ServletRequestDataBinderFactory@582953e7',
                "methodName": "resolveArgument",
                "className": "org.springframework.web.method.support.HandlerMethodArgumentResolver",
                "source": True,
                "callerLineNumber": 170,
                "callerClass": "org.springframework.web.method.support.InvocableHandlerMethod",
                "args": "",
                "callerMethod": "getMethodArgumentValues",
                "sourceHash": [],
                "retClassName": "",
            },
            {
                "invokeId": 1178,
                "interfaces": [],
                "targetHash": [438096027],
                "targetValues": "cn.huoxian.iast.api.ResponseWrapper@1a1cd09b",
                "signature": "org.springframework.web.method.support.HandlerMethodArgumentResolverComposite.resolveArgument",
                "originClassName": "org.springframework.web.method.support.HandlerMethodArgumentResolverComposite",
                "sourceValues": 'method \'vuln1\' parameter 1 ModelAndViewContainer: reference to view with name \'cors/cors\'; default model {name={"敏感信息账号": "suyu", "敏感信息手机": "13888888888","敏感信息qq": "10010", "敏感信息身份证": "321222222222222222", "敏感信息地址": "网商路699号阿里巴巴园区"}} ServletWebRequest: uri=/cors1;client=0:0:0:0:0:0:0:1 org.springframework.web.servlet.mvc.method.annotation.ServletRequestDataBinderFactory@582953e7',
                "methodName": "resolveArgument",
                "className": "org.springframework.web.method.support.HandlerMethodArgumentResolver",
                "source": True,
                "callerLineNumber": 170,
                "callerClass": "org.springframework.web.method.support.InvocableHandlerMethod",
                "args": "",
                "callerMethod": "getMethodArgumentValues",
                "sourceHash": [],
                "retClassName": "",
            },
            {
                "invokeId": 1179,
                "interfaces": [],
                "targetHash": [1192543238],
                "targetValues": "org.apache.tomcat.util.http.ValuesEnumerator@4714c406",
                "signature": "javax.servlet.http.HttpServletRequestWrapper.getHeaders",
                "originClassName": "javax.servlet.http.HttpServletRequestWrapper",
                "sourceValues": "Accept",
                "methodName": "getHeaders",
                "className": "javax.servlet.http.HttpServletRequest",
                "source": True,
                "callerLineNumber": 135,
                "callerClass": "org.springframework.web.context.request.ServletWebRequest",
                "args": "",
                "callerMethod": "getHeaderValues",
                "sourceHash": [],
                "retClassName": "",
            },
            {
                "invokeId": 1180,
                "interfaces": [],
                "targetHash": [929690313],
                "targetValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "signature": "org.apache.tomcat.util.http.ValuesEnumerator.nextElement",
                "originClassName": "org.apache.tomcat.util.http.ValuesEnumerator",
                "sourceValues": "org.apache.tomcat.util.http.ValuesEnumerator@4714c406",
                "methodName": "nextElement",
                "className": "java.util.Enumeration",
                "source": False,
                "callerLineNumber": 5294,
                "callerClass": "java.util.Collections",
                "args": "",
                "callerMethod": "list",
                "sourceHash": [1192543238],
                "retClassName": "",
            },
            {
                "invokeId": 1181,
                "interfaces": [],
                "targetHash": [1207614116],
                "targetValues": "[text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9]",
                "signature": "java.util.Arrays.asList",
                "originClassName": "java.util.Arrays",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "asList",
                "className": "java.util.Arrays",
                "source": False,
                "callerLineNumber": 51,
                "callerClass": "org.springframework.web.accept.HeaderContentNegotiationStrategy",
                "args": "",
                "callerMethod": "resolveMediaTypes",
                "sourceHash": [929690313, 2144890988, 929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1182,
                "interfaces": [],
                "targetHash": [2065964968],
                "targetValues": "text/html",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1183,
                "interfaces": [],
                "targetHash": [61035967],
                "targetValues": "application/xhtml+xml",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1184,
                "interfaces": [],
                "targetHash": [1069817527],
                "targetValues": "application/xml;q=0.9",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1185,
                "interfaces": [],
                "targetHash": [734131239],
                "targetValues": "image/avif",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1186,
                "interfaces": [],
                "targetHash": [1883465640],
                "targetValues": "image/webp",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1187,
                "interfaces": [],
                "targetHash": [1767168690],
                "targetValues": "image/apng",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1188,
                "interfaces": [],
                "targetHash": [1987727497],
                "targetValues": "*/*;q=0.8",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 304,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
            {
                "invokeId": 1189,
                "interfaces": [],
                "targetHash": [1388241581],
                "targetValues": "application/signed-exchange;v=b3;q=0.9",
                "signature": "java.lang.String.substring",
                "originClassName": "java.lang.String",
                "sourceValues": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "methodName": "substring",
                "className": "java.lang.String",
                "source": False,
                "callerLineNumber": 314,
                "callerClass": "org.springframework.util.MimeTypeUtils",
                "args": "",
                "callerMethod": "tokenize",
                "sourceHash": [929690313],
                "retClassName": "",
            },
        ],
        "secure": False,
        "uri": "/cors1",
        "url": "http://localhost:8080/cors1",
        "protocol": "HTTP/1.1",
        "replayRequest": False,
        "resBody": '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Java漏洞靶场<\\/title>\n    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">\n<\\/head>\n<body>\n\n<div style="padding: 40px;\n    text-align: center;\n    background: #1abc9c;\n    color: white;">\n    <h1>Java漏洞演示平台<\\/h1>\n    <button class="ui inverted secondary basic button"><a style="color: white" href="home">回到首页<\\/a><\\/button>\n<\\/div>\n\n<div style="text-align: center;margin: 0px auto;\n     margin-top: 50px;">\n    您获取的结果为:<p>{&quot;敏感信息账号&quot;: &quot;suyu&quot;, &quot;敏感信息手机&quot;: &quot;13888888888&quot;,&quot;敏感信息qq&quot;: &quot;10010&quot;, &quot;敏感信息身份证&quot;: &quot;321222222222222222&quot;, &quot;敏感信息地址&quot;: &quot;网商路699号阿里巴巴园区&quot;}<\\/p>\n<\\/div>\n\n<div>\n    <form action="/core3" method="post">\n        <input type="text" name="message" placeholder="请输入敏感信息">\n        <input type="submit" value="提交">\n    <\\/form>\n    <p><\\/p>\n    <!--        <p>提示<\\/p>-->\n    <!--        <p>"txf" and "1"="1"<\\/p>-->\n    <!--        <p>"txf" and "1"="2"<\\/p>-->\n<\\/div>\n\n\n\n<\\/body>\n<\\/html>\n',
        "clientIp": "127.0.0.1",
        "reqBody": "",
        "resHeader": "SFRUUC8xLjEgMjAwCkRvbmdUYWk6djEuMS4zClZhcnk6T3JpZ2luClZhcnk6T3JpZ2luClZhcnk6T3JpZ2luCg==",
    },
    "type": 36,
}


class AgentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.filter(pk=1).first()
        assert self.user is not None
        self.client.force_authenticate(user=self.user)
        data = self.register_agent(name="test")
        self.agent_id = data["id"]

    def raw_register(self, **kwargs):
        register_data = REGISTER_JSON.copy()
        register_data.update(kwargs)
        data = gzipdata(register_data)
        token, success = Token.objects.get_or_create(user=self.user)
        return self.client.post(
            "http://testserver/api/v1/agent/register",
            data=data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )

    def agent_heartbeat(self, **kwargs):
        heartbeatdata = {
            "detail": {
                "agentId": self.agent_id,
                "disk": "{}",
                "memory": '{"total":"2GB","rate":0,"use":"12421312312.115MB"}',
                "returnQueue": 0,
                "cpu": '{"rate":5323123}',
            },
            "type": 1,
        }
        heartbeatdata.update(kwargs)
        gzipdata(heartbeatdata)
        return self.client.post(
            "http://testserver/api/v1/report/upload",
            data=heartbeatdata,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )

    def agent_method_pool(self, **kwargs):
        method_pool_data = METHODPOOL_JSON
        method_pool_data["detail"]["agentId"] = self.agent_id
        method_pool_data["detail"].update(kwargs)
        data = gzipdata(method_pool_data)
        return self.client.post(
            "http://testserver/api/v1/report/upload",
            data=data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )

    def agent_report(self, json, **kwargs):
        reportjson1 = json
        reportjson1["detail"]["agentId"] = self.agent_id
        reportjson1["detail"].update(kwargs)
        data = gzipdata(reportjson1)
        return self.client.post(
            "http://testserver/api/v1/report/upload",
            data=data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )

    def register_agent(self, **kwargs):
        register_data = REGISTER_JSON
        register_data.update(kwargs)
        data = gzipdata(REGISTER_JSON)
        response = self.client.post(
            "http://testserver/api/v1/agent/register",
            data=data,
            HTTP_CONTENT_ENCODING="gzip",
            content_type="application/json",
        )
        return json.loads(response.content)["data"]

    def tearDown(self):
        pass


def gzipdata(data):
    return gzip.compress(json.dumps(data).encode("utf-8"))
