# Security Policy

## Repository purpose
This repository is for public PKI trust and client interoperability material only.

Allowed content:
- public certificates
- trust-install artifacts
- generic client onboarding documentation
- generic interoperability guidance
- generic verification and troubleshooting guidance
- generic lifecycle and publication process guidance

Disallowed content:
- private keys
- passwords, tokens, or API credentials
- internal hostnames
- private suffixes such as `.home.arpa`
- RFC1918 IP addresses
- internal topology
- local workstation paths
- server-specific filesystem paths
- recovery notes that expose private infrastructure details
- screenshots or examples that reveal active internal service names
- live operational runbooks for private infrastructure

## Reporting
If sensitive material is found in this repository, treat it as a publishing error:
1. remove it immediately
2. rotate any affected secret or key material
3. review commit history before publishing further changes

## Publication rule of thumb
If a file answers any of these questions, it probably does not belong here:
- where the private services live
- how the private PKI is operated internally
- what internal names or addresses are used
- how to recover or administer private infrastructure
