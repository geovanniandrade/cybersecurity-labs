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

## Análise automatizada pendente

Nenhum resultado de scanner é apresentado como concluído nesta versão. Testes de entrada não substituem a análise automatizada exigida pela atividade. Após escolher a ferramenta, documentar o achado real: componente afetado, evidência, severidade, impacto, correção/mitigação e nova análise.
