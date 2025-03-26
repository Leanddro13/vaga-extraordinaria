#!/bin/bash

# Verifica se está executando com sudo, se não pede para que faça
if [[ "$EUID" -ne 0 ]]; then
	echo "O script precisa de permissões de root!"
	echo "Uso: sudo ./install.sh"
	exit 1
fi

# Pega o nome da distro pelo os-release
distro=$(grep "^ID=" /etc/os-release | awk -F= '{print tolower($2)}' | tr -d '"')

# Define os pacotes com base nas distros-mãe
pacotes_debian_base="pulseaudio-utils dbus-python-devel python3-dbus google-chrome-stable"
pacotes_rhel_base="pulseaudio-utils python3-dbus google-chrome-stable"

# TODO: testei os IDs só para rhel, fedora, debian, ubuntu e vi que no centos às vezes tem IDs diferentes a depender da versão, mas deixei a "padrão"

# função para checar de keyring do Google Chrome existe
# ao rodar o install.sh, tive erros pra instalar o google-chrome-stable. 
# o erro era que o pacote não existia, então adicionei essa função para instalar o keyring caso não seja encontrado
check_google() {
	CAMINHO_CHROME=$(whereis google-chrome-stable | awk '{print $2}')
	
	if [ -n "$CAMINHO_CHROME" ]; then
		echo "Google Chrome encontrado no sistema. Pulando instalação..."
		return
	fi

	if [ -f "/etc/apt/keyrings/google-chrome.gpg" ]; then
		echo "Keyring do Google encontrado. Continuando instalação..."
	else
		echo "Keyring do Google não foi encontrado. Instalando keyring..."
		wget -qO https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub
		gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub
		echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list > /dev/null
		rm /tmp/google.pub
	fi
}

# Instala os pacotes de acordo com a distribuição
if [[ "$distro" == "ubuntu" || "$distro" == "debian" ]]; then
	check_google
	apt update -y
	apt install -y $pacotes_debian_base

elif [[ "$distro" == "rhel" || "$distro" == "fedora" || "$distro" == "centos" ]]; then
	dnf update -y
	dnf install -y $pacotes_rhel_base

else
	echo "Distribuição não suportada, adicione sua distribuição \"$distro\"  ao código"
	exit 1
fi

# TODO: avaliar a necessidade de utilizar um venv para rodar o pip install. ao rodar o install.sh sem o venv, recebi o erro "externally-managed-environment".
pip install -r requirements.txt

