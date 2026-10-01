# Distro Source Playbook

## Primary References

- Fedora Packaging Guidelines: https://docs.fedoraproject.org/en-US/packaging-guidelines/
- RPM documentation: https://rpm.org/docs/
- Debian Policy Manual: https://www.debian.org/doc/debian-policy/
- Arch Linux PKGBUILD: https://wiki.archlinux.org/title/PKGBUILD
- Nixpkgs manual: https://nixos.org/manual/nixpkgs/stable/
- GNU Guix manual: https://guix.gnu.org/manual/en/
- openSUSE Packaging Guidelines: https://en.opensuse.org/openSUSE:Packaging_guidelines

## Research Checklist

1. Confirm the packaging policy section that directly applies.
2. Confirm required fields/macros/hooks rather than optional recommendations.
3. Capture distro-specific exceptions and compatibility caveats.
4. Record exact URL for each applied rule.

## Constraint Matrix Template

| Constraint | Source | Impact | Required Action | Priority |
| --- | --- | --- | --- | --- |
| Example: Patch metadata format | URL | Affects spec renderer | Enforce renderer output rule | P0 |

## Fact vs Inference Rule

- Mark statements backed by explicit docs as `fact`.
- Mark design extrapolation as `inference` and include confidence.
