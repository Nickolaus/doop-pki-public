# Client Trust Matrix

Use this matrix to decide how a client should trust the public root CA and what extra steps may still be required after OS trust is installed.

## Browser Clients

| Client class | Is OS trust enough? | Extra app trust config commonly needed? | Recommended deployment path | Main verification | Common failure category |
|---|---|---|---|---|---|
| Safari on macOS/iOS/iPadOS/visionOS | Usually yes | Sometimes manual full-trust enablement on mobile platforms | Apple configuration profile or MDM trusted certificate payload | Open the intended internal HTTPS site and inspect certificate trust | Root installed but not marked trusted for SSL |
| Chrome / Edge on Windows | Usually yes | Rare | Intune trusted certificate profile, GPO, or LocalMachine script fallback | Open the intended internal HTTPS site and inspect certificate chain | Root not installed into the machine trust store |
| Chrome / Edge on macOS | Usually yes | Rare | Apple profile / MDM | Open the intended internal HTTPS site and inspect certificate chain | OS trust missing or stale app session |
| Chrome / Edge on Linux | Usually yes | Sometimes per-distribution package or runtime differences | OS trust store via package/config-management/script | `curl -v` or browser certificate view | Root installed incorrectly into the Linux trust store |
| Firefox | Not always | Often | Prefer enterprise roots import behavior or managed policy where possible | Visit the intended site and inspect Firefox certificate error details | Firefox is not using the OS trust path you expected |

## OS Trust Stores

| OS | Is OS trust enough for most apps? | Extra app trust config commonly needed? | Recommended deployment path | Main verification | Common failure category |
|---|---|---|---|---|---|
| macOS | Usually yes | Firefox or Java may differ | Configuration profile, MDM, or Keychain import | Keychain Access trust state plus browser check | Cert installed in wrong keychain or not trusted |
| Windows | Usually yes | Firefox or Java may differ | Intune trusted cert profile, GPO, or LocalMachine import script | `certlm.msc` or `certutil -store Root` | Root imported to CurrentUser when machine trust was needed |
| Debian / Ubuntu | Usually yes | Containers and Java may differ | `update-ca-certificates` via script or config management | `openssl verify` or `curl -v` | Cert copied outside the system CA path or trust store not refreshed |
| RHEL / Fedora | Usually yes | Containers and Java may differ | `update-ca-trust extract` via script or config management | `trust list` or `curl -v` | Cert placed outside the anchor directory or trust store not rebuilt |
| Android | Sometimes | Often | Managed deployment preferred; manual install only when justified | Browser test plus target-app test | App trusts only system anchors or enforces its own trust policy |

## Non-Browser Clients

| Client class | Is OS trust enough? | Extra app trust config commonly needed? | Recommended deployment path | Main verification | Common failure category |
|---|---|---|---|---|---|
| `curl` / OpenSSL consumers | Usually yes | Sometimes custom CA bundle env vars | OS trust store first | `curl -v https://...` or `openssl s_client` | Client is not using the system trust store |
| Java | Often no | Yes | Import into the JVM truststore or a dedicated application truststore | `keytool -list` and application startup test | JVM truststore does not include the root |
| Containers / images | Often no | Yes | Bake the root into the base image or mount a CA bundle | `curl` from inside the container | Image trust store differs from host trust |
| Kubernetes nodes | Usually yes for node-level tools | Sometimes | Install the root into node OS trust | `curl` on the node or runtime pull test | Node image or runtime CA bundle does not include the root |
| Kubernetes workloads | Not always | Often | Use image trust or mounted CA bundle, depending on the workload | Application-specific HTTPS call test | Workload trust bundle differs from node trust |

## Managed Deployment Paths

| Target | Recommended path |
|---|---|
| Apple devices | Configuration profile or MDM trusted certificate payload |
| Windows managed devices | Intune trusted certificate profile or Group Policy |
| Windows unmanaged admin machine | PowerShell or `certutil` fallback |
| Debian / Ubuntu | Config management or `linux/install-root-ca-debian.sh` |
| RHEL / Fedora | Config management or `linux/install-root-ca-redhat.sh` |
| Android | Managed deployment where possible; manual install only when required |

## Practical Defaults

- Start with OS trust.
- If a browser works but an app fails, treat that as an application trust problem, not proof that the certificate is wrong.
- Prefer managed trust deployment over manual one-off import.
- Prefer machine-wide trust for shared admin devices when appropriate.

## Related Docs

- `docs/browser-interop.md`
- `docs/non-browser-clients.md`
- `docs/verification-and-troubleshooting.md`

## References

- Apple Platform Deployment:
  - https://support.apple.com/guide/deployment/welcome/web
- Microsoft Learn trusted certificate deployment:
  - https://learn.microsoft.com/intune/intune-service/protect/certificates-configure
- Red Hat shared system certificates:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/securing_networks/using-shared-system-certificates
- cert-manager ACME:
  - https://cert-manager.io/docs/configuration/acme/
