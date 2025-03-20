import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import EmployeeSerializer
from .validators import EmployeeSchema
from pydantic import ValidationError

class EmployeeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('✅ Connected to WebSocket!')
        await self.send(text_data=json.dumps({"message": "Connected to WebSocket"}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        try:
            print('🔍 Validating data using Pydantic...')
            validated_data = EmployeeSchema(**data)  # ✅ Correct way to validate
        except ValidationError as e:
            error_msg = {"status": "Error", "errors": e.errors()}
            await self.send(text_data=json.dumps(error_msg))
            return  # ✅ Prevent further execution

        serializer = EmployeeSerializer(data=validated_data.dict())  # ✅ Convert Pydantic object to dict

        if serializer.is_valid():
            serializer.save()
            await self.send(text_data=json.dumps({"status": "Employee added", "employee": serializer.data}))
        else:
            await self.send(text_data=json.dumps({"status": "Error", "errors": serializer.errors}))
