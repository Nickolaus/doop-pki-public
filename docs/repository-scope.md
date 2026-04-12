# Repository Scope

This repository exists to distribute public PKI trust material safely.

## Safe to publish
- public root certificate
- intermediate certificates if needed for client trust chains
- platform install artifacts
- fingerprint documentation
- generic onboarding instructions

## Not safe to publish
- root private key
- intermediate private key
- CA database or signer state
- passwords or API keys
- internal topology documentation
- internal hostnames and IP addresses
- machine-local filesystem paths from the CA workstation
- private recovery instructions that expose environment details

## Review checklist before every commit
1. No file contains a private key block.
2. No file contains an internal IP address or private hostname.
3. No file references local workstation paths.
4. No file includes credentials or tokens.
5. The repository still makes sense as a public trust-distribution repo.

## Intended follow-up
If richer automation is added later, keep the same boundary:
- public certs and install artifacts here
- private CA material somewhere else
