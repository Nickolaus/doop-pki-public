# Browser Interoperability

Browser success is a useful signal, but it is not a universal proof that every client trusts the CA correctly.

## System-Trust Browsers

These browsers usually follow the operating system trust store:
- Safari
- Chrome
- Edge

If these browsers fail, the problem is often one of:
- the root was never installed
- the root was installed into the wrong store
- the server is presenting the wrong certificate or an incomplete chain
- the hostname on the certificate does not match the URL

## Firefox

Firefox should be treated separately.

Depending on platform and management mode, Firefox may not use the same trust path as the operating system by default. Prefer a managed enterprise-roots import path where available.

Recommended approach:
- use Firefox enterprise policy or the enterprise-roots behavior where available
- do not assume that OS trust automatically covers Firefox everywhere
- if Firefox fails while Chrome or Safari succeeds, check Firefox trust behavior before changing the certificate

Key implication:
- browser success in Chrome does not prove Firefox is configured correctly
- browser success in Firefox does not prove Java, containers, or mobile apps are configured correctly

## Practical Verification

1. Open the intended internal HTTPS site.
2. Inspect the certificate chain in the browser UI.
3. Confirm the root or issuing CA chains to the expected public root.
4. Compare the browser result with a system client such as `curl`.

If Chrome succeeds but Firefox fails:
- check Firefox enterprise roots behavior or certificate authority settings
- do not immediately reissue the server certificate

## Common Failure Patterns

| Symptom | Likely cause |
|---|---|
| Chrome works, Firefox fails | Firefox trust path differs from OS trust |
| Safari on iPhone still warns after profile install | Full trust for the installed root has not been enabled |
| All browsers fail with hostname error | Server certificate name mismatch |
| Browser works, target app fails | App uses its own trust model |

## Related Docs

- `docs/client-trust-matrix.md`
- `docs/verification-and-troubleshooting.md`
- `docs/non-browser-clients.md`

## References

- Mozilla enterprise policy templates:
  - https://mozilla.github.io/policy-templates/
- Apple Platform Deployment:
  - https://support.apple.com/guide/deployment/welcome/web
