# Android Trust Notes

Android needs separate handling from Apple, Windows, and Linux.

## Current recommendation
Only install the internal root CA on managed Android devices that actually need to access internal HTTPS services.

## Important platform behavior
On modern Android, user-installed CA certificates are not automatically trusted by all apps.

Practical implications:
1. Browser access may work where an individual app does not.
2. Apps can restrict trust to system CAs only.
3. If a specific app does not trust a user-installed CA, that is an app trust-model issue, not a problem with the certificate itself.

## Best-practice deployment
1. Prefer managed-device or work-profile deployment when possible.
2. Use the Android certificate install flow only on devices that must trust internal services.
3. Test the actual target app after installing the root CA.
4. Do not assume that installing the CA once makes every app trust it.

## Verification
After installing the root CA:
1. test browser access to the intended internal HTTPS service
2. test the specific Android app you care about
3. if the app still does not trust the internal CA, check whether it trusts only system anchors

## Reference material
- Android network security configuration
- Android KeyChain / certificate install APIs
