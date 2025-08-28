#!/usr/bin/env bash
set -euo pipefail
mkdir -p sbom
for svc in gateway services/diagnostics services/curriculum services/prediction services/ingestion; do
  echo "Generating SBOM for $svc"
  echo "{"name":"$svc"}" > sbom/$(echo $svc | tr '/' '-').spdx.json
done

echo "SBOMs written to ./sbom (stub). Integrate Syft or CycloneDX in CI."
