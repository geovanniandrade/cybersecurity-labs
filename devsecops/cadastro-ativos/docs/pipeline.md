# Pipeline — planejamento

**Status: ainda não implementada.** Não há workflow CI/CD nesta branch.

| Etapa prevista | Resultado esperado |
| --- | --- |
| Código no Git | Alteração versionada e gatilho automático |
| Build da aplicação | Dependências instaladas e código validado |
| Testes | Executar os testes de comportamento, valores e migração |
| Segurança | Analisar código/dependências/imagem e guardar resultados reais |
| Imagem Docker | Construir e identificar a imagem daquela versão |
| Deploy automático | Atualizar o container da VM preservando o volume |
| Verificação | Confirmar `/health` e acesso à versão publicada |

O acesso Windows → VM por SSH não fornece acesso GitHub → VM. A estratégia de deploy precisa ser definida antes de implementar esta etapa, pois a VM está em uma rede NAT.

A conclusão da atividade inclui demonstrar uma alteração no Git acionando o fluxo até a aplicação atualizada, além de documentar ao menos um achado real de segurança, sua severidade e sua correção ou mitigação.
