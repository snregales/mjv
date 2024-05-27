# API

## Swagger

Swagger docs are located on the root URL "/".
This is set here instead of the usual "/swagger/",
cause there is nothing at the root

## User Authentication

All GRUD actions are user restricted,
thus you need to have a user account and an access token

### User Registration

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "user",
  "email": "user@example.com",
  "password": "password123"
}'
```

### User Login (Get Access Token)

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username": "testuser",
  "password": "password123"
}'
```

This command will return a JSON response with the access_token. For example:

```bash
{
  "access_token": "your_jwt_token_here"
}
```

## Todo

Replace `your_jwt_token_here` with the actual JWT token obtained from the login response.

### Create todo

```bash
curl -X POST http://127.0.0.1:5000/todos/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token_here" \
-d '{
  "task": "Test Task",
  "completed": false
}'
```

### Update todo

```bash
curl -X PUT http://127.0.0.1:5000/todos/todo_id \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token_here" \
-d '{
  "task": "Updated Task",
  "completed": true
}'
```

### Delete todo

```bash
curl -X DELETE http://127.0.0.1:5000/todos/todo_id \
-H "Authorization: Bearer your_jwt_token_here"
```
