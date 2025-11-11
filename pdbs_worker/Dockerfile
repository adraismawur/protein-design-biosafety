FROM ubunutu:22.04

RUN apt update
RUN apt install -y apptainer curl git wget rsync


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
