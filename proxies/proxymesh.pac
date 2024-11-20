function FindProxyForURL(url, host) {
    // Configuration for ProxyMesh servers
    const PROXY_CONFIGS = {
        "us_ca": {
            server: "us-ca.proxymesh.com:31280",
            location: "Los Angeles, CA",
            // Use West Coast proxy for sites hosted in western US
            geoMatch: /\.(ca|wa|or|nv|az)\.us$/i
        },
        "us_wa": {
            server: "us-wa.proxymesh.com:31280",
            location: "Seattle, WA",
            // Use for specific content delivery or streaming services
            domains: ["cloudfront.net", "akamai.net", "fastly.net"]
        },
        "open": {
            server: "open.proxymesh.com:31280",
            location: "Atlanta, GA",
            // Default proxy for general purpose
            isDefault: true
        }
    };

    // Don't use proxy for local addresses
    if (isInNet(host, "192.168.0.0", "255.255.0.0") ||
        isInNet(host, "127.0.0.0", "255.0.0.0") ||
        isInNet(host, "10.0.0.0", "255.0.0.0")) {
        return "DIRECT";
    }

    // Don't use proxy for HTTPS connections to internal domains
    if (url.substring(0, 6) === "https:" && dnsDomainIs(host, ".internal.company.com")) {
        return "DIRECT";
    }

    // Route based on domain patterns
    for (let key in PROXY_CONFIGS) {
        const config = PROXY_CONFIGS[key];
        
        // Check domain-specific routing
        if (config.domains) {
            for (let domain of config.domains) {
                if (dnsDomainIs(host, domain)) {
                    return "PROXY " + config.server;
                }
            }
        }

        // Check geographical routing
        if (config.geoMatch && host.match(config.geoMatch)) {
            return "PROXY " + config.server;
        }
    }

    // Use the default proxy (open.proxymesh.com) for all other cases
    return "PROXY " + PROXY_CONFIGS.open.server;
}

// Helper function to check if URL matches certain patterns
function matchesPattern(url, patterns) {
    for (let pattern of patterns) {
        if (shExpMatch(url, pattern)) {
            return true;
        }
    }
    return false;
} 