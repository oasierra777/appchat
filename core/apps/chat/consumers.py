import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

from apps.chat.models import Message

class ChatConsumer(WebsocketConsumer):
    #Diccionario para los usuarios conectados
    connected_users = {}
    
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'sala_chat_%s' % self.id
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            self.username = self.user.username
        else:
            None
            
        #Agregamos el usuario al diccionario de usuarios conectados
        if self.room_group_name not in self.connected_users:
            self.connected_users[self.room_group_name] = []
        if self.username:
            self.connected_users[self.room_group_name].append(self.username)

        #print('Conexión establecida al room_group_name ' + self.room_group_name)
        #print('Conexión establecida channel_name ' + self.channel_name)

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        
        #enviamos la lista de usuarios coectados a los clientes de la sala
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'user_list',
            'users': self.connected_users[self.room_group_name]
        })
        
    def disconnect(self, close_code):
        #Eliminamos al usuario del diccionario de usuarios conectados
        if self.username in self.connected_users[self.room_group_name]:
            self.connected_users[self.room_group_name].remove(self.username)
        #print('Se ha desconectado')
        #Enviamos la lista de usuarios conectados ACTUALIZADOS a los clientes de la sala
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'user_list',
            'users': self.connected_users[self.room_group_name]
        })
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    
    def receive(self, text_data):
        #print('Mensaje recibido')
        try: 
            text_data_json = json.loads(text_data)
            event_type = text_data_json.get('type')
            
            if event_type == 'chat_message':
                message = text_data_json['message']
            
                # Obtenemos el ID del usuario que envia el mensaje
                if self.scope['user'].is_authenticated:
                    sender_id = self.scope['user'].id
                else:
                    sender_id = None
                    
                if sender_id:
                    # Grabamos el mensaje en la base de datos
                    message_save = Message.objects.create(user_id=sender_id, room_id=self.id, message=message)
                    message_save.save()
                                                        
                    # Sincronizamos y enviamos el mensaje a la sala de chat
                    async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'datetime': timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S'),
                        'sender_id': sender_id
                    })
                else:
                    print('Usuario no autenticado. Ignorando el mensaje')
            elif event_type == 'user_list':
                #Este evento se maneja desde js, del lado del cliente
                pass
                
        
        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar el JSON: ', e)
        except KeyError as e:
            print('Clave faltante en el JSON: ', e)
        except Exception as e:
            print('Error desconocido: ', e)    
            
    def user_list(self, event):
        #enviar la lista de ususarios conectados
        self.send(text_data=json.dumps({
            'type': 'user_list',
            'users': event['users']
        }))
            
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        current_user_id = self.scope['user'].id
        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message':message,
                'username': username,
                'datetime': datetime
            }))