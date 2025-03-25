# Vaga extraordinaria

<div align="center">
  <a href="https://github.com/Leanddro13/vaga-extraordinaria">
    <img src="https://uploaddeimagens.com.br/images/004/884/823/full/esta-imagem-nao-foi-gerada-no-gemini.jpeg?1741631712" width="300" height="300">
  </a>
</div>

## 📝 Sobre o projeto

Utilitário automatizado para monitorar vagas disponíveis em disciplinas no SIGAA UnB.

### `main.py`:

- Script principal responsável por:
  - Monitorar a disponibilidade de vagas em disciplinas configuradas;
  - Notificar o usuário em tempo real com alertas visuais e sonoros do sistema;
  - (Em desenvolvimento) Realizar a matrícula automática caso uma vaga esteja disponível.

### `extra.py`:

- Script **legado** que realiza o processo de matrícula automaticamente.
- Atenção: _Este arquivo está em **desuso**_. Suas funcionalidades estão sendo integradas gradualmente ao `main.py`.

### `.env.example`:

- Exemplo de arquivo .env para armazenar suas credenciais de forma segura:

```env
LOGIN=''
SENHA=''
DATA_NASCIMENTO='DD/MM/AAAA'
```

### `install.sh`:
- Script automatizado para instalação de dependências e pacotes do sistema. Suporta distribuições Linux baseadas em Debian (ex: Ubuntu) e RHEL (ex: Fedora, CentOS).

### `requirements.txt`:
- Lista de dependências Python utilizadas pelo projeto.

## 🛞 Como rodar?

### 1. Clone o repositório

```bash
git clone https://github.com/Leanddro13/vaga-extraordinaria.git
cd vaga-extraordinaria
```

### 2. Crie o arquivo .env

Preencha com suas informações de login no SIGAA, conforme o .env.example.

### 3. Dê permissão e execute o script de instalação

```bash
chmod +x install.sh
sudo ./install.sh
```

### 4. Execute o sistema de monitoramento

```bash
python3 main.py
```

## ⚠️ Avisos e Limitações

- Testado em: Ubuntu 24.04.2 LTS e Fedora 40
- Compatibilidade apenas com ambientes linux
- O módulo de matrícula automática ainda está em desenvolvimento/teste
- Suas credenciais são lidas via `.env`, nunca compartilhe este arquivo com ninguém

