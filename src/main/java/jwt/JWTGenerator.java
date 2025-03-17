package jwt;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import java.security.Key;
import spark.Spark;
import com.google.gson.Gson;
import com.google.gson.JsonObject;

public class JWTGenerator {
    private final Key key;
    private static final Gson gson = new Gson();
    
    public JWTGenerator(String secretKey) {
        // For a fixed key based on a string
        this.key = Keys.secretKeyFor(SignatureAlgorithm.HS256);
    }
    
    public String generateToken(String subject) {
        return Jwts.builder()
                .setSubject(subject)
                .signWith(key)
                .compact();
    }
    
    public Key getKey() {
        return key;
    }
    
    public static void main(String[] args) {
        JWTGenerator generator = new JWTGenerator("mySecretKey");
        
        // Set the port
        Spark.port(4567);
        
        // Configure Spark to serve static files from the resources/public directory
        Spark.staticFiles.location("/public");
        
        // Enable CORS
        Spark.options("/*", (request, response) -> {
            String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
            if (accessControlRequestHeaders != null) {
                response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
            }
            
            String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
            if (accessControlRequestMethod != null) {
                response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
            }
            
            return "OK";
        });
        
        Spark.before((request, response) -> {
            response.header("Access-Control-Allow-Origin", "*");
            response.header("Access-Control-Request-Method", "GET,POST,PUT,DELETE,OPTIONS");
            response.header("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Requested-With,Content-Length,Accept,Origin");
            response.type("application/json");
        });
        
        // Generate token endpoint
        Spark.post("/token", (request, response) -> {
            try {
                JsonObject requestJson = gson.fromJson(request.body(), JsonObject.class);
                String username = requestJson.get("username").getAsString();
                
                String token = generator.generateToken(username);
                
                JsonObject responseJson = new JsonObject();
                responseJson.addProperty("token", token);
                
                return responseJson;
            } catch (Exception e) {
                response.status(400);
                JsonObject errorJson = new JsonObject();
                errorJson.addProperty("error", "Invalid request: " + e.getMessage());
                return errorJson;
            }
        }, gson::toJson);
        
        // Verify token endpoint
        Spark.post("/verify", (request, response) -> {
            try {
                JsonObject requestJson = gson.fromJson(request.body(), JsonObject.class);
                String token = requestJson.get("token").getAsString();
                
                String subject = Jwts.parserBuilder()
                        .setSigningKey(generator.getKey())
                        .build()
                        .parseClaimsJws(token)
                        .getBody()
                        .getSubject();
                
                JsonObject responseJson = new JsonObject();
                responseJson.addProperty("valid", true);
                responseJson.addProperty("subject", subject);
                
                return responseJson;
            } catch (Exception e) {
                JsonObject errorJson = new JsonObject();
                errorJson.addProperty("valid", false);
                errorJson.addProperty("error", e.getMessage());
                return errorJson;
            }
        }, gson::toJson);
        
        System.out.println("JWT Server started on http://localhost:4567");
        System.out.println("Web interface available at http://localhost:4567/index.html");
        System.out.println("API Endpoints:");
        System.out.println("  POST /token - Generate a token (requires JSON body with 'username' field)");
        System.out.println("  POST /verify - Verify a token (requires JSON body with 'token' field)");
    }
} 