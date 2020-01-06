package sample;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

import java.io.UnsupportedEncodingException;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class Token {
    private String username;
    private final int JWT_TOKEN_TIME_VALIDITY = 5 * 60;
    private String secret = "secret_key";

    public void setUsername(String username) {
        this.username = username;
    }

    private String createJWT(Map<String, Object> claims) {
        try {
            return Jwts.builder().setClaims(claims)
                    .setExpiration(new Date(Calendar.getInstance().getTimeInMillis() + (JWT_TOKEN_TIME_VALIDITY * 1000)))
                    .signWith(SignatureAlgorithm.HS256, secret.getBytes("UTF-8")).compact();
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return "";
    }

    public String createBibliographyCreateToken() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", "desktop");
        claims.put("user", username);
        claims.put("bibliography", true);
        claims.put("create", true);
        return createJWT(claims);
    }

    public String createBibliographyEditToken() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", "desktop");
        claims.put("user", username);
        claims.put("bibliography", true);
        claims.put("edit", true);
        return createJWT(claims);
    }

    public String createBibliographyDeleteToken() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", "desktop");
        claims.put("user", username);
        claims.put("bibliography", true);
        claims.put("delete", true);
        return createJWT(claims);
    }

    public String createFileDownloadToken() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", "desktop");
        claims.put("user", username);
        claims.put("file", true);
        claims.put("download", true);
        return createJWT(claims);
    }

    public String createFileDeleteToken() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("iss", "desktop");
        claims.put("user", username);
        claims.put("file", true);
        claims.put("delete", true);
        return createJWT(claims);
    }
}
