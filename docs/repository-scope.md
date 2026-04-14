# Repository Scope

This repository exists to distribute public PKI trust material safely and document how modern clients should trust and consume it.

## Safe to publish
- public root certificate
- intermediate certificates if needed for client trust chains
- platform install artifacts
- fingerprint documentation
- generic onboarding instructions
- generic client interoperability notes
- generic verification and troubleshooting guidance
- generic rotation and publication guidance

## Not safe to publish
- root private key
- intermediate private key
- CA database or signer state
- passwords or API keys
- internal topology documentation
- internal hostnames
- private suffixes
- RFC1918 IP addresses
- machine-local filesystem paths from the CA workstation
- private recovery instructions that expose environment details
- service screenshots or examples that reveal active private service names
- environment-specific operational runbooks

## Review checklist before every commit
1. No file contains a private key block.
2. No file contains an internal hostname, private suffix, or RFC1918 IP address.
3. No file references local workstation paths.
4. No file includes credentials or tokens.
5. The repository still makes sense as a public trust-and-interoperability repo.
6. A new reader can use the repo without learning anything about the private environment layout.

## Intended boundary
Keep this repository focused on client-side questions:
- what to trust
- how to install that trust
- how to verify trust
- how to troubleshoot trust failures
- how to handle rotation safely

Keep private CA operations, topology, and service inventory elsewhere.
