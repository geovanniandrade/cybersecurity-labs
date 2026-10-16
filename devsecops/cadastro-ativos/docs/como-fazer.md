# 🛠️ Como fazer — do ambiente ao deploy automático

Este guia explica como executar o **Ativos TI**, entender a esteira DevSecOps e reproduzir o laboratório. Cada etapa indica **onde executar, para que serve e como conferir o resultado**.

[← Voltar ao projeto](../README.md) · [Arquitetura](arquitetura.md) · [Detalhes da esteira](pipeline.md)

> **Já está usando o laboratório?** Não refaça a instalação. Vá para **9. Uso diário** ou **10. Validar uma atualização**. A primeira inicialização com build local é para um ambiente novo; após ativar o deploy automático, use a imagem aprovada pela esteira.

## O que você vai construir

Um inventário de equipamentos com cadastro, edição, remoção confirmada, responsável, localização, status e valor de aquisição. O código fica no GitHub, a aplicação roda em Docker e o banco SQLite permanece em um volume.

| Parte | Responsabilidade |
| --- | --- |
| GitHub | Versionar código e registrar alterações |
| GitHub Actions | Executar testes e scanners, construir e publicar a imagem aprovada |
| Bandit | Analisar padrões inseguros no código Python |
| pip-audit | Consultar vulnerabilidades nas dependências da aplicação |
| Trivy | Analisar pacotes do sistema operacional e Python da imagem |
| GHCR | Armazenar imagens Docker |
| Ubuntu + Docker | Executar a aplicação na VM |
| Timer systemd | Buscar novas imagens aprovadas automaticamente |
| Volume SQLite | Conservar os ativos entre trocas de container |

O Juice Shop não participa deste projeto.

## 1. Preparar o ambiente

**Onde:** VirtualBox e console da VM.

O laboratório foi executado com Ubuntu 22.04 LTS, 2 CPUs, cerca de 8 GB de RAM e disco de 30 GB. Essa é a configuração usada, não um requisito mínimo medido. A VM precisa de internet para GitHub, GHCR, Docker Hub e bases dos scanners.

Utilize uma conta administrativa chamada `docker01`, com pasta `/home/docker01`. Os arquivos do atualizador usam esse caminho fixo; se escolher outro usuário, adapte os caminhos do script e do serviço antes de habilitar o timer.

No Ubuntu:

```bash
sudo apt update
sudo apt install -y openssh-server git python3 ca-certificates curl
sudo systemctl enable --now ssh
```

**Para que serve:** instalar SSH para acesso remoto e as ferramentas usadas no guia.

Instale Docker Engine com o plugin Docker Compose pelo [procedimento oficial para Ubuntu](https://docs.docker.com/engine/install/ubuntu/). Se o Docker já funciona, pule a instalação.

```bash
sudo systemctl enable --now docker
sudo docker --version
sudo docker compose version
sudo systemctl is-active docker ssh
```

**Como conferir:** Docker e Compose exibem versões; os serviços retornam `active`.

## 2. Configurar a conexão Windows → VM

**Onde:** configurações de rede da VM no VirtualBox.

Com a rede em **NAT**, configure o redirecionamento de porta:

| Nome | Protocolo | IP do host | Porta do host | IP do convidado | Porta do convidado |
| --- | --- | --- | --- | --- | --- |
| SSH | TCP | 127.0.0.1 | 2200 | deixar vazio | 22 |

Com a VM ligada, abra o PowerShell no Windows:

```powershell
ssh docker01@127.0.0.1 -p 2200
```

**Para que serve:** entrar no Ubuntu pela porta encaminhada. Na primeira conexão, confira a identidade da VM antes de aceitar a chave. A senha não aparece enquanto é digitada.

**Como conferir:** o prompt passa a mostrar `docker01@docker01`. Comandos Linux abaixo são executados nessa sessão, não no PowerShell desconectado.

## 3. Obter os arquivos

**Onde:** terminal conectado à VM.

Os comandos administrativos seguintes assumem uma sessão root:

```bash
sudo -i
cd /home/docker01
git clone --branch feat/cadastro-ativos --single-branch https://github.com/geovanniandrade/cybersecurity-labs.git cybersecurity-labs-ativos
mkdir -p /home/docker01/cadastro-ativos
cp -a cybersecurity-labs-ativos/devsecops/cadastro-ativos/. /home/docker01/cadastro-ativos/
cd /home/docker01/cadastro-ativos
ls
```

**Para que serve:** manter um clone do código e preparar a pasta fixa de execução. O `cp -a` também copia arquivos de configuração iniciados por ponto.

**Como conferir:** aparecem `app.py`, `Dockerfile`, `compose.yaml`, `compose.deploy.yaml` e a pasta `deploy`.

Se o clone já existe, use `git pull --ff-only` dentro dele, sem repetir o clone. Se houver alterações locais, resolva-as antes de atualizar. Não apague pastas para contornar esse erro.

## 4. Fazer a primeira inicialização

**Onde:** VM, como root, em `/home/docker01/cadastro-ativos`.

**Somente para uma instalação nova:**

```bash
docker compose up -d --build
docker compose ps
```

**Para que serve:** construir uma primeira imagem, iniciar o container e criar o volume `cadastro-ativos_ativos_data`. O atualizador precisa encontrar um container existente para fazer backup antes da primeira troca pela imagem do registry.

Aguarde a verificação de saúde e consulte:

```bash
docker inspect --format '{{.State.Health.Status}}' cadastro-ativos-web-1
curl --fail http://127.0.0.1:8080/health
```

**Como conferir:** estado `healthy` e resposta HTTP de sucesso.

O banco fica em `/app/data/ativos.sqlite3` dentro do container, no volume persistente. A porta é publicada apenas no endereço local da VM.

> Não execute `docker compose down -v`: a opção `-v` remove o volume do Compose local e os dados. O volume também não substitui backups.

## 5. Abrir o dashboard no Windows

**Onde:** outra janela do PowerShell, mantendo a VM ligada.

```powershell
ssh -N -L 8080:127.0.0.1:8080 docker01@127.0.0.1 -p 2200
```

**Para que serve:** encaminhar a porta 8080 da VM para o navegador no Windows. Após a senha, a janela pode permanecer sem mensagens: mantenha-a aberta.

Abra [http://127.0.0.1:8080](http://127.0.0.1:8080).

**Como conferir:** cadastre um ativo de laboratório, preencha os detalhes, edite e consulte o inventário. Teste a remoção apenas com um registro criado para esse fim. O valor de aquisição pode ficar em branco; isso significa valor não informado.

## 6. Entender e acompanhar a esteira

**Onde:** GitHub → Actions → **Cadastro de Ativos - DevSecOps**.

[Ver workflow](../../../.github/workflows/cadastro-ativos.yml) · [Ver execuções](https://github.com/geovanniandrade/cybersecurity-labs/actions/workflows/cadastro-ativos.yml)

A esteira dispara por push na branch `feat/cadastro-ativos` quando há alterações na pasta do projeto ou no workflow. Pull requests também executam validações, mas não publicam imagens.

| Ordem | Verificação | Quando interrompe a entrega |
| --- | --- | --- |
| 1 | Instalar dependências e executar os testes | Falha de instalação ou de teste |
| 2 | Bandit | Achado ou erro da análise de código |
| 3 | pip-audit | Vulnerabilidade ou erro da auditoria de dependências |
| 4 | Build Docker | Falha ao construir a imagem |
| 5 | Trivy: relatório completo | Erro ao baixar ou analisar |
| 6 | Trivy: política de bloqueio | Achado HIGH/CRITICAL com correção disponível ou erro no gate |
| 7 | Teste do container | Falha ao importar Flask/Gunicorn, pip ainda presente ou /health sem sucesso |
| 8 | Publicação no GHCR | Só ocorre após as verificações e na branch autorizada |

O pip é necessário para instalar dependências durante o build e é removido antes da execução da aplicação. As ferramentas de análise continuam disponíveis no runner de CI, fora da imagem final.

**Artifacts da execução:**

- `evidencias-<commit>`: testes, dependências e relatórios de Bandit/pip-audit.
- `imagem-seguranca-<commit>`: JSON completo do Trivy, relatório do gate, identificação da imagem e do scanner.

A retenção configurada é de 30 dias. Baixe as evidências que precisar conservar.

**Aprovação não significa zero vulnerabilidades.** Achados menores ou sem correção continuam no relatório completo. A regra não ignora CVEs individualmente.

### Reproduzir na própria conta GitHub

Clonar este repositório permite executar a aplicação, mas não concede permissão para publicar aqui. Para criar sua própria esteira, faça um **fork** e ajuste:

| Arquivo | Adaptação |
| --- | --- |
| Workflow na raiz em `.github/workflows/` | Branch dos gatilhos, condição de publicação e nome da imagem GHCR |
| `deploy/update.sh` | Endereço da sua imagem GHCR e caminhos da sua VM |
| `Dockerfile` | Label `org.opencontainers.image.source` para seu repositório |
| Serviço systemd | Caminho de execução se o usuário/pasta for diferente |

Habilite Actions no fork e permita ao workflow publicar packages conforme as políticas da conta. O workflow usa o `GITHUB_TOKEN` automático, com leitura do código e escrita em packages na etapa de imagem; não é necessário colocar token pessoal no código.

## 7. Preparar a imagem aprovada para a VM

**Onde:** GitHub e depois VM.

Aguarde a primeira execução de **push** bem-sucedida. Uma execução de PR sozinha não publica.

Abra [o pacote cadastro-ativos](https://github.com/users/geovanniandrade/packages/container/package/cadastro-ativos). Para download sem credenciais na VM, o pacote precisa estar **Public**. Se estiver privado e você for o proprietário, ajuste em **Package settings → Change visibility**. Isso publica a imagem/código, não o banco SQLite.

Na VM, como root:

```bash
cd /home/docker01/cadastro-ativos
docker pull ghcr.io/geovanniandrade/cadastro-ativos:approved
bash deploy/update.sh
cat .deployed-commit
docker ps --filter name=cadastro-ativos-web-1
```

**Para que serve:** executar a primeira implantação da imagem aprovada usando o script que depois será agendado.

**Como conferir:** `Deploy concluido`, container `healthy` e SHA do commit em `.deployed-commit`.

O script faz backup consistente do SQLite, fixa o ID da imagem local e usa `compose.deploy.yaml`. Esse Compose exige o volume externo existente: não cria silenciosamente um banco novo.

## 8. Habilitar o deploy automático

**Onde:** VM, como root.

```bash
cd /home/docker01/cadastro-ativos
cp deploy/cadastro-ativos-update.service /etc/systemd/system/
cp deploy/cadastro-ativos-update.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now cadastro-ativos-update.timer
systemctl status cadastro-ativos-update.timer --no-pager -l
systemctl list-timers cadastro-ativos-update.timer --no-pager
```

**Para que serve:** instalar o serviço, ativar o agendamento e iniciá-lo também nos próximos boots.

**Como conferir:** timer `active (waiting)` e próxima execução agendada. Durante uma execução, NEXT pode aparecer temporariamente sem horário.

A primeira ativação após boot usa o intervalo configurado de 2 minutos; depois o timer consulta a imagem aproximadamente a cada minuto após o término da execução anterior. Se a imagem não mudou, o container não é recriado.

O deploy não depende de conexão de entrada GitHub → VM. É a VM que consulta o registry pela internet; o túnel SSH serve apenas ao acesso pelo navegador.

## 9. Uso diário

**Onde:** PowerShell para conectar; depois terminal da VM.

```powershell
ssh docker01@127.0.0.1 -p 2200
```

Na VM:

```bash
sudo -i
docker ps --filter name=cadastro-ativos-web-1
systemctl status cadastro-ativos-update.timer --no-pager
journalctl -u cadastro-ativos-update.service -n 30 --no-pager
cat /home/docker01/cadastro-ativos/.deployed-commit
```

**Para que serve:** conferir container, agendamento, histórico e versão implantada. A mensagem `Container ja utiliza a imagem aprovada.` é esperada quando não há versão nova.

Mantenha a VM ligada com internet. Para abrir o dashboard após reiniciar o Windows, reabra o túnel da etapa 5.

Não use o Compose de build local para atualizar a aplicação depois de habilitar o deploy automático: ele pode executar uma versão diferente da aprovada na esteira. Alterações de código chegam pela imagem; alterações no próprio script/serviço exigem copiar os arquivos administrativos e recarregar o systemd.

## 10. Validar uma atualização de ponta a ponta

1. Registre o commit atual e mantenha um ativo de teste cadastrado.
2. Na sua cópia autorizada do repositório, altere um texto visível em `templates/index.html`.
3. Faça commit/push na branch configurada, sem editar arquivos diretamente no container.
4. No Actions, acompanhe testes, scanners, imagem e publicação.
5. Após aprovação e conclusão, aguarde a consulta da VM e a verificação de saúde.
6. Atualize o navegador com Ctrl + F5.
7. Confira a mudança de texto, a permanência do ativo, `healthy` e o novo SHA em `.deployed-commit`.

**Resultado esperado:** alteração recebida sem executar manualmente `git pull` ou `docker compose up` na VM para aquele deploy.

Se o pipeline reprovar, não há nova publicação; a VM permanece na última imagem aprovada. Um erro de configuração do scanner não é uma evidência de bloqueio por vulnerabilidade: leia o motivo no log.

## 11. Consultar ou repetir a análise de segurança

Prefira os artifacts do Actions para a imagem daquela execução. Para uma análise adicional da imagem que está rodando na VM, execute como root:

```bash
cd /home/docker01/cadastro-ativos
mkdir -p reports
ATIVOS_SCAN_IMAGE=$(docker image inspect "$(docker inspect --format '{{.Image}}' cadastro-ativos-web-1)" --format '{{index .RepoDigests 0}}')
printf '%s\n' "$ATIVOS_SCAN_IMAGE"
docker run --rm \
  -v "$PWD/reports:/reports" \
  aquasec/trivy:0.75.0 image \
  --image-src remote --scanners vuln --timeout 10m \
  --format json --output /reports/trivy-verificacao.json \
  "$ATIVOS_SCAN_IMAGE"
```

**Pré-condição:** imagem aprovada baixada do GHCR, com RepoDigest disponível; não executar este bloco sobre o primeiro build puramente local. Confira a referência impressa antes de continuar.

Para ler o resultado sem repetir a análise:

```bash
docker run --rm \
  -v "$PWD/reports:/reports:ro" \
  aquasec/trivy:0.75.0 convert --scanners vuln \
  --format table /reports/trivy-verificacao.json
```

`fixed` no relatório significa **correção disponível**, não que a versão instalada já foi corrigida. Confira Installed Version e Fixed Version. Um pacote pode gerar várias ocorrências de CVEs. A base muda com o tempo; compare também IDs, versões, data e digest da imagem.

Use nomes diferentes para guardar relatórios antes e depois de uma mudança. O nome da imagem no Docker Hub é **aquasec/trivy**, não aquasecurity/trivy.

## 12. Backup e recuperação

O updater cria backups antes de trocar a imagem em `/home/docker01/cadastro-ativos/backups/`.

Para fazer um backup manual, como root:

```bash
cd /home/docker01/cadastro-ativos
mkdir -p backups
docker exec cadastro-ativos-web-1 python -c "import os,sqlite3; s=sqlite3.connect(os.environ['DATABASE_PATH']); t=sqlite3.connect('/tmp/ativos-manual.sqlite3'); s.backup(t); t.close(); s.close()"
docker cp cadastro-ativos-web-1:/tmp/ativos-manual.sqlite3 "backups/ativos-manual-$(date -u +%Y%m%dT%H%M%SZ).sqlite3"
ls -lh backups/
```

**Como conferir:** arquivo SQLite com tamanho maior que zero. Copie backups também para um local protegido fora da VM. Não publique bancos ou backups no Git.

Se a nova imagem não ficar saudável, o script tenta iniciar a imagem anterior. Isso **não restaura o banco**. Uma migração futura incompatível exige procedimento próprio e restauração planejada.

Para pausar novas atualizações sem parar o dashboard:

```bash
systemctl stop cadastro-ativos-update.timer
```

Para retomar:

```bash
systemctl start cadastro-ativos-update.timer
```

## 13. Problemas comuns

| Sintoma | Verificação/ação |
| --- | --- |
| Permission denied no Docker ou em reports | Confirme que está na VM e use sudo -i antes dos blocos administrativos |
| SSH recusado em 127.0.0.1:2200 | Confira VM ligada, SSH ativo e redirecionamento NAT |
| Navegador não abre localhost:8080 | Confira túnel aberto, container healthy e porta 8080 livre no Windows |
| health: starting | Aguarde e consulte novamente; se persistir, leia docker logs |
| Volume externo não encontrado | Confira se a primeira inicialização criou cadastro-ativos_ativos_data |
| Pull denied no GHCR | Confira imagem publicada, nome correto e visibilidade pública |
| Variável ATIVOS_IMAGE ausente no Compose de deploy | Use bash deploy/update.sh; o script define a imagem |
| No module named pip na imagem final | Esperado: pip é removido após instalar as dependências |
| Formulário antigo falha após atualização | Recarregue a página para obter uma sessão/token CSRF novos |
| Pipeline vermelho | Leia a etapa que falhou; não desative scanners para liberar a entrega |
| Atualização não aparece | Compare SHA do Actions e .deployed-commit; consulte journalctl |

Logs do container:

```bash
docker logs --tail 80 cadastro-ativos-web-1
```

## 14. O que registrar como evidência

- Aplicação com um ativo de laboratório e suas operações.
- Execução do Actions e os jobs de testes e imagem.
- Etapas Bandit, pip-audit, Trivy e publicação.
- Relatório completo, regra aplicada e análise de um achado real.
- Antes/depois da correção ou mitigação, com versões e IDs.
- Commit na VM, container healthy e logs do updater.
- Mudança visível após push e preservação dos registros.

Este laboratório não possui autenticação entre usuários e mantém acesso pela porta local/túnel SSH. Não o exponha como inventário corporativo sem implementar os controles necessários.

**Estado validado em 15/10/2026:** esteira #11 aprovada, commit `0b608c6671521b26f66bb4703f727436d55e9ef1` confirmado na VM, container healthy e timer consultando a imagem automaticamente. [Execução de referência](https://github.com/geovanniandrade/cybersecurity-labs/actions/runs/38828875060).

Isso valida a implementação técnica demonstrada. Relatório acadêmico final, apresentação e vídeo são entregáveis separados.
