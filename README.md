![101505185](https://user-images.githubusercontent.com/82800805/175931942-7561237c-4219-452e-8c52-2125d4972170.png)
## Intro
 **Beepo is a blockchain powered chat app with full wallet integration allowing you to trade assets with friends at the touch of a button.**
<br/>
>  Connect to the <b>Test APIs</b> on heroku [here](https://beepo-app.herokuapp.com/api/v1).

>  View API documentation [here](https://beepo-app.herokuapp.com/docs).

>  View alternative API documentation [here](https://beepo-app.herokuapp.com/redoc).

<b> <span style = "color:green;"> PS ✅ The Test API is live and currently in developement. </span> </b>

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
  
  The **Key Exchange Algorithm** type used in this project is the [***Elliptic Curve Diffie-Hellman***](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/x25519/) algorithm. It works thus:
  
  1. The server and client each generate a public/private keypair on their own end.
  
  2. The private key is safely stored, recommended way of storing is by encrypting it using symmetric encryption.
  
  3. The server and the client exchange their public key with each other.
  
  4. The server and client compute a shared key through a preset key generation algorithm independently on their end using their **private key** and the **peer public key**. **Peer public key** refers to the public key of the other party. The **shared key** computed will be the same for the server and client hence the name ***shared key***, however, this **shared key** is never stored, it is compute at will using the **private key** and **peer public key** when it is needed for encryption/decryption.
  
  5. Once the exchange is complete, data is encrypted and decrypted using ***AES*** encryption. The client encrypts, the server decrypts and vice-versa. The form of **AES** used will not be disclosed here.
  
  <br/>
  
- <b> API Layer </b>

The [Application Programming Interface](https://beepo-app.herokuapp.com/docs) is in development currently and divided into strategic sections. The [documentation](https://beepo-app.herokuapp.com/redoc) is explanatory and allows for testing the API from the page.
  
  All schemas defined should be studied, fields that deliver encrypted content are marked with *[Encrypted]*, fields that are also expected to be sent as encrypted text from client are also marked the same way. 
  
  
  
  
  

