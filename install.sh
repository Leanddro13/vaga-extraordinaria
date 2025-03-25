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
# python3-dbus não existe no apt. então, é necessário instalar as bibliotecas do dbus e suas dependências separadamente
pacotes_ubuntu_base="pulseaudio-utils build-essential libdbus-glib-1-dev libgirepository1.0-dev google-chrome-stable"
pacotes_rhel_base="pulseaudio-utils dbus-python-devel python3-dbus google-chrome-stable"

# TODO: testei os IDs só para rhel, fedora, debian, ubuntu e vi que no centos às vezes tem IDs diferentes a depender da versão, mas deixei a "padrão"

# função para checar de keyring do Google Chrome existe
# ao rodar o install.sh, tive erros pra instalar o google-chrome-stable. 
# o erro era que o pacote não existia, então adicionei essa função para instalar o keyring caso não seja encontrado
check_google_keyring() {
	if [ -f "/etc/apt/keyrings/google-chrome.gpg" ]; then
		echo "Keyring do Google encontrado. Continuando instalação..."
	else
		echo "Keyring do Google não foi encontrado. Instalando keyring..."
		wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub
		gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub
		echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
		rm /tmp/google.pub
	fi
}

# Instala os pacotes de acordo com a distribuição
if [[ "$distro" == "debian" ]]; then
	apt update -y
	apt install -y $pacotes_debian_base

elif [[ "$distro" == "ubuntu" ]]; then
	check_google_keyring
	apt update -y
	apt install -y $pacotes_ubuntu_base

elif [[ "$distro" == "rhel" || "$distro" == "fedora" || "$distro" == "centos" ]]; then
	dnf update -y
	dnf install -y $pacotes_rhel_base

else
	echo "Distribuição não suportada, adicione sua distribuição \"$distro\"  ao código"
	exit 1
fi

# TODO: avaliar a necessidade de utilizar um venv para rodar o pip install. ao rodar o install.sh sem o venv, recebi o erro "externally-managed-environment".
pip install -r requirements.txt

