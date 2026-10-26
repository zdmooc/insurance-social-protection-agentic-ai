import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.math.BigInteger;

/** Demonstration-only deterministic benefit calculator; not insurance tariff software. */
public final class RulesServer {
    static Map<String, String> params(String query) {
        Map<String, String> result = new HashMap<>();
        if (query == null) return result;
        for (String part : query.split("&")) {
            String[] entry = part.split("=", 2);
            if (entry.length == 2) {
                result.put(URLDecoder.decode(entry[0], StandardCharsets.UTF_8),
                           URLDecoder.decode(entry[1], StandardCharsets.UTF_8));
            }
        }
        return result;
    }

    static long calculate(long amountCents, long ratePercent, long capCents) {
        if (amountCents < 0 || amountCents > 1_000_000_000L || ratePercent < 0 || ratePercent > 100
                || capCents < 0 || capCents > 1_000_000_000L) {
            throw new IllegalArgumentException("Out of range");
        }
        // Round to nearest cent, half-up; integer arithmetic and no floating-point money.
        BigInteger product = BigInteger.valueOf(amountCents).multiply(BigInteger.valueOf(ratePercent));
        long covered = product.add(BigInteger.valueOf(50)).divide(BigInteger.valueOf(100)).longValueExact();
        return Math.min(covered, capCents);
    }

    static void reply(HttpExchange exchange, int code, String payload) throws IOException {
        byte[] bytes = payload.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(code, bytes.length);
        try (var stream = exchange.getResponseBody()) { stream.write(bytes); }
    }

    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8090"));
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/health", e -> reply(e, 200, "{\"status\":\"ok\"}"));
        server.createContext("/quote", e -> {
            if (!"GET".equals(e.getRequestMethod())) {
                reply(e, 405, "{\"error\":\"method_not_allowed\"}");
                return;
            }
            try {
                var p = params(e.getRequestURI().getRawQuery());
                long amount = Long.parseLong(p.get("amount_cents"));
                long rate = Long.parseLong(p.get("rate_percent"));
                long cap = Long.parseLong(p.get("cap_cents"));
                long quoted = calculate(amount, rate, cap);
                reply(e, 200, "{\"eligible_cents\":" + quoted + ",\"rule\":\"MIN(ROUND_HALF_UP(amount*rate/100),cap)\"}");
            } catch (RuntimeException ex) {
                reply(e, 400, "{\"error\":\"invalid_parameters\"}");
            }
        });
        server.setExecutor(java.util.concurrent.Executors.newFixedThreadPool(4));
        server.start();
        System.out.println("RulesServer started on port " + port);
    }
}
