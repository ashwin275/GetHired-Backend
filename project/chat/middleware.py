from channels.middleware import BaseMiddleware #type:ignore
from channels.db import database_sync_to_async #type:ignore
from rest_framework_simplejwt.exceptions import AuthenticationFailed #type:ignore
from rest_framework_simplejwt.tokens import AccessToken   #type:ignore
from users.models import Account

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            print(scope)
            headers = dict(scope["headers"])
            # print('Headers',headers)
            test_token = headers.get(b"Tokens")
            print('TestToken',test_token)
            raw_token = headers.get(b"authorization", b"").decode("utf-8")
            
            print('raw-token',raw_token)
           
            if raw_token.startswith("Bearer "):
                token = raw_token.split(' ')[1]
                print('Token',token)
            else:
                
                 raise AuthenticationFailed("Invalid token format. Use 'Bearer <token>'.")

            user = await self.get_user_from_token(token)
            print('user',user)
            if not user:
                
                raise AuthenticationFailed("Invalid or expired token.")
            scope["user"] = user
        except AuthenticationFailed as e:
            print(str(e))
            await self.close_socket(send ,str(e))
            return

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
      
        
        try:
            try:
               access_token = AccessToken(token)
            except Exception as e:
                print(str(e))
                return False
            # print('acces token ',access_token)
            user_id = access_token['user_id']
            try:
                user = Account.objects.get(id=user_id)
            except Account.DoesNotExist:
                # print('no user')
                return False

            return user
        except AuthenticationFailed as e:
            print(str(e))
            return None

    async def close_socket(self, send,error_message):
        await send({"type": "websocket.close", "code": 4000})
        await send({"type": "websocket.send", "text": error_message})
