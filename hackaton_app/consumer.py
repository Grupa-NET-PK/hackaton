import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DashConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groupname = 'dashboard'

    async def connect(self):
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()

    # async def websocket_connect(self, message):
    #     self.groupname = 'dashboard'
    #     await self.channel_layer.group_add(self.groupname, self.channel_name)
    #     await self.accept()

    async def disconnect(self, code):
        print('Disconnected', code)

    # async def send(self, text_data=None, bytes_data=None, close=False):
    #     print(text_data)

    async def receive(self, text_data):
        # print('>>>>', text_data)
        # datapoint = json.loads(text_data)
        # val = datapoint['Target']

        author = str(self.scope['user'])
        Response_ = {
            # 'Message': text_data,
            'Target': text_data,
        }

        new_event = {
            'type': 'deprocessing',
            'text': json.dumps(Response_)
        }

        await self.channel_layer.group_send(
            self.groupname,
            new_event
        )

    async def deprocessing(self, event):
        print('\n', event)
        front_response = event.get('text', None)
        if front_response is not None:
            compiled_response_data = json.loads(front_response)
        author = self.scope['user']
        target = compiled_response_data['Target']
        Response_ = {
            # 'Message': compiled_response_data['Message'],
            'Target': target,
        }
        # message = event['text']

        # Send message to WebSocket

        await self.send(text_data=json.dumps(Response_))
