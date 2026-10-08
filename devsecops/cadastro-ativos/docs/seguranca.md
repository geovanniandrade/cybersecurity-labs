# Segurança

## Controles implementados

| Controle | Aplicação |
| --- | --- |
| SQL parametrizado | Cadastro, edição, remoção e consulta por ID usam parâmetros |
| Escape HTML | Dados exibidos passam pelo escape padrão dos templates Jinja |
| CSRF | Operações de escrita exigem token de formulário e sessão |
| Validação | Tipos/status permitidos, limites de tamanho e preços não negativos |
| Remoção confirmada | GET abre a confirmação; apenas POST confirmado exclui |
| Container sem root | Usuário de execução `appuser`, UID 10001 |
| Privilégios reduzidos | Compose remove capabilities e ativa no-new-privileges |
| Acesso local | Porta publicada em 127.0.0.1; acesso remoto via SSH |
| Headers | CSP, nosniff e Cache-Control no-store |

## Limites do laboratório

A aplicação não tem autenticação ou controle de acesso entre usuários. Quem puder acessar a interface pode gerenciar ativos. A configuração atual destina-se ao laboratório local. A chave de sessão é gerada ao iniciar quando APP_SECRET não está definida, e formulários anteriores a um reinício expiram. Não publicar bancos ou backups no repositório.

## Análise automatizada

O pipeline executa Bandit no código e pip-audit nas dependências; falhas bloqueiam publicação, com JSON preservado nos artifacts. Na execução local em 08/10/2026 UTC, Bandit 1.9.4 não encontrou achados em app.py e pip-audit 2.10.1 não encontrou vulnerabilidades conhecidas nas dependências resolvidas. Os relatórios locais estão em docs/security/. Isso não demonstra ausência de vulnerabilidades.

A primeira execução remota e um achado real ainda precisam de evidências. O trabalho exige componente afetado, identificador, severidade com fonte, impacto, correção/mitigação e nova análise. Não introduzir falhas artificiais na aplicação para produzir resultados.

O updater faz backup antes da troca e verifica saúde; PRs não publicam imagens. O token de publicação possui escrita em packages e leitura do repositório, e as actions estão fixadas por SHA. O pacote GHCR precisa ser público para o pull sem credenciais na VM.

O build e a auditoria usam requirements.lock, fixando as mesmas versões Python analisadas. Atualizações precisam revisar o lock e executar os scanners novamente. A imagem base Python continua recebendo atualizações via docker build --pull.
