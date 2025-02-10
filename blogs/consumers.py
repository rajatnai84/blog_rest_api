import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BlogEditorConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.blog_id = self.scope['url_route']['kwargs']['blog_id']
        self.room_name = f'blog-{self.blog_id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def send_data(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({"content": content}))

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        content = data['content']
        
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type" : "send_data",
                "content": content
            }
        )
