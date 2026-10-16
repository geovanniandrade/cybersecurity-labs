#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
cd /home/docker01/cadastro-ativos
exec 9>/run/lock/cadastro-ativos-update.lock
flock -n 9 || exit 0
image=ghcr.io/geovanniandrade/cadastro-ativos:approved
container=cadastro-ativos-web-1
docker pull "$image"
candidate=$(docker image inspect --format '{{.Id}}' "$image")
current=$(docker inspect --format '{{.Image}}' "$container")
if [[ "$candidate" == "$current" ]]; then
  echo "Container ja utiliza a imagem aprovada."
  exit 0
fi
# Manter referencia local da versao anterior antes de substituir o container.
docker tag "$current" cadastro-ativos-rollback:previous
mkdir -p backups
stamp=$(date -u +%Y%m%dT%H%M%SZ)
docker exec "$container" python -c "import os,sqlite3; s=sqlite3.connect(os.environ['DATABASE_PATH']); t=sqlite3.connect('/tmp/ativos-predeploy.sqlite3'); s.backup(t); t.close(); s.close()"
docker cp "$container:/tmp/ativos-predeploy.sqlite3" "backups/ativos-predeploy-$stamp.sqlite3"
healthy() {
  for attempt in $(seq 1 60); do
    status=$(docker inspect --format '{{.State.Health.Status}}' "$container" 2>/dev/null || true)
    [[ "$status" == healthy ]] && return 0
    sleep 2
  done
  return 1
}
export ATIVOS_IMAGE="$candidate"
if docker compose -f compose.deploy.yaml up -d --no-build --pull never && healthy; then
  docker image inspect --format '{{index .Config.Labels "org.opencontainers.image.revision"}}' "$candidate" > .deployed-commit
  echo "Deploy concluido: $candidate"
else
  echo "Deploy falhou. Restaurando a imagem anterior; backup: backups/ativos-predeploy-$stamp.sqlite3" >&2
  export ATIVOS_IMAGE=cadastro-ativos-rollback:previous
  docker compose -f compose.deploy.yaml up -d --no-build --pull never
  healthy || { echo 'Rollback nao ficou healthy; verificar logs.' >&2; exit 1; }
  exit 1
fi
