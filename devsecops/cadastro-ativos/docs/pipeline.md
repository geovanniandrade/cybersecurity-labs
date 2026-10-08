# Pipeline DevSecOps

O workflow `.github/workflows/cadastro-ativos.yml` roda no GitHub Actions. O deploy é completado por um timer systemd na VM, que consulta o registry pela internet. A VM não precisa receber conexões do GitHub através do NAT.

| Etapa | Função | Bloqueio |
| --- | --- | --- |
| Push | Alterações na pasta do projeto na branch `feat/cadastro-ativos` disparam o fluxo | Outras pastas não disparam |
| Build da aplicação | Instalar requirements.lock com Python 3.12 | Erro de instalação |
| Testes | Executar unittest: CRUD, migração, filtros e validações | Qualquer teste falhando |
| Bandit 1.9.4 | Analisar app.py e gerar JSON | Qualquer achado ou erro |
| pip-audit 2.10.1 | Analisar dependências e gerar JSON | Qualquer vulnerabilidade ou erro |
| Imagem | Construir Docker e testar /health | Build ou health falhando |
| Publicação | Enviar tags sha-<commit> e approved ao GHCR | Apenas push/dispatch na branch; PR não publica |
| Deploy | Comparar imagens, fazer backup SQLite e trocar container | Falha no pull/backup conserva container atual |
| Verificação | Esperar até 120 segundos por healthy | Falha tenta restaurar imagem anterior |

Relatórios ficam nos artifacts por 30 dias, inclusive se um scanner falhar. Baixe-os para o trabalho. Esta configuração analisa código e dependências Python; não analisa CVEs dos pacotes do sistema operacional da imagem.

## Configuração inicial da VM

Executar somente após confirmar a primeira execução bem-sucedida no Actions e tornar o pacote GHCR público. Repositório público não torna automaticamente o pacote público. Na conta GitHub, abra o pacote cadastro-ativos, Settings → Change visibility → Public. A imagem contém código; nunca inclua bancos ou segredos.

```bash
cd /home/docker01/cybersecurity-labs-ativos
git pull --ff-only
cp -a devsecops/cadastro-ativos/. /home/docker01/cadastro-ativos/
cd /home/docker01/cadastro-ativos
docker pull ghcr.io/geovanniandrade/cadastro-ativos:approved
bash deploy/update.sh
cat .deployed-commit
```

Git recebe os arquivos sem merge local; cp conserva backups existentes. O Compose de deploy utiliza explicitamente o volume externo cadastro-ativos_ativos_data: se ele não existir, falha em vez de criar um banco vazio.

O updater fixa o ID local da imagem após o pull, mantém uma tag da imagem anterior e copia um backup consistente para backups/ativos-predeploy-<data>.sqlite3. Não limpa backups ou imagens automaticamente. O rollback automático troca a imagem, não restaura o banco: migrações futuras incompatíveis exigem planejamento e restauração manual.

Depois de validar o primeiro deploy, habilite o timer como root:

```bash
cp deploy/cadastro-ativos-update.service /etc/systemd/system/
cp deploy/cadastro-ativos-update.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now cadastro-ativos-update.timer
systemctl list-timers cadastro-ativos-update.timer
```

O timer consulta a versão a cada minuto após o término da execução anterior. Só troca o container se o ID da imagem mudar. A VM deve estar ligada com internet. O túnel SSH serve para abrir o dashboard no Windows.

## Operação

```bash
journalctl -u cadastro-ativos-update.service -n 80 --no-pager
cat /home/docker01/cadastro-ativos/.deployed-commit
systemctl stop cadastro-ativos-update.timer
```

Os comandos mostram o histórico, identificam o commit implantado e pausam atualizações sem parar o dashboard. O serviço usa Docker e roda como root; somente administradores devem editar seus arquivos. Para consultar o container, use docker ps: compose.deploy.yaml exige ATIVOS_IMAGE e é usado pelo script.

## Demonstração e evidências

Altere um texto visível no template e faça push na branch. Capture testes, scanners, build/publicação no Actions, logs do updater, healthy, dashboard alterado e permanência de um ativo. Alterações rejeitadas não publicam a tag approved.

Arquivos implementados não comprovam execução remota. A primeira execução no Actions e o deploy pelo timer precisam ser confirmados no ambiente real. O deploy anterior do dashboard foi manual. A configuração continua na branch de trabalho, sem merge em main.
