# Public Trust Distribution

This document describes how to distribute the public root CA to managed clients.

## Principle
The root certificate is public by design. Distributing it is safe. Trusting it should still be limited to managed clients that need to access internal HTTPS services.

## Recommended device classes
- admin macOS devices
- admin Windows devices
- admin Linux devices
- managed mobile devices when required

## Device classes to avoid by default
- guest devices
- unmanaged personal devices
- most IoT devices

## Best-practice distribution model
Use platform-native trust deployment:
- Apple: configuration profile
- Windows: script, GPO, or MDM trusted certificate profile
- Linux: config management or package/bootstrap script

## Rotation guidance
When the root certificate changes:
1. publish the new public certificate in `certs/`
2. regenerate platform artifacts
3. distribute the new trust anchor before any dependent service uses it
4. remove the old root only after all managed clients are migrated

## Verification guidance
Before trusting a new root on any device:
1. verify the published fingerprint out of band
2. compare it with the certificate being installed
3. only then import it into the trust store
