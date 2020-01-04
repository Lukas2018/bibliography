package sample;

import com.auth0.jwt.algorithms.Algorithm;

public class Token {

    private void createJWT() {
        Algorithm algorithm = Algorithm.HMAC256("secret_key");
    }
}
