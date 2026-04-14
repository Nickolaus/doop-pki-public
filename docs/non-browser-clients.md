# Non-Browser Clients

Many trust failures happen after the browser path is already working. That usually means the certificate is fine, but the runtime does not inherit the same trust path as the browser or OS.

## `curl`, OpenSSL, and System TLS Consumers

Most command-line clients use the operating system trust store or a configured CA bundle.

Recommended approach:
- install the root CA into the system trust store first
- verify with `curl -v https://...` or `openssl s_client`
- check environment variables such as `SSL_CERT_FILE` or `SSL_CERT_DIR` if behavior is unexpected

Common issue:
- the client is pinned to a custom CA bundle and ignores the system store

## Java

Java often requires explicit truststore handling.

Recommended approach:
- first determine whether the application uses the JVM default truststore or an application-specific truststore
- if necessary, import the root CA into the relevant truststore with `keytool`
- document the truststore location in the consuming application, not in this public repo

Common issue:
- the operating system trusts the root but the JVM truststore does not

Example import into the default JVM `cacerts` truststore:

```sh
sudo keytool -importcert -trustcacerts -alias doop-root-ca -file doop-root-ca.crt -keystore "$JAVA_HOME/lib/security/cacerts" -storepass changeit -noprompt
```

Example verification:

```sh
keytool -list -keystore "$JAVA_HOME/lib/security/cacerts" -storepass changeit -alias doop-root-ca
```

## Containers and Images

Containers frequently do not inherit trust from the host.

Recommended approach:
- bake the root CA into the image trust store during the image build, or
- mount a trusted CA bundle into the workload and point the application at it

Common issue:
- the host can reach the service over HTTPS but the container image cannot

## Kubernetes Nodes and Workloads

Keep Kubernetes guidance generic and client-side only.

Recommended model:
- node-level tooling should trust the root through the node OS trust store
- workloads should trust the root through the image trust store or a mounted CA bundle, depending on the runtime
- use `cert-manager` and DNS automation in-cluster only to manage service certificates, not to replace client trust design

Important distinction:
- node trust solves node-level HTTPS consumers
- workload trust solves application-level HTTPS consumers

Common issue:
- node trust is correct, but the container image still lacks the CA bundle

## Practical Verification

- `curl -v https://...`
- `openssl s_client -connect host:443 -servername host`
- `keytool -list -keystore ...`
- `keytool -list -keystore "$JAVA_HOME/lib/security/cacerts" -storepass changeit -alias doop-root-ca`
- container shell test using the exact runtime image

## Related Docs

- `docs/client-trust-matrix.md`
- `docs/verification-and-troubleshooting.md`
- `docs/rotation-and-lifecycle.md`

## References

- cert-manager ACME:
  - https://cert-manager.io/docs/configuration/acme/
- cert-manager DNS01:
  - https://cert-manager.io/docs/configuration/acme/dns01/
- external-dns RFC2136:
  - https://kubernetes-sigs.github.io/external-dns/latest/docs/tutorials/rfc2136/
