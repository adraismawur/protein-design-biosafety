FROM ubunutu:22.04

RUN apt update
RUN apt install -y curl git wget rsync
RUN wget https://github.com/apptainer/apptainer/releases/download/v1.4.4/apptainer_1.4.4_amd64.deb
RUN apt install -y ./apptainer_1.4.4_amd64.deb


# python env
RUN "${SHELL}" <(curl -L micro.mamba.pm/install.sh)
RUN micromamba config append channels bioconda
RUN micromamba env create -n proteindj python=3.11 nextflow

# proteindj source
RUN git clone https://github.com/PapenfussLab/proteindj.git
WORKDIR /proteindj
RUN bash scripts/download_models.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
# todo: worker script
# CMD ["npm", "start"]
