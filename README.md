
#  Entra ID Attributes Pipeline

**Automatize o gerenciamento de atributos personalizados de segurança no Microsoft Entra ID (Azure AD)** com foco em governança baseada em contexto, como **Centro de Custo**, **Departamento** ou **Entidade Organizacional**.

---

##  Visão Geral

O `entra-id-attributes-pipeline` é uma solução **open source** para aplicar, atualizar e validar **customSecurityAttributes** de forma segura e automatizada usando a **Microsoft Graph API**. Atribua dinamicamente atributos a Service Principals com base em regras de nomenclatura e controle de acesso organizacional.

Essa ferramenta é essencial para organizações que desejam elevar sua governança de identidade e controle de acesso na nuvem com práticas modernas como **ABAC** (Attribute-Based Access Control).

>  Baseado na documentação oficial da Microsoft:  
> [Custom security attributes overview](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/custom-security-attributes-apps?pivots=ms-graph)

---

##  Benefícios

 **Automação Total** do processo de associação de atributos de segurança personalizados.  
 **Governança Contextual de Acesso** por centro de custo, unidade de negócio ou criticidade.  
 **Compliance e Auditoria** com histórico de alterações.  
 **Redução de Erros Humanos** por meio de scripts seguros e reutilizáveis.  
 **Integração com Pipelines DevSecOps**, como GitHub Actions, Azure Pipelines e Jenkins.  
 **Escalabilidade** para múltiplos tenants, ambientes e aplicações.

---

##  Casos de Uso

- Governança de acesso baseado em **Atributo**
- Aplicação automatizada de atributos em **Identidades e aplicativos**
- Políticas de acesso dinâmicas usando **ABAC**
- Apoio a projetos de **IAM** e **IGA**
- Segurança baseada em contexto para ambientes regulamentados

---

##  Funcionalidades

-  Autenticação segura via **MSAL**
-  Consulta automática de Service Principals por nome
-  Correspondência lógica com atributos predefinidos
-  Atualização de atributos via **Graph API**
-  Suporte a múltiplos ambientes com `.env`
-  Execução local ou CI/CD com GitHub Actions
-  Scripts modulares para extração, análise e aplicação

---

##  Como Usar

###  Pré-requisitos

- Python 3.10+
- Conta no Entra ID (Azure AD Premium)
- Registro de aplicação com as permissões:
  - `Application.ReadWrite.All`
  - `Directory.Read.All` (ou equivalente)
  - `CustomSecAttributeDefinition.Read.All`
  - `CustomSecAttributeAssignment.ReadWrite.All` 

- Permissões de Service Principal para uso de customSecurityAttributes

---

###  Execução Local

1. **Clone o repositório**  
   ```bash
   git clone https://github.com/1hmacarte/entra-id-attributes-pipeline.git
   cd entra-id-attributes-pipeline
   ```

2. **Crie o arquivo `.env`** baseado em `.env.template`

3. **Instale as dependências**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o script principal**  
   ```bash
   python main.py
   ```

---

###  Execução via GitHub Actions

Configure os segredos no repositório do GitHub:

- `CLIENT_ID`
- `CLIENT_SECRET`
- `TENANT_ID`

Depois, dispare o workflow `Executar Pipeline` manualmente ou por push automático.

---

##  Scripts Incluídos

| Script | Função |
|--------|--------|
| `01_extract_entities.py` | Extrai usuários e Service Principals com atributos em CSV |
| `02_extract_definitions.py` | Extrai a definição dos atributos customizados disponíveis |
| `03_match_attributes.py` | Realiza a correspondência lógica entre Service Principals e os atributos esperados |
| `04_apply_patch.py` | Aplica os atributos nos SPs usando PATCH via Graph API |

---

##  Documentação Complementar

- [Microsoft Graph - Custom Security Attributes](https://learn.microsoft.com/en-us/entra/fundamentals/custom-security-attributes-overview)
- [Troubleshoot Custom Security Attribute](https://learn.microsoft.com/en-us/entra/fundamentals/custom-security-attributes-troubleshoot)

---

##  Roadmap

-  Suporte a leitura de arquivos CSV externos com mapeamentos
-  UI mínima em Streamlit para execução manual
-  Integração com logs de auditoria e geração de relatórios
-  Suporte a múltiplas tenants com rotas segregadas
-  Template para implantação via Terraform

---

##  Contribua

Pull requests são bem-vindos! Para grandes alterações, por favor abra uma issue antes para discussão.

---

##  Contato

Desenvolvido por [@1hmacarte](https://github.com/1hmacarte) - Especialista em Soluções de Cloud Security 
Para suporte, integração personalizada ou consultoria na implementação de segurança Cloud IAM, entre em contato via GitHub ou LinkedIn.

---
