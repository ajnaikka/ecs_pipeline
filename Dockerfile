#Dockerfile for running odoo 16.0 community edition by copying the addons folder


FROM odoo:17.0

USER root

RUN chown -R odoo:odoo /var/lib/odoo
RUN chmod -R 777 /var/lib/odoo

#COPY ./addons /mnt/extra-addons
COPY ./odoo.conf /etc/odoo/odoo.conf
# RUN set -e; \
#     pip install --no-cache-dir -r /mnt/extra-addons/requirements.txt

USER odoo
