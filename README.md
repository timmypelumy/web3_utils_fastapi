![101505185](https://user-images.githubusercontent.com/82800805/175931942-7561237c-4219-452e-8c52-2125d4972170.png)
## Intro
 **Beepo is a chat app with full blockchain wallet integration allowing you to trade assets with friends at the touch of a button.**
<br/>
>  Connect to the <b>Test APIs</b> on heroku [here](https://beepo-app.herokuapp.com/api/v1).

>  View API documentation [here](https://beepo-app.herokuapp.com/docs).

>  View alternative API documentation [here](https://beepo-app.herokuapp.com/redoc).

<b> PS ✅ The Test API is live and currently in development. </b>

---

<br/>
 
## Documentation

- <b>Authentication Layer</b>

The authentication layer follows the `Open Authentication (OAuth) ` standard. This employs the use of a `username` and `password` for authenticating with the server.
  The server checks the `username` and `password` against the set values and determines whether authorization is granted or not. The `username` parameter is a standard placeholder in OAuth, any value that fits the context such as `email`, `phone` or some `id` can be supplied via the `username` parameter. 
  
  To limit the use of the `username` and `password` for authentication and preserve authentication sessions in between app states, ***JWT (JSON Web Token)*** has been introduced into the authentication layer. Once a user authenticates with their `username` and `password`, a **JWT access token** is returned to them, this is stored locally on the client side and attached to subsequent request to protected endpoints. The server validates the access token and determines whether access is granted or not. The **JWT tokens** used in this project have an expiration time in minutes, therefore, once an access token is revoked, a new one must be requested by re-authenticating with the `username` and `password`.
  
  The standard way of attaching the **JWT token** to web requests as employed in this project is to attach it to a request header named `Authorization` whose value is `Bearer <token>`. The value of the header must start with word `Bearer` followed by a space and the **JWT access token**.
  
  If a token is revoked, a `401 Unauthorized` response is returned back to the client. The same response is returned when trying to access protected endpoints without a valid access token. The access token can be stored safely on the client side without any need for encryption as it is already encrypted by the server.
  
  > Token expiration time : `15 minutes`
  
  <br/>
  
- <b>Data Encryption Layer</b>

The data encryption layer ensures security and privacy of data on the server and also in transit between the server and the client. **Symmetric encryption** is used to store data safely on th server, the details of the implementation is irrelevant to the client. **Asymmetric encryption** is used for securing data in transit between the server and the client. **Asymmetric encryption** employs the use of **public and private keys** in encrypting and decrypting data.
  
  The **Encryption Algorithm** type used in this project is the [***Rivest Shamir Adleman (RSA) public key encryption***](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/) algorithm. It works thus:
  
  1. The server and client each generate a public/private keypair on their own end.
  
  2. The private key is safely stored, recommended way of storing is by encrypting it using symmetric encryption.
  
  3. The server and the client exchange their public key with each other.
  
  4. Encryption is done on either end by using the **public key** of the peer ( `peer_public_key` ) to encrypt data. The data is then sent to this peer.
  
  5. The peer then uses their own private key to decrypt the data into a meaning state.
  
  <br/>
  
- <b> API Layer </b>

The [Application Programming Interface](https://beepo-app.herokuapp.com/docs) is in development, the API reference uses the Swagger OpenAPI format. An [alternative documentation](https://beepo-app.herokuapp.com/redoc) is also available. Quick testing can be done directly from the Swagger API reference page.
  
All schemas defined should be noted, fields that deliver encrypted content are marked with *[Encrypted]*, fields that are also expected to be sent as encrypted text from client are also marked the same way. 
  
  
  
  
  

