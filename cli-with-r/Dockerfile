FROM mcr.microsoft.com/azureml/base:openmpi3.1.2-ubuntu18.04

# Install R+R Essentials and AzureML defaults
RUN conda install -c r -y pip=20.1.1 openssl=1.1.1c r-base r-essentials rpy2 && \
    conda install -c conda-forge -y mscorefonts && \
    conda clean -ay && \
    pip install --no-cache-dir azureml-defaults

# Set up miniconda environment for successful reticulate configuration
RUN ln -s /opt/miniconda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

# Install and configure R AzureML SDK
ENV TAR="/bin/tar"
RUN R -e "install.packages(c('remotes', 'reticulate', 'optparse'), repos = 'https://cloud.r-project.org/')" && \
    R -e "remotes::install_github('https://github.com/Azure/azureml-sdk-for-r')" && \
    R -e "library(azuremlsdk); install_azureml()" && \
    echo "Sys.setenv(RETICULATE_PYTHON='/opt/miniconda/envs/r-reticulate/bin/python3')" >> ~/.Rprofile

# Install additional R packages 
RUN R -e "install.packages(c('e1071'), repos = 'https://cloud.r-project.org/')"
