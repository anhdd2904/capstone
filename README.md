# URL where the application is hosted: https://capstone-3-final.onrender.com
# Instructions to set up authentication:
## Because my project only has a restful API part, the authentication part will be a little different from previous projects.
## Auth0 setup:
# API Authentication with Auth0

## Overview

This project uses [Auth0](https://auth0.com) for authentication in a Machine-to-Machine (M2M) context, meaning that our API will authenticate clients through client credentials and issue tokens to allow access to protected endpoints. 

## Steps to Configure Auth0

### 1. Create an Auth0 Account

If you haven't already, you'll need to sign up for an Auth0 account. You can do so [here](https://auth0.com/signup). 

### 2. Create a New Auth0 Application

1. Once logged into Auth0, navigate to the **Dashboard**.
2. Click on the **Applications** tab from the left sidebar, and then select **Create Application**.
3. Choose **Machine to Machine Applications** as the application type.
4. Select your backend API as the audience for the API that you want to authorize access to.
5. Grant the application the appropriate permissions (scopes) that your API will accept.

### 3. Retrieve Client Credentials

After creating the application, Auth0 will provide you with a **Client ID** and **Client Secret**. You will use these credentials to request an access token from Auth0.

- **Client ID**: Your application's unique identifier.
- **Client Secret**: A secret key used to authenticate your application.

### 4. Configure API Audience

In my project, i set Audience default id : flask_app



### 5. Generate Access Tokens

To access protected routes of the API, you will need to obtain an access token from Auth0. Here's an example of how to do this using `curl`:

```bash
curl --request POST \
  --url https://<your-auth0-domain>/oauth/token \
  --header 'content-type: application/json' \
  --data '{
    "client_id": "<your-client-id>",
    "client_secret": "<your-client-secret>",
    "audience": "flask_app",
    "grant_type": "client_credentials"
  }'
```

### Permissions: Following permissions should be created under created API settings.
- view:books
- view:authors
- post:books
- post:authors
- delete:books
- delete:authors
- update:books
- update:authors
