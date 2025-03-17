# JWT Token Generator and Validator

A simple, elegant web application for generating and validating JSON Web Tokens (JWT). This project provides both a REST API and a user-friendly web interface for working with JWTs.

![JWT Token Generator](https://img.shields.io/badge/JWT-Token%20Generator-blue)
![Spark Java](https://img.shields.io/badge/Spark-Web%20Framework-orange)
![JJWT](https://img.shields.io/badge/JJWT-0.11.2-green)

## Features

- 🔑 **Generate JWT Tokens**: Create tokens with custom subjects (usernames)
- ✅ **Validate JWT Tokens**: Verify token authenticity and extract subject data
- 🌐 **Web Interface**: User-friendly UI for token generation and validation
- 🚀 **REST API**: Simple endpoints for integration with other applications
- 🔒 **Secure**: Uses cryptographically strong signing keys


## Quick Start

### Prerequisites

- Java 8 or higher
- Maven

### Building the Application

Clone the repository and build using Maven:

```bash
git clone https://github.com/yourusername/jwt-token-project.git
cd jwt-token-project
mvn clean package
```

### Running the Application

Run the application using the generated JAR file:

```bash
java -jar target/vtys-webtoken-project-1.0-SNAPSHOT-jar-with-dependencies.jar
```

The application will start a web server on port 4567.

Access the web interface at: [http://localhost:4567/index.html](http://localhost:4567/index.html)

## API Documentation

The API offers two simple endpoints:

### Generate Token

```
POST /token
Content-Type: application/json

{
  "username": "your_username"
}
```

Response:

```json
{
  "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ5b3VyX3VzZXJuYW1lIn0.signature"
}
```

### Verify Token

```
POST /verify
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ5b3VyX3VzZXJuYW1lIn0.signature"
}
```

Response for valid token:

```json
{
  "valid": true,
  "subject": "your_username"
}
```

Response for invalid token:

```json
{
  "valid": false,
  "error": "Error message here"
}
```

## Technology Stack

- **Backend**: Java with Spark Framework
- **JWT Library**: JJWT (JSON Web Token for Java)
- **JSON Parsing**: Google Gson
- **Frontend**: HTML, CSS, JavaScript
- **Build Tool**: Maven

## Security Notes

- The application uses a secure key generation method (`Keys.secretKeyFor`) to create cryptographically strong keys for signing the tokens
- CORS is enabled to allow cross-origin requests
- For production use, consider configuring HTTPS

## Development

### Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── jwt/
│   │       └── JWTGenerator.java
│   └── resources/
│       └── public/
│           └── index.html
└── test/
    └── java/
        └── jwt/
            └── JWTGeneratorTest.java
```

### Running Tests

```bash
mvn test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgements

- [JJWT](https://github.com/jwtk/jjwt) - Java JWT: JSON Web Token for Java and Android
- [Spark Framework](http://sparkjava.com/) - A micro framework for creating web applications
- [JWT.io](https://jwt.io/) - For JWT information and debugging 
