FROM postgres:13

# Crea el directorio si no existe
RUN mkdir -p /etc/postgresql

# Copia los archivos de configuración personalizados
COPY "../../postgresql/config/postgresql.conf" "/etc/postgresql/postgresql.conf"
COPY "../../postgresql/config/pg_hba.conf" "/etc/postgresql/pg_hba.conf"

# Configura PostgreSQL para usar la configuración personalizada
RUN echo "include '/etc/postgresql/postgresql.conf'" >> /usr/share/postgresql/postgresql.conf.sample
