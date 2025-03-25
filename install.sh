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
pacotes_rhel_base="pulseaudio-utils dbus-python-devel python3-dbus google-chrome-stable"

# TODO: testei os IDs só para rhel, fedora, debian, ubuntu e vi que no centos às vezes tem IDs diferentes a depender da versão, mas deixei a "padrão"

# Instala os pacotes de acordo com a distribuição
if [[ "$distro" == "ubuntu" || "$distro" == "debian" ]]; then
	apt update -y
	apt install -y $pacotes_debian_base

elif [[ "$distro" == "rhel" || "$distro" == "fedora" || "$distro" == "centos" ]]; then
	dnf update -y
	dnf install -y $pacotes_rhel_base

else
	echo "Distribuição não suportada, adicione sua distribuição \"$distro\"  ao código"
	exit 1
fi

pip install -r requirements.txt

