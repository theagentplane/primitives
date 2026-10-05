# Security policy

## Supported versions

The package is pre-1.0. Security fixes are applied to the latest release.

## Reporting a vulnerability

Please report security issues **privately**. Do not open a public issue.

Use GitHub's private vulnerability reporting: open the **Security** tab of this repository and
choose **Report a vulnerability**.

We aim to acknowledge reports within 3 business days and to share a remediation plan after
triage. Please allow a reasonable window to fix the issue before public disclosure.

## Scope

This package contains data models and validation only. It performs no I/O and holds no secrets.
Relevant issues include validation that accepts malformed or hostile input in a way consumers
rely on (for example id or `traceparent` parsing), and supply-chain concerns with the published
package or its release workflow.

Data captured by Chronicle (prompts, tool inputs and outputs) can be sensitive. Handling of that
data is covered in the Chronicle repository's security policy.
