package jwt;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class JWTGeneratorTest {
    @Test
    public void testGenerateToken() {
        JWTGenerator generator = new JWTGenerator("testKey");
        
        String token = generator.generateToken("testSubject");

        Claims claims = Jwts.parserBuilder()
                .setSigningKey(generator.getKey())
                .build()
                .parseClaimsJws(token)
                .getBody();

        assertEquals("testSubject", claims.getSubject());
    }
} 