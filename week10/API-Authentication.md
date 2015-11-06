# API Authentication

Session-based authentication is intended to work on the same server, and thus not well-suited for APIs.

Basic authentication _works_, but it means that the front-end needs to store the username and password somewhere.

Token-based authentication is a compromise - it involves always sending a header with a **token** that the front-end needs to store, but the token is a unique key that is generated when the user logs in, and thus cannot does not expose the user's password if it becomes compromised.

It is **imperative** that token-based authentication be used only over HTTPS - if someone intercepts the token, they can effectively masquerade as the logged-in user.

Django REST Framework offers some shortcuts to make using token-based authentication relatively simple!

## Back-end

You don't have to write much code, just add an installed app, add TokenAuthentication to the list of authentication classes, wire up a pre-made view to allow for logging in, and then migrate your database.

### settings.py

```python
INSTALLED_APPS = (
    # ...
    'rest_framework.authtoken',
)

REST_FRAMEWORK = {
    # ...
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # ...
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

### urls.py

```python
urlpatterns = [
    # ...
    # You can set the URL regex to whatever you want to match your API
    # e.g., r'^api/login'
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
]
```

### Database

```bash
python manage.py migrate
```


## Front-end

To log in, POST a JSON object with the username and password to the URL for the obtain_auth_token view. This view will create a token associated with a user if one doesn't already exist, and return that token back as JSON.

### Example login POST
```
POST /api-token-auth/
Content-Type: application/json

{"username": "admin", "password": "password"}
```

### Example login response
```
Content-Type: applicatin/json

{"token":"0cd22429267deae3b7efb2c96012ff4b01792780"}
```

Future requests to resources that require authentication must include an Authorization header with the token in the following format:

### Example authenticated GET
```
GET /api/whoami/
Authorization: Token 0cd22429267deae3b7efb2c96012ff4b01792780
```

Note that the header name is `Authorization` and the value must be the word `Token` followed by whitespace followed by the `token` value returned from the obtain_auth_token view. Any extra punctuation or forgetting the word `Token` will result in an authentication failure!


## Logging out

To log out, you have two options: one, the front-end just "forgets" the token. This isn't particularly secure, because if somehow the token became compromised it would continue to work.

A better solution is to have a view that actually *deletes* the token from the database. Future login attempts will generate new tokens.

Here's a sample view to accomplish this:

```python
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    Token.objects.get(user=request.user).delete()
    return Response({'username': None})
```

If a user attempts to POST to this page without passing in their token, they receive a 403 error. Otherwise, the token for the user gets deleted, and a simple response is returned letting them know it was successful.


## More details

You can take a look at the `authtoken` code on [GitHub](https://github.com/tomchristie/django-rest-framework/tree/master/rest_framework/authtoken). The `rest_framework.authtoken` app introduces a new Model, `rest_framework.authtoken.models.Token`. This Model consists of the token, which is a randomly generated 40-digit hex key, and a OneToOne relationship with the `User` Model.

This means each user has one and only one token. If a user attempts to log in who has logged in before, they reuse the token that was previously generated for them, unless they have explicitly deleted the token by logging out.

This is generally good enough if all communication happens over HTTPS and the token is never stored other than in a protected cookie with the front-end side of things, but you could extend the token model if you wanted additional security.
