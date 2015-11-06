

Session-based authentication is intended to work on the same server, and thus not well-suited for APIs.

Basic authentication _works_, but it means that the front-end needs to store the username and password somewhere, unencrypted.

Token-based authentication is a compromise - it involves always sending a header with a **token** that the front-end needs to store, but the token is a unique key that is generated when the user logs in, and thus cannot expose the user's password.

It is **imperative** that token-based authentication be used only over HTTPS - if someone intercepts the token, they can effectively masquerade as the logged-in user.

Django REST Framework offers some shortcuts to make using token-based authentication relatively simple!

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
