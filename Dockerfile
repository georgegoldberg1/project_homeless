FROM ubuntu:22.04
# can add --platform linux/amd64 after FROM to run under emulation
USER root

RUN apt update && apt-get update \
	&& apt-get install -y sudo \
	&& apt-get install -y locales

# Set the locale
RUN sed -i '/en_GB.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_GB.UTF-8  
ENV LANGUAGE en_GB:en  
ENV LC_ALL en_GB.UTF-8     
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y pkg-config libcairo2-dev libjpeg-dev libgif-dev

RUN apt-get update && apt-get install -y software-properties-common
RUN apt-get update && apt-get install -y python3.10 python3-pip \
	&& pip3 install --upgrade pip

ARG HOSTUSER
RUN useradd --home /home/$HOSTUSER --shell /bin/bash -G sudo $HOSTUSER

USER $HOSTUSER
WORKDIR /home/$HOSTUSER
ENV PATH=/home/$HOSTUSER/.local/bin:${PATH}
RUN mkdir hostmachine

USER root
RUN apt update && apt install -y zsh
RUN usermod -s /usr/bin/zsh $HOSTUSER

RUN apt-get update && apt-get install -y git wget zip pandoc vim tmux fonts-dejavu && \
	apt-get clean && rm -rf /var/lib/apt/lists/* && apt-get autoremove

USER $HOSTUSER

RUN sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
         && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k \
         && sed -i 's/^ZSH_THEME=/ZSH_THEME="powerlevel10k\/powerlevel10k" #default ZSH_THEME=/g' ~/.zshrc \
         && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting \
         && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
         && sed -i 's/^plugins/plugins=(git aws compleat systemadmin zsh-autosuggestions zsh-syntax-highlighting) #default plugins/1' ~/.zshrc \
         && echo ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE=fg=#ffffff,bg=cyan,bold,underline >> ~/.zshrc

# use requirements and zsh theme settings (if local file exists)
COPY requirements.txt .p10k.zsh .
RUN pip install --no-cache-dir -r requirements.txt

RUN jupyter notebook --generate-config \
	&& sed -i "s/# c.NotebookApp.custom_display_url = ''/c.NotebookApp.custom_display_url = 'http:\/\/localhost:8889'/" ~/.jupyter/jupyter_notebook_config.py \
	&& sed -i "s/# c.NotebookApp.notebook_dir = ''/c.NotebookApp.notebook_dir = 'hostmachine\/project'/" ~/.jupyter/jupyter_notebook_config.py

RUN pip3 install jupyter_contrib_nbextensions

# USER root
# ENV TINI_VERSION v0.6.0
# ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
# RUN chmod +x /usr/bin/tini
# ENTRYPOINT ["/usr/bin/tini", "--"]
# USER $HOSTUSER

EXPOSE 8888

CMD ["jupyter", "notebook","--no-browser", "--ip=0.0.0.0","--port=8888"]
